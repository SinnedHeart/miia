import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, directory))
    
    if not target_path.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(target_path):
        return f'Error: "{directory}" is not a directory' 
    
    try:
        files = os.listdir(target_path)
        output_lines = []

        for file in files:
            file_path = os.path.join(target_path, file)

            try:
        
                size = os.path.getsize(file_path)
                is_dir = os.path.isdir(file_path)
                output_lines.append(f'-{file}: file_size={size} bytes, is_dir={is_dir}')

            except Exception as e:
                output_lines.append(f'Error: Could not get info for "{file}": {e}')
                
       
        return "\n".join(output_lines)
    except Exception as e:
        return f'Error: Failed to process directory "{directory}": {e}'
    

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)