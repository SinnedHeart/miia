import os
from config import MAX_CHAR
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    
    try:
        with open(target_path, "r") as f:
            true_size = os.path.getsize(target_path)
            file_content = f.read(MAX_CHAR)

            if true_size > MAX_CHAR:
                file_content += f'...File "{file_path}" truncated at {MAX_CHAR} characters'

        return file_content
    except Exception as e:
        return f'Error: Could not read "{file_path}": {e}'


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description = "Get the content of a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to get the content of, relative to the working directory"
            )
        },
        required=["file_path"]
    )
)