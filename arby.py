from terra_sdk.client.lcd import LCDClient
import time
import winsound
frequency = 500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)
winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)

#print('\a')
terra = LCDClient(chain_id="columbus-5", url="https://lcd.terra.dev")

mnemonic="flee innocent ankle client label toddler concert ripple weapon hire first urge science indicate blossom emerge copy defense execute heavy cycle wing never viable"

from terra_sdk.key.mnemonic import MnemonicKey

mk = MnemonicKey(mnemonic=mnemonic)
#print(terra.treasury.tax_rate())
#print(terra.oracle.parameters())

print(terra.bank.balance(mk.acc_address))

#print(terra.market.swap_rate('1000000uluna', 'terra1xw3h7jsmxvh6zse74e4099c6gl03fnmxpep76h').amount)

print(terra.tendermint.block_info()['block']['header']['height'])
#print(terra.market.terra_pool_delta())
#print(terra.market.swap_rate())

pool="terra1jxazgm67et0ce260kvrpfv50acuushpjsz2y0p"
assets=terra.wasm.contract_query(pool,{'pool':{}})

print(mk.acc_address)


allVals=[]
try:
    while True:
        assets=terra.wasm.contract_query(pool,{'pool':{}})
        bLuna="terra1kc87mu460fwkqte29rquh4hc20m54fxwtsx7gp"
        blunaAmt=int(assets['assets'][0]['amount'])
        lunaAmt=int(assets['assets'][1]['amount'])
        currentVal=round(100*((blunaAmt/lunaAmt)-1), 2)
        print(str(currentVal)+"%")
        allVals.append(round(100*((blunaAmt/lunaAmt)-1), 2))
        if currentVal<=1:
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)


        time.sleep(30)

except KeyboardInterrupt:
    print(allVals)
    print("Interrupted")