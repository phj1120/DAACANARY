"""
작성자 : 박현준
작성일 : 2022.03.09.
수정일 : 2022.04.16.

파일 설명
DAA 카나리아 신호를 계산해서 Slack 으로 전송.
당일 계산 결과를 log/DAA.txt 에 저장해 변경 여부를 확인 한다.
윈도우 작업 스케줄러를 이용해 노트북이 켜질 때 마다 실행 되도록 하였다.

Slack 에 메시지를 전송하기 위해서는 Slack Bot Token 값 만 담겨있는 key.txt 파일이 필요하다.
"""

from bs4 import BeautifulSoup
from datetime import datetime
import requests


# slack 정보 세팅
def get_key():
    f = open('key.txt', 'r')
    key = f.readline()
    f.close()
    return key


token = get_key()
channel = "#daa"
log_path = f'log/DAA.txt'


# txt 파일 쓰기
def txt_write(path, msg):
    f = open(path, 'a', encoding='utf-8')
    f.write(f'{msg}\n')
    f.close()


# txt 파일 읽기
def txt_read(path):
    f = open(path, 'r', encoding='utf-8')
    lines = f.readlines()
    return lines


# Slack 에 전송
def print_and_log(msg):
    print(msg)
    txt_write(log_path, msg)


def print_and_post(msg):
    print(msg)
    response = requests.post("https://slack.com/api/chat.postMessage",
                             headers={"Authorization": "Bearer " + token},
                             data={"channel": channel, "text": msg}
                             )


def print_and_post_and_log(msg):
    print(msg)

    response = requests.post("https://slack.com/api/chat.postMessage",
                             headers={"Authorization": "Bearer " + token},
                             data={"channel": channel, "text": msg}
                             )
    txt_write(log_path, msg)


# Ticker로 지수 조회해 map 반환
def get_jisu(code):
    map = {}
    tmp = []
    try:
        page_url = f'https://finviz.com/quote.ashx?t={code}'
        page_res = requests.get(page_url, headers={'User-Agent': 'Mozilla/5.0'})
        page_soup = BeautifulSoup(page_res.text, "html.parser")
        # trs = page_soup.select('body > div:nth-child(9) > div > table:nth-child(1)')
        trs = page_soup.select("body > div:nth-child(9)")
        # print(trs)
        for tr in trs:
            if tr.find('b'):
                name = tr.find('b').text
            elif len(tr.find_all('td')) == 6:
                name = tr.find_all('td')[2].text
            else:
                name = ''

        map['Ticker'] = code
        map['Name'] = name.replace("\'", "", ).replace("\"", "")

        trs = page_soup.find('table', class_='snapshot-table2').find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            # print(tds)
            for td in tds:
                td.find_all('td')
                tmp.append(td.text)

        cnt = int(len(tds) * len(trs) / 2)
        for idx in range(cnt):
            map[tmp[2 * idx]] = tmp[2 * idx + 1]
    except:
        pass
    return map


# ticker 를 이용해 최근 수익를 반환
def recent_return_rate(ticker):
    # (1개월 * 12) + (3개월 * 4) + (6개월 *2) + (12개월*1)
    DAA_info = get_jisu(ticker)
    Perf_Month = float(DAA_info['Perf Month'].replace('%', ''))
    Perf_Quarter = float(DAA_info['Perf Quarter'].replace('%', ''))
    Perf_Half_Y = float(DAA_info['Perf Half Y'].replace('%', ''))
    Perf_Year = float(DAA_info['Perf Year'].replace('%', ''))

    canary = (Perf_Month * 12) + (Perf_Quarter * 4) + (Perf_Half_Y * 2) + (Perf_Year * 1)
    # print(f'\n{ticker} : {"부정" if canary<0 else "긍정"}  : {canary}')
    print(f'{ticker} 1개월 : {Perf_Month} / 3개월 : {Perf_Quarter} / 6개월 : {Perf_Half_Y} / 12개월 : {Perf_Year} ')
    return canary


canary_assets_ticker = ['VWO', 'BND']
attack_assets_ticker = ['SPY', 'IWM', 'QQQ', 'VGK', 'EWJ', 'VWO', 'VNQ', 'GSG', 'GLD', 'TLT', 'HYG', 'LQD']
defensive_assets_ticker = ['SHY', 'IEF', 'LQD']

'''
사야할 주식 ticker를 딕셔너리로 반환
나중에 DB에 넣으면 편하게 될 것 같은데 일단 txt로...
'''


def portfolio(canary_assets_ticker, attack_assets_ticker, defensive_assets_ticker):
    canary_assets = {}
    attack_assets = {}
    defensive_assets = {}
    for asset in attack_assets_ticker:
        attack_assets[asset] = recent_return_rate(asset)
    for asset in defensive_assets_ticker:
        defensive_assets[asset] = recent_return_rate(asset)
    for asset in canary_assets_ticker:
        canary_assets[asset] = recent_return_rate(asset)
    # print(canary_assets)
    # print(attack_assets)
    # print(defensive_assets)

    attack_assets_sort = sorted(attack_assets.items(), key=lambda item: item[1], reverse=False)
    defensive_assets_sort = sorted(defensive_assets.items(), key=lambda item: item[1], reverse=True)

    print(f'카나리아 신호  : {canary_assets}')
    print(f'공격 자산 : {attack_assets_sort}')
    print(f'방어 자산 : {defensive_assets_sort}')

    date = datetime.today().strftime("%Y%m%d")
    print_and_log(f'\n{date}')

    result = {}
    if canary_assets['BND'] >= 0 and canary_assets['VWO'] >= 0:
        print_and_log('공격 자산 : 100 %')
        print_and_log(f'{attack_assets_sort[-1][0]}')
        print_and_log('방어 자산  : 0 %')
        print_and_log(f'')
        result['attack'] = attack_assets_sort[-1][0]
        result['defensive'] = ''

    elif canary_assets['BND'] >= 0 or canary_assets['VWO'] >= 0:
        print_and_log('공격 자산 : 50 %')
        print_and_log(f'{attack_assets_sort[-1][0]}')
        print_and_log('방어 자산  : 50 %')
        print_and_log(f'{defensive_assets_sort[0][0]}')
        result['attack'] = attack_assets_sort[-1][0]
        result['defensive'] = defensive_assets_sort[0][0]
    else:
        # canary_assets['BND'] < 0 and canary_assets['VWO'] < 0:
        print_and_log('공격 자산 : 0 %')
        print_and_log(f'')
        print_and_log('방어 자산  : 100 %')
        print_and_log(f'{defensive_assets_sort[0][0]}')
        result['attack'] = ''
        result['defensive'] = defensive_assets_sort[0][0]
    return result


# print_and_post(str(portfolio(canary_assets_ticker, attack_assets_ticker, defensive_assets_ticker)))
print(portfolio(canary_assets_ticker, attack_assets_ticker, defensive_assets_ticker))

logs = txt_read(log_path)

for idx, log in enumerate(logs):
    date = datetime.today().strftime("%Y%m%d")
    if date in log:
        today = logs[idx + 1:idx + 5]
        yesterday = logs[idx - 5:idx - 1]
        if today != yesterday:
            print_and_post(f'{date} 변경 발생')
            for index, msg in enumerate(today):
                print_and_post(msg)
        # else:
        #     print("특이사항 없음")
