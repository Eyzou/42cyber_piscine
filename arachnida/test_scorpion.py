import unittest
from unittest.mock import patch, MagicMock
import os
from PIL import Image
import tempfile
import shutil
import scorpion  # Assuming your code is in scorpion.py
import piexif
import time
import pathlib


class TestScorpion(unittest.TestCase):
    def setUp(self):
        # Create a temporary test image with EXIF data
        self.test_dir = tempfile.mkdtemp()
        self.test_image_path = os.path.join(self.test_dir, "test.jpg")

        # Create a simple image
        img = Image.new('RGB', (100, 100), color='red')

        # Add EXIF data
        exif_dict = {
            "0th": {
                piexif.ImageIFD.Make: "Test Camera",
                piexif.ImageIFD.Model: "Test Model"
            }
        }
        exif_bytes = piexif.dump(exif_dict)
        img.save(self.test_image_path, exif=exif_bytes)

        # Create a bad image file
        self.bad_image_path = os.path.join(self.test_dir, "bad.txt")
        with open(self.bad_image_path, 'w') as f:
            f.write("Not an image")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_parse_args(self):
        test_args = ['scorpion.py','image1.jpg', 'image2.jpg']
        with patch('sys.argv', test_args):
            args = scorpion.parse_args()
            self.assertEqual(len(args.image), 2)
            self.assertEqual(str(args.image[0]), 'image1.jpg')

    def test_scorpion_with_valid_image(self):
        metadata = scorpion.scorpion(self.test_image_path)

        # Test basic metadata
        self.assertEqual(metadata['Filename'], self.test_image_path)
        self.assertEqual(metadata['Format'], 'JPEG')
        self.assertEqual(metadata['Image Width'], 100)
        self.assertEqual(metadata['Image Height'], 100)

        # Test EXIF data
        self.assertIn('Make', metadata)
        self.assertEqual(metadata['Make'], 'Test Camera')
        self.assertIn('Model', metadata)
        self.assertEqual(metadata['Model'], 'Test Model')

    @patch('builtins.print')
    def test_scorpion_with_bad_file(self,mock_print):
            metadata = scorpion.scorpion(self.bad_image_path)
            mock_print.assert_called_with("Bad file Format")
            self.assertEqual(metadata['Filename'], self.bad_image_path)
            self.assertNotIn('Format', metadata)

    @patch('scorpion.print_metadata')
    @patch('scorpion.parse_args')
    def test_main_with_valid_images(self, mock_parse_args, mock_print_meta):
        # Setup mock return value for parse_args
        mock_args = MagicMock()
        mock_args.image = [pathlib.Path(self.test_image_path)]  # Ensure it's a Path object
        mock_parse_args.return_value = mock_args

        scorpion.main()

        # Verify print_metadata was called
        mock_print_meta.assert_called_once()

        # Get the arguments passed to print_metadata
        args = mock_print_meta.call_args[0][0]

        # Verify the arguments
        self.assertEqual(len(args), 1)
        self.assertEqual(str(args[0]['Filename']), str(self.test_image_path))

    @patch('scorpion.print_metadata')
    def test_main_with_bad_images(self, mock_print_meta):
        with patch('sys.argv', ['scorpion.py', self.bad_image_path]), \
                patch('builtins.print') as mock_print:
            scorpion.main()
            mock_print_meta.assert_not_called()
            self.assertTrue(mock_print.called)

    @patch('scorpion.print_metadata')
    def test_main_with_no_images(self, mock_print_meta):
        with patch('sys.argv', ['scorpion.py']), \
                patch('builtins.print') as mock_print:
            scorpion.main()
            mock_print_meta.assert_not_called()
            mock_print.assert_called_with("Usage: ./FILE1 [FILE2 ...]")

    @patch('PIL.Image.open')
    @patch('os.path.getsize', return_value=1024)  # Mock filesize
    @patch('os.path.getmtime', return_value=1234567890)  # Mock modification time
    @patch('builtins.print')
    def test_scorpion_with_image_open_error(self, mock_print, mock_getmtime,
                                            mock_getsize, mock_open):
        # Setup the mock to raise IOError when opening image
        mock_open.side_effect = IOError("Test error")

        metadata = scorpion.scorpion("dummy.jpg")

        # Verify error message was printed
        mock_print.assert_called_with("Bad file Format")

        # Verify basic metadata was collected
        self.assertEqual(metadata['Filename'], "dummy.jpg")
        self.assertEqual(metadata['Creation Date'], time.ctime(1234567890))
        self.assertEqual(metadata['File size'], 1024)

        # Verify image-specific metadata wasn't collected
        self.assertNotIn('Format', metadata)
        self.assertNotIn('Mode', metadata)

    def test_file_size_and_date_metadata(self):
        metadata = scorpion.scorpion(self.test_image_path)
        self.assertIn('File size', metadata)
        self.assertGreater(int(metadata['File size']), 0)
        self.assertIn('Creation Date', metadata)

    @patch('tkinter.Tk')
    def test_print_metadata(self, mock_tk):
        test_metadata = [{
            'Filename': 'test.jpg',
            'Format': 'JPEG',
            'Make': 'Test Camera'
        }]

        scorpion.print_metadata(test_metadata)

        # Verify Tkinter was called to create UI
        mock_tk.assert_called_once()


if __name__ == '__main__':
    unittest.main()