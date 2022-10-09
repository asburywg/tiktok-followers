from api_wrapper import TikTokApi
import logging
from datetime import datetime
from constants import TIKTOK_USER
from helper import write_csv, format_output


def tiktok_followers(username: str):
    api = TikTokApi()
    # get user_id from username
    uid = api.get_user_id(username)
    logging.info(f"User ID: {uid} ({username})")
    # get follower list
    followers = api.get_followers(uid)
    logging.info(f"Followers: {len(followers)}")
    # get following list
    following = api.get_following(uid)
    logging.info(f"Following: {len(following)}")
    # API requests used
    logging.info(f"{api.request_count} API requests used")
    # sort, format and output followers CSV
    output = format_output(followers, following)
    suffix = datetime.today().strftime('%Y%m%d')
    write_csv(f'./data/output/{username}_{suffix}.csv', output)


def main():
    logging.basicConfig(level=logging.INFO)
    tiktok_followers(TIKTOK_USER)


if __name__ == "__main__":
    main()
