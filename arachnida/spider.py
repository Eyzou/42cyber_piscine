import argparse
import os
import pathlib

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

VALID_EXTENSIONS =('.jpg', '.jpeg', '.png','.gif', '.bmp')

def parse_args():
    parser = argparse.ArgumentParser(prog="Spider",
                                     description="Program that scrap images from web")
    parser.add_argument("-r","--recursive",action="store_true", help="recursively download the images in a URL received as parameter, default depth is 5")
    parser.add_argument("-l","--level", nargs="?", default = 5, help="indicate the maximum depth of the recursive download", type=int)
    parser.add_argument("-p","--path",default ='./data', type=pathlib.Path, help="indicate the path where the downloaded files will be saved, default is ./data/")
    parser.add_argument("URL",help="URL to download the images from")
    args = parser.parse_args()
    return args

def is_valid(url,base_domain):
    parsed = urlparse(url)
    if not parsed.netloc:
        print("URL has no netloc")
        return False
    if not parsed.scheme:
        print("URL has no scheme")
        return False
    if (parsed.scheme != "https" and parsed.scheme != "http"):
        print("URL should be https or http")
        return False
    if parsed.netloc != base_domain:
        print(f"URL {url} is not the same domain as {base_domain}")
        return False
    return True

def download_img(url,folder):
    try:
        response = requests.get(url,stream=True)
        response.raise_for_status()
        img_name = os.path.join(folder,os.path.basename(urlparse(url).path))
        with open(img_name, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def get_images(url, max_depth,depth, folder,visited,downloaded_images, stop_flag,base_domain):
    print(f"Entering get images with Depth: {depth}, URL {url}")
    global count
    if stop_flag[0]:
        return
    if depth >= max_depth:
        print(f"Max Depth: {max_depth} reach at {url}")
        stop_flag[0] = True
        return

    try:
        visited.add(url)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        img_tags = soup.find_all('img')
        for img_tag in img_tags:
            img_url = img_tag.get('src')
            if img_url and img_url.lower().endswith(VALID_EXTENSIONS):
                img_url = urljoin(url,img_url)
                if img_url not in downloaded_images:
                    download_img(img_url,folder)
                    downloaded_images.add(img_url)
                    count += 1
                    print(f"Downloaded {img_url}, count {count}")

        link_tags = soup.find_all('a',href=True)
        for link_tag in link_tags:
            if stop_flag[0]:
                break
            link_url = link_tag['href']
            absolute_url = urljoin(url,link_url)
            if absolute_url not in visited and is_valid(absolute_url,base_domain):
                get_images(absolute_url,max_depth,depth + 1,folder, visited,downloaded_images,stop_flag,base_domain)
    except Exception as e:
        print(f"Error getting images from {url}: {e}")

def spider(url, max_depth, path):
    global count
    count = 0
    base_domain = urlparse(url).netloc
    if not is_valid(url,base_domain):
        print(f"Invalid URL {url}")
        return
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.isdir(path) or not os.access(path, os.W_OK) or not os.access(path, os.X_OK):
        return
    visited = set()
    downloaded_images = set()
    stop_flag = [False]
    get_images(url, max_depth,0, path,visited,downloaded_images,stop_flag,base_domain)
    print(f"downloaded images {count}")

def main():
    print("WELCOME TO SPIDER")
    args = parse_args()
    spider(args.URL, args.level, args.path)

if __name__ == '__main__':
   main()