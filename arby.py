import asyncio

from terra_sdk.client.lcd import AsyncLCDClient,LCDClient
import time
import os
import csv
import threading
from pprint import pprint

from terra_sdk.client.lcd.api.tx import CreateTxOptions, SignerOptions
from terra_sdk.core.fee import Fee
from terra_sdk.core.bank import MsgSend
import terra_sdk.core.market.msgs as market
from terra_sdk.core import Coin, Coins
from terra_sdk.core.tx import SignMode
from terra_sdk.key.key import SignOptions
from terra_sdk.core.wasm.msgs import MsgExecuteContract
def init():
    global mnemonic
    mnemonic= "flee innocent ankle client label toddler concert ripple weapon hire first urge science indicate blossom emerge copy defense execute heavy cycle wing never viable"
init()




from terra_sdk.key.mnemonic import MnemonicKey

mk = MnemonicKey(mnemonic=mnemonic)

"""
print(terra.bank.balance(mk.acc_address))


print(terra.tendermint.block_info()['block']['header']['height'])
"""

"""

pool="terra1jxazgm67et0ce260kvrpfv50acuushpjsz2y0p"
assets=terra.wasm.contract_query(pool,{'pool':{}})


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

    return int(mirust['return_amount'])

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

async def simulateBuySell(coin,contractDict,rowOne):
    terra = AsyncLCDClient(chain_id="columbus-5", url="https://lcd.terra.dev")

    combos=getCombos(rowOne)
    rowsToUse=rowOne[1:]
    for i in range(len(rowsToUse)):
        for y in range(len(combos[rowsToUse[i]])):
            if contractDict[coin][rowsToUse[i]]=='' or contractDict[coin][combos[rowsToUse[i]][y]]=='':
                continue
            if rowsToUse[i]!=combos[rowsToUse[i]][y]:
                buyPrice=checkPriceForBuyCoin(terra, contractDict[coin][rowsToUse[i]],300)
                buyPrice=await buyPrice
                #print(buyPrice)
                sellPrice=checkPriceForSellCoin(terra, contractDict[coin][combos[rowsToUse[i]][y]],buyPrice)
                sellPrice=await sellPrice
                if sellPrice/1000000>300.1:
                    estimatedProfit=(sellPrice/1000000)-300
                    print(coin,rowsToUse[i],combos[rowsToUse[i]][y],buyPrice/1000000,sellPrice/1000000,"$"+str(round(estimatedProfit,3)),time.ctime())
    await terra.session.close()




coins=contractDict.keys()


#asyncio.set_event_loop(asyncio.new_event_loop())
#asyncio.run(simulateBuySell("MIR",contractDict,rowOne))


async def simulateAllCoinsBuySell(loop):

    coros = [simulateBuySell(key,contractDict,rowOne) for key in coins]
    await asyncio.gather(*coros)
loop = asyncio.get_event_loop()



def makeCoinTrade(coin, contractDict, buyFrom, sellOn):
    terra = LCDClient("https://lcd.terra.dev", "columbus-5")
    wallet = terra.wallet(mk)
    print(coin,buyFrom,sellOn)
    buyFromContract=contractDict[coin][buyFrom]
    sellOnContract=contractDict[coin][sellOn]
    print(buyFromContract,sellOnContract)
    pool="terra17gjf2zehfvnyjtdgua9p9ygquk6gukxe7ucgwh"

    print(buyFromContract)

    tx = wallet.create_and_sign_tx(CreateTxOptions(
    msgs=[MsgSend(
        wallet.key.acc_address,
        mk.acc_address,
        "10000uusd" # send 1 luna
    )],
    memo="test transaction!",
))
    print(tx)
    result = terra.tx.broadcast(tx)
    print(result)
    
    #tx=wallet.create_and_sign_tx(CreateTxOptions(msgs=[swap]))
    #result=terra.tx.broadcast(tx)
    #print(result)



makeCoinTrade("MIR",contractDict,"terraswap","loop")

"""while True:
    try:
        loop.run_until_complete(simulateAllCoinsBuySell(loop))
    except Exception as e:
        print("Error",e)
"""