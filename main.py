<<<<<<< HEAD
#import libraries
import io
import os
import base64
import requests
import pandas as pd
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

#Read variables from .env
directory=os.getenv("WORKING_DIRECTORY")
OLLAMA_URL=os.getenv("OLLAMA_URL")
MODEL=os.getenv("MODEL")

#Check the working directory
if not os.path.exists(directory):
    raise ValueError("Working directory does not exist")
os.chdir(directory)

#Columns expected in the output
COLUMNS=[
"CategoryTitleDefault",
"SubcategoryTitleDefault",
"ItemNameDefault",
"ItemDescriptionDefault",
"ItemPrice"
]

#Build a function that converts the image to base64
def encode_image(image_path):
    with Image.open(image_path) as img:
        img.thumbnail((640,640))
        buffer=io.BytesIO()
        img.save(buffer,format="JPEG",quality=90)
        encoded=base64.b64encode(buffer.getvalue()).decode("utf-8")
    return encoded

#Define the system prompt
system_prompt="""
You are extracting menu items from a restaurant menu image.

Extract only real food or drink items that have a visible price.

Ignore:
Restaurant name
Logos
Page titles
Decorative text
Addresses
Phone numbers
Opening hours

Rules:
Each row must represent exactly one menu item.
Do not invent items that are not clearly visible.
Copy item names exactly as written.
Copy descriptions exactly as written.
Copy prices exactly as written.
If no description exists leave it empty.
If no subcategory exists leave it empty.
Stop generating immediately after the last menu item.

Return the result as a pipe-separated table.

The FIRST line MUST be exactly this header:

CategoryTitleDefault|SubcategoryTitleDefault|ItemNameDefault|ItemDescriptionDefault|ItemPrice

Formatting rules:
Use | as separator
Do not add spaces around |
Do not add explanations
Do not add text before the table
Do not add text after the table
Do not add blank lines
"""

#Define function to call the API
def extract_menu_from_image(image_path):
    image_url=encode_image(image_path)
    response=requests.post(
        OLLAMA_URL,
        json={
            "model":MODEL,
            "prompt":system_prompt,
            "images":[image_url],
            "stream":False,
            "options":{
                "num_predict":1200,
                "temperature":0
            }
        },
        timeout=300
    )
    response.raise_for_status()
    result=response.json()
    if "response" not in result:
        raise ValueError(f"Model error -> {result}")
    return result["response"]

#Ask user for image name
image_name=input("Enter image name (without extension): ").strip()

#Detect image extension automatically
image_file=None
for ext in [".jpg",".jpeg",".png"]:
    if os.path.exists(image_name+ext):
        image_file=image_name+ext
        break

if image_file is None:
    raise FileNotFoundError("Image not found (.jpg .jpeg .png supported)")

#Call model
model_output=extract_menu_from_image(image_file)

#Clean output and remove lines before header
lines=model_output.strip().splitlines()
for i,line in enumerate(lines):
    if "CategoryTitleDefault" in line:
        lines=lines[i:]
        break

clean_output="\n".join(lines)

#Convert model output to dataframe
df=pd.read_csv(io.StringIO(clean_output),sep="|",engine="python")

#Manage the columns
df.columns=df.columns.str.strip()
for col in COLUMNS:
    if col not in df.columns:
        df[col]=""
df=df[COLUMNS]

#Save Excel file
=======
#import libraries
import io
import os
import base64
import requests
import pandas as pd
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

#Read variables from .env
directory=os.getenv("WORKING_DIRECTORY")
OLLAMA_URL=os.getenv("OLLAMA_URL")
MODEL=os.getenv("MODEL")

#Check the working directory
if not os.path.exists(directory):
    raise ValueError("Working directory does not exist")
os.chdir(directory)

#Columns expected in the output
COLUMNS=[
"CategoryTitleDefault",
"SubcategoryTitleDefault",
"ItemNameDefault",
"ItemDescriptionDefault",
"ItemPrice"
]

#Build a function that converts the image to base64
def encode_image(image_path):
    with Image.open(image_path) as img:
        img.thumbnail((640,640))
        buffer=io.BytesIO()
        img.save(buffer,format="JPEG",quality=90)
        encoded=base64.b64encode(buffer.getvalue()).decode("utf-8")
    return encoded

#Define the system prompt
system_prompt="""
You are extracting menu items from a restaurant menu image.

Extract only real food or drink items that have a visible price.

Ignore:
Restaurant name
Logos
Page titles
Decorative text
Addresses
Phone numbers
Opening hours

Rules:
Each row must represent exactly one menu item.
Do not invent items that are not clearly visible.
Copy item names exactly as written.
Copy descriptions exactly as written.
Copy prices exactly as written.
If no description exists leave it empty.
If no subcategory exists leave it empty.
Stop generating immediately after the last menu item.

Return the result as a pipe-separated table.

The FIRST line MUST be exactly this header:

CategoryTitleDefault|SubcategoryTitleDefault|ItemNameDefault|ItemDescriptionDefault|ItemPrice

Formatting rules:
Use | as separator
Do not add spaces around |
Do not add explanations
Do not add text before the table
Do not add text after the table
Do not add blank lines
"""

#Define function to call the API
def extract_menu_from_image(image_path):
    image_url=encode_image(image_path)
    response=requests.post(
        OLLAMA_URL,
        json={
            "model":MODEL,
            "prompt":system_prompt,
            "images":[image_url],
            "stream":False,
            "options":{
                "num_predict":1200,
                "temperature":0
            }
        },
        timeout=300
    )
    response.raise_for_status()
    result=response.json()
    if "response" not in result:
        raise ValueError(f"Model error -> {result}")
    return result["response"]

#Ask user for image name
image_name=input("Enter image name (without extension): ").strip()

#Detect image extension automatically
image_file=None
for ext in [".jpg",".jpeg",".png"]:
    if os.path.exists(image_name+ext):
        image_file=image_name+ext
        break

if image_file is None:
    raise FileNotFoundError("Image not found (.jpg .jpeg .png supported)")

#Call model
model_output=extract_menu_from_image(image_file)

#Clean output and remove lines before header
lines=model_output.strip().splitlines()
for i,line in enumerate(lines):
    if "CategoryTitleDefault" in line:
        lines=lines[i:]
        break

clean_output="\n".join(lines)

#Convert model output to dataframe
df=pd.read_csv(io.StringIO(clean_output),sep="|",engine="python")

#Manage the columns
df.columns=df.columns.str.strip()
for col in COLUMNS:
    if col not in df.columns:
        df[col]=""
df=df[COLUMNS]

#Save Excel file
>>>>>>> e1c2c6c2acbd2c21729ca40f5f57c3348694af8b
df.to_excel(f"{image_name}.xlsx",index=False)