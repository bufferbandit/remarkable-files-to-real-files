from RemarkableFile import RemarkableFile
from os import listdir


class RemarkableFlatFileSystem(set):

    def __init__(self, path_to_rm_files_in, path_to_rm_files_out="/"):
        self.PATH_TO_RM_FILES_IN = path_to_rm_files_in
        self.PATH_TO_RM_FILES_OUT = path_to_rm_files_out
        self.populate_filesystem()
        self.match_parents_to_children()
        self.determine_rm_parent_paths()
        self.determine_rm_file_paths()

    def populate_filesystem(self):
        for file_path in listdir(self.PATH_TO_RM_FILES_IN):
            if "." in file_path:
                # Split file
                file_name, file_ext, *_ = file_path.split(".")
                if file_ext in {"pdf", "epub", "metadata", "pagedata", "content"}:
                    # Create remarkable file
                    remarkable_file = self[file_name] if file_name in self \
                        else RemarkableFile(file_hash=file_name, root=self.PATH_TO_RM_FILES_OUT)

                    remarkable_file.real_file_extensions.add(file_ext)
                    remarkable_file.real_file_paths.add(self.PATH_TO_RM_FILES_IN + file_path)
                    remarkable_file.set_all_data()

                    if remarkable_file.rm_file_metadata and remarkable_file.rm_file_metadata["parent"] != "trash":
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

    def get_children_for_parent_file_hash(self, file_hash):
        for file in self:
            if file.parent_file_hash == file_hash:
                yield file

    def get_children_for_parent(self, parent):
        for file in self:
            parent = self[0]
            if file.parent_rm_file == parent:
                yield file

    def match_parents_to_children(self):
        for file in self:
            try:
                file.parent_rm_file = self[file.parent_file_hash]
            except IndexError:
                pass

    def determine_rm_parent_paths(self):
        for file in self:
            file.rm_parent_path = file.recursively_get_parents()

    def determine_rm_file_paths(self):
        for file in self:
            file.rm_file_path = f"{file.rm_parent_path}{file.rm_file_name}.{file.rm_file_type}"
