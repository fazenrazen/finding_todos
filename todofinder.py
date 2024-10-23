import os
import re

# find the string where the todo could lie
# find print the starting line where the todo is
# find print the todo block 
# find print the next todo block
# Test using pytest

def find_todo_in_comment(comment_block):
    
    there_is_todo = False
    
    if "TODO" or "Todo" in comment_block:
        there_is_todo = True
    
    # print(comment_block)
    
    return there_is_todo



def find_todos_in_file(file_path):
    
    todos = {}
    comment_reader = []

    # Checks
    multiline_check = False
    double_slash_check = False
    startLine = None
    
    # open the file and read the file to find todos
    with open(file_path, "r", encoding='utf-8') as file:
        # use the enumerate to get the line num and string line
        for line_num, line in enumerate(file, start=1):
            stripped_line = line.strip()

            # reading in multiline /* */ commments 
            if stripped_line.startswith("/*"):
                multiline_check = True
                startLine = line_num

            if multiline_check:
                comment_reader.append(stripped_line)
            
            # done reading from multiline /* */ commments
            if stripped_line.endswith("*/"):
                multiline_check = False
                
                comment_content = " ".join(comment_reader)
                
                if find_todo_in_comment(comment_content):
                    todos[startLine] = comment_reader # might have to change this

                    # reset the comment reader after storing
                    comment_reader = [] 
                    comment_content = []
            
            # if todo is wrapped in // comment
            if stripped_line.startswith("//"):
                comment_block = []
                startLine = line_num
                
                # Continue collecting lines until we find a line that does not start with
                while stripped_line.startswith("//"):
                    comment_block.append(stripped_line)

                    try:
                        line = next(file)
                        stripped_line = line.strip()
                    except StopIteration:
                        break  # Exit if we reach the end of the file
            
                # After collecting the block, check if "TODO" is present
                if any("TODO" in line for line in comment_block):
                    todos[startLine] = comment_block
                    
    
    return todos
                            
def process_directory(directory):
    #print(os.listdir(directory))
    
    # write to just one file
    output_filename = 'whatsnext.txt'
    with open(output_filename, "w", encoding='utf-8') as output_file:
        for filename in os.listdir(directory):
            if(filename.endswith(('.cpp', '.hpp'))):
                # concatenates the directory w each file name to help open file
                file_path = os.path.join(directory, filename)
                
                # Return todos dict from that file from a function
                todos = find_todos_in_file(file_path)
                #output_file.write(f'From file: {filename}\n')
                
                # print all the todos in this file
                if todos:
                    for line_num, comment_block in todos.copy().items():
                        # write file name to each todo block
                        output_file.write(f'From file: {filename}\n')
                        output_file.write(f"Starting at line: {line_num}\n")
                        output_file.write("\n".join(comment_block) + "\n\n")
                        print()
                        
                        
                    #print(f"Processed {filename} -> {output_file}")
                else:
                    print(f"No TODOs found in {filename}")


if __name__ == "__main__":
    path_to_dir = input("Please enter the path directory: ")
    process_directory(path_to_dir)
    
    