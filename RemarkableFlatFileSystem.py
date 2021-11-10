from RemarkableFile import RemarkableFile
from os import listdir


class RemarkableFlatFileSystem(set):

    def __init__(self, PATH_TO_RM_FILES_IN):
        self.PATH_TO_RM_FILES_IN = PATH_TO_RM_FILES_IN
        self.populate_filesystem()
        self.match_parents_to_children()

    def populate_filesystem(self):
        for file_path in listdir(self.PATH_TO_RM_FILES_IN):
            if "." in file_path:
                # Split file
                file_name, file_ext, *_ = file_path.split(".")
                if file_ext in {"thumbnails", "pdf", "epub", "metadata",
                                "pagedata", "content", "downloading"}:

                    # Create remarkable file
                    remarkable_file = self[file_name] \
                        if file_name in self \
                        else RemarkableFile(file_hash=file_name)

                    # Add rmfile to remarkable filesystem
                    if file_ext != "pagedata" or file_ext != "epubindex":
                        remarkable_file.file_extensions.add(file_ext)

                    remarkable_file.file_paths.add(self.PATH_TO_RM_FILES_IN + file_path)
                    remarkable_file.set_all_data()

                    # Append
                    self.add(remarkable_file)

    def __contains__(self, key):
        if type(key) is str:
            return any(x for x in self if x.file_hash == key)
        else:
            return super().__contains__(key)

    def __getitem__(self, i):
        if type(i) is str:
            return list(x for x in self if x.file_hash == i)[0]
        elif type(i) is int:
            return list(self)[i]

    def __setitem__(self, i, v):
        print(i, v)

    def get_children_for_parent_id(self, parent_id):
        for file in self:
            if file.parent_id == parent_id:
                yield file

    def get_children_for_parent(self, parent):
        for file in self:
            parent = self[0]
            if file.parent == parent:
                yield file

    def match_parents_to_children(self):
        for file in [file for file in self if file.file_type == "collection"]:
            this_folder_children = self.get_children_for_parent_id(file.file_hash)
            for child_file in this_folder_children:
                child_file.parent_id = file.file_hash
                child_file.parent = file
                child_file.real_file_path = child_file.recursively_get_parents() + f"{child_file.rm_file_name}.{child_file.file_type}"

#     def __len__(self): return len(self.list)
#     def __getitem__(self, i): return self.list[i]
#     def __delitem__(self, i): del self.list[i]
#     def __setitem__(self, i, v): self.list[i] = v
#     def __str__(self): return str(self.list)
