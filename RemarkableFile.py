from json import load


class RemarkableFile:

    def __init__(self, file_hash, root="/"):
        self.file_hash = file_hash

        # Parent data
        self.parent_file_hash = ""
        self.parent_rm_file = None

        # Real file data
        self.real_file_extensions = set()
        self.real_file_paths = set()
        self.real_file_path = ""

        # Remarkable file attributes
        self.rm_parent_path = ""
        self.rm_file_name = ""
        self.rm_file_type = ""


        # Remarkable filepath parts
        self.rm_filepath_parts = []
        self.rm_filepath_parent_files = []


        # Use getters and setters for  to set filepath as to 
        #  set filepath parrents simultaniously
        @rm_file_path.setter
        def rm_file_path(self, val):
            if val: 
                self._rm_file_path = val
                self.rm_filepath_parts = self._rm_file_path.split("/")
                self.rm_filepath_parent_files = self.rm_filepath_parts[:-1]

        @property
        def rm_file_path(self): 
            return self._rm_file_path

        



        # self.rm_file_path = ""

        # Metadata about rm file
        self.rm_file_metadata = None
        self.rm_file_content_data = None

        self.root = root

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

    def recursively_get_parents(self):
        if self.parent_rm_file:
            return self.parent_rm_file.recursively_get_parents() + self.parent_rm_file.rm_file_name + "/"
        return self.root

    def get_metadata_file(self):
        for file_name in self.real_file_paths:
            if file_name.endswith(".metadata"):
                with open(file_name, "r") as f:
                    return load(f)

    def get_content_file(self):
        for file_name in self.real_file_paths:
            if file_name.endswith(".content"):
                with open(file_name, "r") as f:
                    return load(f)

    def set_all_data(self):
        self.rm_file_metadata = self.get_metadata_file()
        if self.rm_file_metadata:
            self.rm_file_name = self.rm_file_metadata["visibleName"]
            self.parent_file_hash = self.rm_file_metadata["parent"]
        self.rm_file_content_data = self.get_content_file()
        self.rm_file_type = self.determine_filetype()
        for path in self.real_file_paths:
            if self.rm_file_type == "pdf" and path.endswith("pdf") \
                    or self.rm_file_type == "epub" and path.endswith(".epub"):
                self.real_file_path = path

    def determine_filetype(self):
        if self.real_file_extensions == {"content", "metadata"}:
            return "Collection"
        if {"downloading"}.issubset(self.real_file_extensions):
            return "Downloading"
        if self.rm_file_content_data:
            return self.rm_file_content_data["fileType"]
        if "epub" in self.real_file_extensions:
            return "epub"
        if "pdf" in self.real_file_extensions:
            return "pdf"
        if self.rm_file_metadata:
            return self.rm_file_metadata["type"]