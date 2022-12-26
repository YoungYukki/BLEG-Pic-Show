import sqlite3
import requests
import re
from bs4 import BeautifulSoup

headers = {
    'Cookie':'d294f_cloudClientUid=53545049; d294f_ck_info=/	; d294f_jobpop=1; d294f_threadlog=,21,; d294f_winduser=Vg9XAFBSaABUBgFSBglXDFwBXABUVgNbUwVTAgFTVwkADQEAXAECOQ; Hm_lvt_b1f830da76c7d98514b0cc042e6ab7ed=1671539346; d294f_readlog=,38787,38835,38800,38794,36987,37068,37067,25300,37591,37777,; d294f_lastpos=other; d294f_lastvisit=0	1671774492	/simple/index.php?t188.html; d294f_ol_offset=21728; d294f_ipstate=1671774492',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'
}

def get_html():
    res = requests.get(url='http://www.itokoo.com/simple/?t188.html', headers=headers)
    text = res.content.decode('gbk')
    return text

def parser(text:str):
    pattern = re.compile('\[Beautyleg\].*')
    soup = BeautifulSoup(text, 'html.parser')
    rows = soup.find_all(name='a', text=pattern)
    number_pattern = re.compile('(?<=No\.)[0-9]{1,4}')
    for row in rows:
        row_text = str(row)
        number = number_pattern.search(row_text).group()
        name_pattern_text = f'(?<=No.{number}\s)\w*'
        name_pattern = re.compile(name_pattern_text)
        name = name_pattern.search(row_text).group()
        record(name=name, number=number)
    database.commit()

def record(name:str, number:str):
    name = name.lower().capitalize()
    if bool(cursor.execute(f'SELECT * FROM IMAGE WHERE number={number};').fetchall()):
        pass
    else:
        cursor.execute(f'INSERT INTO IMAGE(number, name) VALUES({number},"{name}");')
        print(f'No.{number}-{name}录入')


if __name__ == '__main__':
    database = sqlite3.connect('Beautyleg.db')
    cursor = database.cursor()
    text = get_html()
    parser(text)
    