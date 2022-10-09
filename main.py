from api_wrapper import TikTokApi

api = TikTokApi()
uid = api.get_user_id("spinflowstar")
print(uid)

followers = api.get_followers(uid)
print(len(followers))

following = api.get_following(uid)
print(len(following))

print(api.request_count)
