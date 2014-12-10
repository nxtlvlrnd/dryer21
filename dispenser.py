"""
dispenser: Dispenses bitcoins

Iterates through unfulfilled rows of the RedeemerDB, marks them as fulfilled, and then sends BTC.

Requires:
- Mix-out wallet private key (for sending bitcoins)
- RedeemerDB RPC (to find where to send bitcoins)
"""

import bitcoin
from rpc_lib import RedeemerDB
import global_storage

def dispense():
	for row in RedeemerDB.get_unfulfulled_rows():
		# A row is a dict with keys 'bond', 'address', and 'fulfilled'.
		assert row['fulfilled'] == 0 
		RedeemerDB.fulfill(row['bond'])
		send(global_storage.get_dispenser_private_key(), row['address'], global_storage.bond_value)

def send(fromprivkey, toaddr, value):
	tx = bitcoin.mktx(bitcoin.history(bitcoin.privtoaddr(fromprivkey)), [{'value': value, 'address': toaddr}])
	signed_tx = bitcoin.sign(tx, 0, fromprivkey)
	bitcoin.pushtx(signed_tx)

if __name__ == "__main__":
	while True:
		import time
		time.sleep(10)
		dispense()
