def decode_image(path_to_png):
    """
    Decode image from path
    """
    # Open the image using PIL:
    encoded_image = Image.open(path_to_png)

    # Separate the red channel from the rest of the image:
    red_channel = encoded_image.split()[0]

    # Create a new PIL image with the same size as the encoded image:
    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()
    x_size, y_size = encoded_image.size

    for x in range(x_size):
        for y in range(y_size):
            buffer = red_channel.getpixel((x, y))

            binary = bin(buffer)
            lsb = binary[len(binary) - 1]
            lsb = int(lsb)

            rbg = (255, 255, 255) if lsb == 0 else (0, 0, 0)

            decoded_image.putpixel((x, y), rbg)

    decoded_image.save("decoded_image.png")


def encode_image(path_to_png, secret_message):
    """
    Encode secret text to image from path
    """
    base_image = Image.open(path_to_png)
    x_size, y_size = base_image.size

    text_img = Image.new(mode='RGB', size=(x_size, y_size), color=(0, 0, 0))
    draw = ImageDraw.Draw(text_img)

    # Font Source: https://stackoverflow.com/a/59160253/7897036
    relativeness = 25
    font = ImageFont.truetype("Times New Roman.ttf", y_size // relativeness)
    draw.text((x_size // relativeness, y_size // relativeness),
              secret_message, font=font)

    text_img.save("raw_text.png")

    for x in range(x_size):
        for y in range(y_size):

            raw_rgb = base_image.getpixel((x, y))
            red = raw_rgb[0]
            binary = bin(red)
            binary_list = list(binary)
            binary_len = len(binary_list)

            if text_img.getpixel((x, y)) == (255, 255, 255):
                binary_list[binary_len - 1] = "0"
            else:
                binary_list[binary_len - 1] = "1"

            new_red = int("".join(binary_list), 2)
            new_rgb = (new_red, raw_rgb[1], raw_rgb[2])
            base_image.putpixel((x, y), new_rgb)

    base_image.save("encoded.png", "png")

encode_image("dog.png", "hello dani")
decode_image("encoded.png")