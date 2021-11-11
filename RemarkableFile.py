from json import load


class RemarkableFile:
    def __init__(self, file_hash):
        self.file_hash = file_hash
        self.file_extensions = set()
        self.file_paths = set()
        self.file_type = ""
        self.file_name = ""
        self.rm_file_name = ""
        self.parent_id = ""
        self.real_file_path = ""
        self.final_file_path = ""
        self.parent_rm_file = None
        self.metadata = None
        self.content_data = None
        self.parent = None

    def __hash__(self):
        return hash(self.file_hash)

    def __eq__(self, other):
        if type(other) is RemarkableFile:
            return self.file_hash == other.file_hash
        return super().__eq__(other)

    def __ne__(self, other):
        if type(other) is RemarkableFile:
            return self.file_hash != other.file_hash
        return super().__ne__(other)

    def recursively_get_parents(self, root="/"):
        if self.parent:
            return self.parent.recursively_get_parents() + self.parent.rm_file_name + "/"
        return root

    def get_metadata_file(self):
        for file_name in self.file_paths:
            if file_name.endswith(".metadata"):
                with open(file_name, "r") as f:
                    return load(f)

    def get_content_file(self):
        for file_name in self.file_paths:
            if file_name.endswith(".content"):
                with open(file_name, "r") as f:
                    return load(f)

    def set_all_data(self):
        self.metadata = self.get_metadata_file()
        if self.metadata:
            self.rm_file_name = self.metadata["visibleName"]
            self.parent_id = self.metadata["parent"]
        self.content_data = self.get_content_file()
        self.file_type = self.determine_filetype()
        for path in self.file_paths:
            if self.file_type == "pdf" and path.endswith("pdf"):
                self.real_file_path = path
            elif self.file_type == "epub" and path.endswith(".epub"):
                self.real_file_path = path

    def determine_filetype(self):
        if self.file_extensions == {"content", "metadata"}:
            return "collection"
        if {"downloading"}.issubset(self.file_extensions):
            return "downloading"
        if self.content_data:
            return self.content_data["fileType"]
