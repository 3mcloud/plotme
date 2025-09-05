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

from plotme.load_data import Folder, check_filter_match
from plotme.schema import schema, template

template_file_name = "must_rename_template_plot_info.json"
plot_info_id = "plot_info"

def plot_all(args_dict={}):
    """
    generate multiple plots, globs through data_root to find plot_info files, checks previous hash against current hash,
    runs single_plot

    Parameters
    ----------
    args_dict: dictionary
        input arguments

    """

    plot_info_file = args_dict.get('plot_info_file', plot_info_id)

    data_root = Path(args_dict.get('data_root', os.getcwd()))
    plot_info_files = list(data_root.glob(f"**/*{plot_info_file}.json"))

    # save template plot_info.json
    if len(plot_info_files) == 0 or args_dict.get('template'):
        template_stream = json.dumps(template, sort_keys=False, indent=4)
        with open(template_file_name, "w") as json_file:
            json_file.write(template_stream)
            logging.info("template plot_info file generated")
            return 0

    for file in plot_info_files:
        dir_path = file.parent

        # skip template_plot_info.json files
        if template_file_name in str(file):
            logging.info(f"ignoring {file} because the name matches the template file name")
            continue

        # hashing folder recursively
        current_hash = dirhash(dir_path, "md5", ignore=["*previous_hash", "*.html", "*.png", "*.log"])
        hash_file_path = Path(dir_path, f"{file.stem}_previous_hash")
        if hash_file_path.exists():
            with open(hash_file_path) as txt_file:
                previous_hash = txt_file.read()
        else:
            previous_hash = ''

        force = args_dict.get('force')
        if current_hash == previous_hash and not force:
            # only skips entire folder, if multiple plot_info files all must be unchanged to skip
            logging.info(f"no changes detected, skipping {file}")
        else:
            logging.info(f'loading plot settings from {file}')
            with open(file) as json_file:
                plot_info = json.load(json_file)
            validate(instance=plot_info, schema=schema)
            plot_info['plot_dir'] = dir_path
            plot_info['plot_info_file'] = file
            args_and_plot_info = args_dict.copy()
            args_and_plot_info.update(plot_info)
            not_a_plot = args_and_plot_info.get('not_a_plot', False)
            if not_a_plot is False:
                single_plot(args_and_plot_info)  # plot_info can overwrite args
                with open(hash_file_path, "w+") as txt_file:
                    txt_file.write(current_hash)

    return 0


def single_plot(args_dict={}):
    plot_dir = args_dict.get('plot_dir', Path.home())
    pio_template = args_dict.get('pio.template', "plotly_white")
    height = args_dict.get('height', 600)
    width = args_dict.get('width', 1000)

    title = args_dict.get('title_text', 'plotme plot')
    x_id = args_dict.get('x_id', 'index')
    x_title = args_dict.get('x_title', x_id)  # use x_id if no label is given
    y_id = args_dict.get('y_id', 'headers')
    y_title = args_dict.get('y_title', y_id)  # use y_id if no label is given
    trace_mode = args_dict.get('trace_mode', 'markers')
    marker_symbols = args_dict.get('marker_symbols')
    show_legend = args_dict.get('showlegend', True)
    x_axes_kwargs = args_dict.get('x_axes_kwargs', {})
    y_axes_kwargs = args_dict.get('y_axes_kwargs', {})
    x_axes_visible = args_dict.get('xaxes_visible', True)
    y_axes_visible = args_dict.get('yaxes_visible', True)
    include_filter = args_dict.get('folder_include_filter')
    exclude_filter = args_dict.get('folder_exclude_filter')

    trace_label = args_dict.get("schema", {}).get("trace_label", "file_name")
    remove_from_trace_label = args_dict.get("schema", {}).get("remove_from_trace_label", "")
    constant_lines = args_dict.get('constant_lines', {})
    constant_lines_x = constant_lines.get('x=', [])  # list
    constant_lines_y = constant_lines.get('y=', [])  # list
    error_y = args_dict.get('error_y', {})
    if error_y:
        if not error_y.get('visible'):
            error_y['visible'] = True

    folders = glob.glob(f"{plot_dir}/**/", recursive=True)
    folders.append(plot_dir)  # include the data_root directory

    # Add only the folders that the filters allow
    folder_datas = []
    for folder in folders:
        directory = Path(folder)
        if directory.name == 'ignore':
            logging.info(f"ignoring {directory} because named 'ignore'")
            continue
        if include_filter and not check_filter_match(include_filter, directory.name):
            logging.info(f"ignoring {directory} because it does not match folder_include_filter")
            continue
        if exclude_filter and check_filter_match(exclude_filter, directory.name):
            logging.info(f"ignoring {directory} because it does match folder_exclude_filter")
            continue
        folder_data = Folder(directory, x_id, y_id, args_dict)
        if folder_data.empty:
            continue
        folder_datas.append(folder_data)

    # determine plot_source, plot_source used if df_type is 'trace' or 'point'
    n_folder_datas = len(folder_datas)
    logging.debug(f"n_folder_datas: {n_folder_datas}")

    x_dict = {}
    y_dict = {}
    for folder_data in folder_datas:
        x = folder_data.x
        y = folder_data.y
        file_infos = folder_data.file_infos

        # assume all df_type in a folder are the same
        df_type = file_infos[0]['df_type']

        trace_x_id = list(x[0].keys())[0]
        # build the dicts to plot
        # debugging prints
        # print(f"len_y: {len(y)}")
        # print(f"len_x: {len(x)}")
        # print(f"len(x[0][trace_x_id]): {len(x[0][trace_x_id])}")
        for i, traces in enumerate(y):
            # this section of the code finds a unique trace_id for each trace
            # the y data contains trace_y_id and for some cases the trace_id
            num_traces = len(traces)
            
            #overwrite df_type because it is actually a plot
            if num_traces == 1 and n_folder_datas == 1 and len(y) == 1:
                df_type = 'plot'
            
            for trace in traces:
                trace_y_id = list(trace.keys())[0]
                match df_type:
                    case 'plot':
                        trace_id = trace_y_id
                    case 'trace':
                        if trace_label == 'file_name':
                            trace_id = file_infos[i]['file_stem']
                        elif trace_label == 'folder_name':
                            trace_id = folder_data.name
                        else:
                            raise ValueError (f"Unexpected trace_label: {trace_label}, options are file_name or folder_name")
                    case 'point':
                        trace_id = folder_data.name
                    case _:
                        logging.error(f"Unexpected df_type: {df_type}")

                trace_id = trace_id.replace(remove_from_trace_label, "")
                y_dict.update({trace_id: trace[trace_y_id]})
                x_dict.update({trace_id: x[i][trace_x_id]})

    pio.templates.default = pio_template
    fig = make_subplots(rows=1, cols=1, shared_yaxes=True,
                        x_title=x_title, y_title=y_title)

    for i, folder in enumerate(x_dict):
        if isinstance(marker_symbols, list):
            marker_symbol = marker_symbols[i]
        else:
            marker_symbol = i % 55  # there are only 55 marker symbols in plotly

        fig.add_trace(go.Scatter(name=folder, mode=trace_mode, x=x_dict[folder], y=y_dict[folder],
                                 marker_symbol=marker_symbol, error_y=error_y), row=1, col=1)

    for y_value in constant_lines_y:
        fig.add_hline(y=y_value)

    for x_value in constant_lines_x:
        fig.add_vline(x=x_value)

    fig.update_layout(height=height, width=width, title_text=title)
    fig.update_layout(showlegend=show_legend)
    fig.update_xaxes(visible=x_axes_visible, **x_axes_kwargs)
    fig.update_yaxes(visible=y_axes_visible, **y_axes_kwargs)

    # file_name = f"{y_title} vs {x_title}"
    # file_name = file_name.strip()  # remove leading and trailing spaces
    file_name = Path(args_dict['plot_info_file']).stem.replace(plot_info_id, "plot")
    file_path_no_ext = str(Path(plot_dir, f"{file_name}"))
    logging.info(f"num traces in '{file_path_no_ext}': {len(x_dict)}")

    if args_dict.get('html', True):
        fig.write_html(f"{file_path_no_ext}.html", full_html=False, include_plotlyjs='cdn')
    if args_dict.get('png', False):
        fig.write_image(f"{file_path_no_ext}.png")
    if args_dict.get('show', True):
        fig.show()
