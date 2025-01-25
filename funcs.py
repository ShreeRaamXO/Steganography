from PIL import Image

def encode_image(input_image_path, secret_data, output_image_path):
    img = Image.open(input_image_path)
    encoded_img = img.copy()
    width, height = img.size

    # Convert the secret data into binary and add a delimiter to mark the end
    binary_data = ''.join(format(ord(c), '08b') for c in secret_data) + '1111111111111110'
    data_index = 0

    # Check if the data fits into the image
    max_capacity = width * height * 3  # Each pixel has 3 color channels
    if len(binary_data) > max_capacity:
        raise ValueError("Data is too large to encode in the image!")

    # Encode binary data into the image
    pixels = encoded_img.load()
    for y in range(height):
        for x in range(width):
            if data_index < len(binary_data):
                pixel = list(pixels[x, y])  # Get the pixel (as a list for mutability)
                for channel in range(3):  # Iterate through R, G, B channels
                    if data_index < len(binary_data):
                        # Modify the LSB of each channel to embed a bit of the data
                        pixel[channel] = (pixel[channel] & ~1) | int(binary_data[data_index])
                        data_index += 1
                pixels[x, y] = tuple(pixel)  # Update the pixel

    # Save the modified image
    encoded_img.save(output_image_path)
    print(f"Data encoded successfully into {output_image_path}")


def decode_image(input_image_path):
    img = Image.open(input_image_path)
    width, height = img.size
    binary_data = ""

    # Extract binary data from the image
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            for channel in range(3):  # Extract from R, G, B channels
                binary_data += str(pixel[channel] & 1)

    # Convert binary data to text, stopping at the delimiter
    delimiter = '1111111111111110'
    if delimiter in binary_data:
        binary_data = binary_data[:binary_data.index(delimiter)]
        secret_data = ''.join(chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8))
        return secret_data
    else:
        raise ValueError("No hidden data found!")
