from RemarkableFlatFileSystem import RemarkableFlatFileSystem


PATH = "./data/remarkable/xochitl/"

if __name__ == "__main__":
    rm_files = RemarkableFlatFileSystem(PATH)
    for file in rm_files:
        if file.final_file_path:
            pass
            print(file.final_file_path)


