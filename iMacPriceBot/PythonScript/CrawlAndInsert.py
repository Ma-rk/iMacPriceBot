import json
from urllib.request import urlopen
from bs4 import BeautifulSoup

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
            rate = float(json_line['rate'])
            return rate

def attatch_rate(rate):
    for spec_line in IMAC_SPEC_LIST:
        spec_line.append(rate)
        spec_line.append(int(spec_line[5]) * rate)


if __name__ == '__main__':
    get_imac_spec_kr()
    get_imac_price_kr()
    get_imac_price_jp()
    rate = get_jpy_rate()
    attatch_rate(rate)
    for spec_line in IMAC_SPEC_LIST:
        print(spec_line)
