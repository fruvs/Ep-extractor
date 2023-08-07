import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def get_anime_page_url(anime_name):
    search_url = f"https://anilist.co/search/anime?search={quote(anime_name)}"
    response = requests.get(search_url)
    if response.status_code != 200:
        print(f"Failed to retrieve search results for {anime_name}. Status code: {response.status_code}")
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    anime_titles = soup.select(".media-card a.title")
    for title in anime_titles:
        if anime_name.lower() in title.text.lower():
            detail_url = "https://anilist.co" + title['href']
            return detail_url

    print(f"No search results found for {anime_name}.")
    return None

def get_anime_info(anime_page_url):
    response = requests.get(anime_page_url)

    if response.status_code != 200:
        print(f"Failed to retrieve anime page. Status code: {response.status_code}")
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    countdown_element = soup.find("div", class_="countdown el-tooltip value")

    if countdown_element:
        countdown_info = countdown_element.get_text(strip=True)
        ep_count = countdown_info.split(":")[0].strip()
        return ep_count
    else:
        print("Countdown element not found.")
        return None

anime_name = input("Enter the anime name: ").strip()
anime_page_url = get_anime_page_url(anime_name)

if anime_page_url:
    print(f"URL for {anime_name}: {anime_page_url}")
    ep_count = get_anime_info(anime_page_url)
    if ep_count:
        print(f"Episode Count: {ep_count}")
else:
    print(f"Could not find URL for {anime_name}")
