from functions.get_files_info import get_files_info

def tests_get_file_info():
    result = get_files_info("calculator", ".")
    print(f"Result for current directory: {result}")
    
    result = get_files_info("calculator", "pkg")
    print(f"Result for pkg directory: {result}")

    result = get_files_info("/bin")
    print(f"Result for /bin directory: {result}")

    result = get_files_info("calculator", "../")
    print(f"Result for '../' directory: {result}")

if __name__ == "__main__":
    tests_get_file_info()