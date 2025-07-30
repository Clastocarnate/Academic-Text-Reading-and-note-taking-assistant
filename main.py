
import json
import requests
import pyperclip
from keys import NOTION_API_ENDPOINT, NOTION_HEADERS


def get_page_children(page_id):
    url = f"{NOTION_API_ENDPOINT}/blocks/{page_id}/children"
    response = requests.get(url, headers=NOTION_HEADERS)
    return response.json()

parent_page_id = "238e239edbf8806b94cfea32d8da9ca0"
print(get_page_children(parent_page_id))

text = pyperclip.paste()