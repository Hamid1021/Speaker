# import requests

# url = 'https://example.com/api'

# files = {
#     'file': ('filename.txt', open('filename.txt', 'rb'), 'text/plain')
# }

# data = {
#     'param1': 'value1',
#     'param2': 'value2'
# }

# response = requests.post(url, files=files, data=data)
# print(response.text)

from application.Entities.channel_message_model import ChannelMessage, ChatUser, FromUser
from requests import post
import json
from application.utils import convert_unix_to_jalali

# سخنرانی های دریافت شده 10237508
# اطلاع رسانی سخنرانی به سخنرانان 10237460

def send_message_to_channel(
        METHOD_NAME="sendMessage", CHAT_ID="", TITILE="بدون عنوان", TEXT="", *args, **kwargs):
    """
    METHOD_NAME : getMe, sendMessage, sendDocument
    CHAT_ID : سخنرانی های دریافت شده 10237508 | اطلاع رسانی سخنرانی به سخنرانان 10237460
    TITILE: str
    TEXT: str
    disable_notification: int value 1 equal "send without notification"
    reply_to_message_id: int
    pin: int value 1 equal "message pinned"
    viewCountForDelete: int "Delete Message When Reach View Count"
    """
    TOKEN = "bot323348:2fc9fd85-3d00-48ef-8b89-e5908b6803a2"
    METHODS = {
        "getMe":"getMe",
        "sendMessage":"sendMessage",
        "sendDocument":"sendDocument",
    }
    base_url = f"https://eitaayar.ir/api/{TOKEN}/{METHODS[METHOD_NAME]}"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'chat_id': CHAT_ID,
        'title': TITILE,
        'text': TEXT,
    }
    if kwargs.get("disable_notification"):
        data["disable_notification"] = kwargs.get("disable_notification")
    if kwargs.get("reply_to_message_id"):
        data["reply_to_message_id"] = kwargs.get("reply_to_message_id")
    if kwargs.get("pin"):
        data["pin"] = kwargs.get("pin")
    if kwargs.get("viewCountForDelete"):
        data["viewCountForDelete"] = kwargs.get("viewCountForDelete")

    response = post(base_url, data=json.dumps(data), headers=headers)
    result = json.loads(response.content)

    if result['ok'] == True:
        try:
            from_id = result["result"]["from"]["id"]
            from_user, from_user_status = FromUser.objects.get_or_create(m_id = from_id)
            if not from_user_status:
                from_user.is_bot = result["result"]["from"]["is_bot"]
                from_user.first_name = result["result"]["from"]["first_name"]
                from_user.last_name = result["result"]["from"]["last_name"]
                from_user.username = result["result"]["from"]["username"]
                from_user.can_join_groups = result["result"]["from"]["can_join_groups"]
                from_user.can_read_all_group_messages = result["result"]["from"]["can_read_all_group_messages"]
                from_user.supports_inline_queries = result["result"]["from"]["supports_inline_queries"]
                from_user.save()
            
            chat_id = result["result"]["chat"]["id"]
            chat_user, chat_user_status = ChatUser.objects.get_or_create(m_id = chat_id)
            if not chat_user_status:
                chat_user.username = result["result"]["chat"]["username"]
                chat_user.m_type = result["result"]["chat"]["type"]
                chat_user.save()

            c_message = ChannelMessage.objects.create(
                message_id = result["result"]["message_id"],
                date = result["result"]["date"],
                text = result["result"]["text"],
                status = "s" if result["ok"] else "us",
                from_user = from_user, 
                chat_user = chat_user,
            )
            return c_message, True
        except Exception as ee:
            return None, False
    else:
        return None, False
    

# def edit_message_from_channel(message_id, new_text, new_title="بدون عنوان", unix_time=0):
#     url = f'https://eitaayar.ir/admin/message/{message_id}'
#     token = '291b8ecb7ddc108eb74589c9bf517af2'
#     headers = {
#         'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryzi4MEFYQMl2Xe10r',
#         'cookie': 'SESSIONID=78da2d8fc77100510c425b520ee5287cf55f82d76373e1c40310fe44ff1e332e2ff2a6acddd68d3c76163bc20570f9c1b4e0cb8c2e39f3d9c1bed7da80a06a29136e0c297271025789499149c8314a8caf3b159faf0b8e71f66e148953f03823e3c793b80f48c4758fd58afa71bc11e1a97514e66f8a79ba1914418da6856b1d6d7b4c488635e97d3dcccd6b93128c1a32489e1c0472e0fab2fa37fe158c5769c1de3be96d3dcefa7e86c20759cf1eab2e350b455fd9d16bf901a071559f'
#     }
#     jalali_date_time = convert_unix_to_jalali(unix_time)
#     data = {
#         '___TOKEN_FORM___': token,
#         'title': f'{new_title}',
#         'text': f'''{new_text}''',
#         'datetimeSend': jalali_date_time,
#         'state': 'sending',
#         'm_dateTimeDelete': '',
#         'd_dateTimeDelete': '',
#         'h_dateTimeDelete': '',
#         'i_dateTimeDelete': '',
#         'pin': '',
#         'viewCountForDelete': ''
#     }
#     try:
#         response = post(url, headers=headers, data=data)
#         print("status", response.status_code)
#         return True
#     except Exception as err:
#         return False
