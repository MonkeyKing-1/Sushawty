from web3 import Web3
import time
import json
from web3.middleware import geth_poa_middleware

# Replace 'your_infura_api_key' with your Infura API key (polygon mainnet)
infura_api_key = ""
infura_url = "https://polygon-mainnet.infura.io/v3/" + infura_api_key
# Connect to Polygon (Matic) mainnet
web3 = Web3(Web3.HTTPProvider(infura_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)


# Replace 'your_private_key' with the private key of the sender's Ethereum address
private_key = ''
# Replace '0x81C1949445755998C975335509Dc2d210914AF1a' with the sender's Ethereum address
sender_address = ''


f = open('abi.json')
abi = json.load(f)
abi: str = abi
contract_address = "0x6229FD3198f672D0d971fb9b6929d19A4650D951"  
# Create smart contract instance
contract = web3.eth.contract(address=contract_address, abi=abi)
# initialize the chain id, we need it to build the transaction for replay protection
Chain_id = web3.eth.chain_id
start_nonce = web3.eth.get_transaction_count(sender_address)

print("current quotient is:", contract.functions.cur_quotient().call())
ans = int(input("enter a prime divisor: "))

call_function = contract.functions.check_sol(ans).build_transaction({"from": sender_address, "value": 10 ** 17, "nonce": start_nonce})
# Sign transaction
signed_tx = web3.eth.account.sign_transaction(call_function, private_key=private_key)
# Send transaction
send_tx = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
# Wait for transaction receipt
tx_receipt = web3.eth.wait_for_transaction_receipt(send_tx)
print(tx_receipt.status)