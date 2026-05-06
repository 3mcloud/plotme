# plotme
scatter plot all the things in all the folders automatically but only if there have been changes

## Description
Plotme takes tabular data (e.g. excel) and outputs interactive scatter plots. It is a command line tool written in python. It uses json or yaml files to configure the plots. It is for technical and non-techncial folks.

## Features
* specify data_root using argument or current directory
* save the plot's configuration/definition with the data (plot_info.json)
* finds plot_info files at any depth in the folder tree
* validation plot_info.json/yml/yaml using jsonschema
* pass-through to plotly
  * scatter plot
    * `trace_mode` (markers or lines) 
    * `marker_symbols` [documentation](https://plotly.com/python/marker-style/)
    * `constant_lines` constant lines
    * `error_y` error bars
    * `x_axes_kwargs`, `y_axes_kwargs` plotly axes keyword arguments e.g. 'type'
  * [pio.templates](https://plotly.com/python/templates/)
  * `update_layout_kwargs` plotly layout keyword arguments e.g. 'font', 'legend' etc
  * `update_traces_kwargs` plotly traces keyword arguments e.g. 'marker', 'selector' etc
* auto-detect data files (xls, xlsx, csv only)
* supported data files: xls, xlsx, csv, txt, and any text file readable by pandas.read_csv()
* Pass `header` `separator`, `index_col` and any other kwargs using `pandas_read_kwargs` [read_csv()](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html) [read_excel()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html)
* filter data files (include and exclude) `folder_include_filter`, `folder_exclude_filter`, 
* filter folders (include and exclude) `file_include_filter`, `file_exclude_filter`, 
* trace label from y_id (when plot is single file) or file name (default) or folder name `trace_label`
* remove common text from all trace labels `remove_from_trace_label`
* only re-generate plots if data or plot_info has changed, to force regeneration `plotme -f`
* pre-process `pre` options
  * data cleaning: `remove_null`, `remove_zero`, `remove_strings`, `convert_to_float`
  * slice: `slice_start`, `slice_end`, `slice_step`
* post-process `post` (`max`, `min`, `avg`)
* x value time stamp in file name conversion to seconds using [strptime format codes](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes) `x_time_format`
* extract x value from filename using regular expression `x_id_is_reg_exp`

## Install options
* install using [pipx](https://pipx.pypa.io/stable/) from source (recommended if you want system wide availability)
  * `pipx install git+https://github.com/3mcloud/plotme.git`
* install to active python environment from source:
  * SSH: ```python -m pip install git+ssh://git@github.com/3mcloud/plotme.git```
  * HTTPS: ```python -m pip install https://github.com/3mcloud/plotme.git```

## How to use
* from command line: plotme(.exe) -h to see arguments
* from file explorer:
  1. move to data directory or above
  2. run once to generate a template of the plot_info.json
  3. modify the template as needed
  4. run again to generate plot(s)


### example JSON plot_info.json file
in this example
* the x value is extracted from the file name via regular expression
* each point on the scatter plot is the maximum value from a column called `Force(N)-data` where the header is located at the 4th row of a data file
* the legend is inside the plot in the right top corner, by default the legend is outside the plot on the right side
* markers are used and they are 10 pixels in diameter
```json
{
    "title_text": "Force over temperature",
    "x_id": "_(\\d+)C",
    "x_title": "Temperature (C)",
    "y_id": "Force(N)-data",
    "y_title": "Max Force (N)",
    "showlegend": true,
    "update_layout_kwargs": {
        "legend": {"xanchor": "right", "yanchor": "top"},
        "font": {"size": 17}
    },
    "x_axes_kwargs": {
        "type": "-"
    },
    "y_axes_kwargs": {
        "type": "log"
    },
    "xaxes_visible": true,
    "yaxes_visible": true,
    "schema": {
        "header": 3,
        "x_id_is_reg_exp": true
    },
    "post": "max",
    "pio.template": "plotly_white",
    "trace_mode": "markers",
    "update_traces_kwargs": {
        "marker": {"size": 10}
    }
}
```

## Contribute

### unimplemented ideas, in order of priority
0. sign exe and add to releases
1. create better tests
2. Hierarchical plot_info based on folder structure
3. pkl data file support
4. 3D plots
5. plot_info linter

### Develop
1. clone 
1. Navigate into the folder or open the folder with your favorite python IDE
1. create conda env `conda create -n plotme python=3.13`
1. activate env `conda activate plotme`
1. install as -e package `python -m pip install -e .` - Note the dot at the end, it's important

### Build windows exe
1. follow Develop instructions
2. ```choco install visualstudio2019buildtools``` (needed to compile orderedset)
3. ```pip install nuitka orderedset zstandard```
4. ```python -m nuitka plotme --onefile --standalone --include-package=plotly --include-package-data=plotly --nofollow-import-to=module_name=pytest --msvc=latest```

### Test
1. follow Develop instructions
2. Install packages to run automated tests `python -m pip install -e '.[test]'` or `pipx install -e '.[test]' -f`
1. run tests