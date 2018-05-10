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
        self.stock_number_list = None
        self.today_stock_data = None

    def _fetch_lastday_stock_info(self):
        page = self.TWSE_HOST+"exchangeReport/STOCK_DAY_ALL?response=html"

        soup = _get_soup_table(page, self.PAUSE_TIME)

        stock_number_list = []
        stock_data = {}
        for raw in soup.table.tbody:
            if isinstance(raw, bs4.element.Tag):
                raw_content_str = [unicode(items.string) for items in raw.children if isinstance(items, bs4.element.Tag)]
                stock_num = raw_content_str[0]
                date_info = datetime.date.today()
                stock_name = raw_content_str[1]
                volume = int(raw_content_str[2].replace(',', ''))
                amount = int(raw_content_str[3].replace(',', ''))
                open_price = float(raw_content_str[4].replace(',', ''))
                high_price = float(raw_content_str[5].replace(',', ''))
                low_price = float(raw_content_str[6].replace(',', ''))
                close_price = float(raw_content_str[7].replace(',', ''))
                price_diff = float(raw_content_str[8].replace(',', '')) if raw_content_str[8] != "X0.00" else 0.0
                lot = int(raw_content_str[9].replace(',', ''))
                stock_number_list.append((stock_name.strip(), stock_num.strip()))
                stock_data[stock_num] = daily_info._make([date_info, volume, amount, open_price, high_price, low_price, close_price, price_diff, lot])

        self.fetch_time = datetime.datetime.now()
        self.stock_number_list = stock_number_list
        self.today_stock_data = stock_data


    def __avoid_IP_blocking(self):
        time.sleep(self.PAUSE_TIME)

def _get_soup_table(link, retry_time):
    http = urllib3.PoolManager()
    while True:
        result = http.request('GET', link)
        soup = bs4.BeautifulSoup(result.data, 'html.parser')
        try:
            if isinstance(soup.table.tbody, bs4.element.Tag):
                return soup
            else:
                print "Fail to retrive table. Now retry ..."
        except AttributeError:
            print "Empty result. Now retry ..."

    time.sleep(retry_time)
    return soup

class NormalSession(object):
    def get(self, url):
        headers = {'user-agent': 'Chrome/65.0.3325.181'}
        return requests.get(url, headers=headers, timeout=30)