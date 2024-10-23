import os
import re

# find the string where the todo could lie
# find print the starting line where the todo is
# find print the file name of where the todo is
# find print the todo block 
# find print the next todo block
# Test using pytest

def find_todos_in_file(file_path):
    print()
    

def process_directory(directory):
    #print(os.listdir(directory))
    
    # write to just one file
    output_filename = 'whatsnext.txt'
    with open(output_filename, "w", encoding='utf-8') as output_file:
        for filename in os.listdir(directory):
            if(filename.endswith(('.cpp', '.hpp'))):
                file_path = os.path.join(directory, filename)
                # Return the todos list from that file from a function
                todos = find_todos_in_file(file_path)
                
                output_file.write(f'Todos from file: {filename}\n')
                
                # print all the todos in this file
                if todos:
                    for todo_block in todos:
                        output_file.write("\n".join(todo_block) + "\n\n")
                    print(f"Processed {filename} -> {output_file}")
                else:
                    print(f"No TODOs found in {filename}")


if __name__ == "__main__":
    path_to_dir = input("Please enter the path directory: ")
    process_directory(path_to_dir)
    
    