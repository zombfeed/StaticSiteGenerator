import os
import sys
import shutil
from copystatic import copy_files_recursive
from gencontent import generate_pages_recursively


static_dir = "./static"
public_dir = "./docs"
content_dir = "./content"
template_path = "./template.html"


def main():
    base_path = ""
    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    print("Deleting public directory...")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    print("Copying static files to public directory...")
    copy_files_recursive(static_dir, public_dir)

    print("Generating pages...")
    generate_pages_recursively(content_dir, template_path, public_dir, base_path)


if __name__ == "__main__":
    main()
