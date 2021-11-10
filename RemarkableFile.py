from json import load


class RemarkableFile:
    def __init__(self, file_hash):
        self.file_hash = file_hash
        self.file_extensions = set()
        self.file_paths = set()
        self.file_type = ""
        self.file_name = ""
        self.rm_file_name = ""
        self.parent_rm_file = None
        self.metadata = None
        self.content_data = None
        self.parent = None
        self.parent_id = ""
        self.children = []
        self.real_file_path = ""

    def get_metadata_file(self):
        for file_name in self.file_paths:
            if file_name.endswith(".metadata"):
                with open(file_name, "r") as f:
                    json = load(f)
                    if json:
                        return json
                    else:
                        del self

    def get_content_file(self):
        for file_name in self.file_paths:
            if file_name.endswith(".content"):
                with open(file_name, "r") as f:
                    json = load(f)
                    if json:
                        return json
                    else:
                        del self

    def set_all_data(self):
        self.metadata = self.get_metadata_file()
        if self.metadata:
            self.rm_file_name = self.metadata["visibleName"]
            self.parent_id = self.metadata["parent"]
        self.content_data = self.get_content_file()
        self.file_type = self.determine_filetype()
        for path in self.file_paths:
            if self.file_type == "pdf" and  path.endswith("pdf"):
                self.real_file_path = path
            elif self.file_type == "epub" and  path.endswith(".epub"):
                self.real_file_path = path

    def determine_filetype(self):
        if self.file_extensions == {"content", "metadata"}:
            return "collection"
        if {"downloading"}.issubset(self.file_extensions):
            return "downloading"
        if self.content_data:
            return self.content_data["fileType"]
