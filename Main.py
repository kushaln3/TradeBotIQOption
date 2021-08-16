from iqoptionapi.stable_api import IQ_Option
import time


trader = IQ_Option("kushalnjnv10@gmail.com", "Kushal#07")
trader.connect()



def SMA():
    candles = trader.get_candles(ACTIVES, 15, 28, time.time())
    sma7vals = []
    for candle in candles:
        sma7vals.append(candle['close'])



    candles = trader.get_candles(ACTIVES, 15, 56, time.time())
    sma14vals = []
    for candle in candles:
        sma14vals.append(candle['close'])

    if sum(sma7vals)/len(sma7vals) > sum(sma14vals)/len(sma14vals):
        pass
        print("SMA: Call")
        return(True)
    else:
        print("SMA: Put")
        return(False)



def Result(id):
    if trader.check_win_v3(id) >= 0:
        print(f"Profit: {trader.check_win_v3(id)} {trader.get_currency()}")
        return(True)
    else:
        print(f"Loss: {trader.check_win_v3(id)} {trader.get_currency()}")
        return(False)



def ChangedAction(ACTION):
    if ACTION == "call":
        return("put")
    elif ACTION == "put":
        return("call")



def IsOpen(ACTIVES):
    Isopen = (((trader.get_all_open_time())['binary'])[ACTIVES])['open']

    if Isopen == {} or Isopen == False or ((trader.get_all_profit())[ACTIVES])['turbo'] == {}:
        return(False)
    else:
        return(True)



def Incremental(ACTIVES):
    profit_percent = ((trader.get_all_profit())[ACTIVES])['turbo']
    print('profit percent:  ', profit_percent, "\n")
    Increment = (1-profit_percent) + 2.05
    return(Increment)



def ChangeACTIVES():
    openACTIVES = trader.get_all_profit()
    open_list = {}
    for openACTIVE in openACTIVES:
        ACTIVE = (openACTIVES[openACTIVE])['turbo']
        if not ACTIVE == {}:
            open_list[openACTIVE] = ACTIVE

    print(open_list)
    max_key = max(open_list, key=open_list.get)
    return(max_key)



try:
    while True:

        Money=1

        ACTIVES="EURGBP"

        ACTION="call"#or "put"

        expirations_mode=1

        currency = trader.get_currency()


        while True:
            if not IsOpen(ACTIVES):
                ACTIVES = ChangeACTIVES()
            
            if SMA():
                ACTION = "call"
            else:
                ACTION = "put"
            check, id = trader.buy(Money, ACTIVES, ACTION, expirations_mode)

            if check: print(f"{ACTION} order succcessful")
            else:
                print(f"{ACTION} order failed")

            result = Result(id)

            if result:
                break
            else:
                Increment = Incremental(ACTIVES)
                print('Increment is', Increment)
                Money = round(Money*Increment)
                

except KeyboardInterrupt:
    print("Exiting...")
    exit()