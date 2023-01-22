<h1 align="center">ColorMatch-py</h1>
<p align="center">Converts Image to have a specific color scheme</p>

## about
Simple project made in a day.

## example output

Original             |  Ascii
:-------------------------:|:-------------------------:
![](./assets/example.png)  |  ![](./assets/example-transformed.png)

## Install dependencies
```
python -m venv venv
source venv/bin/activate        # Bash/Zsh
source venv/bin/activate.fish   # Fish
pip install -r requirements.txt
```

## Usage
```bash
 → python main.py --help                                   
usage: main.py [-h] [-o OUTPUT] [-c COLORS] convert_file

positional arguments:
  convert_file          image file to be converted

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        File to output procesed image
  -c COLORS, --colors COLORS
```
