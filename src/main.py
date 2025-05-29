import shutil, os

from htmlnode import markdown_to_html_node
from texthandling import extract_title

def main():
    copy_static_to_public()
    generate_pages_recursive("./content", "./template.html", "./public")

def copy_static_to_public():
    shutil.rmtree('./public')
    shutil.copytree('./static', './public')

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    with open(from_path) as markdown_file:
        markdown = markdown_file.read()
    template = ""
    with open(template_path) as template_file:
        template = template_file.read()
    node = markdown_to_html_node(markdown)
    html_string = node.to_html()
    title = extract_title(markdown)
    full_html = template.replace('{{ Title }}', title).replace('{{ Content }}', html_string)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as dest_file:
        dest_file.write(full_html)

def generate_pages_recursive(dir_path_content: str, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        if os.path.isfile(entry_path) and entry.endswith(".md"):
            generate_page(entry_path, template_path, os.path.join(dest_dir_path, entry.replace('.md', '.html')))
        elif os.path.isdir(entry_path):
            generate_pages_recursive(entry_path, template_path, os.path.join(dest_dir_path, entry))

main()