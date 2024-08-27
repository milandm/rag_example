import openai
import requests
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse
from django.conf import settings
import os
import requests
from django.http import HttpRequest
import datetime


def generate_image1(request: HttpRequest, image_url, text_over_image):

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Append the timestamp to the filename
    image_file_timestamp = f"image_{timestamp}.png"
    image_file_with_text_timestamp  = f"image_with_text_{timestamp}.png"


    # Download and save the image locally
    image_response = requests.get(image_url)
    image_path = os.path.join(settings.MEDIA_ROOT, image_file_timestamp)
    with open(image_path, "wb") as f:
        f.write(image_response.content)


    # Open the downloaded image
    img = Image.open(image_path)

    # Initialize ImageDraw
    draw = ImageDraw.Draw(img)

    # Specify a font and size
    font_size = 50 * 4
    font_path = os.path.join(settings.BASE_DIR, 'fonts/DancingScript-Regular.ttf')
    font = ImageFont.truetype(font_path, font_size)

    # Get the bounding box of the text
    bbox = draw.textbbox((0, 0), text_over_image, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # Calculate the position to center the text
    image_width, image_height = img.size
    text_position = ((image_width - text_width) // 2, (image_height - text_height) // 2)

    # Draw black outline
    outline_range = 2  # Thickness of the outline
    for x in range(-outline_range, outline_range + 1):
        for y in range(-outline_range, outline_range + 1):
            draw.text((text_position[0] + x, text_position[1] + y), text_over_image, font=font, fill="black")

    # Draw white text
    draw.text(text_position, text_over_image, font=font, fill="white")

    # Save the edited image
    edited_image_path = os.path.join(settings.MEDIA_ROOT, image_file_with_text_timestamp)
    img.save(edited_image_path)

    # Construct the image URL
    image_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, image_file_with_text_timestamp))

    # Return the image URL
    return image_url


def generate_image(request: HttpRequest, image_url, text_over_image):

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Append the timestamp to the filename
    image_file_timestamp = f"image_{timestamp}.png"
    image_file_with_text_timestamp = f"image_with_text_{timestamp}.png"

    # Download and save the image locally
    image_response = requests.get(image_url)
    image_path = os.path.join(settings.MEDIA_ROOT, image_file_timestamp)
    with open(image_path, "wb") as f:
        f.write(image_response.content)

    # Open the downloaded image
    img = Image.open(image_path)

    # Initialize ImageDraw
    draw = ImageDraw.Draw(img)

    # Specify a font and size
    font_size = 50 * 2
    font_path = os.path.join(settings.BASE_DIR, 'fonts/DancingScript-Regular.ttf')
    font = ImageFont.truetype(font_path, font_size)

    # Get image dimensions
    image_width, image_height = img.size

    # Calculate maximum width for the text
    max_text_width = image_width * 0.9  # Allow some padding

    # Split the text into lines that fit within the image width
    lines = []
    words = text_over_image.split(' ')
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        test_line_width = bbox[2] - bbox[0]
        if test_line_width <= max_text_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    lines.append(line)

    # Calculate the total height of the text block
    total_text_height = sum([draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines])

    # Calculate the initial vertical position for the first line
    y_position = (image_height - total_text_height) // 2

    # Draw each line of text
    outline_range = 2  # Thickness of the outline
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x_position = (image_width - text_width) // 2

        # Draw black outline
        for x in range(-outline_range, outline_range + 1):
            for y in range(-outline_range, outline_range + 1):
                draw.text((x_position + x, y_position + y), line, font=font, fill="black")

        # Draw white text
        draw.text((x_position, y_position), line, font=font, fill="white")

        # Update y_position for the next line
        y_position += bbox[3] - bbox[1]

    # Save the edited image
    edited_image_path = os.path.join(settings.MEDIA_ROOT, image_file_with_text_timestamp)
    img.save(edited_image_path)

    # Construct the image URL
    image_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, image_file_with_text_timestamp))

    # Return the image URL
    return image_url
