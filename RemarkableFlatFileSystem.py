class RemarkableFlatFileSystem(set):
    def __contains__(self, key):
        if type(key) is str:
            return any(x for x in self if x.file_hash == key)
        else:
            return super().__contains__(key)

    def __getitem__(self, i):
        if type(i) is str:
            return list(x for x in self if x.file_hash == i)[0]
        elif type(i) is int:
            return super().__getitem__(i)

    def __setitem__(self, i, v):
        print(i, v)

    def get_children_for_parent_id(self, parent_id):
        for file in self:
            if file.parent_id == parent_id:
                yield file

    # def traverse_filesystem_recursively(self,parent_id):
    #     for x in self:
    #         if x.parent_id == parent_id:
    #             print(x.rm_file_name)
    #             self.traverse_filesystem_recursively(x.file_hash)
    #         else:
    #             continue

    def recursive_method(self, files, path=""):
        for file in files:
            this_folder_children = self.get_children_for_parent_id(file.file_hash)
            child_folders = []
            folder_path = ""

            # Loop through all the children of this folder
            for child_file in this_folder_children:
                child_file.parent_id = file.file_hash

                # If child is a folder or in root
                if child_file.file_type == "collection" or not file.parent_id:
                    child_folders.append(child_file)
                    if not file.parent_id:
                        folder_path = child_file.rm_file_name
                    else:
                        folder_path = f"{path}/{child_file.rm_file_name}"
                    self.recursive_method(child_folders, folder_path)

                # # Root
                # if not file.parent_id:
                #     folder_path = f"{child_file.rm_file_name}/"
                #     self.recursive_method(child_folders, path)
                else:
                    print(f"{path}/{child_file.rm_file_name}.{child_file.file_type}")



                    #print(child_file.rm_file_name)
               # print(f"{path}/{child_file.rm_file_name}.{child_file.file_type}")



            # newpath = ""
            # if file.file_type == "collection":
            #     child_folders = []
            #     for child in this_folder_children:
            #         child.parent_id = file.file_hash
            #         if child.file_type == "collection":
            #             child_folders.append(child)
            #             newpath = f"{path}/{child.rm_file_name}"
            #
            #     self.recursive_method(child_folders,newpath)
            # else:
            #     print(file.rm_file_name)

                    # self.recursive_method(this_folder_children)

    # def pair_children_with_parents(self):
    #     for file in self:
    #         if file.file_type == "collection":
    #             # Get the root folders
    #             if not file.parent_id:
    #                 # get children from root files and loop recursively from there on
    #                 for child in self.get_children_for_parent_id(file.file_hash):
    #                     child.parent_id = file.file_hash
    #                     print(child.rm_file_name)

    # print(x.rm_file_name)
    # self.get_children_for_parent_id(x.file_hash)))
    # for y in l2:
    #     print(y.rm_file_name)

#    def add(self, v):
#     if True:#v.metadata:  # and v.content_data:
#         return super().add(v)

# def append(self, v):
#     print(v.metadata)
#     if v not in list(self):
#         return super().append(v)
#     else:
#         return self.update(v)
#

#     def insert(self, i, v):pass
#     def __len__(self): return len(self.list)
#     def __getitem__(self, i): return self.list[i]
#     def __delitem__(self, i): del self.list[i]
#     def __setitem__(self, i, v): self.list[i] = v
#     def __str__(self): return str(self.list)
