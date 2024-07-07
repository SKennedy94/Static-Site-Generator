from htmlnode import *
from textnode import *
import os
import shutil
import pathlib

def recursive_file_copy(source,destination):
    for dir in os.listdir(source):
        path = os.path.join(source,dir)
        destination_path = os.path.join(destination,dir)

        if os.path.isfile(path):
            print(f"Copying file {path}")
            shutil.copy(path,destination)
        else:
            os.mkdir(destination_path)
            recursive_file_copy(path,destination_path)

def static_copy(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    
    os.mkdir(destination)
    recursive_file_copy(source,destination)

def extract_title(block):
    if not block.startswith("# "):
        raise ValueError("Markdown Error: Markdown Must start with a h1 header block.")
    return block[2:]   

def generate_page(from_path, dest_path, template_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as markdown_file, open(template_path) as template_file:
        template = template_file.read()
        markdown = markdown_file.read()

    title = extract_title(markdown.split('\n')[0])
    root_node = markdown_to_html_node(markdown)
    html = root_node.to_html()

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    print(f"generating page for {dest_path}")
    with open(dest_path, "a+") as html_file:
            html_file.truncate(0)
            html_file.write(template)

def generate_pages_recursive(dir_path_content, dest_dir_path, template_path ):
    directories = os.listdir(dir_path_content)
    print(dest_dir_path)
    for dir in directories:
        print(dir)
        path = os.path.join(dir_path_content,dir)
        print(path)
        if dir.endswith('.md') and os.path.isfile(path):
            dest_file_path = pathlib.Path(os.path.join(dest_dir_path, os.path.splitext(dir)[0] + '.html'))
            print(dest_file_path)
            generate_page(path,dest_file_path,template_path)
        elif os.path.isdir(path):
            dest_path = pathlib.Path(os.path.join(dest_dir_path,dir))
            generate_pages_recursive(path,dest_path,template_path)

def main():
    #Static Copy
    static_path = r"./static"
    static_dest = r"./public"
    #generate page
    from_path = r"./static/content"
    dest_path = r"./public/content"
    template_path = r"./template.html"

    static_copy(static_path,static_dest)
    generate_pages_recursive(from_path,dest_path,template_path)

main()

