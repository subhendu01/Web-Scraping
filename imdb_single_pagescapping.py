import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
# from requests import get
import requests
import re

headers = {"Accept-Language": "en-US, en;q=0.5"}
url = "https://www.imdb.com/search/title/?groups=top_1000&ref_=adv_prv"
results = requests.get(url, headers=headers)
soup = BeautifulSoup(results.text, "html.parser")

titles = []
years = []
time = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []

movie_div = soup.find_all('div', class_='lister-item mode-advanced')
for container in movie_div:
    name = container.h3.a.text
    titles.append(name)

    year = container.h3.find('span',class_= 'lister-item-year').text
    # start = year.find("(")
    # end = year.find(")")
    # if start != -1 and end != -1:
    #     result = year[start + 1:end]
    #     years.append(result)
    years.append(year)

    #runtime
    runtime = container.find('span', class_='runtime').text if container.p.find('span', class_='runtime') else '_'
    time.append(runtime)

    imdb = float(container.strong.text)
    imdb_ratings.append(imdb)

    m_score = container.find('span', class_='metascore').text if container.find('span', class_='metascore') else '-'
    metascores.append(m_score)

    nv = container.find_all('span', attrs={'name': 'nv'})
    vote = nv[0].text
    votes.append(vote)

    grosses = nv[1].text if len(nv) > 1 else '-'
    us_gross.append(grosses)

movies = pd.DataFrame({
'movie': titles,
'year': years,
'timeMin': time,
'imdb': imdb_ratings,
'metascore': metascores,
'votes': votes,
'us_grossMillions': us_gross
})

movies['year'] = movies['year'].str.extract('(\d+)').astype(int)
movies['timeMin'] = movies['timeMin'].str.extract('(\d+)').astype(int)
movies['metascore'] = movies['metascore'].astype(int)
movies['votes'] = movies['votes'].str.replace(',', '').astype(int)
movies['us_grossMillions'] = movies['us_grossMillions'].map(lambda x: x.lstrip('$').rstrip('M'))
movies['us_grossMillions'] = pd.to_numeric(movies['us_grossMillions'], errors='coerce')
print(movies.to_string())
print(movies.dtypes)
movies.to_csv('movies.csv', index=False)