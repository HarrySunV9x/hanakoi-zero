import json
import requests

from config import llm_config


class HanaChat:
    _instance = None

    CHAT_RECORD_DATABASE_BASE_URL = llm_config.get('CHAT_RECORD_DATABASE_BASE_URL')
    DATABASE_LOGIN_URL = llm_config.get('DATABASE_LOGIN_URL')
    DATABASE_IDENTIFY = llm_config.get('DATABASE_IDENTIFY')
    DATABASE_PASSWORD = llm_config.get('DATABASE_PASSWORD')

    login_username = ''
    headers = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HanaChat, cls).__new__(cls)
        return cls._instance

    # 登录并获取 token
    def login(self):
        response = requests.post(self.DATABASE_LOGIN_URL,
                                 json={"identity": self.DATABASE_IDENTIFY, "password": self.DATABASE_PASSWORD})
        if response.status_code == 200:
            self.login_username = response.json().get("record").get("username")
            return response.json().get("token")  # 返回 token
        else:
            print("Error logging in:", response.status_code, response.text)
            return None

    # 获取全部历史记录
    def get_history(self, hana_chat_username):
        response = requests.get(
            f"{self.CHAT_RECORD_DATABASE_BASE_URL}?filter=(userName='{hana_chat_username}')&sort=-context_id",
            headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if len(response.json().get("items")) == 0:
                return None
            if isinstance(data, dict) and 'records' in data:
                return data['records']
            return data
        else:
            print("Error fetching history:", response.status_code, response.text)
            return None

    # 根据 context_id 获取历史记录
    def get_history_by_context_id(self, hana_chat_context_id):
        response = requests.get(f"{self.CHAT_RECORD_DATABASE_BASE_URL}?filter=(context_id={hana_chat_context_id})",
                                headers=self.headers)
        if response.status_code == 200:
            if len(response.json().get("items")) == 0:
                return None
            data = response.json().get("items")[0].get("id")
            return data
        else:
            print("Error fetching history:", response.status_code, response.text)
            return None

    # 获取详细对话
    def get_conversation(self, hana_chat_context_id):
        response = requests.get(f"{self.CHAT_RECORD_DATABASE_BASE_URL}?filter=(context_id='{hana_chat_context_id}')",
                                headers=self.headers)
        if response.status_code == 200:
            if len(response.json().get("items")) == 0:
                return None
            data = response.json().get("items")[0].get("chathistory")
            return data
        else:
            print("Error fetching conversation:", response.status_code, response.text)
            return None

    def get_max_context_id(self):
        # 获取当前最大 context_id
        history = self.get_history(self.login_username)
        if history and 'items' in history:  # 确保 history 包含 'items'
            items = history['items']
            if items:  # 如果 items 不为空
                max_context_id = max(record['context_id'] for record in items)
                return max_context_id
            else:
                return 0  # 如果没有历史记录，context_id 从 1 开始

    # 写入记录
    def write_record(self, hana_chathistory, new_context_id=None):
        if new_context_id is None:
            new_context_id = self.get_max_context_id() + 1
        if self.get_history_by_context_id(new_context_id) is not None:
            return None
        new_record = {
            "userName": self.login_username,
            "context_id": new_context_id,
            "title": hana_chathistory,
            "chathistory": hana_chathistory
        }

        # 发送 POST 请求
        response = requests.post(self.CHAT_RECORD_DATABASE_BASE_URL, json=new_record, headers=self.headers)
        if response.status_code == 200:
            print("Record written successfully!")
        else:
            print("Error writing record:", response.status_code, response.text)

    def update_record(self, update_id, hana_chathistory):
        new_record = {
            "chathistory": hana_chathistory
        }
        response = requests.patch(f"{self.CHAT_RECORD_DATABASE_BASE_URL}/{update_id}", json=new_record,
                                  headers=self.headers)
        if response.status_code == 200:
            print("Record updated successfully!")
            return response.json()  # 返回更新后的记录
        else:
            print("Error updating record:", response.status_code, response.text)
            return None


def get_hana_chat():
    hana_chat = HanaChat()
    hana_chat.headers = {"Authorization": f"Bearer {hana_chat.login()}"}
    return hana_chat
