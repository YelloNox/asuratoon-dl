#!/bin/bash

echo -n "Enter URL: "
read url

source ./venv/bin/activate

python ../asuratoon_dl.py --path ../downloads/Asuratoon --cbz --link $url