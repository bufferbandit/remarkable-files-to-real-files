from RemarkableFile import RemarkableFile
from os import listdir


class RemarkableFlatFileSystem(set):

    def __init__(self, PATH_TO_RM_FILES_IN):
        self.PATH_TO_RM_FILES_IN = PATH_TO_RM_FILES_IN
        self.populate_filesystem()
        self.match_parents_to_children()
        self.determine_final_file_paths()

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
        return super().__contains__(key)

    def __getitem__(self, i):
        if type(i) is str:
            return list(x for x in self if x.file_hash == i)[0]
        elif type(i) is int:
            return list(self)[i]

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
        for file in self:
            try:
                file.parent = self[file.parent_id]
            except IndexError:
                pass

    def determine_final_file_paths(self):
        for file in self:
            file.final_file_path = file.recursively_get_parents() + f"{file.rm_file_name}.{file.file_type}"