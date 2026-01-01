import os
import shutil


def copy_files_recursive(src_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    for item in os.listdir(src_dir):
        src_item = os.path.join(src_dir, item)
        dst_item = os.path.join(dst_dir, item)
        print(f"Copying {src_item} -> {dst_item}")
        if os.path.isfile(src_item):
            shutil.copy(src_item, dst_item)
        else:
            copy_files_recursive(src_item, dst_item)
