import argparse
import os
import pathlib
import time
from PIL import Image
from PIL.ExifTags import TAGS
import re
import tkinter as tk

def parse_args():
    parser = argparse.ArgumentParser(prog="Scorpion",
                                     description="Program that display EXIF and metadata of an image")
    parser.add_argument("image", type = pathlib.Path, nargs="+",help= "Image URL to be parsed for EXIF and other metadata")
    args = parser.parse_args()
    return args

def print_metadata(all_metadata : list[dict]):
    root = tk.Tk()
    root.title("Image Metadata Viewer")

    canvas = tk.Canvas(root)
    frame = tk.Frame(canvas)
    vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    vsb2 = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
    canvas.configure(yscrollcommand=vsb.set)
    canvas.configure(xscrollcommand=vsb2.set)

    vsb.pack(side="right", fill="y")
    vsb2.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((4,4), window=frame, anchor="nw")

    def onFrameConfigure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", onFrameConfigure)

    for idx,metadata in enumerate(all_metadata):
        img_frame = tk.LabelFrame(frame, text="Image {}".format(idx))
        img_frame.pack(side="left", fill="both", expand=True)

        for key,value in metadata.items():
            row_frame = tk.Frame(img_frame)
            row_frame.pack(side="top", fill="x", anchor="w", padx=5, pady=2)

            tk.Label(row_frame, text=key, width=20, anchor="w").pack(side="left")
            tk.Label(row_frame, text=value, anchor="w").pack(side="left")

    exit_button = tk.Button(root, text="Exit", command=root.destroy)
    exit_button.pack(side="bottom", pady=10)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nGUI closed by user (Ctrl+C).")
        root.destroy()


def scorpion(img_path):
    metadata = {}
    metadata['Filename'] = img_path

    try:
        try:
            metadata['Creation Date'] = time.ctime(os.path.getmtime(img_path))
            metadata['File size'] = os.path.getsize(img_path)
        except OSError as e:
            print(f"Error getting file info: {e}")
            return metadata
        try:
            image = Image.open(img_path)
            metadata['Format'] = image.format
            metadata['Mode'] = image.mode
            metadata['Image Width'] = image.width
            metadata['Image Height'] = image.height
            exifdata = image._getexif()
            if exifdata:
                for k,v in exifdata.items():
                    tag = TAGS.get(k)
                    metadata[tag] = str(v)
        except IOError:
            print("Bad file Format")
    except Exception as e:
        print(f"Error processing image: {e}")
    return metadata

def main():
    print("WELCOME TO SCORPION")
    try:
        args = parse_args()
        all_metadata = []

        if not args.image:
            print("Usage: ./FILE1 [FILE2 ...]")
            return

        for img_path in args.image:
            if re.search(r'\.jpg$|\.jpeg$|\.png|\.gif|\.bmp$', str(img_path), re.IGNORECASE):
                try:
                    meta = scorpion(img_path)
                    all_metadata.append(meta)
                except Exception as e:
                    print(f"Skipping {e}")

        if all_metadata:
            print_metadata(all_metadata)
    except SystemExit:
        print("Usage: ./FILE1 [FILE2 ...]")

if __name__ == '__main__':
   main()