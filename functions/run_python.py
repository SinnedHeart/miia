import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_target_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_target_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_target_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    
    try: 
        result = subprocess.run(
        ["python", abs_target_path] + args,
        cwd=abs_working_dir,
        timeout=30,
        capture_output=True,
        text=True
        ) 
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        output = ""

        if stdout:
            output += f"STDOUT:\n{stdout}\n"
        if stderr:
            output += f"STDERR:\n{stderr}\n"
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"
        if not output:
            return "No output produced."
        return output
    
    except subprocess.TimeoutExpired:
        return f'Error: Execution timed out after 30 seconds.'
    except Exception as e:
        return f"Error: executing Python file: {e}"