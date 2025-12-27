from functions.run_python_file import run_python_file

def test():
    work_dir = "calculator"

    result = run_python_file(work_dir, "main.py")
    print(result)

    result = run_python_file(work_dir, "main.py", ["3 + 5"])
    print(result)

    result = run_python_file(work_dir, "tests.py")
    print(result)

    result = run_python_file(work_dir, "../main.py")
    print(result)

    result = run_python_file(work_dir, "nonexist.py")
    print(result)

    result = run_python_file(work_dir, "lorem.txt")
    print(result)

if __name__ == "__main__":
    test()