"""
작성자 : 박현준
작성일 : 2022.03.09.
수정일 : 2022.03.09.

파일 설명
지수 전체를 DB에 저장하는 것은 비효율적이라 생각.
txt 파일에 필요한 정보만 저장하도록 변경.
지수 전체 저장하는 것은 RSI 낮은 주식 서칭하는 프로그램 만들 때 참고 하기 위해 지우지 않음.
"""
# 별도의 파일을 만들어 pymysql 인증
import pymysql_auth
import pymysql

con = pymysql_auth.con


# 초기 실행 시 테이블 생성
def create_table():
    cur = con.cursor(pymysql.cursors.DictCursor)
    table_names = ['canary', 'attack', 'defensive']
    for table_name in table_names:
        sql = f"""
        CREATE TABLE IF NOT EXISTS `{table_name}` (
        `ID` BIGINT PRIMARY KEY AUTO_INCREMENT,
        `Date` DATE NOT NULL,
        `Ticker` VARCHAR(5) NOT NULL,
        `Momentum` FLOAT(5,2) NOT NULL,
        `Perf_Month` FLOAT(4,2) NOT NULL,
        `Perf_Quarter` FLOAT(4,2) NOT NULL,
        `Perf_Half_Y` FLOAT(4,2) NOT NULL,
        `Perf_Year` FLOAT(4,2) NOT NULL        
        );
        """
        cur.execute(sql)

    sql = f"""
            CREATE TABLE IF NOT EXISTS `portfolio` (
            `ID` BIGINT PRIMARY KEY AUTO_INCREMENT,
            `Date` DATE NOT NULL,
            `Type` VARCHAR(5) NOT NULL,
            `Ticker` VARCHAR(5) NOT NULL,
            `Ratio` FLOAT(5,2) NOT NULL        
            );
            """
    cur.execute(sql)

    con.commit()
    con.close()


def insert_momentum():
    pass


def insert_portfolio():
    pass


def update_momentum():
    pass


def update_portfolio():
    pass


class Momentum:
    pass


class Portfolio:
    pass
