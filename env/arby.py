from terra_sdk.client.lcd import LCDClient
import time
import os
import pickle


def init():
    global mnemonic
    mnemonic= "flee innocent ankle client label toddler concert ripple weapon hire first urge science indicate blossom emerge copy defense execute heavy cycle wing never viable"
init()

terra = LCDClient(chain_id="columbus-5", url="https://lcd.terra.dev")


from terra_sdk.key.mnemonic import MnemonicKey

mk = MnemonicKey(mnemonic=mnemonic)

print(terra.bank.balance(mk.acc_address))


print(terra.tendermint.block_info()['block']['header']['height'])


pool="terra1jxazgm67et0ce260kvrpfv50acuushpjsz2y0p"
assets=terra.wasm.contract_query(pool,{'pool':{}})



def fetchData():
    readFile=open("bLuna_Luna.p","rb")
    try:
        while True:
            allVals=pickle.load(readFile)
            assets=terra.wasm.contract_query(pool,{'pool':{}})
            bLuna="terra1kc87mu460fwkqte29rquh4hc20m54fxwtsx7gp"
            blunaAmt=int(assets['assets'][0]['amount'])
            lunaAmt=int(assets['assets'][1]['amount'])
            currentVal=round(100*((blunaAmt/lunaAmt)-1), 2)
            print(str(currentVal)+"%")

            
            allVals.append(currentVal)


        


            time.sleep(3)

    except KeyboardInterrupt:
        print("Interrupted")


        
fetchData()