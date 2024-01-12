# asuratoon-dl / Asura Scans

> Download full comics from asuratoon.com

If you find any bugs, issues or have a feature request, open a request. I will respond in an unknown ammount of time... probably...

## 🗒️ Note: Currently only tested on Windows :(

I have not tested linux, but the implementation should work!\

## ✅ Features

-   Downlaods Entire comic: START to END
-   Download all new chapters in one command
-   Save chapters as image folder or CBZ archive
-   CLI options for scripting
-   Create quick link to webpage in path (Windows)

## ⬇️ Install

Install and run:

1. Clone this repo to desired directory: `git clone https://github.com/YelloNolo/asuratoon-dl`
2. Create venv env: `python -m venv venv`
3. Activate venv: `.\venv\Scripts\activate.bat`
4. Install requirements: `pip install -r requirements.txt`
5. Run script: [#Usage](https://github.com/YelloNolo/asuratoon-dl?tab=readme-ov-file#Usage)

## 🪴 Usage

Activate Python venv: `.\venv\Scripts\activate.bat`

```bash
Usage: asuratoon_dl.py --path /path/to/dir --cbz https://example.com

Options:

        --help | -h: Displays this message

        --path | -p: Path to download to (--path <DIR>)

        --cbz: Download as a CBZ

        --link: Create a shortcut file

        --update: Updates all downloads to latest chapter
                --update-help: For more information

```

## ✅ ToDo

-   [ ] Add a network throttle
-   [ ] Add a network cap

## ❓ Q&A

### Why don't I use multiprocessing to download multiple images at once?

I do not want to burden the host of the server

### Will there be support for other sources?

Maybe. I have no current plans, but I made the script flexable for more sources. If there are any requests, feel free to open a [discussion](https://github.com/YelloNolo/asuratoon-dl/discussions).

## 🌟 Thanks

-   [asuratoon.com](https://asuratoon.com/)

## 🪪 License

This project is licensed under the terms of the MIT License. See the [LICENSE](LICENSE) file for details.

### MIT License

The MIT License is a permissive open-source license that allows you to use, modify, and distribute this software freely, as long as you include the original copyright notice and disclaimers.
