from functions.get_file_content import get_file_content

def test_get_file_content():
    work_dir = "calculator"

    content = get_file_content(work_dir, 'main.py')
    print(f"Content of main.py: {content}")

    content = get_file_content(work_dir, 'pkg/calculator.py')
    print(f"Content of calculator.py: {content}")

    content = get_file_content(work_dir, '/bin/cat')
    print(f"Content of '/bin/cat': {content}")

    content = get_file_content(work_dir, 'pkg/does_not_exist.py')
    print(f"Content of 'pkg/does_not_exist.py': {content}")



if __name__ == "__main__":
    test_get_file_content()