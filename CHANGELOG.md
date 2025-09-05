# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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