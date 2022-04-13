import asyncio

from terra_sdk.client.lcd import AsyncLCDClient,LCDClient
import time
import os
import csv
import threading
from pprint import pprint
import json
from terra_sdk.client.lcd.api.tx import CreateTxOptions, SignerOptions
from terra_sdk.core.fee import Fee
from terra_sdk.core.bank import MsgSend
import terra_sdk.core.market.msgs as market
from terra_sdk.core import Coin, Coins
from terra_sdk.core.tx import SignMode
from terra_sdk.key.key import SignOptions
from terra_sdk.core.wasm.msgs import MsgExecuteContract
import math
def init():
    global mnemonic
    mnemonic= "flee innocent ankle client label toddler concert ripple weapon hire first urge science indicate blossom emerge copy defense execute heavy cycle wing never viable"
init()
import base64




from terra_sdk.key.mnemonic import MnemonicKey

mk = MnemonicKey(mnemonic=mnemonic)
terra = LCDClient("https://lcd.terra.dev", "columbus-5")
    
print(terra.bank.balance(mk.acc_address))
assets=terra.wasm.contract_query("terra1jxazgm67et0ce260kvrpfv50acuushpjsz2y0p",{'pool':{}})
print(assets,"\n")
"""



print(terra.tendermint.block_info()['block']['header']['height'])
"""

"""

pool="terra1jxazgm67et0ce260kvrpfv50acuushpjsz2y0p"



def fetchData():
    readFile=open("bLuna_Luna.p","rb")
    try:
        while True:

            assets=terra.wasm.contract_query(pool,{'pool':{}})
            bLuna="terra1kc87mu460fwkqte29rquh4hc20m54fxwtsx7gp"
            blunaAmt=int(assets['assets'][0]['amount'])
            lunaAmt=int(assets['assets'][1]['amount'])
            currentVal=round(100*((blunaAmt/lunaAmt)-1), 2)
            print(str(currentVal)+"%")







            time.sleep(3)

    except KeyboardInterrupt:S
        print("Interrupted")

fetchData()"""
#only luna based contracts
"""terraswapContracts=[]
contracts={
    'terraswap':terraswapContracts
}"""

#contract="terra1amv303y8kzxuegvurh0gug2xe9wkgj65enq2ux" #terraswap
#contract="terra1cpzkckgzz90pq8fkumdjc58ee5llrxt2yka9fp" #loop
#contract="terra143xxfw5xf62d5m32k3t4eu9s82ccw80lcprzl9" #astroport

async def checkPriceForBuyCoin(terra,contract,amountToBuyWith):

    mirust= await terra.wasm.contract_query(contract,
        {
            "simulation": {
                "offer_asset": {
                    "info" : {
                        "native_token":{
                            "denom":"uusd"
                        }
                    },
                    "amount": str(amountToBuyWith*1000000)
                }
            }
        }
    )
    
    return int(mirust['return_amount'])

async def checkPriceForSellCoin(terra,contract,amountToSell):
    
    otherAssetPrep=await terra.wasm.contract_query(contract,{'pool':{}})
    try:
        otherAsset=otherAssetPrep['assets'][1]['info']['token']['contract_addr']
    except:
        otherAsset=otherAssetPrep['assets'][0]['info']['token']['contract_addr']
    
    mirust=await terra.wasm.contract_query(contract,
        {
            "simulation": {
                "offer_asset": {
                    "info" : {
                        "token":{
                            "contract_addr":otherAsset
                        }
                    },
                    "amount": str(amountToSell)
                }
            }
        }
        
    )

    return int(mirust['return_amount']),otherAsset

contractDict={}
with open('contracts.csv', 'r') as file:
    allContracts = csv.reader(file,delimiter='\t')
    i=0
    for row in allContracts:

        if i==0:
            rowOne=row
        if i>=1:
            token={}
            for y in range(1,len(rowOne)):
                token[rowOne[y]]=row[y]
            contractDict[row[0]]=token
        i+=1

print(contractDict)

def checkAllValuesForACoin(coin,contractDict,rowOne):
    thisCoin=contractDict[coin]
    for i in range(1,len(rowOne)):
        price=checkPriceForBuyCoin(thisCoin[rowOne[i]],100)
        print(rowOne[i],price)

def getCombos(rowOne):
    combos={}

    for i in range(len(rowOne)):
        if rowOne[i]!='':
            combos[rowOne[i]]=rowOne[1:]

    return combos

#print(getCombos(rowOne))

async def simulateBuySell(coin,contractDict,rowOne,amount):
    terra = AsyncLCDClient(chain_id="columbus-5", url="https://lcd.terra.dev")

    combos=getCombos(rowOne)
    rowsToUse=rowOne[1:]
    for i in range(len(rowsToUse)):
        for y in range(len(combos[rowsToUse[i]])):
            if contractDict[coin][rowsToUse[i]]=='' or contractDict[coin][combos[rowsToUse[i]][y]]=='':
                continue
            if rowsToUse[i]!=combos[rowsToUse[i]][y]:
                buyPrice=checkPriceForBuyCoin(terra, contractDict[coin][rowsToUse[i]],amount)
                buyPrice=await buyPrice
                #print(buyPrice)
                sellPrice=checkPriceForSellCoin(terra, contractDict[coin][combos[rowsToUse[i]][y]],buyPrice)
                sellPrice=await sellPrice
                otherAsset=sellPrice[1]
                sellPrice=sellPrice[0]
                #print(sellPrice)
                if sellPrice/1000000>300.1:
                    estimatedProfit=(sellPrice/1000000)-amount
                    print(coin,rowsToUse[i],combos[rowsToUse[i]][y],buyPrice/1000000,sellPrice/1000000,"$"+str(round(estimatedProfit,3)),time.ctime())
                    makeCoinTrade(coin,contractDict,rowsToUse[i],combos[rowsToUse[i]][y],str(amount),str(buyPrice),otherAsset,str(int(1000000*amount)),str(int(1000000*amount))+"uusd")
                    
    await terra.session.close()




coins=contractDict.keys()


#asyncio.set_event_loop(asyncio.new_event_loop())
#asyncio.run(simulateBuySell("MIR",contractDict,rowOne))


async def simulateAllCoinsBuySell(loop):

    coros = [simulateBuySell(key,contractDict,rowOne,300) for key in coins]
    await asyncio.gather(*coros)
loop = asyncio.get_event_loop()



def makeCoinTrade(coin, contractDict, buyFrom, sellOn,amount,beliefBuyPrice,coinContract,money,moneyDisplay):
    terra = LCDClient("https://lcd.terra.dev", "columbus-5")
    wallet = terra.wallet(mk)
    
    buyFromContract=contractDict[coin][buyFrom]
    sellOnContract=contractDict[coin][sellOn]
    

    print(buyFromContract)

    print("writing swaps")
    #money=str(int(1000000*amount))
    #moneyDisplay=str(int(1000000*amount))+"uusd"
    swap1=MsgExecuteContract(
                mk.acc_address,
                buyFromContract,
                {
                    "swap": {
                    "max_spread": "0.01",
                    "offer_asset": {
                        "info": {
                        "native_token": {
                            "denom": "uusd",
                        },
                        },
                        "amount": money,
                    },
                    "belief_price": beliefBuyPrice,
                    },
                },
                Coins.from_str(moneyDisplay)
            )
    print("swap 1 written")
    swap_msg = {
        "swap":{
            "max_spread":"0.01"
            }
        }
    encoded_json = base64.b64encode(json.dumps(swap_msg).encode("utf-8")).decode('ascii')
    message=MsgExecuteContract(
        sender = mk.acc_address,
        contract = coinContract, #coin
        execute_msg={
            "send": {
            "msg": encoded_json,
            "amount": str(int(int(beliefBuyPrice)*0.99)),
            "contract": sellOnContract #pair contract
            }
        },
    )
    print("swap 2 written")
    tx=wallet.create_and_sign_tx(CreateTxOptions(
        msgs=[swap1,message]
    ))
    print(tx)
    result = terra.tx.broadcast(tx)
    print(result)

"""async def main():   
    a=simulateBuySell("aUST",contractDict,rowOne,300)
    await a
loop.run_until_complete(main())
"""
#makeCoinTrade("aUST",contractDict,"loop","terraswap",300,"242341056","terra1hzh9vpxhsk8253se0vv5jj6etdvxu3nv8z07zu")


while True:
    try:
        loop.run_until_complete(simulateAllCoinsBuySell(loop))
    except Exception as e:
        print(e)
