import requests
import os
import urllib
import re
import zipfile
import shutil
import sys
from bs4 import BeautifulSoup

dl_log = "download_log.txt"
dl_path = ""
book_title = ""
url = ""
is_cbz = False
create_link = False

# Options {START}


def checkOptions():
    userInput = sys.argv
    print("")

    if 'http' in userInput[-1]:
        global url
        url = userInput[-1]
    else:
        print("Missing URL (Example: *_dl.py --path /path/to/dir https://example.com)")
        exit()
    
    
    i = 0
    while i < len(userInput):
        item = userInput[i]
        if item == "--help" or item == "-h":
            printOptions()
            exit()
        elif item == "--cbz":
            global is_cbz
            is_cbz = True
            print(f"    {item} Enabled (Converting folders to CBZ)")
        elif item == "--path" or item == "-p":
            global dl_path
            dl_path = userInput[i+1] + "\\"
            print(f"    Path set to {dl_path}")
        elif item == "--link" or item == "-l":
            global create_link
            create_link = True
            print(f"    {item} Enabled (Will create shortcut to URL)")
        i += 1
        
    print("")


def printOptions():
    print("")
    print("Usage: *_dl.py --path /path/to/dir https://example.com")
    print("")
    print("Options:")
    print("--help | -h: Displays this message")
    print("--path | -p: Path to download to (--path <DIR>)")
    print("--cbz: Download as a CBZ")
    print("--link: Create a shortcut file")
    print("")


# Options {END}
checkOptions()

# Creates working directory and log file

def createShortcut(path):
    shortcut_name = f"URL - {book_title}.url"
    shortcut_content = f"[InternetShortcut]\nURL={url}"

    shortcut_path = os.path.join(path, shortcut_name)
    try:
        with open(shortcut_path, "x") as url_shortcut:
            url_shortcut.write(shortcut_content)
    except FileExistsError:
        print(f"URL shortcut already exists: Skipping...")
    except Exception as e:
        print(f"Error: {e}")

    print(f"Shortcut Created: {shortcut_path}")

def createDir():
    getTitle()
    global dl_log
    log_path = dl_path + book_title + "\\"
    dl_log = log_path + dl_log
    print(f"Creating Path: {log_path}")
    os.makedirs(log_path, exist_ok=True)
    print(f"Creating log file: {dl_log}")
    try:
        with open(dl_log, 'x'):
            pass
    except FileExistsError:
        print(f"Log file already exists: Skipping...")
    except Exception as e:
        print(f"Error: {e}")
    if create_link:
        createShortcut(log_path)


def scanPage(curUrl):
    print(f"Scanning page {curUrl}")


def getTitle():
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find('h1', {'class': 'entry-title'})
        global book_title
        book_title = div.text
        book_title = book_title.replace(" ", "-")
    else:
        print("Missing Title")

# Finds the link to the first chapter by navigating the title page


def chapList():
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find('div', {'id': 'chapterlist'})
        if div:
            links = div.find_all('a', href=True)
            links.reverse()
            linkList = []
            for link in links:
                href = link.get('href')
                linkList.append(href)
            return linkList
        else:
            print("firstChap: Missing div")
    else:
        print("firstChap: Missing Button")

# Gets the last chapter in the list


def lastChap(links):
    last_line = links[-1]
    pattern = r'chapter-\d+'
    for i in range(2):
        curChap = re.findall(pattern, last_line)
        pattern = r'\d+'
    return int(curChap[1])

# Checks if last chapter was allready downloaded, if not, checks link, then requests download


def downloadUnique(curChap, links):
    if lastChap(links) == curChap:
        print("---------------- No more chapters ----------------\n")
        exit()
    for link in links[curChap:]:
        response = requests.get(link)
        if response.status_code == 200:
            downloadImages(link)

# For testing (no download)


def fakeDownloadImages(page):
    print(f"Downloading: {page}")
    logCompleted(page)

# Download all images in a page under a div


def downloadImages(page):
    print(f"Downloading: {page}")
    response = requests.get(page)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        div = soup.find('div', class_='entry-content')

        if div:

            for img in div.find_all('img'):
                img_url = img.get('src')

                if not img_url.startswith('http'):
                    img_url = urllib.parse.urljoin(url, img_url)
                img_data = requests.get(img_url).content
                img_filename = os.path.basename(
                    urllib.parse.urlparse(img_url).path)

                dl_folder = dl_path + book_title + \
                    '\chapter-' + str(lastDownload() + 1)
                os.makedirs(dl_folder, exist_ok=True)

                with open(os.path.join(dl_folder, img_filename), 'wb') as img_file:
                    img_file.write(img_data)

            print(f"Downloaded {len(div.find_all('img'))} images.")
            if is_cbz:
                convertToCBZ(dl_folder)
            logCompleted(page)
        else:
            print("Div not found on the page.")
    else:
        print(
            f"Failed to retrieve the webpage (HTTP Status Code: {response.status_code}).")

# Convert the download folder into a cbz


def convertToCBZ(path):
    print(f"Converting {path} to CBZ")
    zip_path = path + '.cbz'
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        for root, dirs, files in os.walk(path):
            for file in files:
                zip_file.write(os.path.join(root, file))
    # Remove old (uncompressed) photo folder
    try:
        shutil.rmtree(path)
    except OSError as e:
        print(f"Error: {e}")

# Log downloaded chapters to folder


def logCompleted(page):
    with open(dl_log, "a") as f:
        f.write(f"{page}\n")

# Finds the latest chapter


def lastDownload():
    try:
        with open(dl_log, "r") as f:
            lines = f.readlines()

        if lines != []:
            last_line = lines[-1]
            pattern = r'chapter-\d+'
            for i in range(2):
                curChap = re.findall(pattern, last_line)
                pattern = r'\d+'
            return int(curChap[1])
        else:
            return 0
    except Exception as e:
        print(e)


def main():
    createDir()
    links = chapList()
    last_downlaod = lastDownload()
    downloadUnique(last_downlaod, links)


main()
