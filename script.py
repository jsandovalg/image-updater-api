import base64
from io import BytesIO
from PIL import Image, PngImagePlugin

def update_png_metadata(image_b64, user_comment):
    # Decode the base64 image
    image_data = base64.b64decode(image_b64)
    image = Image.open(BytesIO(image_data))

    # Ensure the image is in PNG format
    if image.format != 'PNG':
        raise ValueError("The provided image is not a PNG")

    # Create a new metadata dictionary
    meta = PngImagePlugin.PngInfo()

    # Adding or updating the custom metadata. This uses the 'tEXt' chunk for textual data.
    meta.add_text("UserComment", user_comment)

    # Save the modified image to a new file with the updated metadata
    image.save("updated_image.png", format="PNG", pnginfo=meta)

    # Return the path to the new file (or other desired output)
    return "updated_image.png"

# Example usage:
if __name__ == "__main__":
    with open("updated_image.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    new_image_path = update_png_metadata(encoded_string, "This is a user comment")

    # Open the new image and print all metadata
    with Image.open(new_image_path) as img:
        for k, v in img.info.items():
            print(f"{k}: {v}")
