
from functions.run_python import run_python_file
def main ():
    
    print("Should print the calculator's usage instructions")
    print(run_python_file("calculator", "main.py"))

    print("\n\nshould run the calculator...")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))

    print("\n\nResult for 'calculator, test.py'")
    print(run_python_file("calculator", "tests.py"))

    print("\n\nThis should return an error")
    print(run_python_file("calculator", "../main.py"))

    print("\n\nThis should also return an error")
    print(run_python_file("calculator", "nonexistent.py"))

if __name__ == "__main__":
    main()