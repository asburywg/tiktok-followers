from api_wrapper import TikTokApi

api = TikTokApi()
uid = api.get_user_id("spinflowstar")
print(uid)
