from PIL import Image
from colorama import Fore, init
from os import listdir
from random import randrange

ASCII_CHARS = ['.',',',':',';','+','*','?','%','S','#','@']
ASCII_CHARS = ASCII_CHARS[::-1]

PALLETE = [
    255, 255, 255,
    255, 0, 0,
    255, 255, 0,
    0, 255, 0,
    0, 255, 255,
    255, 0, 255,
    0, 0, 255,
    0, 0, 0,
] + [0, ] * 248 * 3

PALLETE_VALUES = [
    Fore.WHITE,
    Fore.RED,
    Fore.YELLOW,
    Fore.GREEN,
    Fore.CYAN,
    Fore.MAGENTA,    
    Fore.BLUE,
    Fore.BLACK,
]

'''
method resize():
    - takes as parameters the image, and the final width
    - resizes the image into the final width while maintaining aspect ratio
'''
def resize(image, new_width=50):
    (old_width, old_height) = image.size
    aspect_ratio = float(old_height)/float(old_width)
    new_height = int(aspect_ratio * new_width)
    new_dim = (new_width, new_height)
    return image.resize(new_dim)

'''
method grayscalify():
    - takes an image as a parameter
    - returns the grayscale version of image
'''
def grayscalify(image):
    return image.convert('L')

'''
    method paletizize():
    - takes an image as a parameter
    - returns the palette version of image
'''
def paletizize(image):
    pal_image= Image.new("P", (1,1), 0)
    pal_image.putpalette(PALLETE)
    return image.convert("RGB").quantize(palette=pal_image, dither = 0)

'''
method modify():
    - replaces every pixel with a character whose intensity is similar
'''
def modify(image, rgb_image, buckets=25):
    initial_pixels = list(image.getdata())
    rgb_pixels = list(rgb_image.getdata())
    new_pixels = [ ([PALLETE_VALUES[rgb_value]], ASCII_CHARS[pixel_value//buckets]) for pixel_value, rgb_value in zip(initial_pixels, rgb_pixels)]
    return new_pixels


def pixels_line_to_string(pixels):
    string = ''
    for (fore, char) in pixels:
        string += str(''.join(fore)) + str(char)
    return string

'''
method do():
    - does all the work by calling all the above functions
'''
def do(image, new_width=50):
    image = resize(image)
    imageRGB = paletizize(image)
    image = grayscalify(image)

    pixels = modify(image, imageRGB)
    len_pixels = len(pixels)

    # Construct the image from the character list
    new_image = [pixels[index:index+new_width] for index in range(0, len_pixels, new_width)]

    return '\n'.join(map(pixels_line_to_string ,new_image))

'''
method runner():
    - takes as parameter the image path and runs the above code
    - handles exceptions as well
    - provides alternative output options
'''
def runner(path):
    image = None
    print(path)
    try:
        image = Image.open(path)
     
    except Exception:
        try: 
            path ='./github-resources/'
            files = listdir(path)
            index = randrange(0, len(files))
            image = Image.open(path + files[index])
        except Exception:
            print("Unable to find image in",path)
                #print
                # (e)
            return
    
    image = do(image)

    init(wrap=True)

    # To print on console
    print(image)

    # Else, to write into a file
    # Note: This text file will be created by default under
    #       the same directory as this python file,
    #       NOT in the directory from where the image is pulled.
    f = open('img.txt','w')
    f.write(image)
    f.close()

'''
method main():
    - reads input from console
    - profit
'''
if __name__ == '__main__':
    import sys
    import urllib.request
    try:
        if sys.argv[1].startswith('http://') or sys.argv[1].startswith('https://'):
            urllib.request.urlretrieve(sys.argv[1], "asciify.jpg")
            path = "asciify.jpg"
        else:
            path = sys.argv[1]
    except:
        pass #try from the default path
    runner(path)
