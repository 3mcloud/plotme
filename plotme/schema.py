schema = {
    "type": "object", "properties":
        {
            "not_a_plot": {"type": "boolean"},
            "title_text": {"type": "string"},
            "x_title": {"type": "string"},
            "x_id": {"type": "string"},
            "y_title": {"type": "string"},
            "y_id": {"type": ["array", "string"], "items": {"type": "string"}},
            "schema": {"type": "object", "properties": {
                "file_extension": {"type": "string", "enum": [
                    "csv",
                    "txt",
                    "xls",
                    "xlsx"
                ]},
                "seperator": {"type": "string"},
                "header": {"type": ["integer", "array", "null", "string"]},
                "index_col": {"type": ["null", "integer"]},
                "x_id_in_file_name": {"type": "boolean"},
            }},
            "pre": {"type": "array", "items": {"type": "string", "enum": [
                "remove_null",
                "remove_zero",
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
    "not_a_plot": False,
    "title_text": "plot title",
    "x_title": "label in plot, x_id used if unspecified",
    "x_id": "x column header name or name of parameter to be extracted from file name",
    "y_title": "label in plot, y_id used if unspecified",
    "y_id": ["list of column headers, single column header or column letter"],
    "schema": {
        "file_extension": "only set if you want to limit the data files to a certain type ie csv or xlsx",
        "seperator": ",(default)",
        "header": "int",
        "index_col": "int of index column, NULL or don't include if not used",
        "x_id_in_file_name": "true or false"
    },
    "pre": ["remove_null", "remove_zero"],
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
    "marker_symbols": ["list of marker symbols numbers, must have one for each trace"]
}
