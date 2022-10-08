import requests as r
from constants import API_KEY_DEV, API_KEY_PROD
import logging


def init_logging(debug: bool = True, write_file: bool = True, log_file="logs/dev.log"):
    log_level = logging.DEBUG if debug else logging.INFO
    request_logger = logging.getLogger('urllib3')
    request_logger.setLevel(log_level)
    logging.basicConfig(filename=log_file if write_file else None, datefmt='%H:%M:%S', level=log_level,
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')


class TikTokApi:
    API_HOST = "tiktok-video-no-watermark2.p.rapidapi.com"

    def __init__(self, production: bool = False):
        init_logging()
        logging.info("Initializing TikTok API")
        self.request_count = 0
        self.headers = {
            "X-RapidAPI-Key": API_KEY_PROD if production else API_KEY_DEV,
            "X-RapidAPI-Host": self.API_HOST
        }

    def __get(self, api_path, parameters):
        res = r.request("GET", f"https://{self.API_HOST}{api_path}", headers=self.headers, params=parameters)
        self.request_count += 1
        res.raise_for_status()
        logging.debug(res.text)
        return res.json()

    def get_user_id(self, username: str):
        """
        Return user_id from a TikTok username / user unique_id
        :param username: i.e. tiktok or @tiktok
        :return: user_id
        """
        response = self.__get("/user/info", {"unique_id": username})
        return response.get("data").get("user").get("id")
