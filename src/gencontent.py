import os
from markdown_blocks import markdown_to_html_node


def generate_page(from_path, template_path, dest_path, base_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    content = ""
    with open(from_path, "r") as markdown_file:
        content = markdown_file.read()

    template = ""
    with open(template_path, "r") as template_file:
        template = template_file.read()

    html = markdown_to_html_node(content)
    title = extract_title(content)
    template = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", html.to_html()
    )

    if base_path:
        template = template.replace('href="/', f'href="{base_path}').replace(
            'src="/', f'src="{base_path}'
        )

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)


def generate_pages_recursively(
    dir_path_content, template_path, dest_dir_path, base_path
):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    for item in os.listdir(dir_path_content):
        content_item = os.path.join(dir_path_content, item)
        dest_item = os.path.join(dest_dir_path, item)
        if os.path.isfile(content_item):
            dest_item = dest_item.replace(".md", ".html")
            generate_page(content_item, template_path, dest_item, base_path)
        else:
            generate_pages_recursively(
                content_item, template_path, dest_item, base_path
            )


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:]
    raise Exception("Error: no title found")
