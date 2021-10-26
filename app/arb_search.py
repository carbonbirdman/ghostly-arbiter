""" looking for opportunity
"""
from web3 import Web3
import sys
import os
import pathlib
import pandas as pd

# Set up for Fantom
sys.path.append(os.path.join(pathlib.Path().absolute(), 'app'))
from ftm_secrets import working_path, wallet_address, holy_key, endpoint
sys.path.append(working_path)
from ftm_addresses import token_abi, pairs_abi, router_abi, factory_abi
from ftm_addresses import factory_addresses, router_addresses
from ftm_addresses import token_address_dict, pair_address_dict

import math
from datetime import datetime
import calendar
from getprice import getprice
from approve import approve_spend
from ftmbuy import buy

if os.path.isfile("arbfile.csv"):
    arb_record = pd.read_csv("arbfile.csv")
else:
    arb_record = pd.DataFrame(columns=['dexhi','dexlo','token','ask','bid','profit','txbuy','txsell','time'])

web3 = Web3(Web3.HTTPProvider(endpoint))
print("Looking for arbortunity. Web3 connection status:", web3.isConnected())
wallet_address = web3.toChecksumAddress(wallet_address)
weth_address = web3.toChecksumAddress(token_address_dict["WFTM"])
tokens = token_address_dict.keys()

# Configuration
spend_amount = 10
slippage = 0.05
# how much price difference do we need?
margin = 0.01
weth_decimal = 18

# Dex pairs
# Configure manually because some pairs don't make sense to check
# e.g. if they have low liquidity.
tokens_to_search = [*token_address_dict]
tokens_to_search.remove('FTM')
tokens_to_search.remove('WFTM')
dex_pairs_tokens = {
        #('spooky', 'hyper'): ['WBTC', 'WETH', 'BNB'],
        #('spooky', 'sushi'): ['CRV'],
        ('spooky', 'spirit'): tokens_to_search
        #('spooky', 'spirit'): ['BNB','SUSHI','LINK','ZOO'], 
        #('spooky', 'waka'): ['WBTC','ZOO','WETH','BAND'],
        #('spirit','waka'):  ['WBTC','ZOO','WETH']
}
dexpairlist = list(list(dex_pairs_tokens.keys()))
# Make the pairs
#dexpairs = []
#for dex in dexlist:
#    otherdex = dexlist.copy()
#    otherdex.remove(dex)
#    for odex in otherdex:
#        dexpairs.append((dex,odex))
#print('Dexpairs: ' + str(dexpairs))
import time
try:
    #while True:
    for i in range(1):
        time.sleep(2)
        for dexpair in dexpairlist:
            dex1, dex2 = dexpair
            token_list = dex_pairs_tokens[dexpair]
            for token_symbol in token_list:
                print("---------------------------------------------------")
                print("SEARCHING: {} {} {}".format(dex1, dex2, token_symbol))

                try:
                    bid_price1, ask_price1, bid_price1_ftm, ask_price1_ftm = getprice(web3, token_symbol, dex1)
                except:
                    print("Failed to get price for {} from {}".format(token_symbol, dex1))
                    continue
                try:
                    bid_price2, ask_price2, bid_price2_ftm, ask_price2_ftm = getprice(web3, token_symbol, dex2)
                except:
                    print("Failed to get price for {} from {}".format(token_symbol, dex2))
                    continue
                # If we got here then we have two prices.
                # We want an ask less than a bid, which is to say we want to pay
                # a smaller amount, and receive a larger amount
                print("ask 1: {:6f} bid 2: {:6f}, {:2.2f}% difference".format(
                        ask_price1, bid_price2, 100*(ask_price1 - bid_price2)/ask_price1))
                print("ask 2: {} bid 1: {}, {}% difference".format(
                        ask_price2, bid_price1, 100*(ask_price2 - bid_price1)/ask_price2))

                scale = 1.0 - margin
                potential_trade = False

                if (ask_price1_ftm < (bid_price2_ftm * scale)):
                    print("Potential trade found")
                    # we can buy on dex1 for less than dex2 will sell to us
                    dexlo, dexhi = dex1, dex2
                    ask_price, bid_price = ask_price1, bid_price2
                    potential_trade = True

                elif (ask_price2_ftm < (bid_price1_ftm * scale)):
                    print("Potential trade found")
                    # we can buy on dex2 for less than dex1 will sell to us
                    dexlo, dexhi = dex2, dex1
                    ask_price, bid_price = ask_price2, bid_price1
                    potential_trade = True 
                else:
                    print("ask {} bidscale {}".format(ask_price2_ftm, bid_price1_ftm * scale))
                    dexlo, dexhi = dex2, dex1
                    ask_price, bid_price = ask_price2, bid_price1
                    potential_trade = False
                
                if potential_trade:
                    try:
                        print("******** POTENTIAL PROFITABLE TRADE *************")
                        print("1. Buy {} from {} for {}".format(token_symbol, dexlo, ask_price))
                        print("2. Sell {} to {} for {}".format(token_symbol, dexhi, bid_price))
                        print("CHECKING .... ")
                        # Lets run through the transaction
                        token_address = web3.toChecksumAddress(token_address_dict[token_symbol])
                        token_contract = web3.eth.contract(address=token_address, abi=token_abi)
                        weth_contract = web3.eth.contract(address=weth_address, abi=token_abi)
                        decimal = token_contract.functions.decimals().call()

                        # First buy low
                        eth_in_wei = web3.toWei(str(spend_amount), 'Ether')
                        router_address_lo = router_addresses[dexlo]
                        router_contract_lo = web3.eth.contract(address=web3.toChecksumAddress(router_address_lo), 
                                            abi=router_abi)
                        token_amount_out = router_contract_lo.functions.getAmountsOut(eth_in_wei, 
                                    [weth_address, token_address]).call()
                        token_out = token_amount_out[1] / math.pow(10, decimal)
                        min_token_out = token_out * (1.0 - slippage)
                        print("Phase One {}: Input {}  Output {} ({} minimum)".format(
                              dexlo, spend_amount, token_out, min_token_out))

                        # Then sell high
                        router_address_hi = router_addresses[dexhi]
                        token_in_wei = token_amount_out[1]
                        router_contract_hi = web3.eth.contract(
                                             address=web3.toChecksumAddress(router_address_hi), abi=router_abi)
                        token_amount_out = router_contract_hi.functions.getAmountsOut(
                                           token_in_wei, [token_address, weth_address]).call()
                        eth_out = token_amount_out[1] / math.pow(10, weth_decimal)
                        token_in = token_in_wei / math.pow(10, decimal)
                        min_eth_out = eth_out  * (1.0 - slippage)
                        print("Phase Two {}: Input {}  Output {} ({} minimum)".format(
                              dexhi, token_in, eth_out, min_eth_out))
                        eth_in = spend_amount
                        if eth_out < eth_in * (1 + margin):
                            print(".... not actually profitable .....")
                            print("1. Buy {} {} from {} for {}".format(token_out, token_symbol, dexlo, eth_in))
                            print("2. Sell {} {} to {} for {}".format(token_in, token_symbol, dexhi, eth_out))
                            print(".... not actually profitable .....")
                            print("")

                        if eth_out > eth_in * (1 + margin):
                            print("> ******** PROFITABLE TRADE CONFIRMED *******************")
                            print("> 1. Buy {} {} from {} for {}".format(token_out, token_symbol, dexlo, eth_in))
                            print("> 2. Sell {} {} to {} for {}".format(token_in, token_symbol, dexhi, eth_out))
                            print("> Profit {} ether".format(eth_out - eth_in))
                            print("> ******** PROFITABLE TRADE CONFIRMED *******************")

                            total_max_spend = spend_amount * 2
                            token_balance_start = token_contract.functions.balanceOf(wallet_address).call()
                            eth_balance_start = weth_contract.functions.balanceOf(wallet_address).call()
                            # Buy from the cheap dex
                            print("buying")
                            time.sleep(1)
                            amount_approved, txa1 = approve_spend(web3, weth_address, dexlo,
                                                                  wallet_address, 
                                                                  total_max_spend=total_max_spend)
                            time.sleep(1)
                            tokens_min_bought_wei, txb1 = buy(web3, weth_address, token_address, 
                                                          dexlo, wallet_address, spend_amount=spend_amount,
                                                          gas_price=62)
                            # Can we get amount received in the transaction?
                            trying = True
                            while(trying):
                                time.sleep(2)
                                try:
                                    receipt =  web3.eth.getTransactionReceipt(txb1)
                                    token_balance_finish = token_contract.functions.balanceOf(wallet_address).call()
                                    trying = False
                                except:
                                    print('retry')
                            amount_bought = token_balance_finish - token_balance_start
                            print("2. Bought {} {} from {} for {}".format(amount_bought,token_symbol,dexlo,spend_amount))
                            # Sell on the dear dex
                            print("Selling")
                            amount_to_spend = amount_bought / math.pow(10, decimal)
                            time.sleep(1)
                            approved, txa2 = approve_spend(web3, token_address, dexhi, 
                                                           wallet_address, 
                                                           total_max_spend=amount_to_spend*2)
                            time.sleep(1)
                            time.sleep(1)
                            eth_received, txb2 = buy(web3, token_address, weth_address, dexhi, 
                                                     wallet_address, spend_amount=amount_to_spend)
                           
                            time.sleep(1)
                            print("min:{}".format(web3.fromWei(eth_received, 'Ether')))
                            eth_balance_finish = weth_contract.functions.balanceOf(wallet_address).call()
                            eth_made = eth_balance_finish - eth_balance_start
                            print("2. Bought {} {} from {} for {}".format(eth_made, 'eth', dexhi, spend_amount))
                            print("proft:{}".format(eth_made/10**18, 'Ether'))
                            thisframe = pd.DataFrame([[dexhi,dexlo,token_symbol,ask_price,
                                                       bid_price,eth_made,str(web3.toHex(txb1)),str(web3.toHex(txb2)),str(datetime.now())]],
                                            columns=['dexhi','dexlo','token','ask','bid','profit','txbuy','txsell','time'])
                            arb_record = arb_record.append(thisframe)
                            arb_record.to_csv('arbfile.csv')

                    except Exception as e:
                        print(e)
                        print("some kind of error")

except KeyboardInterrupt:
    print("stop")
