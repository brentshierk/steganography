
from PIL import Image, ImageDraw
def decode_image(path_to_png):
 # Open the image using PIL:
    encoded_image = Image.open(path_to_png)
 # Separate the red channel from the rest of the image:
    encoded_image_pixels = encoded_image.load()
# Create a new PIL image with the same size as the encoded image:
    decoded_image = Image.new("RGB", encoded_image.size)
    x_size, y_size = encoded_image.size
# For pixels in image
    for i in range(x_size):
        for j in range(y_size):

            # Get red channel value of each pixel
            r_value = encoded_image.getpixel((i, j))[0]

            # Convert red value to binary
            r_value_bin = bin(r_value)

            # If first bit of binary is 1, write a red pixel to blank canvas
            if r_value_bin[-1] == '1':
                decoded_image.putpixel((i, j), (255, 0, 0))

    decoded_image.save('./decoded_image.png')


def encode_image(path_to_png):

    text_to_write = input("Text to encode: ")

    original = Image.open(path_to_png).convert('RGB')
    x, y = original.size

    # Get list of coords where text is
    text_pixel_locations = write_text(text_to_write, x, y)

    for location in text_pixel_locations:

        # get original rgb value for pixel location where text will go
        print(location)
        print(original.getpixel((location[0], location[1])))
        rgb = original.getpixel((location[0], location[1]))

        # convert red value to binary
        r_value_bin = bin(rgb[0])

        # Set binary LSB to 1
        list_binary = list(r_value_bin)
        list_binary[-1] = '1'

        # Convert binary back to string
        r_value_bin = ''.join(list_binary)
        r_value_int = int(r_value_bin, 2)

        # Create new rgb tuple
        rgb = (r_value_int, rgb[1], rgb[2])

        # Rewrite coord with new rgb tuple
        original.putpixel((location[0], location[1]), rgb)

        original.save('./new_encoded_image.png')

def write_text(text_to_write, x, y):
    # Create white canvas
    img = Image.new('RGB', (x, y), color='white')
   # Write black text to canvas
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text_to_write, (0, 0, 0))
    img.save('./text.png')
    # Record coords of each black pixel on canvas
    pixel_locations = []
    for i in range(x):
        for j in range(y):
            rgb = img.getpixel((i, j))
            if rgb == (0, 0, 0):
                pixel_locations.append((i, j))

    return pixel_locations

# encode_image('./rick.png')
decode_image('./rick.png')