schema = {
    "type": "object", "properties":
        {
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
