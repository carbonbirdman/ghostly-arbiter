""" Arb buy sell
    What this needs is to check the liquidity
"""
from web3 import Web3
import sys
import os
import pathlib
#sys.path.append(os.path.join(pathlib.Path().absolute(), 'fantom'))
from ftm_secrets import working_path, wallet_address, holy_key, endpoint
sys.path.append(working_path)
from ftm_addresses import token_abi, pairs_abi, router_abi, factory_abi
from ftm_addresses import factory_addresses, router_addresses
from ftm_addresses import token_address_dict, pair_address_dict

def approve_spend(web3, token_address_in, thisdex, wallet_address, total_max_spend=1.0):
    router_address = router_addresses[thisdex]
    cs_router_address = web3.toChecksumAddress(router_address)
    cs_wallet_address = web3.toChecksumAddress(wallet_address)
    token_contract_in = web3.eth.contract(address=web3.toChecksumAddress(token_address_in), abi=token_abi)
    allowed = int(token_contract_in.functions.allowance(cs_wallet_address, cs_router_address).call())
    print("Approved up to {}".format(allowed))
    max_amount = int(web3.toWei(total_max_spend, 'ether'))
    if allowed < max_amount:
        nonce = web3.eth.getTransactionCount(wallet_address)
        tx = token_contract_in.functions.approve(cs_router_address, max_amount).buildTransaction({
            'from': wallet_address,
            'nonce': nonce
        })
        signed_tx = web3.eth.account.signTransaction(tx, holy_key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx = web3.toHex(tx_hash)
    else:
        tx = 'approval exists'
    allowed = token_contract_in.functions.allowance(cs_wallet_address, cs_router_address).call()
    return(allowed, tx)

if __name__ == '__main__':
    web3 = Web3(Web3.HTTPProvider(endpoint))
    print("Operational?", web3.isConnected())
    token_symbol = 'BOO'
    wallet_address = web3.toChecksumAddress(wallet_address)
    this_dex = 'spooky'
    token_address = web3.toChecksumAddress(token_address_dict[token_symbol])
    approved_amt, tx = approve_spend(web3, token_address, this_dex, wallet_address, total_max_spend=1.0)
    print("amn: {} tx: {}".format(web3.fromWei(approved_amt, 'Ether'),tx))

