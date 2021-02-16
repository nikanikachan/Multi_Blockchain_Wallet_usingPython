#Homework MultiWallet

# Imports
import subprocess
import json
import os
from constants import *
from web3 import Web3
from dotenv import load_dotenv
from web3.auto.gethdev import w3
from web3.middleware import geth_poa_middleware # Note that we are importing this because we are using PoA consensus for our blockchain
from web3 import Web3
from eth_account import Account
from bit import wif_to_key
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI

#Loading mnemonic from .env file
load_dotenv()
mnemonic = os.getenv('mnemonic')

#Make sure im working in the right directory
os.chdir(r'C:\Users\riett\Desktop\blockchain-tools') 

#Creating a function to get the different wallets. Note that I took only 3 addresses from BTC, ETH and BTCTEST

def derive_wallets(x):
    command = f'php derive -g --mnemonic="{mnemonic}" --cols=path,address,privkey,pubkey --coin={x} --numderive=3 --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    keys = json.loads(output)
    return(keys)

btckeys = derive_wallets(x='BTC')
ethkeys = derive_wallets(x='ETH')
btctestkeys = derive_wallets(x='btc-test')

#Creating a dictionary of all the addresses

coins = dict(BTC = btckeys,
         ETH = ethkeys,
         BTCTEST = btctestkeys)
coins

#TO SELECT SPECIFIC CHILD ACCOUNTS:
# 1. get index of keys change the "--cols" flag to "all"
# 2. to get a specific address, change index if necessary : coins["ETH"][0]['pubkey']


# SENDING OUT TRANSACTIONS IN ETH

#Adding poa middleware
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

#Using keystore to open our wallet and do a transaction

with open(
    Path(
        "./node1/keystore/UTC--2021-02-03T22-07-43.150280400Z--c05b85c29bbb120c09f32a2c06118a670c5b1f98"
    )
) as keyfile:
    encrypted_key = keyfile.read()
    private_key = w3.eth.account.decrypt(
        encrypted_key, getpass("Enter keystore password: ")
    )
    account_one = Account.from_key(private_key)


#Function to get keys

def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)


#Function to create txn metadata

def create_tx(coin, account, amount, recipient):
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": to, "value": amount}
        )
        return {
            "from": account.address,
            "to": to,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
            "chainID": web3.eth.chainId
        }
    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])

#Function to send txn

def send_tx(coin, account, to, amount):
    txn = create_tx(coin, account, to, amount)
    signed_tx = account.sign_transaction(txn)
    if coin == ETH: 
        result_eth = w3.eth.sendRawTransaction(signed.rawTransaction)
        return result_eth.hex()
    elif coin == BTCTEST: 
        return NetworkAPI.broadcast_tx_testnet(signed_tx)


# Sending a Transaction

result = send_txn(BTC, account_one, 1818181818181818181, "0x2810e1BDA9b02c0286FC8d0e786E8E9c1B31Cf00")
print(result)