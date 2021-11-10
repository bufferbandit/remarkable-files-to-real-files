from RemarkableFile import RemarkableFile
from os import listdir

from RemarkableFlatFileSystem import RemarkableFlatFileSystem

# PATH = "~/.var/app/com.usebottles.bottles/data/bottles/bottles/TrueResBottle/drive_c/users//AppData/Roaming/remarkable/desktop/"
# PATH = "./data/xochitl/"
PATH = "./data/remarkable/xochitl/"

rm_files = RemarkableFlatFileSystem()

for file_path in listdir(PATH):
    if "." in file_path:
        # Split file
        file_name, file_ext, *_ = file_path.split(".")
        if file_ext in {"thumbnails", "pdf", "epub", "metadata",
                        "pagedata", "content", "downloading"}:

            # Create remarkable file
            remarkable_file = rm_files[file_name] \
                if file_name in rm_files \
                else RemarkableFile(file_hash=file_name)

            # Add rmfile to remarkable filesystem
            if file_ext != "pagedata" or file_ext != "epubindex":
                remarkable_file.file_extensions.add(file_ext)

            remarkable_file.file_paths.add(PATH + file_path)
            remarkable_file.set_all_data()

            # Append
            rm_files.add(remarkable_file)


# f = rm_files
f = [file for file in rm_files if file.file_type == "collection"]
r = rm_files.recursive_method(f)

# for x in rm_files:
#     if x.file_type == "collection":
#         # Get the root folders
#         if not x.parent_id:
#             print(x.rm_file_name)

        # print(x.file_extensions)  # print(x.file_paths,x.file_extensions, x.file_type, x.rm_file_name)
        # print(x.rm_file_name)
        # print(x.parent_id)

