import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
from ssg import update_index_file
from bs4 import BeautifulSoup
from ssg import update_index_file




class TestUpdateIndexFile(unittest.TestCase):

    def test_update_index_file(self):
        content = '<div id="albums"></div>'
        container_snippet = '<div>{{album-cover}}</div><div>{{album-name}}</div>'
        album_name = "Test Album"
        album_cover = "cover.jpg"

        expected_snippet = '<div>cover.jpg</div><div>Test Album</div>'
        expected_content = f'<div id="albums">{expected_snippet}</div>'

        result = update_index_file(content, container_snippet, album_name, album_cover)
        self.assertEqual(result, expected_content)

    def test_update_index_file_no_album_container(self):
        content = '<div id="no-albums"></div>'
        container_snippet = '<div>{{album-cover}}</div><div>{{album-name}}</div>'
        album_name = "Test Album"
        album_cover = "cover.jpg"

        result = update_index_file(content, container_snippet, album_name, album_cover)
        self.assertIn('<div id="no-albums"></div>', result)
        self.assertNotIn('cover.jpg', result)
        self.assertNotIn('Test Album', result)


if __name__ == '__main__':
    unittest.main()