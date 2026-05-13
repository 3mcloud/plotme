# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.7.0] - 2026-05-13

### Added
- sorting of data folders, makes behavior more consistant with different OSes
- ability to use wild cards in filters using fnmatch
- `auto_clean` `pre` processing option

### Changed
- plot_info_id override argument to --config from --json to be consistent with support for both json and yml

### Fixed
- `pre` processsing option `remove_strings` but it also removes any Null
- `x_id_in_file_name` with `x_time_format` on MacOS and Linux 

## [1.6.0] - 2026-05-06

### Added
- array type for folder include/exclude (schema)
- ability to slice the input data

### Changed
- schema no longer allows unsupported keys thus spelling errors are caught

### Fixed
- file extension matching, was only matching lower case, now matches any
- implementation and spelling of `separator`

## [1.5.0] - 2026-04-11

### Added
- ability to use yaml for plot_info files as well as json

## [1.4.0] - 2025-12-29

### Added
- ability to pass plotly traces keyword arguments e.g. 'marker', 'selector' etc via `update_traces_kwargs`
- top level schema validation for `x_axes_kwargs` and `y_axes_kwargs`
- example of marker size to example json in readme

### Changed
- schema validation for trace_mode now allows combinations such as 'lines+markers'
- readme to better indicate the keys of the pass through arguments

## [1.3.0] - 2025-09-25

### Added
- ability to pass plotly layout keyword arguments e.g. 'font, 'legend' etc via `update_layout_kwargs`

### Changed
- useability improvement: space characters are stripped from x_id, y_id and also from the loaded dataframe column headers therefore leading and trailing spaces no longer create errors

## [1.2.0] - 2025-09-05

### Added
- remove_from_trace_label
- file and folder filters can take an array of strings as will as a single string
- x_time_format: x value time stamp in file name conversion to seconds using [strptime format codes](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes)
- x_id_is_reg_exp
- this changelog

### Changed
- features section of readme indicates the keys for the referenced features
- html/png file name generation: my_plot_info.json -> my_plot.html
- correct references of list to array in schema template - JSON calls them arrays

### Fixed
- min and max post processing functionality
- load_data.py: stack trace logging on error during try in Folder init