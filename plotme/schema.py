schema = {
    "type": "object", "properties":
        {
            "not_a_plot": {"type": "boolean"},
            "title_text": {"type": "string"},
            "x_title": {"type": "string"},
            "x_id": {"type": "string"},
            "y_title": {"type": "string"},
            "y_id": {"type": ["array", "string"], "items": {"type": "string"}},
            "showlegend": {"type": "boolean"},
            "xaxes_visible": {"type": "boolean"},
            "yaxes_visible": {"type": "boolean"},
            "folder_include_filter": {"type": "string"},
            "folder_exclude_filter": {"type": "string"},
            "schema": {"type": "object", "properties": {
                "file_include_filter": {"type": ["string", "array"]},
                "file_exclude_filter": {"type": ["string", "array"]},
                "file_extension": {"type": "string"},
                # "file_extension": {"type": "string", "enum": [
                #     "csv",
                #     "txt",
                #     "xls",
                #     "xlsx"
                # ]},
                "seperator": {"type": "string"},
                "header": {"type": ["integer", "array", "null", "string"]},
                "index_col": {"type": ["null", "integer"]},
                "x_id_in_file_name": {"type": "boolean"},
                "x_time_format": {"type": "string"},
                "x_id_is_reg_exp": {"type": "boolean"},
                "trace_label": {"type": "string", "enum": [
                    # "y_id",  # this shouldn't be needed anymore
                    "folder_name",
                    "file_name",
                ]},
                "remove_from_trace_label": {"type": "string"},
            }},
            "pre": {"type": "array", "items": {"type": "string", "enum": [
                "remove_null",
                "remove_zero",
                "remove_strings",
                "convert_to_float",
            ]}},
            "post": {"type": "string", "enum": [
                "avg",
                "max",
                "min",
            ]},
            "constant_lines": {"type": "object", "properties": {
                "x=": {"type": "array", "items": {"type": "number"}},
                "y=": {"type": "array", "items": {"type": "number"}},
            }},
            "error_y": {"type": "object", "properties": {
                "type": {"type": "string", "enum": [
                    "percent",
                    "data"
                ]},
                "value": {"type": "number"},
                "visible": {"type": "boolean"},
            }},
            "pio.template": {"type": "string"},
            "trace_mode": {"type": "string", "enum": [
                "markers",
                "lines"
            ]},
            "marker_symbols": {"type": "array", "items": {"type": "integer"}},
        }
}

template = {
    # "not_a_plot": False,  # inheritance not implemented yet
    "title_text": "plot title",
    "x_title": "label in plot, x_id used if unspecified",
    "x_id": "x column header name or name of parameter to be extracted from file name",
    "y_title": "label in plot, y_id used if unspecified",
    "y_id": ["array of column headers, single column header or column letter"],
    "showlegend": True,
    "xaxes_visible": True,
    "yaxes_visible": True,
    "folder_include_filter": "must be in the folder name, string or array of strings",
    "folder_exclude_filter": "must not be in the folder name, string or array of strings",
    "schema": {
        "file_include_filter": "must be in data file name, string or array of strings",
        "file_exclude_filter": "must not be in data file name, string or array of strings",
        "file_extension": "only set if you want to limit the data files to a certain type ie csv or xlsx",
        "seperator": ",(default)",
        "header": "int row number(s) containing column labels and marking the start of the data (zero-indexed).",
        "index_col": "int of index column, NULL or don't include if not used",
        "x_id_in_file_name": "true or false",
        "x_time_format": "string datetime format e.g. %y%m%d_%H%M%S",
        "x_id_is_reg_exp": "true or false, set to true if x_id is a regular expression",
        "trace_label": "file_name(default), other options: folder_name",
        "remove_from_trace_label": "string to remove from trace labels"
    },
    "pre": ["remove_null", "remove_zero", "remove_strings", "convert_to_float"],
    "post": "avg, max or min",
    "constant_lines": {
        "x=": [],
        "y=": []
    },
    "error_y": {
        "type": "percent",
        "value": "change to floating point or integer",
        "visible": True},
    "pio.template": "plotly_white, see readme for more examples",
    "trace_mode": "markers(default) or lines",
    "marker_symbols": ["array of marker symbols numbers, must have one for each trace"]
}
