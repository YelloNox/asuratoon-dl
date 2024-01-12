import requests
import os
import urllib
import re
import zipfile
import shutil
import sys
from bs4 import BeautifulSoup

dl_log = "download_log.txt"
tmp_dl_log = ""
distro_nav = "\\"
dl_path = ""
book_title = ""
book_titles = []
url = ""
is_cbz = False
create_link = False

# HTML content location

title_html = ('h1', {'class': 'entry-title'})
chapter_html = ('div', {'id': 'chapterlist'})
image_html = ('div', {'class': 'entry-content'})
top_link_html = ('div', {'class': 'allc'})


# Options {START}


def checkOptions():
    userInput = sys.argv
    is_updating = False
    print("")

    i = 0
    while i < len(userInput):
        item = userInput[i]

        if item == "--help" or item == "-h":
            print(f"Printing options...")
            printOptions()
            exit()
        elif item == "--cbz":
            global is_cbz
            is_cbz = True
            print(f"\t{item} Enabled (Converting folders to CBZ)\n")
        elif item == "--path" or item == "-p":
            global dl_path
            dl_path = userInput[i+1] + distro_nav
            print(f"\tPath set to: {userInput[i+1]}\n")
        elif item == "--link" or item == "-l":
            global create_link
            create_link = True
            print(f"\t{item} Enabled (Will create shortcut to URL)\n")
        elif item == "--update":
            print(f"\t{item} Enabled: Updating...\n")
            is_updating = True
        elif item == "--update-help":
            printUpdateHelp()
            exit()
        i += 1

    if 'http' in userInput[-1]:
        global url
        url = userInput[-1]
    elif is_updating:
        updateSource()
        exit()
    else:
        print("Missing URL (Example: *_dl.py --path /path/to/dir https://example.com)")
        exit()


def printOptions():
    print(f"")
    print(f"Usage: *_dl.py --path /path/to/dir https://example.com")
    print(f"")
    print(f"Options:")
    print(f"\t--help | -h: Displays this message\n")
    print(f"\t--path | -p: Path to download to (--path <DIR>)\n")
    print(f"\t--cbz: Download as a CBZ\n")
    print(f"\t--link: Create a shortcut file\n")
    print(f"\t--update: Updates all downloads to latest chapter")
    print(f"\t\t--update-help for more information\n")
    print(f"")


def printUpdateHelp():
    print(f"")
    print(f"Usage: *_dl.py --update")
    print(f"")
    print(f"Options:")
    print(f"\t--update: Updates all downloads to latest chapter")
    print(f"\t\t--update-help for more information\n")
    print(f"")

# Options {END}

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

# Create the path and set dl_log locaiton


def createDir():
    getTitle()
    global tmp_dl_log
    log_path = dl_path + book_title + distro_nav
    tmp_dl_log = log_path + dl_log
    print(f"Creating Path: {log_path}")
    os.makedirs(log_path, exist_ok=True)
    print(f"Creating log file: {tmp_dl_log}")
    try:
        with open(tmp_dl_log, 'x'):
            pass
    except FileExistsError:
        print(f"Log file already exists: Skipping...")
    except Exception as e:
        print(f"Error: {e}")
    if create_link:
        createShortcut(log_path)


def scanPage(curUrl):
    print(f"Scanning page {curUrl}")


# Gets the book title from the webpage
def getTitle():
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find(title_html[0], title_html[1])
        global book_title
        book_title = div.text
        book_title = book_title.replace(" ", "-")
    else:
        print("Missing Title")

# Finds the link to the first chapter by navigating the title page


def chapList():
    print(f"Finding chapters: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find(chapter_html[0], chapter_html[1])
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
        return
    for link in links[curChap:]:
        response = requests.get(link)
        if response.status_code == 200:
            downloadImages(link)

# For testing (no download)


def fakeDownloadImages(page):
    print(f"/nDownloading: {page}")
    logCompleted(page)

# Download all images in a page under a div


def downloadImages(page):
    print(f"Downloading: {page}")
    response = requests.get(page)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        div = soup.find(image_html[0], image_html[1])

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
    with open(tmp_dl_log, "a") as f:
        f.write(f"{page}\n")

# Finds the latest chapter


def lastDownload():
    try:
        with open(tmp_dl_log, "r") as f:
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


def listDir():
    global book_titles
    global dl_path
    print(f"Items:")

    if dl_path == "":
        dl_path = os.getcwd() + distro_nav

    print(f"Current Path {dl_path}")

    i = 0
    if os.path.exists(dl_path):
        file_list = os.listdir(dl_path)
        file_list = [item for item in file_list if not (
            item.startswith('.') or item.endswith('.bat'))]
        for file_name in file_list:
            book_titles.append(file_name)
            print(f"\t{i+1}: {file_name}")
            i += 1
    else:
        print(f"{dl_path} does not exist")
    print("")


def getLinkFromLog(book_dir):
    cur_book_dir = dl_path + book_dir + distro_nav + dl_log
    print("Checking: " + cur_book_dir)
    print(f"dl_log: {dl_log}")
    with open(cur_book_dir, 'r') as f:
        links = f.readlines()
    print("")
    return links[0]


def getTopLink():
    print(f"Finding head source of: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find(top_link_html[0], top_link_html[1])
        if div:
            links = div.find_all('a', href=True)
            links.reverse()
            linkList = []
            for link in links:
                href = link.get('href')
                linkList.append(href)
            print(f"Found: {linkList[0]}")
            return linkList[0]
        else:
            print("firstChap: Missing div")
    else:
        print("firstChap: Missing Button")


def downloadSource():
    createDir()
    links = chapList()
    last_downlaod = lastDownload()
    downloadUnique(last_downlaod, links)
    print("---------------- No more chapters ----------------\n")


def updateSource():
    global url
    listDir()
    for i in range(len(book_titles)):
        url = getLinkFromLog(book_titles[i])
        url = getTopLink()
        downloadSource()


# Execution
checkOptions()
downloadSource()
