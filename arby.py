from terra_sdk.client.lcd import LCDClient

terra = LCDClient(chain_id="columbus-5", url="https://lcd.terra.dev")

mnemonic="flee innocent ankle client label toddler concert ripple weapon hire first urge science indicate blossom emerge copy defense execute heavy cycle wing never viable"

from terra_sdk.key.mnemonic import MnemonicKey

mk = MnemonicKey(mnemonic=mnemonic)
#print(terra.treasury.tax_rate())
#print(terra.oracle.parameters())

print(terra.bank.balance(mk.acc_address))

print(terra.market.swap_rate('1000000uluna', 'terra1xw3h7jsmxvh6zse74e4099c6gl03fnmxpep76h').amount)

