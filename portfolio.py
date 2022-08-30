from NewsToGod import *
from sequencing import *
import talib as ta
ACCOUNT_ID = 11509188
BUY_RANK = 5
SELL_RANK = 5
TRADE_SIZE = 0.25

# # self.symbols_basket =  ['IYZ','XLY','XHB', 'PEJ','XLP','XLC','PBJ','XLE','XES','ICLN','XLF','KIE','KCE','KRE','XLV','PPH','XLI','IGF',
#                 'XLK','FDN','XLU','FIW','FAN','XLRE','XLB','PYZ','XME','HAP','MXI','IGE','MOO','WOOD','COPX','FXZ','URA','LIT']
# self.etfs_xlc = ['XLC','FIVG','IYZ','VR']
# self.etfs_xly = ['XLY','XHB', 'PEJ', 'IBUY','BJK','BETZ''AWAY','SOCL','BFIT','KROP']
# self.etfs_xlp = ['XLP','FTXG','KXI','PBJ']
# self.etfs_xle = ['XLE','XES','CNRG','FTXN','SOLR','ICLN']
# self.etfs_xlf = ['XLF','KIE','KCE','KRE']
# self.etfs_xlv = ['XLV','XHE','XHS','GNOM','HTEC','PPH','AGNG','EDOC']
# self.etfs_xli = ['XLI','AIRR','IFRA','IGF','SIMS']
# self.etfs_xlk = ['XLK','HERO','FDN','IRBO','FINX','IHAK','SKYY','SNSR']
# self.etfs_xlu = ['XLU','RNRG','FIW','FAN']
# self.etfs_xlre = ['XLRE','KBWY','SRVR','VPN','GRNR'] #VPN, GRNR
# self.etfs_xlb = ['XLB','PYZ','XME','HAP','MXI','IGE','MOO','WOOD','COPX','FXZ','URA','LIT']


class Portfolio:

    def __init__(self,trade_station,market_sentiment,sector_sentiment):
        self.trade_station = trade_station
        self.cash = get_cash(trade_station)
        self.equity = get_equity(trade_station)
        self.net_wealth = self.cash + self.equity
        self.holdings = get_holdings(trade_station)
        self.trade_size_cash = TRADE_SIZE * self.net_wealth
        self.market_sentiment = market_sentiment
        self.sector_sentiment = sector_sentiment
        self.etfs = {'XLC':['XLC','FIVG','IYZ','VR'],'XLY':['XLY','XHB', 'PEJ', 'IBUY','BJK','BETZ''AWAY','SOCL','BFIT','KROP'],'XLP':['XLP','FTXG','KXI','PBJ'],
                    'XLE':['XLE','XES','CNRG','FTXN','SOLR','ICLN'],'XLF':['XLF','KIE','KCE','KRE'],'XLV':['XLV','XHE','XHS','GNOM','HTEC','PPH','AGNG','EDOC'],
                    'XLI':['XLI','AIRR','IFRA','IGF','SIMS'],'XLK':['XLK','HERO','FDN','IRBO','FINX','IHAK','SKYY','SNSR'],'XLU':['XLU','RNRG','FIW','FAN'],
                    'XLRE':['XLRE','KBWY','SRVR','VPN','GRNR'],'XLB':['XLB','PYZ','XME','HAP','MXI','IGE','MOO','WOOD','COPX','FXZ','URA','LIT']}
        self.etfs_to_buy = get_best_etfs(self)
       
    def buy(self,symbol,quantity,order_type='Market'):
        #order_type = "Limit" "StopMarket" "Market" "StopLimit"
        #"TimeInForce": {"Duration": "DAY"\ 'GTC'
        url = "https://api.tradestation.com/v3/orderexecution/orders"
        payload = {
            "AccountID": ACCOUNT_ID,
            "Symbol": symbol,
            "Quantity": quantity,
            "OrderType": order_type,
            "TradeAction": "BUY",
            "TimeInForce": {"Duration": "DAY"},
            "Route": "Intelligent"
        }
        headers = {
            "content-type": "application/json",
            "Authorization": f'Bearer {self.trade_station.TOKENS.access_token}'
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        print(response.text)

    def sell(self,symbol,quantity,order_type='Market'):
        #order_type = "Limit" "StopMarket" "Market" "StopLimit"
        url = "https://api.tradestation.com/v3/orderexecution/orders"
        payload = {
            "AccountID": ACCOUNT_ID,
            "Symbol": symbol,
            "Quantity": quantity,
            "OrderType": order_type,
            "TradeAction": "SELL",
            "TimeInForce": {"Duration": "DAY"},
            "Route": "Intelligent"
        }
        headers = {
            "content-type": "application/json",
            "Authorization": f'Bearer {self.trade_station.TOKENS.access_token}'
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        print(response.text)

    def run_buy_and_sell_strategy(self):
        pass

def get_best_etfs(self):
    pass

def get_cash(trade_station):
    try:
        url = "https://api.tradestation.com/v3/brokerage/accounts/11509188/balances"
        headers = {"Authorization":f'Bearer {trade_station.TOKENS.access_token}'}
        account_details = requests.request("GET", url, headers=headers)
        account_details = json.loads(account_details.text)
        if(account_details['Balances'][0]['AccountID'] == ACCOUNT_ID):
            return account_details['Balances'][0]['CashBalance']
        else: 
            print("PROBLEM WITH FINDING YOUR TRADE STATION ACCOUNT - PROBLEM ACCURED IIN 'get_cash' function")
            return 0
    except Exception:
        print(f"CONNECTION problem with TradeStation, accured while tried to check account balances, Details: \n {traceback.format_exc()}")
        return 0

def get_equity(trade_station):
    try:
        url = "https://api.tradestation.com/v3/brokerage/accounts/11509188/balances"
        headers = {"Authorization":f'Bearer {trade_station.TOKENS.access_token}'}
        account_details = requests.request("GET", url, headers=headers)
        account_details = json.loads(account_details.text)
        if(account_details['Balances'][0]['AccountID'] == ACCOUNT_ID):
            return account_details['Balances'][0]['Equity']
        else: 
            print("PROBLEM WITH FINDING YOUR TRADE STATION ACCOUNT - PROBLEM ACCURED IIN 'get_equity' function")
            return 0
    except Exception:
        print(f"CONNECTION problem with TradeStation, accured while tried to check account balances, Details: \n {traceback.format_exc()}")
        return 0

def get_holdings(trade_station):
    holdings = {}
    try:
        url = "https://api.tradestation.com/v3/brokerage/accounts/11509188/positions"
        headers = {"Authorization":f'Bearer {trade_station.TOKENS.access_token}'}
        account_details = requests.request("GET", url, headers=headers)
        account_details = json.loads(account_details.text)
        for position in account_details['Positions']:
            if(position['AccountID'] != ACCOUNT_ID):
                continue
            position_id = position["PositionID"]
            quantity = position["Quantity"]
            long_short = position["LongShort"]
            average_price = position["AveragePrice"]
            trade_yield = position["UnrealizedProfitLossPercent"]
            total_cost = position["TotalCost"]
            market_value = position["MarketValue"]
            holdings[position["Symbol"]] = {"PositionID":position_id,"Quantity":quantity,"LongShort":long_short,
                "AveragePrice":average_price,"UnrealizedProfitLossPercent":trade_yield,"TotalCost":total_cost,"MarketValue":market_value}
        return holdings
    except Exception:
        print(f"CONNECTION problem with TradeStation, accured while tried to check account balances, Details: \n {traceback.format_exc()}")
        return holdings

def get_buy_ratings(self,symbols,today):
    rating = {}
    for etf in self.etfs_to_buy:
        symbol_data_day = pd.DataFrame(yf.download(tickers=etf, period='max',interval='1d',progress=False)).dropna()
        symbol_data_month = pd.DataFrame(yf.download(tickers=etf, period='max',interval='1mo',progress=False)).dropna()
        symbol_data_weekly = pd.DataFrame(yf.download(tickers=etf, period='max',interval='1wk',progress=False)).dropna()
        rating[etf] = self.buy_rate(symbol_data_month,symbol_data_weekly,symbol_data_day,etf)
    return rating

def buy_rate(data_monthly,data_weekly,data_day,etf):
    rank = 0
    today = date.today()
    buy_ret = {'day':today,'rank':rank,'today': True}
    seq_daily = SequenceMethod(data_day,'day',today)
    seq_weekly = SequenceMethod(data_weekly,'weekly',today)
    seq_month = SequenceMethod(data_monthly,'monthly',today)
    avg_weekly_move = seq_weekly.get_avg_up_return()
    start_move_price = check_seq_price_by_date_weekly(seq_weekly.get_seq_df(),today)
    try:
        data_daily = yf.download(etf,start = today, end= (today +timedelta(days=3)),progress=False)
        daily_price = data_daily['Open'][0]
    except:
        daily_price = None
    if(daily_price != None and start_move_price != None): move_return = (daily_price - start_move_price)/start_move_price*100
    else: move_return = None
    data_weekly = data_weekly
    data_monthly = data_monthly
    data_day['SMA13'] = ta.SMA(data_day['Close'],timeperiod=13)
    data_day['SMA5'] = ta.SMA(data_day['SMA13'], timeperiod=5)
    data_weekly['SMA13'] = ta.SMA(data_weekly['Close'],timeperiod=13)
    data_weekly['SMA5'] = ta.SMA(data_weekly['SMA13'], timeperiod=5)
    data_monthly['SMA13'] = ta.SMA(data_monthly['Close'],timeperiod=13)
    data_monthly['SMA5'] = ta.SMA(data_monthly['SMA13'], timeperiod=5)
    data_monthly = data_monthly.dropna()
    data_weekly = data_weekly.dropna()
    first_monthly_date = data_monthly.index[0].date()
    first_weekly_date = data_weekly.index[0].date()
    month = today.replace(day=1)
    pre_week = today - timedelta(days=7*4)
    last_month = month - timedelta(days=1) 
    last_month = last_month.replace(day = 1)
    pre_month = today.replace(day =1)
    for i in range(3):
        pre_month = pre_month - timedelta(days=1)
        pre_month = pre_month.replace(day = 1)
    if(check_seq_by_date_daily(seq_daily.get_seq_df(),today) == 1):
        rank += 1
    if(check_seq_by_date_weekly(seq_weekly.get_seq_df(),today) == 1):
        rank += 1
    else :
        buy_ret['rank'] = rank
        return buy_ret
    if(check_seq_by_date_monthly(seq_month.get_seq_df(),today) == 1):
        rank += 2
    try:
        if(data_day.loc[str(today - timedelta(days=3)),'SMA13'] < data_day.loc[str(today - timedelta(days=3)),'SMA5'] and data_day.loc[str(today - timedelta(days=5)),'SMA13'] < data_day.loc[str(today - timedelta(days=5)),'SMA5']):
            rank += 1
    except:
        rank += 0
    try:
        if(first_monthly_date <= last_month and data_monthly.loc[str(last_month),'SMA13'] > data_monthly.loc[str(last_month),'SMA5']):
            rank += 1
    except:
        rank += 0
    if(is_moving_away_weekly(data_weekly,today,pre_week)):
        rank += 1
    if(is_moving_away_monthly(data_monthly,last_month,pre_month)):
        rank += 1
    if(move_return != None and move_return <= avg_weekly_move/2.5):
        rank += 1

    buy_ret['rank'] = rank
    buy_ret['day'] = today
    if(rank >= BUY_RANK):
        return buy_ret

    for day, row in data_daily.iterrows():
        if(today == (day - timedelta(days=day.weekday()))):
            if(row['Close'] > data_day.loc[str(day),'SMA13'] and check_seq_by_date_daily(seq_daily.get_seq_df(),day) == 1):#WAS datedaily2
                rank += BUY_RANK
                buy_ret['rank'] = rank
                buy_ret['day'] = day
                buy_ret['today'] = False
                return buy_ret
    return buy_ret







def is_moving_away_weekly(data_weekly,today,pre_week):
    try:
        if((data_weekly.loc[str(today),'SMA13'] - data_weekly.loc[str(today),'SMA5']) > (data_weekly.loc[str(pre_week),'SMA13'] - data_weekly.loc[str(pre_week),'SMA5'])):
            return True
    except:
        return False
    return False

def is_moving_away_monthly(data_monthly,last_month,pre_month):
    try:
        if((data_monthly.loc[str(last_month),'SMA13'] - data_monthly.loc[str(last_month),'SMA5']) > (data_monthly.loc[str(pre_month),'SMA13'] - data_monthly.loc[str(pre_month),'SMA5'])):
            return True
    except:
        return False
    return False



def check_seq_by_date_monthly(seq,date):
    previous_row = 0
    first = True
    for index,row in seq.iterrows():
        if(row["Date"] < date ):
            previous_row = row
            first = False
        else: break
    if(first): return 0
    return int(previous_row['Sequence'])

def check_seq_by_date_weekly(seq,date):
    previous_row = 0
    first = True
    for index,row in seq.iterrows():
        if(row["Date"] < date):
            previous_row = row
            first = False
        else: break
    if(first): return 0
    return int(previous_row['Sequence'])

def check_seq_by_date_daily(seq,date):
    previous_row = 0
    first = True
    for index,row in seq.iterrows():
        if(row["Date"] < date):
            previous_row = row
            first = False
        else: break
    if(first): return 0
    return int(previous_row['Sequence'])


def check_seq_price_by_date_weekly(seq,date):
    previous_row = 0
    first = True
    for index,row in seq.iterrows():
        if(row["Date"] < date):
            previous_row = row
            first = False
        else: break
    if(first): return None
    return (previous_row['Entry Price'])



# sold_symbols = []
# symbols_sell_ratings = get_sell_rating(self,week)
# if(symbols_sell_ratings != None):
# for symbol in symbols_sell_ratings.items():
#     if(symbol[1]['rank'] >= SELL_RANK):
#         try:
#             day_str = str(symbol[1]['day'].date())
#         except:
#             day_str = str(symbol[1]['day'])
#         day = datetime.strptime(day_str,'%Y-%m-%d')
#         sold_symbols.append(symbol[0])
#         data_daily = yf.download(symbol[0],start=day_str, end=(day +timedelta(days=4)).strftime('%Y-%m-%d'),interval='1d',progress=False)
#         if(symbol[1]['today']):
#             sell_price = data_daily['Open'][0]
#         else:
#             sell_price = data_daily['Open'][1]
#         self.place_sell_order(symbol[0],data_daily,sell_price)

# if(self.cash > self.leverage_amount): 
# symbols_buy_ratings = get_buy_ratings(self,symbols,week)
# symbols_buy_ratings = {key:value for key, value in sorted(symbols_buy_ratings.items(), key=lambda x: x[1]['rank'],reverse=True)}
# for symbol in symbols_buy_ratings.items():
#     if(symbol[1]['rank'] >= BUY_RANK and not self.is_holding(symbol[0]) and self.cash > self.leverage_amount and (symbol[0] not in sold_symbols)):
#         try:
#             day_str = str(symbol[1]['day'].date())
#         except:
#             day_str = str(symbol[1]['day'])
#         day = datetime.strptime(day_str,'%Y-%m-%d')
#         data_daily = yf.download(symbol[0],start = day_str, end= (day +timedelta(days=4)).strftime('%Y-%m-%d'),interval='1d',progress=False)
#         if(symbol[1]['today']):
#             buy_price = data_daily['Open'][0]
#         else:
#             buy_price = data_daily['Open'][1]
#         self.place_buy_order(symbol[0],data_daily,buy_price)
# self.close_out()
