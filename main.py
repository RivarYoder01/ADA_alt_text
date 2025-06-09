#!/usr/bin/env python3

import requests # Library that requests content from HTML
# import openai # Passes into ChatGPT to generate alt text
import sys

pulled_images = ''

def capture_wp_images():
    url = "https://bestpointwebdesign.com/wp-json/wp/v2/media" # Need to find a way to autopopulate
    response = requests.get(url)

    if response.status_code == 200: # Request successful, json file has been pulled
        images = response.json() # Reads files
        image_urls = [image['source_url'] for image in images if image['media_type'] == 'image'] # FOR LOOP Pulls images
        return image_urls
    else:
        print("Error fetching images.") # Error handling
        return []

def generate_alt_text(pulled_images):
    print(pulled_images)


if __name__ == "__main__":
    """
    Generate alternative text for this image 
    {https://bestpointwebdesign.com/wp-content/uploads/2025/02/App-Image-Home.png} that is no longer than 150 
    characters long. Do not give any other text and clear all formatting. Describe the image's purpose, essential 
    information, and only include what is relevant to a sighted user. Use natural language, no abbreviations or jargon. 
    Avoid phrases like 'click here' and 'image of'. End with a period.
    """
    pulled_images = capture_wp_images()
    print(pulled_images)

    if pulled_images == "":
        print('No images found')
        sys.exit(0)
    else:
        generate_alt_text(pulled_images)

