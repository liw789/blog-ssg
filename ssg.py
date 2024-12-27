import sys
import os
import json
from shutil import copytree, copy
from bs4 import BeautifulSoup


def main(theme:str, src:str, output_path: str) -> int:
    if not theme or not theme.strip():
        theme = "Default"
    if not src or not src.strip():
        #default to current directory
        src = os.getcwd()
    gen(theme, src, output_path)
    return 0

def gen(theme:str, src:str, output_path:str):
    config_path = os.path.join(src, "config.json")

    #read json config file
    with open(config_path, 'r') as file:
        data = file.read()
    parsed_data = json.loads(data)
    
    app_path = sys.path[0]
    theme_path = os.path.join(app_path, "Theme", theme)

    #setup the site for the album
    album_name = parsed_data["album-name"]
    setup_site(theme_path, output_path, album_name)
    
    #update the index.html file
    snippet_path = os.path.join(theme_path, "templates", "index-image-container.snippet")
    container_snippet = open(snippet_path, "r").read()

    html_file_path = os.path.join(output_path, "index.html")

    index=''

    with open(html_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        index = update_index_file(content, container_snippet, album_name, parsed_data["album-cover"])

    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(index)

    #update the album.html file

    album_file_path = os.path.join(output_path, "photos", album_name, "album.html")


    return 0


def update_index_file(content:str, container_snippet:str, album_name:str, album_cover:str) -> str:
     #add the album cover to index.html
    container_snippet = container_snippet.replace("{{album-cover}}", album_cover)
    container_snippet = container_snippet.replace("{{album-name}}", album_name)

    soup = BeautifulSoup(content, 'html.parser')

    #find the div with the class "album-container" and insert the snippet
    album_container = soup.find("div", id="albums")
    if album_container:
        album_container.insert(0, BeautifulSoup(container_snippet, 'html.parser'))

    return str(soup)
    

#creates the output directory for the album if it doesn't exist
def create_output_dir(output_path:str, album_name:str) -> str:   
    album_path = os.path.join(output_path, "photos", album_name)
    os.makedirs(album_path, exist_ok=True)

    return album_path

#sets up the site by copying the theme files to the output path if they don't exist and creating the album directory
def setup_site(theme_path:str, output_path:str, album_name:str):
    
    #create the directory for the album
    album_path = create_output_dir(output_path, album_name)

    #at this point, we have the full path to the album directory, but the index.html file may be missing if this is the first time running the program
    #we need to verify and then copy everything over if it's missing    
    
    if not verify_index_file_exists(output_path):
        #first time setting up the site
        def ignore_files(dir, files):
            return [f for f in files if f in ['album.html', 'templates']]
        
        #copy the theme files to the output path, except for album.html and templates directory
        copytree(theme_path, output_path, dirs_exist_ok=True, ignore=ignore_files)
    
    # Example of copying a specific file to the output_path
    album_file = os.path.join(theme_path, "album.html")
    if os.path.exists(album_file):
        copy(album_file, album_path)



#checks the path for an index.html file. Returns true if it exists, false otherwise
def verify_index_file_exists(path:str) -> bool:
    index_file_path = os.path.join(path, "index.html")
    return os.path.exists(index_file_path)