schema = {
    "type": "object",
    "properties":
        {
            "title_text": {"type": "string"},
            "x_title": {"type": "string"},
            "x_id": {"type": "string"},
            "y_title": {"type": "string"},
            "y_id": {"type": "array", "items": {"type": "string"}},
            "schema": {"type": "object", "properties": {
                "file_extension": {"type": "string", "enum":[
                                            "csv",
                                            "txt",
                                            "xls",
                                            "xlsx"
                                         ]},
                "seperator": {"type" "string"},
                "header": {"type": ["int", "array", "NULL", "string"]},
                "index_col",
                "x_id_in_file_name"
            }},

        }
}
