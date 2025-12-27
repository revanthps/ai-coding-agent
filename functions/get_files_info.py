import os
from langchain_core.tools import tool


get_files_info_schema = {
    "type": "object",
    "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
    "properties": {
        "directory": {
            "type": "string",
            "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)"
        }
    },
    "required": []
}

@tool(args_schema = get_files_info_schema)
def get_files_info(working_dir, directory = "."):
    try:
        abs_work_dir = os.path.abspath(working_dir)
        target_dir = os.path.normpath(os.path.join(abs_work_dir, directory))
        if os.path.commonpath([abs_work_dir, target_dir]) != abs_work_dir:
           return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        files_info = []
        for content in os.listdir(target_dir):
            filepath = os.path.join(target_dir, content)
            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(filepath)
            files_info.append(
                f"- {content}: file_size={file_size} bytes, is_dir={is_dir}"
            )
        
        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"