from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_files_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file_content import write_file
from config import WORKING_DIRECTORY

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args

    function_args['working_directory'] = WORKING_DIRECTORY



    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    FUNCTION_REGISTRY = {
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
        "get_files_info": get_files_info,
    }

    if function_name in FUNCTION_REGISTRY:
        func = FUNCTION_REGISTRY[function_name]
        func_result = func(**function_args) 

        
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result":func_result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )