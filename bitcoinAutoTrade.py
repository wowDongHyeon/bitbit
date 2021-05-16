import time
import pyupbit
import datetime

access = "MCxeLg2Sm7n93V5wF0x8uCdtgipHYxH81prcHgzg"
secret = "odpQxPk9DK2Gnj0RfGx6rhper4GvxuaS7YUATsLr"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

isAbleBuy = True
# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-DOGE")
        end_time = start_time + datetime.timedelta(days=1)
       

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            # 수익률 15%넘어서 전체 매도했으면 매수 불가
            if(isAbleBuy == False):
                time.sleep(10)
                continue
                
            #총매수
            buyKRW = upbit.get_amount("KRW-DOGE") 
            #총평가
            nowKRW= upbit.get_balance("KRW-DOGE")*pyupbit.get_orderbook(tickers="KRW-DOGE")[0]["orderbook_units"][0]["ask_price"]
            suic = ((float(nowKRW)-float(buyKRW))/float(buyKRW))*100
           
            if(suic > 15) :
                btc = get_balance("DOGE")
            
                #최소거래금액 5000원 넘으면, 도지코인이 대략 600원이니까 60*10 = 6000
                if btc > 10:
                   
                    isAbleBuy = False
                    upbit.sell_market_order("KRW-DOGE", btc*0.9995)
                    continue

           

            target_price = get_target_price("KRW-DOGE", 0.5)
            current_price = get_current_price("KRW-DOGE")
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-DOGE", krw*0.9995)
        else:
            isAbleBuy = True
            btc = get_balance("DOGE")
            if btc > 10:
                upbit.sell_market_order("KRW-DOGE", btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)