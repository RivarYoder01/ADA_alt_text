#!/usr/bin/env python3

"""
Program aims to pull information from a given URL and pass it to ChatGPT to generate alternative text based on what is
in the given image.

FUNCTIONS:
main()
pull_wp_images()
generate_alt_text(pulled_images: list)
alt_text_to_wp(result.choices[0].message.content) IN PROGRESS
"""

__author__ = 'Rivar Yoder'
__version__ = '1.0'
__date__ = '2025.06.02'
__status__ = 'Development'

import requests # Requests content from HTML
import sys # Ending of program
import os # Access to other platforms (openAI and WordPress)
import openai # Chatgpt access
from dotenv import load_dotenv # .env access

# TEMPORARY INFORMATION
# WP_USERNAME = "Noah"
# WP_APP_PASSWORD = "iZg8 Jhk1 kYTY spxJ yQm3 yJc9"
# AUTH = HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD)

def pull_wp_images():
    """
    Function accesses provided URL and IF the request is successful, the program reads the file and pulls the image's
    urls with a FOR LOOP.
    :return: image_urls OR null:
    """
    url = "https://bestpointwebdesign.com/wp-json/wp/v2/media" # Need to find a way to autopopulate
    response = requests.get(url)

    if response.status_code == 200: # Request successful, json file has been pulled
        images = response.json() # Reads files
        pulled_images = [image['source_url'] for image in images if image['media_type'] == 'image'] # FOR LOOP pulls images
        if pulled_images != "": # pulled_images is not empty, loop through list and pass to generate_alt_text
            for image in pulled_images:
                generate_alt_text(pulled_images[0])
            return []
        else: # pulled_images is empty
            print('No images found')
            sys.exit(0)
    else: # Request unsuccessful != 200
        print("Error fetching images.") # Error handling
        return []

def generate_alt_text(pulled_images: list):
    """
    Takes in pulled_images as a list, using load_dotenv() to pull the API key from .env file. OS is used to access
    ChatGPT with that key.

    The Prompt: Generate alternative text for this image that is no longer than 150 characters long. Do not give any
                other text and clear all formatting. Describe the image's purpose, essential information, only include
                what is relevant to a sighted user. Use natural language, no abbreviations or jargon. Avoid phrases
                like 'click here' and 'image of'. End with a period.

    Image URL: Pulled from pull_wp_images

    FOR NOW: Prints result from Chatgpt, will soon pass into a function to pass alt text into WordPress

    :param pulled_images:
    :return:
    """
    load_dotenv() # opens .env
    openai.api_key = os.getenv("OPENAI_API_KEY") # Pulls key from .env

    prompt = ("Generate alternative text for this image that is no longer than 150 characters long. Do not give any "
              "other text and clear all formatting. Describe the image's purpose, essential information, only include "
              "what is relevant to a sighted user. Use natural language, no abbreviations or jargon. Avoid phrases "
              "like 'click here' and 'image of'. End with a period.")

    result = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[ # Message to chatgpt
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": pulled_images}}] # pulled_images passed into function
            }
        ]
    )

    print(result.choices[0].message.content)

    alt_text_to_wp(result.choices[0].message.content)


def alt_text_to_wp(result):
    print(result) # temp

    return


def main():
    """
    Calls pull_wp_images() to pull image URLs from a provided link.
    """
    pull_wp_images()


if __name__ == "__main__":
    main()