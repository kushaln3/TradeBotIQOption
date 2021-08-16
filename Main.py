from iqoptionapi.stable_api import IQ_Option

trader = IQ_Option("kushalnjnv10@gmail.com", "Kushal#07")

trader.connect()


def Result(id):
    if trader.check_win_v3(id) >= 0:
        return(True)
    else:
        return(False)



def ChangedAction(ACTION):
    if ACTION == "call":
        return("put")
    elif ACTION == "put":
        return("call")




while True:

    Money=1

    Increment = 2.0

    ACTIVES="EURUSD"

    ACTION="call"#or "put"

    expirations_mode=1


    while True:
        check, id = trader.buy(Money, ACTIVES, ACTION, expirations_mode)

        if check: print(f"{ACTION} order succcessful")
        else: print(f"{ACTION} order failed")

        result = Result(id)

        if result:
            break
        else:
            Money = round(Money*Increment)
            ACTION = ChangedAction(ACTION)

