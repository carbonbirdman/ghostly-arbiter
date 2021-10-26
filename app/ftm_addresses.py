import json
import sys
import os
import pathlib
sys.path.append(os.path.join(pathlib.Path().absolute(), 'app'))
from ftm_secrets import working_path
sys.path.append(working_path)

def load_abi(abi_filename, working_path=working_path):
    #with open(os.path.join(os.path.dirname(working_path), 'abi', abi_filename)) as f:
    with open(os.path.join(working_path, 'abi', abi_filename)) as f:
        return json.load(f)

token_abi = load_abi("token.abi")
pairs_abi = load_abi("pairs.abi")
router_abi = load_abi("router.abi")
factory_abi = load_abi("factory.abi")

factory_addresses = {'spooky': "0x152eE697f2E276fA89E96742e9bB9aB1F2E61bE3",
                     'hyper': "0x991152411A7B5A14A8CF0cDDE8439435328070dF",
                     'spirit': "0xEF45d134b73241eDa7703fa787148D9C9F4950b0",
                     'waka': "0xB2435253C71FcA27bE41206EB2793E44e1Df6b6D",
                     'sushi': "0xc35DADB65012eC5796536bD9864eD8773aBc74C4"}

router_addresses = {'spooky': '0xF491e7B69E4244ad4002BC14e878a34207E38c29',
                    'hyper': '0x53c153a0df7E050BbEFbb70eE9632061f12795fB',
                    'spirit': '0x16327E3FbDaCA3bcF7E38F5Af2599D2DDc33aE52',
                    'waka': '0x7B17021FcB7Bc888641dC3bEdfEd3734fCaf2c87',
                    'sushi': '0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506'
                    }

token_address_dict = {
    'FTM': "0x21be370d5312f44cb42ce377bc9b8a0cef1a4c83",
    'WFTM': "0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83",
    'BOO': "0x841fad6eae12c286d1fd18d1d525dffa75c7effe",
    'DAI': "0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E",
    'xBOO': "0xa48d959AE2E88f1dAA7D5F611E01908106dE7598",
    'WETH': "0x74b23882a30290451A17c44f4F05243b6b58C76d",
    'WBTC': "0x321162Cd933E2Be498Cd2267a90534A804051b11",
    'BNB': "0xD67de0e0a0Fd7b15dC8348Bb9BE742F3c5850454",
    'USDC': "0x04068DA6C83AFCFA0e13ba15A6696662335D5B75",
    'CREAM': "0x657A1861c15A3deD9AF0B6799a195a249ebdCbc6",
    'COVER': "0xB01E8419d842beebf1b70A7b5f7142abbaf7159D",
    'BAND': "0x46E7628E8b4350b2716ab470eE0bA1fa9e76c6C5",
    'CRV': "0x1E4F97b9f9F913c46F1632781732927B9019C68b",
    'SNX': "0x56ee926bD8c72B2d5fa1aF4d9E4Cbb515a1E3Adc",
    'AAVE': "0x6a07A792ab2965C72a5B8088d3a069A7aC3a993B",
    'YFI': "0x29b0Da86e484E1C0029B56e817912d778aC0EC69",
    'LINK': "0xb3654dc3D10Ea7645f8319668E8F54d2574FBdC8",
    'SUSHI': "0xae75A438b2E0cB8Bb01Ec1E1e376De11D44477CC",
    'DAI': "0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E",
    'ICE': "0xf16e81dce15B08F326220742020379B855B87DF9",
    'BADGER': "0x753fbc5800a8C8e3Fb6DC6415810d627A387Dfc9",
    'DIGG': "0x08f6fE8f4dC577CF81E40E03E561d29B8b33E19b",
    'fUSDT': "0x049d68029688eabf473097a2fc38ef61633a3c7a",
    'WOOFY': "0xD0660cD418a64a1d44E9214ad8e459324D8157f1",
    'ANY': "0xdDcb3fFD12750B45d32E084887fdf1aABAb34239",
    'BIFI': "0xd6070ae98b8069de6B494332d1A1a81B6179D960",
    'MIM': "0x82f0B8B456c1A451378467398982d4834b6829c1",
    'ZOO':"0x09e145a1d53c0045f41aeef25d8ff982ae74dd56"
}

pair_address_dict = {
    "FTM-BOO" : "0xec7178f4c41f346b2721907f5cf7628e388a7a58"
}

# UniswapV02Factory: 0x152eE697f2E276fA89E96742e9bB9aB1F2E61bE3
# UniswapV02Router: 0xF491e7B69E4244ad4002BC14e878a34207E38c29
# Farm: 0x2b2929E785374c651a81A63878Ab22742656DcDd
# BooToken: 0x841FAD6EAe12c286d1Fd18d1d525DFfA75C7EFFE
# IFO Contract: 0xACACa07e398d4946AD12232F40f255230e73Ca72
# Boo MirrorWorld (xBOO): 0xa48d959AE2E88f1dAA7D5F611E01908106dE7598
# BrewBoo:  0xcA79f97d3aF4bCE5BfaA9821A0887E50542636F7

# https://hyperjump.fi/contracts-ftm.html
