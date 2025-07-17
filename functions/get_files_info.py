import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)

    abs_working_dir = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)

    if not abs_full_path.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(full_path):
        return f'Error: "{directory} is not a directory' 
    
    try:
        files = os.listdir(full_path)
        output_lines = []

        for file in files:
            file_path = os.path.join(full_path, file)

            try:
        
                size = os.path.getsize(file_path)
                is_dir = os.path.isdir(file_path)
                output_lines.append(f'-{file}: file_size={size} bytes, is_dir={is_dir}')

            except Exception as e:
                output_lines.append(f'Error: Could not get info for "{file}": {e}')
                
       
        return "\n".join(output_lines)
    except Exception as e:
        return f'Error: Failed to process directory "{directory}": {e}'