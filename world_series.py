import requests
from bs4 import BeautifulSoup
import re

def scrape_world_series():
    URL = "https://en.wikipedia.org/wiki/List_of_World_Series_champions"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/124.0.0.0 Safari/537.36'
    }

    try:
        print(f"Fetching data from: {URL}\n")
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the URL: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table', {'class': 'wikitable'})

    if not tables:
        print("Could not find the World Series data table on the page.")
        return

    target_table = None
    for table in tables:
        headers = [th.get_text(strip=True) for th in table.find_all('th')]
        if any("Year" in h for h in headers) and any("Winning team" in h for h in headers):
            target_table = table
            break

    if not target_table:
        print("Target table not found.")
        return

    champions = []

    for row in target_table.find_all('tr')[1:]:
        cols = row.find_all(['td', 'th'])
        if len(cols) < 5:
            continue

        try:
            # Clean year by removing any brackets, footnote numbers, or superscripts
            year = re.sub(r'\[.*?\]', '', cols[0].text.strip())
            year = re.sub(r'[^0-9]', '', year)

            winner = re.sub(r'\[.*?\]', '', cols[1].text.strip().split('(')[0]).strip()
            score = cols[3].text.strip()
            runner_up = re.sub(r'\[.*?\]', '', cols[4].text.strip().split('(')[0]).strip()

            if year and winner:
                champions.append({
                    'Year': year,
                    'Champion': winner,
                    'Score': score,
                    'Runner_Up': runner_up
                })
        except Exception as e:
            print(f"Error parsing row: {e}")
            continue

    print("World Series Results:\n" + "="*45)
    for champ in champions:
        score = champ.get('Score', 'N/A')
        runner_up = champ.get('Runner_Up', 'N/A')
        print(f"{champ['Year']}: {champ['Champion']} ({score}) vs {runner_up}")

if __name__ == "__main__":
    scrape_world_series()