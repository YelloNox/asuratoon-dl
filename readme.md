# asuratoon-dl / Asura Scans

> Download full books from asuratoon.com

## Note: Currently only works with windows

> I have not tested linux!

The script has directory mapping optimised for windows that might be incompatable on linux. (i.e. using "\\\\" instead of "/")

If you find any bugs, issues or have a feature request, open a request. I will respond in an unknown ammount of time... probably...

## Features

- Downlaods Entire source from chapter 1 to END
- Resume download where you left off (skipping previous downloads)
- Ability to save as image folder or archive to CBZ
- CLI options for scripting
- Create shortcut to webpage in path (for windows)

## Usage

```
Usage: *_dl.py --path /path/to/dir --cbz https://example.com

Options:

        --help | -h: Displays this message

        --path | -p: Path to download to (--path <DIR>)

        --cbz: Download as a CBZ

        --link: Create a shortcut file

        --update: Updates all downloads to latest chapter
                --update-help for more information

```

## Install

Install and run:

1. Clone this repo to desired directory: `git clone https://github.com/YelloNolo/asuratoon-dl`
2. Create venv env: `python -m venv venv`
3. Activate venv: `.\venv\Scripts\activate.bat`
4. Install requirements: `pip install -r requirements.txt`
5. Run script: [#Usage](https://github.com/YelloNolo/asuratoon-dl?tab=readme-ov-file#Usage)
