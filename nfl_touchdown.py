import requests
from bs4 import BeautifulSoup

def scrape_nfl_touchdown():

    URL = "https://www.cbssports.com/nfl/stats/player/scoring/nfl/regular/qualifiers/"

    try:
        print(f"Fetching data from: {URL}\n")
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the URL: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    table_body = soup.find('tbody')

    if not table_body:
        print("Could not find the main statistics table body on the page.")
        return

    player_stats = []

    for row in table_body.find_all('tr'):
        cols = row.find_all('td')

        try:
            player_info_element = cols[0].find('a')
            
            if not player_info_element:
                continue
            player_name = player_info_element.text.strip()
            raw_info = cols[0].text.strip()
            parts = raw_info.split()
            
            player_pos = "N/A"
            player_team = "N/A"
            
            if len(parts) >= 2:
                player_team = parts[-1]  
                player_pos = parts[-2]

            td_columns = [cols[i].text.strip() for i in range(2, 8)]

            def safe_int(stat):
                zero_values = {'—', '-', ''}
                return int(stat) if stat not in zero_values and stat.isdigit() else 0

            rushing_td = safe_int(td_columns[0])
            receiving_td = safe_int(td_columns[1])
            pr_td = safe_int(td_columns[2])
            kr_td = safe_int(td_columns[3])
            intr_td = safe_int(td_columns[4])
            fumr_td = safe_int(td_columns[5])

            total_tds = rushing_td + receiving_td + pr_td + kr_td + intr_td + fumr_td

            player_stats.append({
                'name': player_name,
                'position': player_pos,
                'team': player_team,
                'total_tds': total_tds
            })
        except Exception as e:
            print(f"An unexpected error occurred during parsing: {e}")
            continue

    player_stats.sort(key=lambda x: x['total_tds'], reverse=True)

    print(f"{'Rank':<4} | {'Player':<25} | {'Pos':<5} | {'Team':<4} | {'Total TDs':<9}")
    print("-" * 55)

    for rank, player in enumerate(player_stats[:20], 1):
        print(
            f"{rank:<4} | "
            f"{player['name']:<25} | "
            f"{player['position']:<5} | "
            f"{player['team']:<4} | "
            f"{player['total_tds']:<9}"
        )

if __name__ == "__main__":
    scrape_nfl_touchdown()
