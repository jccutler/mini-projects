import requests
import re
from bs4 import BeautifulSoup

HEADERS = {
    'Content-Type': 'application/json',
    'Referer' : 'https://www.google.com',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
}

def scrape_id(url, artist_list_path):
    response = requests.get(url, headers=HEADERS)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    target_script = soup.find('script', {'id': '__NEXT_DATA__'})
    if target_script:
        script_content = target_script.text
        # Search for artist id using regular expressions
        match = re.search(r'"artist\({\\"id\\":\\"(\d+)\\"}\)"', script_content)
        if match:
            artist_id = match.group(1)
            print(f'Found artist ID: {artist_id}')
            write_id(artist_id, artist_list_path)
        else:
            print("Artist ID not found.")
    else:
        print("GraphQL query script not found")

def write_id(artist_id, artist_list_path):
    with open(artist_list_path, 'a') as file:
        file.write(f'{artist_id}')
