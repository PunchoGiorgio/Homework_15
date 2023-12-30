from bs4 import BeautifulSoup
from pathlib import Path
import requests
import imdb
import os
import string
import json

for letter in string.ascii_uppercase:
    os.makedirs('{}/{}'.format('film_storage', letter), exist_ok=True)


class Film:

    def __init__(self, mov_title, storage_address=None):
        self.mov_title = mov_title
        self.storage_address = storage_address

    def movie_id_search(self):
        url_rapid = "https://imdb8.p.rapidapi.com/auto-complete"

        querystring = {"q": self.mov_title}

        headers = {
            "X-RapidAPI-Key": "5eec186a63msh5331489a8cd1e42p17e80ajsn8eb371963c9c",
            "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
        }

        response = requests.get(url_rapid, headers=headers, params=querystring)

        film_id = response.json()['d'][0]['id']

        return film_id

    def genre_movie(self):
        ia = imdb.IMDb()
        code = f"{obj.movie_id_search()[2:]}"
        series = ia.get_movie(code)
        genre = series.data['genres']
        return genre

    def plot_summary(self):
        ia = imdb.IMDb()
        code = f"{obj.movie_id_search()[2:]}"
        series = ia.get_movie(code)
        plot = series.data['plot']
        return plot

    def main_cast_movie(self):
        url = f'https://www.imdb.com/title/{obj.movie_id_search()}/fullcredits/?ref_=tt_cl_sm'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        all_cast_1 = soup.findAll('tr', class_="odd")

        data_1 = []
        for i in all_cast_1:
            link = i.find('td', class_="primary_photo").find('img').get('title')
            data_1.append(link)

        all_cast_2 = soup.findAll('tr', class_="even")

        data_2 = []
        for k in all_cast_2:
            link = k.find('td', class_="primary_photo").find('img').get('title')
            data_2.append(link)

        result = [result for x in zip(data_1[:5], data_2[:5]) for result in x]
        return result

    def save_data(self):
        list_keys = ['Movie title', 'Genre', 'Description', 'Main cast']
        list_values = [self.mov_title.title(), obj.genre_movie(), obj.plot_summary(), obj.main_cast_movie()]
        dict_movie = dict(zip(list_keys, list_values))
        json_file = json.dumps(dict_movie)

        for i in list(os.walk(os.getcwd() + '/film_storage'))[1:]:
            if self.mov_title[0].capitalize() == i[0][-1]:
                os.makedirs('{}/{}/{}'.format('film_storage', i[0][-1], self.mov_title.title()), exist_ok=True)

                path_dir = ('{}/{}'.format(i[0], self.mov_title.title()))
                file_obj = Path(path_dir + '/{}.json'.format(self.mov_title))
                file_obj.touch()
                with open(file_obj, 'w', encoding='UTF-8') as f:
                    f.write(json_file)

    def upload_file(self):
        for p in list(os.walk(os.getcwd() + '/film_storage'))[1:]:
            if self.mov_title[0].capitalize() == p[0][-1]:
                path_dir = ('{}/{}'.format(p[0], self.mov_title.title()))
                file_obj = Path(path_dir + '/{}.txt'.format(self.mov_title.title()))
                file_obj.touch()

    def get_film_address(self):
        self.storage_address = '{}/{}/{}'.format('film_storage', self.mov_title.title()[0], self.mov_title.title())
        txt_file = '{}.txt'.format(self.mov_title.title())
        for t in list(os.walk(os.getcwd() + '/film_storage'))[1:]:
            if txt_file in t[2]:
                path_file = '{}/{}'.format(self.storage_address, txt_file)
                full_path = os.path.abspath(path_file)
                return full_path


obj = Film("last action hero")
print('imdb movie id:\n', obj.movie_id_search(), end='\n\n')
print('Genre:\n', obj.genre_movie(), end='\n\n')
print('Description:\n', obj.plot_summary(), end='\n\n')
print('Main cast:\n', obj.main_cast_movie(), end='\n\n')
obj.save_data()
obj.upload_file()
print('Full path to file:\n', obj.get_film_address())
