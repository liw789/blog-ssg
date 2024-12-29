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
    return gen(theme, src, output_path)

def gen(theme:str, src:str, output_path:str) -> int:

    app_root = sys.path[0]
    try:
        #set and validate src paths
        config_file_path, theme_path, index_image_container_snippet_path, album_html_src_path, album_slide_snippet_path = set_and_validate_source_paths(src, theme, app_root)
        
        #read json config file
        with open(config_file_path, 'r') as file:
            data = file.read()
        
        parsed_data = json.loads(data)
        album_title = parsed_data["album-title"]
        photos_metadata = parsed_data["photos"]
        album_cover = parsed_data["album-cover"]
    
    except FileNotFoundError as e:
        print(str(e))
        return 1
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1
    
    #generate output paths
    index_html_file_output_path, album_output_path, album_output_relative_path, album_html_output_path = generate_output_paths(output_path, album_title)


    #setup the site for the album
    setup_site(theme_path, output_path, album_output_path, index_html_file_output_path, album_html_src_path)

    #update the index.html file
    with open(index_image_container_snippet_path, "r") as file:
        container_snippet = file.read()    

    with open(index_html_file_output_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    index = update_index_html_file(content, container_snippet, album_title, album_cover, album_output_relative_path)

    #write the updated index.html file
    with open(index_html_file_output_path, 'w', encoding='utf-8') as file:
        file.write(index)    
    
    #update the album.html file

    create_album(album_output_path, album_html_output_path, album_slide_snippet_path, album_title, src, photos_metadata)    

    return 0



def set_and_validate_source_paths(src:str, theme:str, app_root:str) -> tuple:
    

    #set & validate paths
    config_file_path = os.path.join(src, "config.json")
    if not os.path.exists(config_file_path):
        raise FileNotFoundError("config.json file not found in the source directory")   

    theme_path = os.path.join(app_root, "Theme", theme)
    if not os.path.exists(theme_path):
        raise FileNotFoundError("Theme not found")
    
    template_path = os.path.join(theme_path, "templates")

    index_image_container_snippet_path = os.path.join(template_path, "index-image-container.snippet")
    if not os.path.exists(index_image_container_snippet_path):      
        raise FileNotFoundError("index-image-container.snippet not found")

    album_html_src_path = os.path.join(theme_path, "album.html")
    if not os.path.exists(album_html_src_path):
        raise FileNotFoundError("album.html not found")

    album_slide_snippet_path = os.path.join(template_path, "album-slide.snippet")
    if not os.path.exists(album_slide_snippet_path):
        raise FileNotFoundError("album-slide.snippet not found")
    


    return config_file_path, theme_path, index_image_container_snippet_path, album_html_src_path, album_slide_snippet_path

def generate_output_paths(output_path:str, album_title:str)->tuple:
    
    #expected output paths are like the following:
    #output_path/index.html
    #output_path/photos/album_title/album.html

    index_html_file_output_path = os.path.join(output_path, "index.html")
    album_output_path = os.path.join(output_path, "photos", album_title)
    album_output_relative_path = os.path.join("photos", album_title)
    album_html_output_path = os.path.join(album_output_path, "album.html")

    return index_html_file_output_path, album_output_path, album_output_relative_path, album_html_output_path

#sets up the site by copying the theme files to the output path if they don't exist and creating the album directory
def setup_site(theme_path:str, output_path:str, album_output_path:str, index_html_file_output_path:str, album_html_file_path:str):
    
    #create the directory for the album
    os.makedirs(album_output_path, exist_ok=True)

    #at this point, we have the full path to the album directory, but the index.html file may be missing if this is the first time running the program
    #we need to verify and then copy everything over if it's missing    
    if not os.path.exists(index_html_file_output_path):
        #first time setting up the site
        def ignore_files(dir, files):
            return [f for f in files if f in ['album.html', 'templates']]
        
        #copy the theme files to the output path, except for album.html and templates directory
        copytree(theme_path, output_path, dirs_exist_ok=True, ignore=ignore_files)
    
    #copy the album.html from the theme to the album directory
    if os.path.exists(album_html_file_path):
        copy(album_html_file_path, album_output_path)

def update_index_html_file(content:str, container_snippet:str, album_title:str, album_cover:str, album_relative_path:str) -> str:

    #add the album cover to index.html
    container_snippet = container_snippet.replace("{{album-cover}}", os.path.join(album_relative_path, album_cover))
    container_snippet = container_snippet.replace("{{album-title}}", album_title)
    container_snippet = container_snippet.replace("{{album-url}}", os.path.join(album_relative_path, "album.html"))

    soup = BeautifulSoup(content, 'html.parser')

    #find the div with the class "album-container" and insert the snippet
    album_container = soup.find("div", id="albums")
    if album_container:
        album_container.insert(0, BeautifulSoup(container_snippet, 'html.parser'))

    return str(soup)

def create_album(album_output_path:str, album_html_output_path:str, album_slide_snippet_path:str,  album_title:str, src:str, photos_metadata:dict):
      
    with open(album_html_output_path, 'r', encoding='utf-8') as file2:
        content = file2.read()
    
    content = content.replace("{{album-title}}", album_title)
    soup = BeautifulSoup(content, 'html.parser')
    images_div = soup.find("div", id="images")

    with open(album_slide_snippet_path, 'r', encoding='utf-8') as slide_file:
        slide_snippet = slide_file.read()

        #for each jpg or webp file in the src directory, add a snippet to the album.html file and copy the picture to the same directory
    files = sorted(os.listdir(src))
    for f in files:
        if f.endswith(".jpg") or f.endswith(".webp"):
            #copy the file to the album directory
            copy(os.path.join(src, f), os.path.join(album_output_path, f))

            photo_metadata = find_photo_by_name(photos_metadata, f)
            
            description = ""
            position = ""

            if photo_metadata:
                description = photo_metadata["description"]
                position = photo_metadata["position"]

            #add a snippet to the album.html file
            slide_text = slide_snippet.replace("{{filename}}", f)
            slide_text = slide_text.replace("{{description}}", description)
            slide_text = slide_text.replace("{{position}}", position)

            images_div.append(BeautifulSoup(slide_text, 'html.parser'))

    with open(album_html_output_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))
    
#finds a photo by its filename
def find_photo_by_name(photos, file_name):
    for photo in photos:
        if photo["filename"] == file_name:
            return photo
    return None