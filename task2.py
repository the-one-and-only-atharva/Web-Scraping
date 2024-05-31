from requests_html import HTMLSession
import pandas as pd

base_url = 'https://www.scrapethissite.com/pages/forms/'

#Function to scrape
def scrape(url):
    s = HTMLSession()
    r = s.get(url)
    r.html.render(sleep=1)
    
    data = []
    rows = r.html.find('tr')[1:]  #Exclude titles
    for row in rows:
        row_data = {}
        for column, cell in zip(columns, row.find('td')):
            row_data[column] = cell.text
        data.append(row_data)
    
    return data

pagination = {'page_num': 1, 'per_page': 100}

columns = ['name', 'year', 'wins', 'losses', 'ot_losses','win_percent', 'goals_for', 'goals_against', 'plus_minus']

#Scrape data from all pages
teams = []
while True:
    url = base_url + '?' + '&'.join([f'{k}={v}' for k, v in pagination.items()])
    page_data = scrape(url)
    if not page_data:  #End of page
        break
    teams.extend(page_data)
    pagination['page_num'] += 1

df = pd.DataFrame(teams)

df.to_csv('hockey_teams.csv')
