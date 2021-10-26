""" Buy a token
"""
from web3 import Web3
import sys
import os
import pathlib
from ftm_secrets import working_path, wallet_address, holy_key, endpoint
sys.path.append(working_path)
from ftm_addresses import token_abi, pairs_abi, router_abi, factory_abi
from ftm_addresses import factory_addresses, router_addresses
from ftm_addresses import token_address_dict, pair_address_dict
from approve import approve_spend
import math
from datetime import datetime
import calendar
#189820
#62
def buy(web3, token_address_in, token_address_out, thisdex, wallet_address,
        spend_amount=0.1, slippage=0.05, dt=20, max_gas = 323186, gas_price = 120):
    d = datetime.utcnow()
    unixtime = calendar.timegm(d.utctimetuple())
    deadline = unixtime + dt * 1000
    amount_in = web3.toWei(str(spend_amount), 'Ether')
    token_contract_in = web3.eth.contract(address=web3.toChecksumAddress(token_address_in), abi=token_abi)
    token_balance_in = token_contract_in.functions.balanceOf(wallet_address).call()
    if token_balance_in < amount_in:
        print("Insufficient balance, transaction will fail")
    router_address = router_addresses[thisdex]
    router_contract = web3.eth.contract(address=web3.toChecksumAddress(router_address), abi=router_abi)
    token_amount_out = router_contract.functions.getAmountsOut(amount_in, [token_address_in, token_address_out]).call()
    decimal = token_contract_in.functions.decimals().call()
    print("Expected out: {}".format(token_amount_out[1] / 10**decimal))
    min_amount_out = int(token_amount_out[1] * (1.0 - slippage))
    time.sleep(1)
    buy_tx = router_contract.functions.swapExactTokensForTokens(
        amount_in,
        min_amount_out,
        [web3.toChecksumAddress(token_address_in),
         web3.toChecksumAddress(token_address_out)],
        wallet_address,
        deadline).buildTransaction({
        'gas': max_gas,
        'gasPrice': web3.toWei(gas_price, 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address),
    })
    signed_tx = web3.eth.account.sign_transaction(buy_tx, holy_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return min_amount_out, tx_hash

import time
if __name__ == '__main__':
    web3 = Web3(Web3.HTTPProvider(endpoint))
    token_symbol = 'CRV'
    token_symbol = 'WBTC'
    #token_symbol = 'BOO'
    wallet_address = web3.toChecksumAddress(wallet_address)
    weth_address = web3.toChecksumAddress(token_address_dict["WFTM"])
    dex = 'sushi'
    #dex = 'spooky'
    spend_amount = 0.1
    slippage = 0.05
    total_max_spend = spend_amount * 5
    token_address = web3.toChecksumAddress(token_address_dict[token_symbol])
    token_contract = web3.eth.contract(address=token_address, abi=token_abi)
    decimal = token_contract.functions.decimals().call()
    amount_approved, tx = approve_spend(web3, weth_address, dex, wallet_address, total_max_spend=total_max_spend)
    print(tx)
    time.sleep(2)
    token_balance_start = token_contract.functions.balanceOf(wallet_address).call()
    tokens_bought, tx = buy(web3, weth_address, token_address, dex, wallet_address, spend_amount=spend_amount)
    # Can we get amount received in the transaction?

    # testing block
    spend_amount=0.1 
    slippage=0.05 
    dt=20
    max_gas = 323186
    gas_price = 62
    d = datetime.utcnow()
    unixtime = calendar.timegm(d.utctimetuple())
    deadline = unixtime + dt * 1000
    amount_in = web3.toWei(str(spend_amount), 'Ether')
    token_address_in = weth_address
    token_address_out = token_address
    token_contract_in = web3.eth.contract(address=web3.toChecksumAddress(token_address_in), abi=token_abi)
    token_balance_in = token_contract_in.functions.balanceOf(wallet_address).call()
    if token_balance_in < amount_in:
        print("Insufficient balance, transaction will fail")
    router_address = router_addresses[dex]
    router_contract = web3.eth.contract(address=web3.toChecksumAddress(router_address), abi=router_abi)
    token_amount_out = router_contract.functions.getAmountsOut(amount_in, [token_address_in, token_address_out]).call()
    decimal = token_contract_in.functions.decimals().call()
    print("Expected out: {}".format(token_amount_out[1] / 10**decimal))
    min_amount_out = int(token_amount_out[1] * (1.0 - slippage))
    buy_tx = router_contract.functions.swapExactTokensForTokens(
        amount_in,
        min_amount_out,
        [web3.toChecksumAddress(token_address_in),
         web3.toChecksumAddress(token_address_out)],
        wallet_address,
        deadline).buildTransaction({
        'gas': max_gas,
        'gasPrice': web3.toWei(gas_price, 'gwei'),
        'nonce': web3.eth.get_transaction_count(wallet_address),
    })
    signed_tx = web3.eth.account.sign_transaction(buy_tx, holy_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    tx = tx_hash
    #tokens_bought, tx = buy(web3, weth_address, token_address, dex, wallet_address, spend_amount=spend_amount)
    # Can we get amount received in the transaction?
    trying = True
    while(trying):
        time.sleep(6)
        try:
            receipt =  web3.eth.getTransactionReceipt(tx)
            token_balance_finish = token_contract.functions.balanceOf(wallet_address).call()
            trying = False
        except:
            print('retry')
    # get balance before
    amount = token_balance_finish - token_balance_start
    print(tx)
    print("Token bought: {}".format(amount))


