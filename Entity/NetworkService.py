import requests


class UNOGSRequest:
    def __init__(self):
        self.url = "https://kinopoiskapiunofficial.tech/api/v2.2/films/collections?type=TOP_POPULAR_ALL&page=1"
        self.headers = {"accept": "application/json",
                        "X-API-KEY": "d4348626-8046-4ca8-945d-44838d1aecdc"}

    def make_request(self):
        response = requests.get(self.url, headers=self.headers)
        return response.json()


# Protocol for accessing the UNOGSRequest class in other files
class UNOGSRequestProtocol:
    def __init__(self):
        self.unogs_request = UNOGSRequest()

    def get_data(self):
        return self.unogs_request.make_request()
