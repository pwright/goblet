import os

def find_picasa_files(path):
    picasa_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.lower() == ".picasa.ini":
                picasa_files.append(os.path.join(root, file))
    return picasa_files

def parse_picasa_file(filepath):
    albums = {}
    with open(filepath, "r") as file:
        lines = file.readlines()
        current_img = ""
        for line in lines:
            line = line.strip()
            if line.startswith("["):
                current_img = line
            elif "albums=" in line:
                album_ids = line.split("=")[-1].split(",")
                for album_id in album_ids:
                    if album_id not in albums:
                        albums[album_id] = []
                    albums[album_id].append(current_img)        
    return albums

def write_markdown_files(albums, output_path):
    for album_id, images in albums.items():
        md_filename = f"{output_path}/{album_id}.md"
        if os.path.exists(md_filename):
            mode = "a"
        else:
            mode = "w"
        with open(md_filename, mode) as md_file:
            for image in images:
                md_file.write(f"![{image}]({image})\n")

def main():
    search_path = "./"
    output_path = "./"

    picasa_files = find_picasa_files(search_path)
    all_albums = {}
    for filepath in picasa_files:
        albums = parse_picasa_file(filepath)
        for album_id, images in albums.items():
            if album_id not in all_albums:
                all_albums[album_id] = []
            all_albums[album_id].extend(images)
    write_markdown_files(all_albums, output_path)
  
if __name__ == "__main__":
    main()
