from functions.write_file import write_file


def test():

    work_dir = "calculator"

    result = write_file.invoke({
        "work_dir": work_dir,
        "file_path": "lorem.txt", 
        "content":"wait, this isn't lorem ipsum"
        })    
    print(result)

    result = write_file.invoke({
        "work_dir": work_dir, 
        "file_path": "pkg/morelorem.txt", 
        "content": "more lore ipsum has been written"
        })
    print(result)

    result = write_file.invoke({
        "work_dir": work_dir, 
        "file_path": "/tmp/temp.txt", 
        "content": "this should not be allowed"
        })
    print(result)

    result = write_file.invoke({
        "work_dir": work_dir, 
        "file_path":"pkg2/temp.txt", 
        "content": "this should be allowed"
        })
    print(result)

    # result = write_file(work_dir, "/tmp/temp.txt", "this should not be allowed")
    # print(result)

    # result = write_file(work_dir, "pkg2/temp.txt", "this should not be allowed")
    # print(result)


if __name__=="__main__":
    test()

