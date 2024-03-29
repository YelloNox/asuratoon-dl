import requests
import os
import urllib
import re
import zipfile
import shutil
import sys
from bs4 import BeautifulSoup

dl_log = "download_log.txt"
active_site = "asuratoon"
tmp_dl_log = ""
distro_nav = "\\"
dl_path = ""
book_title = ""
book_titles = []
url = ""
is_cbz = False
create_link = True  # Required to update books

# Options {START}


def checkOptions():
    userInput = sys.argv
    is_updating = False
    print("")

    i = 0
    while i < len(userInput):
        global is_cbz, dl_path, create_link, active_site
        item = userInput[i]

        if item == "--help" or item == "-h":
            print(f"Printing options...")
            printOptions()
            exit()
        elif item == "--site" or item == "--source" or item == "-s":
            # Not fully implemented
            active_site = userInput[i+1].lower()
            print(f"\t{item} Enabled (Active site set to: {active_site})\n")
        elif item == "--cbz":
            is_cbz = True
            print(f"\t{item} Enabled (Converting folders to CBZ)\n")
        elif item == "--path" or item == "-p":
            dl_path = userInput[i+1] + distro_nav
            print(f"\tPath set to: {userInput[i+1]}\n")
        elif item == "--update":
            print(f"\t{item} Enabled: Updating...\n")
            is_updating = True
        elif item == "--update-help":
            printUpdateHelp()
            exit()
        i += 1

        """elif item == "--link" or item == "-l":
            create_link = True
            print(f"\t{item} Enabled (Will create shortcut to URL)\n")"""  # Will allways be true

    if 'http' in userInput[-1]:
        global url
        url = userInput[-1]
    elif is_updating:
        updateSource()
        exit()
    else:
        print("Missing URL (Example: *_dl.py --path /path/to/dir https://example.com)")
        exit()

# I would make a txt document for this, but I don't know if someone wants the script without the luggage.


def printOptions():
    print(f"")
    print(f"Usage: *_dl.py --path /path/to/dir https://example.com")
    print(f"")
    print(f"Options:")
    print(f"\t--help | -h: Displays this message\n")
    print(f"\t--site | -s: Specify what site to download from (learn more in info.md)\n")
    print(f"\t--path | -p: Path to download to (--path <DIR>)\n")
    print(f"\t--cbz: Download as a CBZ\n")
    # print(f"\t--link | -l: Create a shortcut file\n")
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

# Checks the current OS to set mapping to


def checkDistro():
    global distro_nav
    if os.name == 'nt':
        distro_nav == "\\"
    else:
        distro_nav = "/"

# Sets the html info to match the site (for future implementaiton of other sites)
# More informaiton in info.md: HTML Content Location


def setSite():
    global title_html, chapter_list_html, image_html, top_link_html, global_pattern
    if active_site == "":
        print(
            "Error [setSite]: No site selected! Use --site <site-name> or --help for more info.")
        exit()

    if active_site == "asuratoon":
        title_html = ('h1', {'class': 'entry-title'})
        chapter_list_html = ('ul', {'class': 'clstyle'})
        top_link_html = ('div', {'class': 'allc'})
        image_html = ('div', {'class': 'entry-content'})
        global_pattern = r'chapter-\d+'
        return
    elif active_site == "mamayuyu":
        title_html = ('h1', {'class': 'entry-title'})
        chapter_list_html = ('li', {'id': 'ceo_latest_comics_widget-3'})
        top_link_html = ('p', {'id': 'breadcrumbs'})
        image_html = ('div', {'class': 'entry-content'})
        global_pattern = r'chapter-\d+'
        return
    elif active_site == "sssclasshunter" or active_site == "yourtalentismine":
        title_html = ('h1', {'class': 'entry-title'})
        chapter_list_html = ('ul', {'class': 'su-posts-list-loop'})
        top_link_html = ('a', {'class': 'home-link'})
        image_html = ('div', {'class': 'entry-content'})
        global_pattern = r'chapter-\d+'
        return
    elif active_site == "mangaread":
        title_html = ('div', {'class': 'post-title'}, 1)
        chapter_list_html = ('ul', {'class': 'main'})
        top_link_html = ('ol', {'class': 'breadcrumb'}, 2)
        image_html = ('div', {'class': 'reading-content'})
        global_pattern = r'chapter-\d+'
        return
    # elif active_site == "manganato": - Tried, but site has SQL protection. Maybe another time.

    print(f"Error [setSite] `{active_site}`: Invalid site selection!")
    exit()


# Creates working directory and log file


def createShortcut(path, forceRecreate=False):
    shortcut_name = f"URL - {book_title}.url"
    shortcut_content = f"[InternetShortcut]\nURL={url}"

    shortcut_path = os.path.join(path, shortcut_name)
    if forceRecreate:
        if os.path.exists(shortcut_path):
            print(f"Removing shortcut: {shortcut_path}")
            os.remove(shortcut_path)
    try:
        with open(shortcut_path, "x") as url_shortcut:
            url_shortcut.write(shortcut_content)
    except FileExistsError:
        print(f"URL shortcut already exists: Skipping...")
    except Exception as e:
        print(f"Error: {e}")

    print(f"Shortcut [createShortcut]: {shortcut_path}")


# Create the path and set dl_log locaiton


def createDir(forceRecreateShortcut=False):
    getTitle()
    global tmp_dl_log
    if book_title == "":
        print("Error, book_title missing!")
        exit()
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
        exit()
    if forceRecreateShortcut:
        createShortcut(log_path, True)
    if create_link:
        createShortcut(log_path)


# Gets the book title from the webpage


def getTitle(tmp_url=""):
    global book_title, url
    if tmp_url != "":
        print(f"Using tmp_url [getTitle]: {tmp_url}")
        url = tmp_url
    response = requests.get(url)

    hasParent = False
    if len(title_html) >= 3:
        hasParent = True
    hasAltChild = False
    if len(title_html) >= 4:
        hasAltChild = True

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find(title_html[0], title_html[1])

        if hasParent:
            children = div.find_all(recursive=False)
            print(f"children [getTitle:title_html]: {children}")
            try:
                div = children[title_html[2]]
            except:
                print(
                    f"Failed to get title [getTitle:hasParent]: {title_html[2]}")
        if hasParent & hasAltChild:
            print(f"children [getTitle:hasAltChild]: {children}")
            try:
                div = children[title_html[3]]
            except:
                print(
                    f"Failed to get title [getTitle:hasAltChild]: {title_html[3]}")

        book_title = div.text
        book_title = book_title.replace(" ", "-")
        book_title = book_title.replace("\n", "")
        if book_title.endswith("-"):
            book_title_list = list(book_title)
            book_title_list[-1] = ""
            book_title = ''.join(book_title_list)
        print(f"Obtained book title: {book_title}")
    else:
        print(f"Page Error [getTitle]: {book_title}")


# Finds the link to the first chapter by navigating the title page


def getChapList(tmp_url=""):
    if tmp_url != "":
        print(f"Chap list tmp_url: {tmp_url}")
        print(f"Finding chapters: {tmp_url}")
        response = requests.get(tmp_url)
    else:
        print(f"Chap list URL: {url}")
        print(f"Finding chapters: {url}")
        response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find(chapter_list_html[0], chapter_list_html[1])
        if div:
            links = div.find_all('a', href=True)
            links.reverse()
            linkList = []
            for link in links:
                href = link.get('href')
                linkList.append(href)
            return linkList
        else:
            print(
                f"firstChap [chapter_list_html]: Missing div: {chapter_list_html}")
    else:
        print(
            f"firstChap [chapter_list_html]: Missing page items: {chapter_list_html}: URL: {url}")

    resetChapterURLShortcut()
    return getChapList()  # If broke, try again...


def resetChapterURLShortcut():
    global url
    print(
        f"\nSeems like the URL is old or corrupted. Please enter a new URL for: {url}")
    url = input('Please enter new URL: ')
    createDir(True)


def lastChap(links):
    print(f"links: {links}")
    last_line = links[-1]
    pattern = global_pattern
    # I don't remember why I did this, but it is important. I think...
    for i in range(2):
        curChap = re.findall(pattern, last_line)
        pattern = r'\d+'
    return int(curChap[-1])


# Checks if last chapter was allready downloaded, if not, checks link, then requests download


def downloadUnique(curChap, links):
    if lastChap(links) == curChap:
        return
    try:
        for link in links[curChap:]:
            response = requests.get(link)
            downloadImages(link)
    except Exception as e:
        print(f"Error downloading images [downloadUnique]: {e}")


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
                img_url = img_url.strip()  # There is a weird gap at the start of some links
                if not img_url.startswith('http'):
                    img_url = urllib.parse.urljoin(url, img_url)

                img_response = requests.get(img_url)
                img_response.raise_for_status()
                img_data = img_response.content

                img_filename = os.path.basename(
                    urllib.parse.urlparse(img_url).path)
                dl_folder = dl_path + book_title + distro_nav + \
                    'chapter-' + str(getLastDownload() + 1)
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


# Finds the latest chapter to downlaod


def getLastDownload():
    try:
        with open(tmp_dl_log, "r") as f:
            lines = f.readlines()

        if lines != []:
            last_line = lines[-1]
            pattern = global_pattern
            for i in range(2):
                curChap = re.findall(pattern, last_line)
                pattern = r'\d+'
            return int(curChap[-1])
        else:
            return 0
    except Exception as e:
        print(e)


# Get the main chapter page link


def getHomeLink(tmp_dl_path=""):
    if tmp_dl_path != "":
        dl_path = tmp_dl_path

    dl_path = os.getcwd() + distro_nav

    shortcut_file = dl_path
    print(f"shortcut_file: {shortcut_file}")

    try:
        with open(shortcut_file, "r") as f:
            lines = f.readlines()

        if lines != []:
            curLink = f.read()
            return curLink
    except FileNotFoundError:
        curLink = setNewLink()
        return curLink
    except Exception as e:
        print(e)


def getFileByExtension(ext, folder_path):
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith(ext):
                return os.path.join(root, filename)

    print("No .url files found in the folder.")
    return None


# Check if homelink exists


def checkHomeLink(tmp_book_title=""):
    global url
    if tmp_book_title != "":
        log_path = dl_path + tmp_book_title + distro_nav
    else:
        log_path = dl_path + book_title + distro_nav

    print(f"\n[checkHomeLink] Using: {log_path}")

    shortcut_file = getFileByExtension(".url", log_path)

    print(f"[shortcut_file] set to: {shortcut_file}")

    with open(shortcut_file, 'r') as f:
        for line in f:
            shortcut_file_contents = line.strip()
            print(
                f"Found [checkHomeLink:shortcut_file_contents]: {shortcut_file_contents}")
            if shortcut_file_contents.startswith('URL='):
                break

    shortcut = shortcut_file_contents.replace("URL=", "")
    print(f"Sending URL [checkHomeLink]\n: {shortcut}")
    url = shortcut
    return shortcut


# Gets a list links for each chapter from the main page


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

# Find the last downloaded chapter using the log


def getLinksFromLog(book_dir):
    cur_book_dir = dl_path + book_dir + distro_nav + dl_log
    print("Checking: " + cur_book_dir)
    print(f"dl_log: {dl_log}")
    with open(cur_book_dir, 'r') as f:
        links = f.readlines()
    print("")
    if len(links) == 0:
        print("Error [getLinksFromLog]")
        # YEAH, IM WORKING ON IT (note: work on this later) (note: Fixed... I think...)
        print(f"No links found [getLinksFromLog]: {links}")
        tmp_url = checkHomeLink(book_dir)
        print(f"[getLinksFromLog] getting: {tmp_url}")
        tmp_links = getChapList(tmp_url)
        print(f"Chapters obtianed [getLinksFromLog]: {tmp_links}\n")
        return tmp_links
    print(f"Links Found [getLinksFromLog] sending: {links[0]}")
    return links[0]

# Get the homepage URL by the last link on the list


def getTopLink(tmp_book_title=""):
    print(f"Finding head source of [getTopLink]: {url}")
    old_url = url

    tmp_home_link = checkHomeLink(tmp_book_title)

    if url != old_url:
        print(f"Head source found [getTopLink]: {url}")
        return url

    if tmp_home_link != False:
        print(f"Using tmp_home_link [getTopLink]: {tmp_home_link}")
        return tmp_home_link

    hasParent = False
    if len(top_link_html) >= 3:
        hasParent = True

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find(top_link_html[0], top_link_html[1])
        if hasParent:
            children = div.find_all(recursive=False)
            print(f"children [getTopLink:top_link_html]: {children}")
            div = children[title_html[2]]
        if div:
            links = div.find_all('a', href=True)
            links.reverse()
            linkList = []
            for link in links:
                href = link.get('href')
                linkList.append(href)
            print(f"Found [getTopLink]: {linkList[0]}")
            return linkList[0]
        else:
            print("firstChap: Missing div: Passing")
    else:
        print("firstChap: Missing Button: Passing")

    home_link = getHomeLink()
    if home_link != "":
        print(f"Using home_link [getTopLink]: {home_link}")
        return home_link


def getNextChap(links):
    lastChap(links)


def downloadSource():
    checkDistro()
    setSite()
    createDir()
    links = getChapList()
    last_downlaod = getLastDownload()
    downloadUnique(last_downlaod, links)
    print(
        f"---------------- No more chapters: {book_title} ----------------\n")


def updateSource():
    global url
    checkDistro()
    setSite()
    listDir()
    for i in range(len(book_titles)):
        url = getLinksFromLog(book_titles[i])
        print(f"URL set to: {url}")
        url = getTopLink(book_titles[i])
        print(f"URL set to again: {url}")
        downloadSource()


# Execution
checkOptions()
downloadSource()
