#Import Libraries
import os
import base64
from matplotlib import text
import pandas as pd
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

#Retrive the OpenAI API key
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

#Connect to the api and set the gpt model
client = OpenAI()
MODEL = "gpt-5"

#Select the folder where the images are
IMAGE_DIR = input("Enter the name of the folder: ")
print(f"Image directory set to {IMAGE_DIR}!")

#Build a function that converts images into base64
def encode_image(image_path):
    with open(image_path, "rb") as file:
        b64 = base64.b64encode(file.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64}"

#Get the images
rows = []
image_files = sorted(
    [file for file in os.listdir(IMAGE_DIR) if file.endswith((".jpeg",".png",".jpg"))]
)
print(image_files)

#Build a class for the Menu Item
class MenuItem(BaseModel):
    CategoryTitleDefault: str = ""
    SubCategoryTitleDefault: str = ""
    ItemNameDefault: str = ""
    ItemDescriptionDefault: str = ""
    ItemPrice: str = ""

#Extract the columns
COLUMNS = list(MenuItem.model_fields.keys())

#Build a Payload Class
class MenuPayLoad(BaseModel):
    items: list[MenuItem]

#Define the System Prompt
system_prompt = """
You convert menu images in to a structured Excel-ready dataset with EXACTLY these 5 columns.

Rules:
- Each row is one time.
- Leave fields as "" if unknown or not shown.
- Append only; do not remove anything.
- Output ONLY JSON that matches the schema exactly.

Columns and Limits:
- CategoryTitleDefault: text, max 30 chars
- SubCategoryTitleDefault: text, max 30 chars ("" if none)
- ItemNameDefault : text, max 40 chars
- ItemDescriptionDefault : text, max 300 chars ("" if none)
- ItemPrice : decimal number as text, no currency symbol (e.g., "2.50" or "2,50")
"""

#Test the API call with 1 image
image_url = encode_image(os.path.join(IMAGE_DIR, image_files[0]))
response = client.responses.parse(
    model = MODEL,
    instructions = system_prompt,
    input = [
        {
            "role": "user",
            "content": [
                { "type": "input_text", "text": "Extract the menu items from this image. Output must match the schema." },
                { "type": "input_image", "image_url": image_url }
            ]
        }
    ],
    text_format = MenuPayLoad
)
print(response)