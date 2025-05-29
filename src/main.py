import shutil, os, sys

from htmlnode import markdown_to_html_node
from texthandling import extract_title

def main():
    basepath = "/" if len(sys.argv) < 2 else sys.argv[1]
    copy_static_to_public()
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)

def copy_static_to_public():
    shutil.rmtree('./docs')
    shutil.copytree('./static', './docs')

def generate_page(from_path, template_path, dest_path, basepath):
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
    full_html = template.replace('{{ Title }}', title).replace('{{ Content }}', html_string).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as dest_file:
        dest_file.write(full_html)

def generate_pages_recursive(dir_path_content: str, template_path, dest_dir_path, basepath):
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        if os.path.isfile(entry_path) and entry.endswith(".md"):
            generate_page(entry_path, template_path, os.path.join(dest_dir_path, entry.replace('.md', '.html')), basepath)
        elif os.path.isdir(entry_path):
            generate_pages_recursive(entry_path, template_path, os.path.join(dest_dir_path, entry), basepath)

main()