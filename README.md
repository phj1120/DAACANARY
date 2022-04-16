# DAA Canary Slack

## 프로젝트 설명

카나리아 신호를 이용해 투자해야할 자산을 알려주는 Slack 봇 제작

[DAA란?](etc/DAA.md)

## 요구사항 분석

- 카나리아 신호, 공격 자산, 수비 자산의 최근 모멘텀을 계산한다.
- 전날과 비교하여 변경된 사항이 있을 경우 Slack 으로 메시지를 전송한다.
- 메시지에는 해당일, 종목, 비중이 포함 된다.

## 개발 초기 설정

[초기 설정](https://parkhj.notion.site/233f5dd21ef34eb5b71028f89b1ed3ba)

## 한계

자동 매매 까지 구현하고 싶었으나 자동 매매로 해외 ETF 를 구매할 수 있는 방법을 못 찾음

국내 ETF 로도 동일한 전략이 통한다면 국내 ETF 로는 제작 가능함

추후 백테스트를 거쳐 가능하다면 자동 매매까지 구현 해 볼 것

## 추후 수정

### 기능

- 모드1. 이전 날과 투자 자산이 바뀐 경우 Slack 을 통해 메시지를 전송한다.
- 모드2. 이전 달과 투자 자산이 바뀐 경우 Slack 을 통해 메시지를 전송한다.
- 사용자가 원하는 모드를 선택해 사용할 수 있도록 한다.

### DB

- 처음 개발을 시작할 때 DB 설계
- 구현하고자 하는 기능이 간단해 DB 를 쓰는 것은 과하다고 판단
- 추후를 위해 설계한 DB 기록

#### DB 설계

canary

`Date, Ticker, Perf_Month, Perf_Quarter, Perf_Half_Y, Perf_Year, Momentum`

attack

`Date, Ticker, Perf_Month, Perf_Quarter, Perf_Half_Y, Perf_Year, Momentum`

defensive

`Date, Ticker, Perf_Month, Perf_Quarter, Perf_Half_Y, Perf_Year, Momentum`

portfolio

`Date, Type, Ticker, Ratio`

#### DB 를 나눈 이유

하루에 한 번 씩 canary, attack, defensive 테이블에 값을 저장할 예정

저장 후 카나리아 신호를 조회 후 그 신호에 맞게 최근 모멘텀을 확인 할 텐데

이 때 canary, attack, defensive 가 한 테이블에 있으면

1. 자산의 유형을 구분하는데 쿼리 비용 발생
2. 불필요한 데이터 까지 쿼리에 사용

이와 같은 이유로 데이터가 많이 쌓이게 되면 조회가 느려질 것이라 판단해 테이블을 나눴다.
