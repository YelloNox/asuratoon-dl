# 📚 asuratoon-dl / Asura Scans

> Download full comics from asuratoon.com (and other sources (kinda))

If you find any bugs, issues or have a feature request, open a request. I will respond in "SOME" ammount of time... probably...

## 💸 Note

Linux is back to testing phase... New changes might break some things...


## ✅ Features

-   Downlaods Entire comic: START to END
-   Download all new chapters in one command (--update)
-   Save chapters as image folder or CBZ archive
-   CLI options for scripting
-   Create quick link (shortcut) to webpage in directory (Windows)
-   Works on both Windows and Linux

## ⬇️ Install

Install and run:

1. Clone this repo to desired directory: `git clone https://github.com/YelloNolo/asuratoon-dl`
2. Create venv env: `python -m venv venv`
3. Activate venv: `.\venv\Scripts\activate.bat`
4. Install requirements: `pip install -r requirements.txt`
5. Run script: [#Usage](https://github.com/YelloNolo/asuratoon-dl?tab=readme-ov-file#Usage)

## 🪴 Usage

Activate Python venv: `.\venv\Scripts\activate.bat`

```
Usage: asuratoon_dl.py --path /path/to/dir --cbz https://example.com

Options:

        --help | -h: Displays this message

        --site | -s: Specify what site to download from (learn more in info.md)

        --path | -p: Path to download to (--path <DIR>)

        --cbz: Download as a CBZ

        --update: Updates all downloads to latest chapter
                --update-help: For more information

```

## ✅ ToDo

-   [x] Test Linux
-   [ ] Test Linux... Again...
-   [ ] Add support for more sources (might make a seperate script or repo) (In progress)
-   [ ] Add a network throttle (and/or network cap (and/or image cap))
-   [ ] Add ".updateignore" to ignore specified books
-   [ ] Add metadata to csv (If possible)
-   [ ] Add download option for cover

> Sticky-Note For Later: https://pypi.org/project/pycbzhelper/

## ❓ Q&A

### Why don't I use multiprocessing to download multiple images at once?

I do not want to burden the host of the server. They are allready doing a great service to the community!

### Will there be support for other sources?

Maybe. I have no current plans, but I made the script flexable for more sources. If there are any requests, feel free to open a [discussion](https://github.com/YelloNolo/asuratoon-dl/discussions).

## 🌟 Thanks

-   [asuratoon.com](https://asuratoon.com/)

## 🪪 License

This project is licensed under the terms of the MIT License. See the [LICENSE](LICENSE) file for details.

### MIT License

The MIT License is a permissive open-source license that allows you to use, modify, and distribute this software freely, as long as you include the original copyright notice and disclaimers.
