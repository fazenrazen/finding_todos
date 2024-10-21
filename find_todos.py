import os
import re


def find_todos_in_file(file_path):

    # find all the todos and store them into the list
    todos = []
    multiline = []
    double_slash_multiline = []

    file_path = 'test_case.cpp'
    
    # Checks
    multiline_check = False
    double_slash_check = False
    previous_double_slash = True
    count = 0
    
    # open the file and read the file in    
    with open(file_path, "r", encoding='utf-8') as file:
        for lineNumber, line in enumerate(file, start=1):
            stripped_line = line.strip()

            # Working on messages between /* */
            if stripped_line.startswith("/*"):
                multiline_check = True
                
            if multiline_check:
                multiline.append(stripped_line)
            
            if stripped_line.endswith("*/"):
                multiline_check = False
                multiline_content = " ".join(multiline)
                
                if "TODO" in multiline_content:
                    todos.append(multiline[:])  
                multiline = []
            
            if stripped_line.startswith("//"):
                # Collect all lines in a comment block until a non-comment line is found
                comment_block = []
                
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
                    todos.append(comment_block)  # Add the entire block if it contains "TODO"
                      
    return todos


def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(('.cpp', '.hpp')):
            file_path = os.path.join(directory, filename)
            todos = find_todos_in_file(file_path)
            
            if todos:
                output_filename = f"output_{filename}.txt"
                with open(output_filename, "w", encoding='utf-8') as output_file:
                    output_file.write(f"Processed {filename} -> {output_filename} \n")
                    for todo_block in todos:
                        output_file.write("\n".join(todo_block) + "\n\n")

            else:
                print(f"No TODOs found in {filename}.")


if __name__ == "__main__":
    directory_path = input("Please enter the path here: ")    
    process_directory(directory_path)

    
    
            
