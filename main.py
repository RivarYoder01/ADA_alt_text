#!/usr/bin/env python3

import requests # Library that requests content from HTML
import sys # Allows ending of program
import os
import openai
from dotenv import load_dotenv

# from requests.auth import HTTPBasicAuth

# WP_USERNAME = "Noah"
# WP_APP_PASSWORD = "iZg8 Jhk1 kYTY spxJ yQm3 yJc9"
# WP_API_BASE = "https://bestpointwebdesign.com/wp-json/wp/v2/media"

# AUTH = HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD)
OPENAI_API_KEY = ('sk-proj-eh0mLZJTyQgKwSWnux-5yudtUaHpzBUqg6WjhcMVKmTUeZ4T-yFdGxTrDcH8LKhw2qm4QDXfXVT3BlbkFJfMLA0pm38iesB2'
              'pS1icSyd-oClbJ7OV3deMlS2PX8vjY-A93X6-IatDgzvspG0K1ocwIYbx_4A')

def capture_wp_images():
    url = "https://bestpointwebdesign.com/wp-json/wp/v2/media" # Need to find a way to autopopulate
    response = requests.get(url)

    if response.status_code == 200: # Request successful, json file has been pulled
        images = response.json() # Reads files
        image_urls = [image['source_url'] for image in images if image['media_type'] == 'image'] # FOR LOOP pulls images
        return image_urls
    else:
        print("Error fetching images.") # Error handling
        return []

def generate_alt_text(pulled_images):
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    prompt = ("Generate alternative text for this image that is no longer than 150 characters long. Do not give any "
              "other text and clear all formatting. Describe the image's purpose, essential information, only include "
              "what is relevant to a sighted user. Use natural language, no abbreviations or jargon. Avoid phrases "
              "like 'click here' and 'image of'. End with a period.")

    result = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print(result.choices[0].message.content)


if __name__ == "__main__":
    """
    Generate alternative text for this image 
    {https://bestpointwebdesign.com/wp-content/uploads/2025/02/App-Image-Home.png} that is no longer than 150 
    characters long. Do not give any other text and clear all formatting. Describe the image's purpose, essential 
    information, only include what is relevant to a sighted user. Use natural language, no abbreviations or jargon. 
    Avoid phrases like 'click here' and 'image of'. End with a period.
    """
    pulled_images = capture_wp_images()

    if pulled_images == "":
        print('No images found')
        sys.exit(0)
    else:
        for image in pulled_images:
            generate_alt_text(pulled_images)

        sys.exit(0)

