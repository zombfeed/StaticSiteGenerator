import os
from markdown_blocks import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    content = ""
    with open(from_path, "r") as f:
        content = f.read()

    template = ""
    with open(template_path, "r") as f:
        template = f.read()

    html = markdown_to_html_node(content)
    title = extract_title(content)
    template = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", html.to_html()
    )

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:]
    raise Exception("Error: no title found")
