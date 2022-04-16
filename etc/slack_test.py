"""
작성자 : 박현준
작성일 : 2022.03.09.
수정일 : 2022.03.09.

파일 설명
Slack 메시지 전송 테스트
"""
import requests


def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
                             headers={"Authorization": "Bearer " + token},
                             data={"channel": channel, "text": text}
                             )
    print(response)


def get_key():
    f = open('../key.txt', 'r')
    str = f.readline()
    f.close()
    return str


myToken = get_key()

post_message(myToken, "#daa", "test")
