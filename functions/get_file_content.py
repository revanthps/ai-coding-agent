import os
from config import MAX_CHARS
from langchain_core.tools import tool


get_file_content_schema = {
    "type": "object",
    "description": f"Retrieves the content (at most {MAX_CHARS} characters) of a specified file within the working directory",
    "properties": {
        "file_path": {
            "type": "string",
            "description": "Path to the file to read, relative to the working directory"
        }
    },
    "required": ["file_path"]
}

@tool(args_schema = get_file_content_schema)
def get_file_content(working_dir, file_path):
    try:
        abs_work_dir = os.path.abspath(working_dir)
        abs_file_path = os.path.normpath(os.path.join(abs_work_dir, file_path))
        if os.path.commonpath([abs_work_dir, abs_file_path]) != abs_work_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or not a regular file: "{file_path}"'
        with open(abs_file_path, 'r') as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return content


    except Exception as e:
        return f'Error reading file "{file_path}": {e}'