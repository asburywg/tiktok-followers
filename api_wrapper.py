import time
from typing import List
import requests as r
from cache import read, append
from constants import API_KEY_DEV, API_KEY_PROD
import logging


USER_CACHE_FILE = "data/user_id_cache.json"
FOLLOWING_CACHE_FILE = "data/following_cache.json"
FOLLOWERS_CACHE_FILE = "data/followers_cache.json"


def init_logging(debug: bool = True, write_file: bool = True, log_file="logs/dev.log"):
    log_level = logging.DEBUG if debug else logging.INFO
    request_logger = logging.getLogger('urllib3')
    request_logger.setLevel(log_level)
    logging.basicConfig(filename=log_file if write_file else None, datefmt='%H:%M:%S', level=log_level,
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')


def parse_users(cache_file, users, enhance):
    mapping = {}
    for user in users:
        mapping[user.get("unique_id")] = {"uid": user.get("id"), "unique_id": user.get("unique_id"),
                                          "region": user.get("region"), "nickname": user.get("nickname"),
                                          "follower_count": user.get("follower_count"),
                                          "total_favorited": user.get("total_favorited"),
                                          "favoriting_count": user.get("favoriting_count"),
                                          "videos_uploaded": user.get("aweme_count"),
                                          "url": f"https://www.tiktok.com/@{user.get('unique_id')}",
                                          **enhance}
    append(cache_file, mapping)
    return mapping.values()


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

    def get_user_id(self, username: str, use_cache: bool = True):
        """
        Return user_id from a TikTok username / user unique_id
        :param username: i.e. tiktok or @tiktok
        :param use_cache: optionally read/write username -> uid key/value to local file to cache result
        :return: user_id
        """
        uid = read(USER_CACHE_FILE, username) if use_cache else None
        if not uid:
            response = self.__get("/user/info", {"unique_id": username})
            uid = response.get("data").get("user").get("id")
            if use_cache:
                append(USER_CACHE_FILE, {username: uid})
        return uid

    def __follow_api(self, api_path: str, cache_file: str, user_id: str, request_epoch: str = None, acc: List = None):
        if acc is None:
            acc = []
        if not request_epoch:
            request_epoch = str(int(time.time()))
        response = self.__get(api_path, {"user_id": user_id, "count": "200", "time": request_epoch})
        data = response.get("data")
        response_epoch, has_more, total = str(data.get("time")), data.get("hasMore"), data.get("total")
        users = data.get("followers") or data.get("followings")
        # parse and enhance user list, cache results of each call
        acc.extend(parse_users(cache_file, users,
                               {"request_epoch": request_epoch, "response_epoch": response_epoch, "total": total}))
        # recursive call until done, return list of users
        if has_more:
            return self.__follow_api(api_path, cache_file, user_id, response_epoch, acc)
        return acc

    def get_followers(self, user_id: str):
        return self.__follow_api("/user/followers", FOLLOWERS_CACHE_FILE, user_id)

    def get_following(self, user_id: str):
        return self.__follow_api("/user/following", FOLLOWING_CACHE_FILE, user_id)
