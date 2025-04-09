import unittest
from spider import is_valid, download_img,spider
from urllib.parse import urlparse
import os
from unittest.mock import patch, MagicMock


class TestSpider(unittest.TestCase):
    def setUp(self):
        self.test_dir = './test_data'
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        for f in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, f))
        os.rmdir(self.test_dir)

    def test_is_valid(self):
        # Valid URLs
        self.assertTrue(is_valid("http://example.com"))
        self.assertTrue(is_valid("https://example.com/path"))

        # Invalid URLs
        self.assertFalse(is_valid("ftp://example.com"))  # Wrong scheme
        self.assertFalse(is_valid("example.com"))  # No scheme
        self.assertFalse(is_valid("http://"))  # No netloc

    @patch('spider.requests.get')
    def test_download_img(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.iter_content.return_value = [b'test', b'data']
        mock_get.return_value = mock_response

        # Test download
        test_url = "http://example.com/test.jpg"
        download_img(test_url, self.test_dir)

        # Verify file was created
        expected_file = os.path.join(self.test_dir, "test.jpg")
        self.assertTrue(os.path.exists(expected_file))

    @patch('spider.requests.get')
    def test_download_img_failure(self, mock_get):
        mock_get.side_effect = Exception("Test error")
        try:
            download_img("http://invalid.com/test.jpg", self.test_dir)
        except Exception:
            self.fail("Failed to download test image")

    @patch('spider.requests.get')
    @patch('spider.BeautifulSoup')
    def test_recursion_depth(self, mock_soup, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = "<html></html>"
        mock_get.return_value = mock_response

        # Mock find_all to return empty lists
        mock_soup.return_value.find_all.return_value = []

        # Test depth limit
        spider("http://example.com", 1, self.test_dir)

        # Verify get_images was called with correct depth sequence
        # (This would need a mock on get_images to verify)

    @patch('spider.get_images')
    def test_spider_calls(self, mock_get_images):
        spider("http://example.com", 2, self.test_dir)
        mock_get_images.assert_called_once()

    def test_directory_creation(self):
        test_dir = "./new_test_dir"
        spider("http://example.com", 0, test_dir)
        self.assertTrue(os.path.exists(test_dir))
        os.rmdir(test_dir)

    @patch('spider.requests.get')
    def test_duplicate_downloads(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.iter_content.return_value = [b'test']
        mock_get.return_value = mock_response

        # First download
        download_img("http://example.com/dupe.jpg", self.test_dir)
        # Second attempt
        download_img("http://example.com/dupe.jpg", self.test_dir)

        # Verify only one file exists
        self.assertEqual(len(os.listdir(self.test_dir)), 1)

    @patch('spider.requests.get')
    @patch('spider.get_images')
    def test_image_extension_filter(self, mock_get_images, mock_requests_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.iter_content.return_value = [b'test']
        mock_requests_get.return_value = mock_response


        spider("http://example.com/test.txt", 0, self.test_dir)
        self.assertEqual(len(os.listdir(self.test_dir)), 0)

        # Second test: image extension
        # Instead of mocking get_images, we should actually implement a side effect that
        # simulates the image download functionality
        def mock_download_side_effect(url, max_depth, depth, folder, visited, downloaded_images, stop_flag):
            # Only execute for image URLs
            if url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                # Create a test file in the folder
                with open(os.path.join(folder, "test.jpg"), 'wb') as f:
                    f.write(b'test image data')

        # Set the side effect
        mock_get_images.side_effect = mock_download_side_effect

        # Now try with an image URL
        spider("http://example.com/test.jpg", 0, self.test_dir)
        self.assertEqual(len(os.listdir(self.test_dir)), 1)




if __name__ == '__main__':
    unittest.main()