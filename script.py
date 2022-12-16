'''
- Book has 5 chapters under 'Book/Chapter # files'.
- For each chapter, get all files' contents from *.txt as snippet to dict entry
- Path to all files in pattern: 'Book/Chapter # files/Listings'
- Write each snippet as nbformat code cell:
    nbformat.v4.new_code_cell(source='', **kwargs)
        Create a new code cell
- Path to datasets differs in git repo from actual snippet in Book
- Snippets are written in Python 2, utilize a package to auto-convert to Python 3
- Save to chapter#.ipynb
'''
import os
import nbformat as nbf

def main():
    BOOK_PATH = 'Book/'

    PATH = 'Book/Chapter 1 files/Listings/'  # const to test out initial code
    # print("getcwd", os.getcwd())
    # print("Length of BOOK PATH dir", len(os.listdir(BOOK_PATH)))
    file_list = get_sorted_file_list(BOOK_PATH)
    # print(file_list)
    # print("COUNT of dirs in BOOK PATH", len(file_list))

    for count in range(len(file_list)):
    
        # print("COUNT: ", count)
        cur_dir = file_list[count]
        # print("Current Dir:", cur_dir)
        
        chapter_num = cur_dir[8:9]
        # print("Chapter_num: ", chapter_num)
        
        # rename_files(path_left+chapter_num+path_right)

        snippets = extract_contents_from_files(chapter_num)
        # print(snippets)

        write_to_Jupyter_notebook(chapter_num, snippets)


def get_sorted_file_list(dir):
    try:
        file_list = [f for f in os.listdir(dir) if not f.startswith('.')]
        # print(file_list)
    except FileNotFoundError:
        pass
    else:
        # source: https://www.codegrepper.com/tpc/python+sort+files+by+number+in+name
        file_list.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    
    return file_list


def rename_files(dir):
    for file in os.listdir(dir):
        
        if file.endswith(".txt"):
            # print(file)
            new_name = file.removeprefix("Listing 1-")
            os.rename(dir+file, dir+new_name)
            print(file)


def extract_contents_from_files(num):
    # print()
    # print("-- extract_contents_from_files(num) --")
    text = {}
    path_left = 'Book/Chapter '              # for actual looping
    path_right = ' files/Listings/' 
    cur_path = path_left+num+path_right
    # print("PATH:", cur_path)
    file_list = get_sorted_file_list(cur_path)
    # print("SORTED", file_list)

    for file in file_list:
        try:
            # print(file)
            with open(cur_path+file,'r') as f:
                k, _ = file.split(".txt")
                v = f.read()
                # print(f"key: {k}, contents: {v}")
                text[k] = v
        except FileNotFoundError("file not found"):
            pass
            
    return text

def write_to_Jupyter_notebook(num , contents):

    chapter = "Chapter " + num

    # Create a new jupyter notebook object.
    nb = nbf.v4.new_notebook()

    # The header 1 title for the jupyter notebook, using chapter numbers. 
    nb_title = f"# {chapter} "

    # Create a new markdown cell object that contains the title.
    markdown_cell = nbf.v4.new_markdown_cell(nb_title)

    # Add the above markdown cell object into the jupyter notebook cells.
    nb['cells'] = [markdown_cell]

    for k, data in contents.items():
        # print(k)
        # use the chapter number and listing number to verify cells are in correct sorted order.
        expanded = "# "+ k + "\n\n"+data
        # create new cell of type code
        cell = nbf.v4.new_code_cell(source=expanded)
        # append to notebook list of cells
        nb['cells'].append(cell)


    # write the above notebook object to a .ipynb file.
    nbf.write(nb, "chapter" + num + ".ipynb", 4)
    print(f"\nwrite_to_Jupyter_notebook\t## Chapter {num} ##")



if __name__ == "__main__":
    main()
