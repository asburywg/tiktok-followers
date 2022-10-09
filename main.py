from api_wrapper import TikTokApi
import logging
from datetime import datetime
from constants import TIKTOK_USER
from helper import write_csv, format_output

LOG_FILE = "data/logs/prod.log"


def init_logging(debug: bool = True, write_file: bool = True):
    log_level = logging.DEBUG if debug else logging.INFO
    request_logger = logging.getLogger('urllib3')
    request_logger.setLevel(log_level)
    logging.basicConfig(filename=LOG_FILE if write_file else None, datefmt='%H:%M:%S', level=log_level,
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')


def tiktok_followers(username: str, use_cache: bool = True, prod: bool = False):
    api = TikTokApi(production=prod)
    # get user_id from username
    uid = api.get_user_id(username)
    logging.info(f"User ID: {uid} ({username})")
    # get follower list
    followers = api.get_followers(uid, use_cache=use_cache)
    logging.info(f"Followers: {len(followers)}")
    # get following list
    following = api.get_following(uid, use_cache=use_cache)
    logging.info(f"Following: {len(following)}")
    # API requests used
    logging.info(f"{api.request_count} API requests used")
    # sort, format and output followers CSV
    output = format_output(followers, following)
    suffix = datetime.today().strftime('%Y%m%d')
    write_csv(f'./data/output/{username}_{suffix}.csv', output)


def main():
    init_logging()
    tiktok_followers(TIKTOK_USER, use_cache=False, prod=True)


if __name__ == "__main__":
    main()
