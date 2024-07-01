import requests


class Http:

    def request(self, method: str, endpoint: str, json=None):
        base_url = "https://api.spacexdata.com/v4"
        url = base_url + endpoint
        return requests.request(method, url, json=json).json()

    def get(self, method: str, endpoint: str, json=None):
        return self.request(method, endpoint, json)


class SpaceXRequester(Http):
    def request_launches(
        self,
    ):
        return self.get("get", "/launches")
