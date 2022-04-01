from terra_sdk.client.lcd import LCDClient
import time
import os
import csv

def init():
    global mnemonic
    mnemonic= "flee innocent ankle client label toddler concert ripple weapon hire first urge science indicate blossom emerge copy defense execute heavy cycle wing never viable"
init()

terra = LCDClient(chain_id="columbus-5", url="https://lcd.terra.dev")



from terra_sdk.key.mnemonic import MnemonicKey

mk = MnemonicKey(mnemonic=mnemonic)


print(terra.bank.balance(mk.acc_address))


print(terra.tendermint.block_info()['block']['header']['height'])


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

def checkPriceForBuyCoin(contract,amountToBuyWith):

    try:
        otherAsset=terra.wasm.contract_query(contract,{'pool':{}})['assets'][1]['info']['token']['contract_addr']
    except:
        otherAsset=terra.wasm.contract_query(contract,{'pool':{}})['assets'][0]['info']['token']['contract_addr']
    
    mirust=terra.wasm.contract_query(contract,
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

def checkPriceForSellCoin(contract,amountToSell):
    
    try:
        otherAsset=terra.wasm.contract_query(contract,{'pool':{}})['assets'][1]['info']['token']['contract_addr']
    except:
        otherAsset=terra.wasm.contract_query(contract,{'pool':{}})['assets'][0]['info']['token']['contract_addr']
    
    mirust=terra.wasm.contract_query(contract,
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

def simulateBuySell(coin,contractDict,rowOne):
    combos=getCombos(rowOne)
    rowsToUse=rowOne[1:]
    for i in range(len(rowsToUse)):
        for y in range(len(combos[rowsToUse[i]])):
            if contractDict[coin][rowsToUse[i]]=='' or contractDict[coin][combos[rowsToUse[i]][y]]=='':
                continue
            if rowsToUse[i]!=combos[rowsToUse[i]][y]:
                buyPrice=checkPriceForBuyCoin(contractDict[coin][rowsToUse[i]],100)
                sellPrice=checkPriceForSellCoin(contractDict[coin][combos[rowsToUse[i]][y]],buyPrice)
                if sellPrice>1000000:
                    estimatedProfit=((sellPrice/1000000)-1)*363
                    print(combos[rowsToUse[i]][y],rowsToUse[i],sellPrice,"$"+str(round(estimatedProfit,3)))


def simulateAllCoinsBuySell(coins,contractDict,rowOne):
    for key in coins:
        print(key)
        simulateBuySell(key,contractDict,rowOne)


coins=contractDict.keys()




#print(contractDict)


while True:
    simulateAllCoinsBuySell(coins,contractDict,rowOne)

#simulateBuySell("STT",contractDict,rowOne)
#checkAllValuesForACoin("MIR",contractDict,rowOne)