""" Get the price of a token on a dex.
"""
from web3 import Web3
import sys
import os
import pathlib
sys.path.append(os.path.join(pathlib.Path().absolute(), 'fantom'))
from ftm_secrets import working_path, endpoint
sys.path.append(working_path)
from ftm_addresses import token_abi, pairs_abi, router_abi, factory_abi
from ftm_addresses import factory_addresses, router_addresses
from ftm_addresses import token_address_dict
import math
weth_decimal = 18

def getprice(web3, token_symbol, thisdex, weth_symbol='WFTM', eth_in=1, weth_decimal=18,
             verbose=False):
    """ Returns bid price, ask price.
        Bid price is how much they will give you in fantom for the token.
        Ask price is how much fantom you need to give for the token.
    """
    if verbose:
        print("Getting price for", thisdex, token_symbol)
    try:
        token_address = web3.toChecksumAddress(token_address_dict[token_symbol])
        weth_address = web3.toChecksumAddress(token_address_dict[weth_symbol])
        token_contract = web3.eth.contract(address=token_address, abi=token_abi)
        decimal = token_contract.functions.decimals().call()
        factory_address = factory_addresses[thisdex]
        factory_contract = web3.eth.contract(address=web3.toChecksumAddress(factory_address), abi=factory_abi)
        pair_address = factory_contract.functions.getPair(token_address, weth_address).call()
        pair_contract = web3.eth.contract(address=web3.toChecksumAddress(pair_address), abi=pairs_abi)
        # Check is this pair on this dex
        # web3.eth.getCode
        token0_address = pair_contract.functions.token0().call()
        token1_address = pair_contract.functions.token1().call()
        reserves = pair_contract.functions.getReserves().call()
        if token0_address == weth_address:
            reserves_price = reserves[0]/reserves[1]
        elif token1_address == weth_address:
            reserves_price = reserves[1]/reserves[0]
        else:
            return("Error matching weth equivalent")
        adjusted_reserves_price = (reserves_price)  * (math.pow(10, weth_decimal)) / (reserves[1] / math.pow(10, decimal))
        router_address = router_addresses[thisdex]
        eth_in_wei = web3.toWei(eth_in, 'Ether')
        router_contract = web3.eth.contract(address=web3.toChecksumAddress(router_address), abi=router_abi)
        # First call: for a given FTM input, find how much token we get out
        amount_out_token = router_contract.functions.getAmountsOut(eth_in_wei, [weth_address, token_address]).call()
        ask_price_wei = eth_in_wei / amount_out_token[1]
        ask_price_ftm = ask_price_wei * ( math.pow(10, decimal) / math.pow(10, weth_decimal))
        adjusted_token_out = amount_out_token[1] * math.pow(10, -decimal)
        # Second call: selling this amount of eth back, how much token do we get?
        tokens_in = amount_out_token[1]
        amount_out_ftm = router_contract.functions.getAmountsOut(tokens_in, [token_address, weth_address]).call()
        bid_price_wei =  amount_out_ftm[1] /tokens_in   # price is in the input units
        bid_price_ftm = bid_price_wei * (math.pow(10, decimal) / math.pow(10, weth_decimal))
        if verbose:
            print("getprice: {} FTM gets you {} tokens".format(eth_in, adjusted_token_out))
            print("getprice: {} tokens gets you {} FTM".format(adjusted_token_out, amount_out_ftm[1]/math.pow(10, weth_decimal)))
            print("Price  Reserves: {} , Bid: {} Ask: {}".format(adjusted_reserves_price, bid_price_ftm, ask_price_ftm))
        return(bid_price_wei, ask_price_wei, ask_price_ftm, bid_price_ftm)
    except Exception as e:
        print("Contract error " + str(e))

if __name__ == '__main__':
    web3 = Web3(Web3.HTTPProvider(endpoint))
    print("Testing getprice.py. Connected=", web3.isConnected())
    token_symbol, weth_symbol = 'WBTC', 'WFTM'
    dex1, dex2 = 'spooky', 'sushi'
    dex1, dex2 = 'waka', 'sushi'
    print("Testing getprice.py. Tokens: {}, {}.".format(token_symbol,weth_symbol))
    print("Testing getprice.py. Dexs: {}, {}".format(dex1,dex2))
    weth_address = web3.toChecksumAddress(token_address_dict[weth_symbol])
    token_address = web3.toChecksumAddress(token_address_dict[token_symbol])
    token_contract = web3.eth.contract(address=token_address, abi=token_abi)
    decimal = token_contract.functions.decimals().call()

    factory_address = factory_addresses[dex1]
    factory_contract = web3.eth.contract(address=web3.toChecksumAddress(factory_address), abi=factory_abi)
    pair_address = factory_contract.functions.getPair(token_address, weth_address).call()
    pair_contract = web3.eth.contract(address=web3.toChecksumAddress(pair_address), abi=pairs_abi)
    # Check is this pair on this dex
    # web3.eth.getCode
    token0_address = pair_contract.functions.token0().call()
    token1_address = pair_contract.functions.token1().call()
    reserves = pair_contract.functions.getReserves().call()
    print("reserves")
    router_address = router_addresses[dex1]
    router_contract = web3.eth.contract(address=web3.toChecksumAddress(router_address), abi=router_abi)
    print("router")

    bid_price1, ask_price1 = getprice(web3, token_symbol, dex1, verbose=True)
    bid_price2, ask_price2 = getprice(web3, token_symbol, dex2, verbose=True)
    print("Function called, now checking")

    # Now check
    for thisdex in [dex1, dex2]:
        # eth_out, token_out = getAmountsOut(ether_in, [weth_address, token_address])
        eth_in = 2
        UNIT_MAIN = web3.toWei(eth_in, 'Ether')
        router_address = router_addresses[thisdex]
        router_contract = web3.eth.contract(address=web3.toChecksumAddress(router_address), abi=router_abi)
        amount_token_out = router_contract.functions.getAmountsOut(UNIT_MAIN, [weth_address, token_address]).call()
        adjusted_token_out = (amount_token_out[1] / math.pow(10, decimal))
        print("{} FTM nets you {} token".format(eth_in, adjusted_token_out))
        ask_price_token = UNIT_MAIN / amount_token_out[1]  # this puts it in units of tokens
        # Adjust for different token decimals
        ask_price = ask_price_token * (math.pow(10, decimal) / math.pow(10, weth_decimal))
        print("Ask price {}".format(ask_price))

        # token_out, eth_out = getAmountsOut(token_in, [token_address, weth_address])
        INPUT_AMNT = amount_token_out[1]
        amount_out_eth = router_contract.functions.getAmountsOut(INPUT_AMNT, [token_address, weth_address]).call()
        bid_price_wei = amount_out_eth[1] / INPUT_AMNT     # price is in the input units
        bid_price_eth = bid_price_wei * (math.pow(10, decimal) / math.pow(10, weth_decimal))
        print("{} tokens gets you {} FTM".format(INPUT_AMNT / (math.pow(10, decimal)), amount_out_eth[1] / math.pow(10, weth_decimal)))
        print("Bid price (out) {} {}".format(thisdex, bid_price_eth))

        # for a given output, what do we need to put in?
        # token_in, eth_in = getAmountsIn(tokens_out, [token_address, weth_address])
        ntokens = int(adjusted_token_out * math.pow(10, decimal))
        token_amount_in = router_contract.functions.getAmountsIn(ntokens, [weth_address, token_address]).call()
        ether_in = token_amount_in[0] / math.pow(10, weth_decimal)
        ask_price_in = (token_amount_in[0] / token_amount_in[1]) * (math.pow(10, decimal) / math.pow(10, weth_decimal))
        print("{:10.8f} token costs you {} ftm".format(adjusted_token_out, ether_in))
        print("Ask price (in) {} {}".format(thisdex, ask_price_in))

        # eth_in, token_in = getAmountsIn(ether_out, [weth_address, token_address])
        eth_out = amount_out_eth[1]
        eth_out = int(2 * math.pow(10, weth_decimal))
        eth_out_eth = eth_out / math.pow(10, weth_decimal)
        token_amount_in = router_contract.functions.getAmountsIn(eth_out, [token_address, weth_address]).call()
        bid_price_in = eth_out / token_amount_in[0]
        bid_price_in_eth = (bid_price_in) * (math.pow(10, decimal) / math.pow(10, weth_decimal))
        token_amount_in_adjusted = (token_amount_in[0] / math.pow(10, decimal))
        print("To get {} FTM you need {:10.8f} token".format(eth_out_eth, token_amount_in_adjusted))
        print("Bid price {} {}".format(thisdex, bid_price_in_eth))


