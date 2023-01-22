import pathlib
import argparse
from functools import lru_cache
import numpy as np
from PIL import Image

# catppuccin mocha color list
# colorList = [
#     [245, 224, 220],  # #f5e0dc
#     [242, 205, 205],  # #f2cdcd
#     [245, 194, 231],  # #f5c2e7
#     [203, 166, 247],  # #cba6f7
#     [243, 139, 168],  # #f38ba8
#     [235, 160, 172],  # #eba0ac
#     [250, 179, 135],  # #fab387
#     [249, 226, 175],  # #f9e2af
#     [166, 227, 161],  # #a6e3a1
#     [148, 226, 213],  # #94e2d5
#     [137, 220, 235],  # #89dceb
#     [116, 199, 236],  # #74c7ec
#     [137, 180, 250],  # #89b4fa
#     [180, 190, 254],  # #b4befe
#     [205, 214, 244],  # #cdd6f4
#     [186, 194, 222],  # #bac2de
#     [166, 173, 200],  # #a6adc8
#     [147, 153, 178],  # #9399b2
#     [127, 132, 156],  # #7f849c
#     [108, 112, 134],  # #6c7086
#     [88, 91, 112],    # #585b70
#     [69, 71, 90],     # #45475a
#     [49, 50, 68],     # #313244
#     [30, 30, 46],     # #1e1e2e
#     [24, 24, 37],     # #181825
#     [17, 17, 27]      # #11111b
# ]


def loadcolors(infile):
    if not infile:
        print("no file specified please specifi a file")
        exit(131)
    colorList = []
    for i, hexCode in enumerate(open(infile)):
        # remove comments
        hexCode = hexCode.split("//")[0].replace("\n", "")
        if hexCode.isspace() or "" == hexCode:
            continue

        RGB = hexToIntList(hexCode)
        try:
            colorList.append(tuple(RGB))
        except ValueError:
            print(f"Invalid color on line {i + 1}")

    return tuple(colorList)


def hexToIntList(color="#000000"):
    if not color.startswith("#"):
        color = "#" + color
    if 4 == len(color):
        color = color[1] + color[1] + color[2] + color[2] + color[3] + color[3]
    if 7 != len(color):
        raise ValueError("Invalid Hexcode")
    return [int(color[1] + color[2], 16), int(color[3] + color[4], 16), int(color[5] + color[6], 16)]


def newFileName(NF_filename, NF_InsertString="-transformed", NF_Lastseperator="."):
    NF_filename = str(NF_filename)
    if "." in NF_filename:
        return NF_filename[:NF_filename.rindex(NF_Lastseperator)] + NF_InsertString + NF_filename[NF_filename.rindex(NF_Lastseperator):]
    else:
        return NF_filename + NF_InsertString


@lru_cache(maxsize=4294967296)
def findColosestcolor(colorToFind, colorList):
    if len(colorToFind) > 3:
        colorToFind = colorToFind[:3]
    color_array = np.array(colorList)
    colorToFind = np.array(colorToFind)
    distances = np.sqrt(np.sum((color_array - colorToFind)**2, axis=1))
    index_of_smallest = np.where(distances == np.amin(distances))
    return color_array[index_of_smallest]


@lru_cache(maxsize=4294967296)
def procesImage(imgPixel, outImgPixel, imgWidth, imgHeight, colorList):
    for x in range(imgWidth):
        for y in range(imgHeight):
            r, g, b = imgPixel[x, y]
            r, g, b = findColosestcolor((r, g, b), colorList)[0]
            outImgPixel[x, y] = (r, g, b)
        print(f"progress: {round((x / imgWidth * 100), 1)}%", end="\r")


@lru_cache(maxsize=4294967296)
def procesImageAlpha(imgPixel, outImgPixel, imgWidth, imgHeight, colorList):
    for x in range(imgWidth):
        for y in range(imgHeight):
            r, g, b, a = imgPixel[x, y]
            r, g, b = findColosestcolor((r, g, b), colorList)[0]
            outImgPixel[x, y] = (r, g, b, a)
        print(f"progress: {round((x / imgWidth * 100), 1)}%", end="\r")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("convert_file", type=pathlib.Path, help="image file to be converted")
    parser.add_argument("-o", "--output", type=pathlib.Path, help="File to output procesed image")
    parser.add_argument("-c", "--colors", help="file containg the color codes")
    args = parser.parse_args()

    if not args.convert_file:
        print("Give a valid file to convert")
        exit(130)

    colorList = loadcolors(args.colors)
    image_path = args.convert_file
    if args.output:
        output_file = args.output
    else:
        output_file = newFileName(image_path)

    # Open original Image to be transformed
    with Image.open(image_path) as img:
        imgWidth, imgHeight = img.size
        imgPixel = img.load()

    # Create A new file to use as output
    outImg = Image.new(img.mode, img.size)
    outImgPixel = outImg.load()

    # implement procetagee done
    try:
        _, _, _ = imgPixel[0, 0]
        hasAlphaChannel = False
    except ValueError:
        hasAlphaChannel = True

    if hasAlphaChannel:
        procesImageAlpha(imgPixel, outImgPixel, imgWidth, imgHeight, colorList)
    else:
        procesImage(imgPixel, outImgPixel, imgWidth, imgHeight, colorList)

    outImg.save(output_file)


if __name__ == "__main__":
    main()
