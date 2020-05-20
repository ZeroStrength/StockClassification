import pandas as pd
from bs4 import BeautifulSoup
import requests

class crawler():
    def __init__(self, market="KOSPI", top=100):
        self.market = market
        self.top = top

        self.data = pd.DataFrame(columns=["no","code","name"])

    def _getUrl(self):
        NAVER = {
            "KOSPI": "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page=",
            "KOSDAQ": "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=1&page=",
        }
        return NAVER[self.market]

    def get(self):
        row_num = 1
        page_num = 1
        
        url = self._getUrl()

        while row_num <= self.top:
            page_url = url + str(page_num)

            html = requests.get( page_url ).text
            soup = BeautifulSoup( html, 'html.parser')

            table = soup.find_all('table')[1]

            for tr in table.find_all('tr'):
                tds = tr.find_all('td')
                if len(tds) > 1:
                    code = tds[1].a['href'].split('code=')[1]
                    name = tds[1].text

                    self.data = self.data.append( [ { "no": row_num, "code":code, "name": name } ] )
                    row_num += 1

            page_num += 1

        return self.data

    def save(self, filename):
        # self.data -> file
        self.data.to_csv(filename)

if __name__ == '__main__':
    c = crawler("KOSDAQ", 100)
    c.get()
    c.save("data/kosdaq_100.csv")
