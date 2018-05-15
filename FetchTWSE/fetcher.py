
import json
import logging
import urllib3

class FetchTWSE(object):
    def __init__(self, speed_up=False):
        self.TWSE_HOST = 'http://www.twse.com.tw/'
        if speed_up:
            # TODO : session that changes IP
            # self.PAUSE_TIME = 0.5
            pass
        else:
            self.session = NormalSession()
            self.PAUSE_TIME = 4.5
        self.stock_ID_list = None
        self.today_stock_data = None

    def _fetch_STOCK_DAY_ALL(self):
        page = self.TWSE_HOST+"exchangeReport/STOCK_DAY_ALL?response=json"

        stock_list = _get_json(page)

        stock_ID_list = []
        stock_data = {}
        for raw in stock_list:
            stock_ID = raw[0]
            date_info = datetime.date.today()
            stock_name = raw[1]
            volume = int(raw[2].replace(',', ''))
            amount = int(raw[3].replace(',', ''))
            open_price = float(raw[4].replace(',', ''))
            high_price = float(raw[5].replace(',', ''))
            low_price = float(raw[6].replace(',', ''))
            close_price = float(raw[7].replace(',', ''))
            price_diff = float(raw[8].replace(',', '')) if raw[8] != "X0.00" else 0.0
            lot = int(raw[9].replace(',', ''))
            stock_ID_list.append((stock_name.strip(), stock_ID.strip()))
            stock_data[stock_ID] = daily_info(date_info, volume, amount, open_price, high_price, low_price, close_price, price_diff, lot)

        self.fetch_time = datetime.datetime.now()
        self.stock_ID_list = stock_ID_list
        self.today_stock_data = stock_data


    def __avoid_IP_blocking(self):
        time.sleep(self.PAUSE_TIME)

def _get_json(link, retry_time=5):
    MAX_RETRY = 5

    http = urllib3.PoolManager()
    for i in range(MAX_RETRY):
        result = json.loads(http.request('GET', link).data)
        try:
            if result['stat'] == 'OK'
                if 'data' in result:
                    return result['data']
                elif 'date1' in result:
                    return result['data1']
                else:
                    logging.error("Can not find proper key for json data.")
            else:
                logging.info("Fail to retrive data. Now retry ...")
        except keyError:
            logging.info("Empty result. Now retry ...")
        finally:
            time.sleep(retry_time)
    else:
        errmsg = 'Reach maximum retry times.'
        logging.error(errmsg)
        raise ValueError(errmsg)

class NormalSession(object):
    def get(self, url):
        headers = {'user-agent': 'Chrome/65.0.3325.181'}
        return requests.get(url, headers=headers, timeout=30)