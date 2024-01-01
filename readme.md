# asuratoon-dl

> Download full books from asuratoon.com

## Note: Currently only works with windows

> I have not tested linux!

The script has directory mapping optimised for windows that might be incompatable with linux. (i.e. using "\\\\" instead of "/")

## Features

- Downlaods Entire source from chapter 1 to END
- Resume download where you left off (skipping previous downloads)
- Ability to save as image folder or archive to CBZ
- CLI options for scripting
- Create shortcut to webpage in path (for windows)

## Usage

```
Usage: \*\_dl.py --path /path/to/dir --cbz https://example.com

Options:

    --help | -h: Displays this message
    --path <url> | -p <url>: Path files save under
    --cbz: Archive as CBZ
    --link: Create a shortcut file

```

## Install

Install and run:

1. Clone this repo to desired directory: `git clone https://github.com/YelloNolo/asuratoon-dl`
2. Create venv env: `python -m venv venv`
3. Activate venv: `.\venv\Scripts\activate.bat`
4. Install requirements: `pip install -r requirements.txt`
5. Run script: [#Usage](https://github.com/YelloNolo/asuratoon-dl?tab=readme-ov-file#Usage)
