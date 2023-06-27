import streamlit as st
import functions
#the entire script gets executed fromm top to bottom when an 'event' occurs

obtained_todos=functions.get_todos("tasks.txt")

def add_todo():
    todo_to_add=st.session_state["new_todo"]
    with open("tasks.txt", 'a+') as file:
        file.write(todo_to_add + "\n")

st.title("My Todo list")

for index,todo in enumerate(obtained_todos):
    checkbox=st.checkbox(todo,key=todo)
    # you need a key so that the item becomes a part of session state
    #the key needs to be unique for diff items
    if checkbox:
        obtained_todos.pop(index)
        file = open('tasks.txt', 'w')
        for item in obtained_todos:
            file.writelines(item + "\n")

        file.close()

        del st.session_state[todo] #to upadate session_state dictionary
        st.experimental_rerun() #just needed syntax if dosent work just try st.rerun()


st.text_input(label="Enter a todo:",placeholder="Add new todo",on_change=add_todo,
              key="new_todo")

#st.session_state  ---writing this will print the dictionary like item on browser
# session_state is like a dictionary
