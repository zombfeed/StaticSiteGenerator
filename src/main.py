import os
import shutil
from copystatic import copy_files_recursive

static_dir = "./static"
public_dir = "./public"


def main():
    print("Deleting public directory...")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    print("Copying static files to public directory...")
    copy_files_recursive(static_dir, public_dir)


if __name__ == "__main__":
    main()
