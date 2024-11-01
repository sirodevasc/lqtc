#
from os import path
import sys, json
from time import time, ctime, sleep
import requests
from web3 import Web3
#
import LQTC_config #its a .py file
#
#   telegram my token and my chatids
TOKEN, chat_id = LQTC_config.TGtoken, LQTC_config.TGchat_id
#       my private key & my BSC wallet
mywallet, mykey = LQTC_config.mywallet2, LQTC_config.mykey2
#           adress of a Token and address of a pair for that token on pancakeswap
The_Token, Token_Pair = LQTC_config.TheToken, LQTC_config.TokenPair
#
# *********************************************
#                   definir le taux de change utilisateur.
taux = "0.19"
#                   nombre de token a vendre. 
quantiter = "10000"
# *********************************************
# concatenate string quantiter + virgul obligatoire et convert en int, #amount = int(str(quantiter) + str(virgul)) 
#virgul = "000000000000000000"
amount = int("".join([quantiter , "000000000000000000"]))   # convert la quantité tokens
#amount = int("".join([quantiter , virgul]))   # concatenate les deux string et convert en int, amount = int(str(quantiter) + str(virgul))  
#quantiter = web3.from_wei(amount, 'ether') # mode auto via web3, envois le meme que la var quantiter(retire les 18 decimales)
#
#  # BNB / wbnb Address et usdt token
token_bnb, USDT = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c', '0x55d398326f99059fF775485246999027B3197955'
#token_bnb = web3.to_checksum_address("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c") # auto check WBNB Address
#
bsc = "https://bsc-dataseed.binance.org/" #rpc
PcsRouter, PcsFactory = '0x10ED43C718714eb63d5aA57B78B54704E256024E', '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73'
pcs_abi = '[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
pcs_swap_abi = '[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
pcs_sell_Abi = '[{"inputs":[{"internalType":"string","name":"_NAME","type":"string"},{"internalType":"string","name":"_SYMBOL","type":"string"},{"internalType":"uint256","name":"_DECIMALS","type":"uint256"},{"internalType":"uint256","name":"_supply","type":"uint256"},{"internalType":"uint256","name":"_txFee","type":"uint256"},{"internalType":"uint256","name":"_lpFee","type":"uint256"},{"internalType":"uint256","name":"_MAXAMOUNT","type":"uint256"},{"internalType":"uint256","name":"SELLMAXAMOUNT","type":"uint256"},{"internalType":"address","name":"routerAddress","type":"address"},{"internalType":"address","name":"tokenOwner","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"minTokensBeforeSwap","type":"uint256"}],"name":"MinTokensBeforeSwapUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"tokensSwapped","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"ethReceived","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"tokensIntoLiqudity","type":"uint256"}],"name":"SwapAndLiquify","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"enabled","type":"bool"}],"name":"SwapAndLiquifyEnabledUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"_liquidityFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_maxTxAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_taxFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claimTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tAmount","type":"uint256"}],"name":"deliver","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"excludeFromFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"excludeFromReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"geUnlockTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"includeInFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"includeInReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"isExcludedFromFee","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"isExcludedFromReward","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"time","type":"uint256"}],"name":"lock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"numTokensSellToAddToLiquidity","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tAmount","type":"uint256"},{"internalType":"bool","name":"deductTransferFee","type":"bool"}],"name":"reflectionFromToken","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"liquidityFee","type":"uint256"}],"name":"setLiquidityFeePercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"maxTxPercent","type":"uint256"}],"name":"setMaxTxPercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"swapNumber","type":"uint256"}],"name":"setNumTokensSellToAddToLiquidity","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_enabled","type":"bool"}],"name":"setSwapAndLiquifyEnabled","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"taxFee","type":"uint256"}],"name":"setTaxFeePercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"swapAndLiquifyEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"rAmount","type":"uint256"}],"name":"tokenFromReflection","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalFees","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"uniswapV2Pair","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"uniswapV2Router","outputs":[{"internalType":"contract IUniswapV2Router02","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"unlock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
#
#
#zepat = path.dirname(sys.argv[0]) #affiche le dossier courant du py
#
class LQTC:
    def __init__(self):

        self.web3, self.Event, self.Epoch = 0, 0, 0
        self.onetime = 1
        self.prix, self.liqui, self.schedule, self.TimeViewOld, self.NomToken  = '', '', '', '', ''
        self.Connected = False
# initialise le time pour msg PRINT , msg tg ,limite les achats , msg TGV pour pas pop toutes les 2sec de boucles
        self.timebasePRT, self.timebaseTG, self.timebaseBUY, self.timebaseTGV = int(time()), int(time()), int(time()), int(time())
#
#
    ###################
    #   Send_TG()
    ###################
    def Send_TG(self, msgTG):
        url = (f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msgTG}") #methode 2
        try:
            #response = requests.post(apiURL, json={'chat_id': chat_id, 'text': message}) #methode 1 nok
            response = requests.get(url)#.json() # methode 2 sends message. avec le json ca rend un dict
            print(f'\n Telegram sent: {response}')
        except Exception as e:
            print(f'error Tg: {e}')
            #print(f'error Tg : ', end=' '); print(e)
        return
#
    ###################
    #   Swap()
    ###################
    def Swap(self, quantiter):
    #
        #balance = web3.eth.get_balance(mywallet)
    #
    # Create token Instance for Token
        contract = lqtc.web3.eth.contract(address=PcsRouter, abi=pcs_abi)
        sellTokenContract = lqtc.web3.eth.contract(The_Token, abi=pcs_sell_Abi)  # Create token Instance for 11up
        nonce = lqtc.web3.eth.get_transaction_count(mywallet)
        #symbol = sellTokenContract.functions.symbol().call()
        #tokenValue2 = web3.from_wei(amount, 'ether')
    #
    # token approval pour le router PCS, a faire une fois
    #
    #    bal = 25000
    #    nonce = web3.eth.get_transaction_count(mywallet)
    #    balance = sellTokenContract.functions.balanceOf(mywallet).call() # Get Token Balance
    #    approve = sellTokenContract.functions.approve(PcsRouter,bal).build_transaction({'from': mywallet,'gasPrice': web3.to_wei('3','gwei'),'nonce': nonce,})
    #    signed_txn = web3.eth.account.sign_transaction(approve, private_key=mykey)
    #    tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    #    print("Token Approved ? : " + web3.to_hex(tx_token))
    #
        # Swaping
        estimated_gas = lqtc.web3.eth.estimate_gas({'from': mywallet})
        pancakeswap2_txn = contract.functions.swapExactTokensForETH(amount,
                    0,      # 0, ou specifié la quantiter minimal de BNB token voulue - consider decimals !!!
                    [The_Token, token_bnb],mywallet,(int(time()) +4)  #deadline en secondes, sinon revert la transac
                    ).build_transaction({'from': mywallet,'gasPrice': lqtc.web3.to_wei('3','gwei'),'nonce': nonce,})
#                    ).build_transaction({'from': mywallet,'gas':estimated_gas,'gasPrice': lqtc.web3.to_wei('3','gwei'),'nonce': nonce,})
        signed_txn = lqtc.web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=mykey)
        tx_token = lqtc.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print("Swap Hash: " + lqtc.web3.to_hex(tx_token))
        return
#
    ##################
    # maj
    ##################
    def maj(self):
    #
    # Setup getReserves ABI & Create Pair Contract Instance
        getReserves_abi = {"constant":"true","inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":"false","stateMutability":"view","type":"function"},{"constant":"true","inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":"false","stateMutability":"view","type":"function"},{"constant":"true","inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":"false","stateMutability":"view","type":"function"}
        pair_contract = lqtc.web3.eth.contract(address=Token_Pair, abi=getReserves_abi)
    # retourne en Gwei INT quantité des 2 token et le lqtc.TimeViewtime
        reserves = pair_contract.functions.getReserves().call() #Output: list[reserve0, reserve1, timestamp]
        Epoch = reserves[2]             # last blockchan event, Epoch time de pcs esr en secondes INT pas float
        Event = ctime(Epoch)       # last blockchan event, converti en time & date
        #print (Epoch,' -- ',Event)
    #
        if Event != lqtc.Event: # si nouveau epoch time event on met a jour le reste
            lqtc.Event = Event 
            token0 = pair_contract.functions.token0().call() #we dont know if token0 is bnb or token.
            if token0 == token_bnb:                         # check if reserve0 (token0) is token or bnb.
                pool_token = reserves[1]
                pool_bnb = reserves[0]
            else:
                pool_token = reserves[0]
                pool_bnb = reserves[1]
    # MANUEL "Human Readable" value
            value_pool_bnb = float(pool_bnb/(10**18)) #18 is bnb token decimals
            value_pool_token = float(pool_token/(10**18)) #18 is bnb token decimals
            #print (f'Token reserves, BNB: {value_pool_bnb:.2f}   11up: {value_pool_token:.2f}')
    # Get BNB price in USDT
            routerContract = lqtc.web3.eth.contract(address=PcsRouter, abi=pcs_swap_abi)
            oneToken = lqtc.web3.to_wei(1, 'Ether')
            price = routerContract.functions.getAmountsOut(oneToken, [token_bnb, USDT]).call()
            BNBPRICE = float(lqtc.web3.from_wei(price[1], 'Ether'))  #recup un float
            
            lqtc.prix = (value_pool_bnb/value_pool_token)*BNBPRICE   # calcul du prix du token
            lqtc.liqui = (value_pool_bnb*BNBPRICE)+(value_pool_token*lqtc.prix)   # liquiditée en usdt = poo1 + pool2
            #print (f' from maj: Prix: {lqtc.prix:.5f} USDT, liquidity: {lqtc.liqui:.0f}')
        return
#
##################
#           MAIN
##################
    def main(self):
        while True:
            lqtc.Connected = lqtc.web3.is_connected()   # check if still connected
            if lqtc.Connected is False:
                lqtc.DoConnect()
            #
            lqtc.maj()    # met a jour les valeurs du token et recup les vars
            #
            if lqtc.Event != lqtc.TimeViewOld:  # si un new event, on met a jour la var d'afficage
                lqtc.TimeViewOld = lqtc.Event   # sauve pour next loop
                lqtc.TimeView = lqtc.Event      # maj la var pour le display
            else:
                lqtc.TimeView = 'old event'  # sinon on met 'rien' dans la var pour l'affichage
#
#
            timeactu = int(time())         # on recup le time actuel en INT
#
# achete si condition prix & liqui ok, uniquement toute les 30 secs (le timer BUY empeche d'acheter toutes les 500 millis),
#                                                                                                       lqtc.onetime definit combien de fois on buy (onetime =1 par defaut)
#
            if (lqtc.prix >= lqtc.schedule) and (lqtc.liqui >= 10000) and ((timeactu - lqtc.timebaseBUY) >= 30) and (lqtc.onetime == 1):
            #
                BuyingTime = time()            #chope le temsp avant et apres swap pour voir le timing  
        #-------------
                lqtc.Swap(quantiter)
        #-------------
                BuyedTime = time()            #chope le temsp avant et apres swap pour voir le timing
                message = (f' {quantiter} {lqtc.NomToken} VENDU a {lqtc.prix:.5f}\n pcs-Time: {lqtc.TimeView}\n Buying-Epoch:{BuyingTime}\n Buyed-Epoch: {BuyedTime}')
                lqtc.Send_TG(message)
                print (message)
                lqtc.timebaseBUY = timeactu     # set le time actuel comme base pour next loop
#
                lqtc.onetime += 1                 # add 1 , on a fait le buy x fois (voir le IF)
#
# force send un message TG toute les X secs si liqui a 10000
#
            if (lqtc.liqui >= 10000) and ((timeactu - lqtc.timebaseTGV) >=20):    # msg toute les x SECS si liquiditée plus grand que
                message =(f' {lqtc.NomToken} Liquiditee: {lqtc.liqui:.2f}  prix: {lqtc.prix:.5f} pcs-Time: {lqtc.TimeView}')
                lqtc.Send_TG(message)
                print(message)
                lqtc.timebaseTGV = timeactu      # set le time actuel comme base pour next loop
#
# msg Tg toute les 180 minutes (10800)
#
            if (timeactu - lqtc.timebaseTG) >=10800:
                message =(f'{lqtc.NomToken}: liquidity = {lqtc.liqui:.2f}  prix = {lqtc.prix:.5f} pcs-Time: {lqtc.TimeView}') #\n BTC blocks {lqtc.responseBTC}')
                lqtc.Send_TG(message)
                lqtc.timebaseTG=timeactu
#
# msg en local toutes les 30 minutes (1800)
#
            if (timeactu - lqtc.timebasePRT) >=1800:     # msg  toute les 10 minutes (600)
                print (f' \n CTRL - C pour stop\n {lqtc.NomToken}: liquidity = {lqtc.liqui:.2f}  prix = {lqtc.prix:.5f} pcs-Time: {lqtc.TimeView}') #\n BTC blocks {lqtc.responseBTC}') #
                lqtc.timebasePRT=timeactu          #place le time actu dans timebasePRT pour prochain check
                #
#
            sleep(0.5) #pause en SECONDES
        return
#
    ##################
    #   INIT stuff
    ##################
    def init(self):
        lqtc.DoConnect()           
        # get Token name from contract
        sellTokenContract = lqtc.web3.eth.contract(The_Token, abi=pcs_sell_Abi)  # Create token Instance for 11up
        lqtc.NomToken = sellTokenContract.functions.symbol().call()
#
        lqtc.schedule = float(taux) # convert le taux de change en float. init ca ici car hors code lqtc is not defined
        return
#
    ##################
    # connect to chain
    ##################
    def DoConnect(self):          # gestion de reconnection: reesaye en doublant le temps chaque fois + msg user
        timeconnect = 30
        while True:     # simule une do while loop
            lqtc.web3 = Web3(Web3.HTTPProvider(bsc))    # web3 connection
            lqtc.Connected = lqtc.web3.is_connected()   # check result
            if lqtc.Connected is True:
            #if {lqtc.Connected == lqtc.web3.is_connected()} is True:   # check result
                message = (f'\n Init web3 connection, result is {lqtc.Connected}')
                print(message)
                lqtc.Send_TG(message)
                break
            timeconnect =  timeconnect * 2
            message = (f'\n Not connected, retrying in {timeconnect/60:.0f} minutes')
            print(message)
            lqtc.Send_TG(message)
            sleep(timeconnect) # en secs
        return
#
#
if __name__ == '__main__':
#
    lqtc = LQTC()   #instance
    lqtc.init()     #setup des trucs , une fois

    lqtc.main()     # go dans la boucle
#
#
#
# error check: python3 -m py_compile fichier.py
# compiler en EXE: pyinstaller -F --hide-console minimize-early .\LQTC_1.4.py
#
#version 1.52
# ajout de gestion de reconnection: reesaye en doublant le temps chaque fois + msg user
#
#version 1.51
# ajout fichier config
#
#version 1.5
# chope les infos de pancakeswap, pas des sites web, creation d'une Class
#------------------------------------------------------------------------
# le epoch de pancake est en INT
# epoch = int(time.time()) # le epoch de python est en Float x,y (x secondes) donc on convert en int.
# date = time.ctime(epoch) # python convertit en format txt date et heure
#
# -> bot pour connaitre son ID cht perso: https://t.me/get_myidbot
# prix gwei: https://tokentool.bitbond.com/gas-price/bsc
# https://bscscan.com/gastracker
#
#
