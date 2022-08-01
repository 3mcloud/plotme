import glob
import json
import logging
import os
from pathlib import Path

import plotly.graph_objects as go
import plotly.io as pio
from dirhash import dirhash
from jsonschema import validate
from plotly.subplots import make_subplots

from plotme.load_data import Folder
from plotme.schema import schema, template

template_file_name = "must_rename_template_plot_info.json"


def plot_all(args_dict={}):
    """
    generate multiple plots, globs through data_root to find plot_info files, checks previous hash against current hash,
    runs single_plot

    Parameters
    ----------
    args_dict: dictionary
        input arguments

    """

    plot_info_file = args_dict.get('plot_info', 'plot_info.json')

    data_root = Path(args_dict.get('data_root', os.getcwd()))
    plot_info_files = list(data_root.glob(f"**/*{plot_info_file}"))

    # save template plot_info.json
    if len(plot_info_files) == 0 or args_dict.get('template'):
        template_stream = json.dumps(template, sort_keys=False, indent=4)
        with open(template_file_name, "w") as json_file:
            json_file.write(template_stream)
            logging.info("template plot_info file generated")

    for file in plot_info_files:
        dir_path = file.parent

        # skip template_plot_info.json files
        if template_file_name in str(file):
            logging.info(f"ignoring {file} because it is probably a template")
            continue

        # hashing folder recursively
        current_hash = dirhash(dir_path, "md5", ignore=["*previous_hash", "*.html", "*.png"])
        hash_file_path = Path(dir_path, f"{file.stem}_previous_hash")
        if hash_file_path.exists():
            with open(hash_file_path) as txt_file:
                previous_hash = txt_file.read()
        else:
            previous_hash = ''

        force = args_dict.get('force')
        if current_hash == previous_hash and not force:
            logging.info(f"no changes detected, skipping {dir_path}")
        else:
            logging.info(f'loading plot settings from {file}')
            with open(file) as json_file:
                plot_info = json.load(json_file)
            validate(instance=plot_info, schema=schema)
            plot_info['plot_dir'] = dir_path
            args_and_plot_info = args_dict.copy()
            args_and_plot_info.update(plot_info)
            single_plot(args_and_plot_info)  # plot_info can overwrite args
            with open(hash_file_path, "w+") as txt_file:
                txt_file.write(current_hash)

    return 0


def single_plot(args_dict={}):
    plot_dir = args_dict.get('plot_dir', Path.home())
    pio_template = args_dict.get('pio.template', "plotly_white")
    height = args_dict.get('height', 600)
    width = args_dict.get('width', 1000)

    title = args_dict.get('title', 'plotme plot')
    x_id = args_dict.get('x_id', 'index')
    x_title = args_dict.get('x_title', x_id)  # use x_id if no label is given
    y_id = args_dict.get('y_id', 'headers')
    y_title = args_dict.get('y_title', y_id)  # use y_id if no label is given
    trace_mode = args_dict.get('trace_mode', 'markers')
    marker_symbols = args_dict.get('marker_symbols')

    exclude_from_trace_label = args_dict.get('exclude_from_trace_label', '')  # remove this
    constant_lines = args_dict.get('constant_lines', {})
    constant_lines_x = constant_lines.get('x=', [])  # list
    constant_lines_y = constant_lines.get('y=', [])  # list
    error_y = args_dict.get('error_y', {})
    if error_y:
        if not error_y.get('visible'):
            error_y['visible'] = True

    folders = glob.glob(f"{plot_dir}/*/")
    folders.append(plot_dir)  # include the data_root directory
    x_dict = {}
    y_dict = {}
    x_max = 0
    for folder in folders:
        directory = Path(folder)
        if directory.name == 'ignore':
            continue
        if exclude_from_trace_label not in directory.name:
            continue
        else:
            if exclude_from_trace_label:
                d_name_part = directory.name.strip(exclude_from_trace_label)
            else:
                d_name_part = directory.name
        folder_data = Folder(directory, x_id, y_id, args_dict)
        x = folder_data.x_values()
        y = folder_data.y_values()
        if len(x) == 1:
            # if not x:
            #     x, y = collect_from_pkl(directory, x_id, y_id)
            trace_x_id = list(x[0].keys())[0]
            trace_x_vals = x[0][trace_x_id]
            x_max = max(max(trace_x_vals), x_max)

            for trace in y[0]:
                trace_y_id = list(trace.keys())[0]
                y_dict.update(trace)
                x_dict.update({trace_y_id: x[0][trace_x_id]})

        elif len(x) > 1:
            # TODO more than one graph per folder
            logging.info("multiple plots or multiple traces per file per folder not implemented")

    pio.templates.default = pio_template
    fig = make_subplots(rows=1, cols=1, shared_yaxes=True,
                        x_title=x_title, y_title=y_title)

    for i, folder in enumerate(x_dict, start=1):
        if isinstance(marker_symbols, list):
            marker_symbol = marker_symbols[i - 1]
        else:
            marker_symbol = i - 1

        fig.add_trace(go.Scatter(name=folder, mode=trace_mode, x=x_dict[folder], y=y_dict[folder],
                                 marker_symbol=marker_symbol, error_y=error_y), row=1, col=1)

    for y_value in constant_lines_y:
        fig.add_hline(y=y_value)

    for x_value in constant_lines_x:
        fig.add_vline(x=x_value)

    fig.update_layout(height=height, width=width, title_text=title)

    if args_dict.get('html', True):
        fig.write_html(str(Path(plot_dir, f"{y_title} vs {x_title}.html")))
    if args_dict.get('png', False):
        fig.write_image(str(Path(plot_dir, f"{y_title} vs {x_title}.png")))
    if args_dict.get('show', True):
        fig.show()
