# This file is used for testing pieces of code 

from iqoptionapi.stable_api import IQ_Option
import time

print("imported all modules")
trader = IQ_Option("kushalnjnv10@gmail.com", "Kushal#07")

trader.connect()
print("connected")
ACTIVES="CHFJPY"

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

ChangeACTIVES()