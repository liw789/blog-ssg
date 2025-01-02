import unittest
import os
import sys
from ssg import set_and_validate_source_paths, generate_output_paths, update_index_html_file

class TestSSG(unittest.TestCase):

    def test_set_and_validate_source_paths(self):
        src = "test_src"
        theme = "test_theme"

        app_root = src

        os.makedirs(os.path.join(src, "Theme", theme, "templates"), exist_ok=True)
        with open(os.path.join(src, "config.json"), 'w') as f:
            f.write('{}')
        with open(os.path.join(src, "Theme", theme, "templates", "index-image-container.snippet"), 'w') as f:
            f.write('')
        with open(os.path.join(src, "Theme", theme, "album.html"), 'w') as f:
            f.write('')
        with open(os.path.join(src, "Theme", theme, "templates", "album-slide.snippet"), 'w') as f:
            f.write('')

        config_file_path, theme_path, index_image_container_snippet_path, album_html_src_path, album_slide_snippet_path = set_and_validate_source_paths(src, theme, app_root)

        self.assertTrue(os.path.exists(config_file_path))
        self.assertTrue(os.path.exists(theme_path))
        self.assertTrue(os.path.exists(index_image_container_snippet_path))
        self.assertTrue(os.path.exists(album_html_src_path))
        self.assertTrue(os.path.exists(album_slide_snippet_path))

    def test_generate_output_paths(self):
        output_path = "test_output"
        album_title = "test_album"
        index_html_file_output_path, album_output_path, album_output_relative_path, album_html_output_path = generate_output_paths(output_path, album_title)

        self.assertEqual(index_html_file_output_path, os.path.join(output_path, "index.html"))
        self.assertEqual(album_output_path, os.path.join(output_path, "photos", album_title))
        self.assertEqual(album_output_relative_path, os.path.join("photos", album_title))
        self.assertEqual(album_html_output_path, os.path.join(album_output_path, "album.html"))

    def test_update_index_html_file(self):
        content = '<div id="albums"></div>'
        container_snippet = '<div class="album-container">{{album-cover}} {{album-title}} {{album-url}}</div>'
        album_title = "test_album"
        album_cover = "cover.jpg"
        album_relative_path = "photos/test_album"

        expected = f'<div id="albums"><div class="album-container">{album_relative_path}/{album_cover} {album_title} {album_relative_path}/album.html</div></div>'

        updated_content = update_index_html_file(content, container_snippet, album_title, album_cover, album_relative_path)
        self.assertIn(album_title, updated_content)
        self.assertIn(album_cover, updated_content)
        self.assertIn(album_relative_path, updated_content)
        self.assertEqual(updated_content, expected)

if __name__ == '__main__':
    unittest.main()