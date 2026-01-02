import os
import shutil
from copystatic import copy_files_recursive
from gencontent import generate_pages_recursively


static_dir = "./static"
public_dir = "./public"
content_dir = "./content"
template_path = "./template.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    print("Copying static files to public directory...")
    copy_files_recursive(static_dir, public_dir)

    print("Generating pages...")
    generate_pages_recursively(content_dir, template_path, public_dir)


if __name__ == "__main__":
    main()
