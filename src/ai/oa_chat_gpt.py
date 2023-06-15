import os
import openai
import time

from PyQt5.QtCore import pyqtSignal, QThread

from config import SphinxConfig


class ChatGptThread(QThread):
    session_response = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        openai.api_key = SphinxConfig.open_ai_key
        os.environ["http_proxy"] = SphinxConfig.open_ai_proxy
        os.environ["https_proxy"] = SphinxConfig.open_ai_proxy

        self.in_conversation = True
        self.session_content = ''
        self.conversation = [{"role": "system", "content": "你现在是很有用的助手！"}]

    def run(self) -> None:
        while self.in_conversation:
            if not self.session_content:
                time.sleep(0.1)
                continue
            self.conversation.append({"role": "user", "content": self.session_content})
            answer = generate_answer(self.conversation)

            self.conversation.append({"role": "assistant", "content": answer})
            self.session_response.emit(answer)
            self.session_content = ''

    def handle_session(self, content: str) -> None:
        self.session_content = content


# openai.api_key = "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"
# os.environ["http_proxy"] = "http://127.0.0.1:15732"
# os.environ["https_proxy"] = "http://127.0.0.1:15732"
#
# # 单轮对话调用
# # model可选"gpt-3.5-turbo"与"gpt-3.5-turbo-0301"
def generate_answer(messages):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )
    res_msg = completion.choices[0].message
    print(res_msg)
    return res_msg["content"].strip()

#
# if __name__ == '__main__':
#     # 维护一个列表用于存储多轮对话的信息
#     messages = [{"role": "system", "content": "你现在是很有用的助手！"}]
#     while True:
#         prompt = input("请输入你的问题:")
#         messages.append({"role": "user", "content": prompt})
#         res_msg = generate_answer(messages)
#         messages.append({"role": "assistant", "content": res_msg})
#         print(res_msg)