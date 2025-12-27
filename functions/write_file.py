import os
from langchain_core.tools import tool

write_file_schema = {
    "type": "object",
    "description": "Writes text content to a specified file within the working directory (overwriting if the file exists)",
    "properties": {
        "file_path": {
            "type": "string",
            "description": "Path to the file to write, relative to the working directory"
        },
        "content": {
            "type": "string",
            "description": "Text content to write to the file"
        }
    },
    "required": ["file_path", "content"]
}

@tool(args_schema = write_file_schema)
def write_file(working_dir, file_path, content):
    try:
        abs_work_dir = os.path.abspath(working_dir)
        abs_file_path = os.path.normpath(os.path.join(abs_work_dir, file_path))

        if os.path.commonpath([abs_work_dir, abs_file_path]) != abs_work_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(abs_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(abs_file_path), exist_ok = True)
        
        with open(abs_file_path, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: writing to file: {e}"