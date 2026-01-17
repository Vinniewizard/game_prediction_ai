import requests
from bs4 import BeautifulSoup
from predictor.models import MatchOdds

def scrape_odds():
    # Example: replace this URL with the actual odds website
    url = "https://www.forebet.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find matches - adjust selectors based on website structure
    matches = soup.find_all('div', class_='match')

    for match in matches:
        home = match.find('span', class_='home').text.strip()
        away = match.find('span', class_='away').text.strip()
        gg_odds = float(match.find('span', class_='gg').text.strip())
        over25_odds = float(match.find('span', class_='over25').text.strip())

        # Save or update GG odds
        MatchOdds.objects.update_or_create(
            home_team=home,
            away_team=away,
            market='GG',
            defaults={'odds': gg_odds, 'source': 'Site1'}
        )

        # Save or update Over 2.5 odds
        MatchOdds.objects.update_or_create(
            home_team=home,
            away_team=away,
            market='Over 2.5',
            defaults={'odds': over25_odds, 'source': 'Site1'}
        )

    print("Odds scraping completed successfully.")

