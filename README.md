# GPT Menu Reader

Converts photos of restaurant menus into an Excel spreadsheet using the OpenAI Responses API with structured output.

## How it works

1. You enter the name of a folder containing menu images (`.jpg`, `.jpeg`, `.png`).
2. Each image is base64-encoded and sent to the model.
3. The model returns structured JSON that is validated with Pydantic.
4. All items are combined into one table and saved as an `.xlsx` file.

## Output columns

| Column | Description |
|---|---|
| CategoryTitleDefault | Menu category (max 30 chars) |
| SubCategoryTitleDefault | Subcategory, empty if none (max 30 chars) |
| ItemNameDefault | Item name (max 40 chars) |
| ItemDescriptionDefault | Description, empty if none (max 300 chars) |
| ItemPrice | Price as text, no currency symbol |

## Setup

1. Clone the repo and install dependencies:
```bash
   pip install -r requirements.txt
```
2. Create a `.env` file in the project root:
```
   OPENAI_API_KEY=your-key-here
```
3. If you use a restricted API key, set **Responses** permission to allow requests.
4. Put your menu images in a folder next to `main.py`.

## Usage

```bash
python main.py
```

Enter the image folder name and the output Excel file name when prompted.

## Notes

- Never commit `.env`. It is listed in `.gitignore`.
- Menu pages are processed one image per request, so large menus use more tokens.
- Always spot-check extracted prices against the original images.

## Tech

Python, OpenAI API (Responses + structured output), Pydantic, pandas, openpyxl