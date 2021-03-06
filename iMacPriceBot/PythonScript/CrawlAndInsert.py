import sys
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql

URL_KR = "https://www.apple.com/kr/shop/buy-mac/imac"
HTML_BODY_KR = BeautifulSoup(urlopen(URL_KR).read(), "html.parser")
URL_JP = "https://www.apple.com/jp/shop/buy-mac/imac"
HTML_BODY_JP = BeautifulSoup(urlopen(URL_JP).read(), "html.parser")

IMAC_SPEC_LIST = []

URL_CURRNCY_RATE = "https://api.manana.kr/exchange/rate.json"
CURRNCY_RATE_JSON = str(urlopen(URL_CURRNCY_RATE).read().decode('utf8'))
JSON_LIST = json.loads(CURRNCY_RATE_JSON)


def get_imac_spec_kr():
    for dom_element in HTML_BODY_KR.find_all('ul', {'class': "as-macbundle-modelspecs"}):
        dom_element_text = dom_element.text
        dom_element_text_list = dom_element_text.split('\n')
        del dom_element_text_list[7]
        del dom_element_text_list[6]
        del dom_element_text_list[3]
        del dom_element_text_list[0]

        idx = 0
        while idx < len(dom_element_text_list):
            dom_element_text_list[idx] = dom_element_text_list[idx].replace(' 프로세서', '')
            dom_element_text_list[idx] = dom_element_text_list[idx].replace('Boost ', 'Boost')
            dom_element_text_list[idx] = dom_element_text_list[idx].replace(' 드라이브1', '')
            dom_element_text_list[idx] = dom_element_text_list[idx].replace(' 드라이브 1', '')
            dom_element_text_list[idx] = dom_element_text_list[idx].replace(' Drive1', 'Drive')
            dom_element_text_list[idx] = dom_element_text_list[idx].replace(' Drive 1', 'Drive')
            dom_element_text_list[idx] = dom_element_text_list[idx].replace(' 비디오 메모리', '')
            idx += 1

        IMAC_SPEC_LIST.append(dom_element_text_list)


def get_imac_price_kr():
    i = 0
    for dom_element in HTML_BODY_KR.find_all('span', {'class': "current_price"}):
        dom_element_text = dom_element.text
        dom_element_text = dom_element_text.replace('￦', '')
        dom_element_text = dom_element_text.replace(' ', '')
        dom_element_text = dom_element_text.replace('\n', '')
        dom_element_text = dom_element_text.replace(',', '')
        IMAC_SPEC_LIST[i].append(dom_element_text)
        i += 1


def get_imac_price_jp():
    i = 0
    for dom_element in HTML_BODY_JP.find_all('span', {'class': "current_price"}):
        dom_element_text = dom_element.text
        dom_element_text = dom_element_text.replace('￥', '')
        dom_element_text = dom_element_text.replace('(税別)', '')
        dom_element_text = dom_element_text.replace(' ', '')
        dom_element_text = dom_element_text.replace('\n', '')
        dom_element_text = dom_element_text.replace(',', '')
        IMAC_SPEC_LIST[i].append(dom_element_text)
        i += 1


def get_jpy_rate():
    for json_line in JSON_LIST:
        if json_line['name'] == "JPYKRW=X":
            rate = round(float(json_line['rate']), 2)
            return rate


def attatch_rate(rate):
    executor = get_executor()
    for spec_line in IMAC_SPEC_LIST:
        spec_line.append(str(rate))
        spec_line.append(str(int(spec_line[5]) * rate))
        spec_line.append(executor)


def insert_spec_and_price():
    db_conn_info = open("./db_conn_info.cfg", 'r')
    
    db_conn_info_lines = db_conn_info.readlines()
    db_conn_info_user = db_conn_info_lines[0][:-1]
    db_conn_info_password = db_conn_info_lines[1]

    conn = pymysql.connect(host='localhost'
                           , user=db_conn_info_user
                           , password=db_conn_info_password
                           , db='imacpricebot'
                           , charset='utf8')
    curs = conn.cursor()
    curs.execute("select ifnull(max(cwral_seq), '0') from imac_spec_prc")
    rows = curs.fetchall()

    new_cwral_seq = str(int(rows[0][0]) + 1)

    for idx, val in enumerate(IMAC_SPEC_LIST):
        insert_qry = get_insert_qry_line(new_cwral_seq, idx, val)
        insert_result = curs.execute(insert_qry)
        print(insert_qry)
        print(insert_result)

    conn.commit()
    conn.close()


def get_insert_qry_line(cwral_seq, idx, val):
    model_type = idx + 1
    str_list = []
    str_list.append("insert into imac_spec_prc "
                    + "(cwral_seq,model_type"
                    + ",cpu_default,cpu_max,hdd,graphic,prc_krw,prc_jpy,crrency_rate,converted_prc"
                    + ",executor)"
                    + " values ('" + cwral_seq + "', '" + str(model_type) + "', '")
    for value in val:
        str_list.append(value + "', '")
    str_list[9] = str_list[9][0:-3]
    str_list.append(');')
    return ''.join(str_list)


def get_executor():
    num_of_args = len(sys.argv)
    if num_of_args <= 1:
        return 'tester'
    else:
        return sys.argv[1]


if __name__ == '__main__':
    get_imac_spec_kr()
    get_imac_price_kr()
    get_imac_price_jp()
    rate = get_jpy_rate()
    attatch_rate(rate)

    insert_spec_and_price()
