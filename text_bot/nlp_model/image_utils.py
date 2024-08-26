import openai
import requests
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse
from django.conf import settings
import os
import requests
from django.http import HttpRequest
import datetime


def generate_image(request: HttpRequest, image_url, text_over_image):

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
