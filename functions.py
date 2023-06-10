def get_todos(filepath):
    with open(filepath, 'r') as file:
        content = file.readlines()  # each line of the file will be an item of the list 'content'
        modified_todos=[]
        for item in content:
            if item != "\n":
                modified_todos.append(item.strip('\n'))


    return modified_todos

if __name__=="__main__" :
    print("well hello there looks like you ran functions.py directly")

#when you run functions.py using import via main the value of __name__ = "__functions__"
#when you run functions .py directly __name__="__main__" i know weird hai ulta hotay