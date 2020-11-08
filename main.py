# (C) Daniel Desmond Dennis 2020

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import argparse
import datetime
import os

def main():
    parser = argparse.ArgumentParser(description='Add a watermark to my photos')
    parser.add_argument('-i', '--image_path', metavar='path/to/image.jpg', help='Location of image', required=True, nargs='+')
    parser.add_argument('-n', '--name', metavar='John Smith', help='Name of copyrighht holder', default='Daniel Dennis')
    parser.add_argument('-y', '--year', metavar='1962', help='Year photograph was taken', default=datetime.date.today().year)
    parser.add_argument('-s', '--save_name', metavar='_dd', help='Name to add to image when saving', default='')
    parser.add_argument('-f', '--font_size', metavar='64', help='Size of text, height in pixels', default=64, type=int)
    parser.add_argument('-o', '--offset', metavar='64', help='How much the notice is offset from the corner in pixels', default=10, type=int)
    parser.add_argument('-d', '--destination_path', metavar='path/to/destination/folder', default=None)
    args = parser.parse_args()

    if (args.destination_path == None) and (args.save_name == ''):
        print('--destination_path or --save_name must be set')
        exit()

    for image in args.image_path:
        img = read_image(image)
        img_watermarked = add_copyright(img, args.name, args.year, font_size=args.font_size, offset=args.offset)
        if args.destination_path != None:
            new_path = merge_path1_to_path2(image, args.destination_path)
            save_image(img_watermarked, new_path, args.save_name)
        else:
            save_image(img_watermarked, image, args.save_name)

def read_image(image_path):
    return Image.open(image_path)

def add_copyright(img, name, year, font_size=64, offset=10):
    height = img.size[1] - font_size - offset
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('Times New Roman.ttf', font_size)
    draw.text((offset, height), f'\u00A9 {year} {name}', (255,255,255), font=font)
    return img

def save_image(img, img_path, save_name):
    save_path = add_extension(img_path, save_name)
    exif = img.info['exif']
    img.save(save_path, exif=exif)

def merge_path1_to_path2(path1, path2):
    old_path, name = os.path.split(path1)
    merged = os.path.join(path2, name)
    return merged

def add_extension(img_path, save_name):
    img_path = os.path.expandvars(img_path)
    path, name = os.path.split(img_path)
    name_split = name.split('.')
    print(path, name)
    new_name = '.'.join(name_split[:-1]) + save_name + '.' + name_split[-1]
    save_path = os.path.join(path, new_name)
    return save_path

if __name__ == '__main__':
    main()