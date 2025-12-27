from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from langchain_core.messages import ToolMessage
import json
from config import WORKING_DIR



tools = [get_files_info, get_file_content, run_python_file, write_file]

function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

def call_function(function_call, verbose=False):
    if verbose:
        print(f" - Calling function: {function_call['name']}({function_call["args"]})")
    else:
        print(f" - Calling function: {function_call['name']}")

    function_name = function_call["name"] or ""
    if function_name not in function_map:
        return ToolMessage(
            content=json.dumps({"error": f"Unknown function: {function_name}"}),
            tool_call_id=function_call["id"], 
            name=function_name
        )
    
    args = dict(function_call["args"]) if function_call["args"] else {}
    args["working_dir"] = WORKING_DIR
    result = function_map[function_name].invoke(args)

    return ToolMessage(
        content = json.dumps({"result": result}),
        tool_call_id=function_call["id"], 
        name=function_name,
    )

