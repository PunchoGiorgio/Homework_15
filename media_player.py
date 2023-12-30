import requests


class Player:
    def __init__(self, video_link=None, full_movie=None, exist_movie=None):
        self.video_link = video_link
        self.full_movie = full_movie
        self.exist_movie = exist_movie

    def check_link(self):
        req = requests.get(self.video_link)

        if req.status_code == 200:
            return 'The link is correct'

    def full_movie_by_title(self):
        url = "https://youtube-v2.p.rapidapi.com/search/"

        querystring = {"query": self.full_movie}

        headers = {
            "X-RapidAPI-Key": "5eec186a63msh5331489a8cd1e42p17e80ajsn8eb371963c9c",
            "X-RapidAPI-Host": "youtube-v2.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        for i in response.json()['videos']:
            if len(str(i['video_length'])) == 7 and int(str(i['video_length'])[0]) >= 1:
                return 'https://www.youtube.com/watch?v=' + i['video_id']
            else:
                return 'There is no full version of this movie on YouTube'

    def film_presence(self):
        url = "https://netflix54.p.rapidapi.com/search/"

        querystring = {"query": self.exist_movie}

        headers = {
            "X-RapidAPI-Key": "5eec186a63msh5331489a8cd1e42p17e80ajsn8eb371963c9c",
            "X-RapidAPI-Host": "netflix54.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        for k in response.json()['suggestions']:
            if len(self.exist_movie) == len(k['summary']['name']):
                return f"A movie '{k['summary']['name']}' was found on Netflix, {k['summary']['entityId']}"
            else:
                return 'No such movie on Netflix'


obj = Player("https://youtube.com.ua", "class of 1999", "quiet cool")
print(obj.check_link())
print(obj.full_movie_by_title())
print(obj.film_presence())
