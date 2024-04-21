import requests

class UNOGSRequest:
    def __init__(self):
        self.url = "https://unogs-unogs-v1.p.rapidapi.com/search/titles"
        self.headers = {
            "X-RapidAPI-Key": "a5402757a6msh682d9fc7beb97aep1c6e44jsn4c05f2d6efd4",
            "X-RapidAPI-Host": "unogs-unogs-v1.p.rapidapi.com"
        }

    def make_request(self):
        response = requests.get(self.url, headers=self.headers)
        return response.json()

# Protocol for accessing the UNOGSRequest class in other files
class UNOGSRequestProtocol:
    def __init__(self):
        self.unogs_request = UNOGSRequest()

    def get_data(self):
        return self.unogs_request.make_request()
