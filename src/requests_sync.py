import requests
import logging


class RequestsSync:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def send_request(
        self, endpoint: str = "", method: str = "GET", params: dict = None
    ):
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.request(method=method, url=url, params=params)
            logging.info(f"successful call: {response.status_code}")
            return response.json()
        except requests.exceptions.RequestException as e:
            return logging.error(f"failed call: {e}")
