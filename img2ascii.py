from PIL import Image
import sys
ASCII_CHARS = [".", "+", "o", "P", "O", "?", "@", "#"]
BLOCKS_CHARS = ["\u2588"]
BRAILLE_CHARS = ["\u28FF"]

# Resize image while maintaining aspect ratio
def resize_image(image, new_width=100,scale=2.1):
    width, height = image.size
    aspect_ratio = height / width / scale  # Adjusting ratio for ASCII look
    if(new_width % 2 != 0 ):
        new_width-=1
    new_height = int(aspect_ratio * new_width)
    if(new_height% 2 != 0 ):
        new_height-=1
    return image.resize((new_width, new_height))

def upper_lower_pixels_to_ascii(up,lp):
    ascii = "[38;2;{lr};{lg};{lb};48;2;{ur};{ug};{ub}m\u2584".format(ur=up[0],ug=up[1],ub=up[2],lr=lp[0],lg=lp[1],lb=lp[2])
    return ascii

def pixels_to_ascii(r,g,b, select_pattern):
    lum = (0.2126 * r + 0.7152 *g+ 0.0722 * b)/255  # 0-1
    bin_size = len(select_pattern)
    word = select_pattern[round(lum * (bin_size-1))]
    ascii = "[38;2;{0};{1};{2}m{3}".format(r,g,b,word)
    return ascii

# Convert image to ASCII art
def image_to_ascii(image_path,store_path, new_width=100, pattern='a'):
    f = open(store_path, "w", encoding="utf-8")
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Unable to open image file {image_path}. {e}")
        return

    select_pattern = []
    match pattern:
        case 'n':
            select_pattern = ASCII_CHARS
        case 'fb':
            select_pattern = BLOCKS_CHARS 
        case 'bp':
            select_pattern = BRAILLE_CHARS
        case _:
            select_pattern = ASCII_CHARS

    if(pattern != 'hb'):
        image = resize_image(image, new_width)
        rgbImage = image.convert('RGB')
        size = rgbImage.size;
        for i in range(size[1]):
            ascii_str = ""
            for j in range(size[0]):
                r,g,b = rgbImage.getpixel((j,i));
                ascii = pixels_to_ascii(r,g,b, select_pattern)
                ascii_str += ascii;
            print(ascii_str)
            ascii_str += "[m"
            ascii_str += "\n"
            f.write(ascii_str)
        f.close()
    else:
        image = resize_image(image, new_width,1)
        rgbImage = image.convert('RGB')
        size = rgbImage.size;
        for j in range(0,size[1],2):
            ascii_str = ""
            for i in range(size[0]):
                up = rgbImage.getpixel((i,j));
                lp = rgbImage.getpixel((i,j+1));
                ascii = upper_lower_pixels_to_ascii(up,lp)
                ascii_str += ascii;
            print(ascii_str)
            ascii_str += "[m"
            ascii_str += "\n"
            f.write(ascii_str)
        f.close()



if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python script.py <image_path> <width> <store-path> <pattern>")
        sys.exit(1)

    image_path = sys.argv[1]
    width = int(sys.argv[2])
    store_path = sys.argv[3]
    pattern = sys.argv[4]

    image_to_ascii(image_path, store_path,width, pattern)


