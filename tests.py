from functions.get_files_content import get_file_content

def main ():
    
    print("Result for current directory:")
    print(get_file_content("calculator", "main.py"))

    print("\n\nResult for 'pkg' directory:")
    print(get_file_content("calculator", "pkg/calculator.py"))

    print("\n\nResult for '/bin directory:")
    print(get_file_content("calculator", "/bin/cat"))

    print("\n\nResult for 'pkg/' directory:")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

if __name__ == "__main__":
    main()