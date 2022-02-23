""" Looking for opportunity
"""
from web3 import Web3
import sys
import os
import pathlib
import pandas as pd
import math
from datetime import datetime
import calendar

yeh_ftm_pair = "0x041B498844d6f19CE30Df960CDCD8F480B913526"
yeh_harry_pair = "0x0779f273F8f4A7D3A802dA9c6c808033b66c3D24"
harry_ftm = "0xc26AFaFCb13AFCFbf801BA297b093a754178a74f"

token_address_dict = {
    'FTM': "0x21be370d5312f44cb42ce377bc9b8a0cef1a4c83",
    'WFTM': "0x21be370d5312f44cb42ce377bc9b8a0cef1a4c83",
    'YEH':"0x5b1a83715496A7bfC9327CeF0ECbd81cA6d6c6aF",
    'HARRY': "0xc7561291DFb4c92F4b85ac366135fa442AC6debf"
}

# Set up for Fantom
sys.path.append(os.path.join(pathlib.Path().absolute(), 'app'))
from ftm_secrets import working_path, wallet_address, holy_key, endpoint
sys.path.append(working_path)
from ftm_addresses import token_abi, pairs_abi, router_abi, factory_abi
from ftm_addresses import factory_addresses, router_addresses
#from ftm_addresses import token_address_dict, pair_address_dict

from getprice import getprice
from approve import approve_spend
from ftmbuy import buy

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

web3 = Web3(Web3.HTTPProvider(endpoint))
print("Looking for arbortunity. Web3 connection status:", web3.isConnected())
wallet_address = web3.toChecksumAddress(wallet_address)
weth_address = web3.toChecksumAddress(token_address_dict["WFTM"])
eth_address = web3.toChecksumAddress(token_address_dict["FTM"])

print(bcolors.OKBLUE + "Using wallet: ", wallet_address + bcolors.ENDC)
weth_address = web3.toChecksumAddress(token_address_dict["WFTM"])
weth_contract = web3.eth.contract(address=eth_address, abi=token_abi)
balance = weth_contract.functions.balanceOf(wallet_address).call()

# Configuration
spend_amount = 10
slippage = 0.05
# how much price difference do we need?
margin = 0.01
weth_decimal = 18
dex = 'spooky'

import time
#try:
    #while True:
for i in range(2000):
    time.sleep(10)
    token_address = web3.toChecksumAddress(token_address_dict['HARRY'])
    token_contract = web3.eth.contract(address=token_address, abi=token_abi)
    weth_contract = web3.eth.contract(address=weth_address, abi=token_abi)
    decimal = token_contract.functions.decimals().call()

    # GET HARRY FOR FANTOM
    harry_address = web3.toChecksumAddress(token_address_dict["HARRY"])
    eth_in_wei = web3.toWei(str(spend_amount), 'Ether')
    router_address = router_addresses[dex]
    router_contract = web3.eth.contract(address=web3.toChecksumAddress(router_address), 
                        abi=router_abi)
    token_amount_out = router_contract.functions.getAmountsOut(eth_in_wei, 
                [weth_address, harry_address]).call()
    token_out = token_amount_out[1] / math.pow(10, decimal)
    min_token_out = token_out * (1.0 - slippage)
    print("Phase One: Input {}  Output {} ({} minimum)".format(
           spend_amount, token_out, min_token_out))

    # PHASE 2
    yeh_address = web3.toChecksumAddress(token_address_dict["YEH"])

    scale = 1.0 - margin
    potential_trade = False

    harry_in_wei = token_amount_out[1]
    yeh_amount_out = router_contract.functions.getAmountsOut(
                       harry_in_wei, [harry_address, yeh_address]).call()
    yeh_out = yeh_amount_out[1] / math.pow(10, weth_decimal)
    harry_in = harry_in_wei / math.pow(10, decimal)
    min_yeh_out = yeh_out  * (1.0 - slippage)
    print("Phase Two: Input {}  Output {} ({} minimum)".format(
           harry_in, yeh_out, min_yeh_out))

    # PHASE3 
    yeh_in_wei = yeh_amount_out[1]
    yeh_amount_out = router_contract.functions.getAmountsOut(
                       yeh_in_wei, [yeh_address, weth_address]).call()
    eth_out = yeh_amount_out[1] / math.pow(10, weth_decimal)
    yeh_in = yeh_in_wei / math.pow(10, decimal)
    min_eth_out = eth_out  * (1.0 - slippage)
    print("Phase Three: Input {}  Output {} ({} minimum)".format(
          yeh_in, eth_out, min_eth_out))
    eth_in = spend_amount

    if eth_out < eth_in * (1 + margin):
        print(".... not actually profitable .....")
        print("")

    if eth_out > eth_in * (1 + margin):
        print("> ******** PROFITABLE TRADE CONFIRMED *******************")
        print("> Profit {} ether".format(eth_out - eth_in))
        print("> ******** PROFITABLE TRADE CONFIRMED *******************")

#        except Exception as e:
#            print(e)
#            print("some kind of error")
#
#except KeyboardInterrupt:
#    print("stop")
