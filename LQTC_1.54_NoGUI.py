#
from os import path
import sys, json
from time import time, ctime, sleep, localtime, asctime
import requests
from web3 import Web3
#
#                   import private informations from LQTC_config.py file. its a .py file with YOUR PRIVATE INFORMATION INSIDE
#
import LQTC_configs
TgTOKEN, chat_id = LQTC_configs.TGtoken, LQTC_configs.TGchat_id           # import my telegram:  token & my chatids (search for TG botfather for how to)
mywallet, mykey = LQTC_configs.mywallet2, LQTC_configs.mykey2             # import my BSC wallet:  address & private key
The_Token, Token_Pair = LQTC_configs.TheToken, LQTC_configs.TokenPair     # import choosed token:  address & address of a pair for that token on pancakeswap
#
# ************* USER DEFINE VARIABLES *************
#
taux = "0.5"        # value of the token in usdt to trigger the swap.
quantiter = "20000" # number of token to swap. 
MaxSwap = 4         # Max swap , after we off
liquidity = 10000    # value of liquidity threshold
#
# *************************************************
#
token_bnb, USDT, bsc = LQTC_configs.token_bnb, LQTC_configs.USDT, LQTC_configs.bsc    #  BNB/wbnb Address & usdt token + the rpc adress
PcsRouter, PcsFactory, pcs_abi, pcs_swap_abi, pcs_sell_Abi = LQTC_configs.PcsRouter, LQTC_configs.PcsFactory, LQTC_configs.pcs_abi, LQTC_configs.pcs_swap_abi, LQTC_configs.pcs_sell_Abi
#
amount = int("".join([quantiter , "000000000000000000"]))   # concatenate strings (quantiter + virgul) + convert int
#
#
class LQTC:
    def __init__(self):
        self.web3, self.Event, self.Epoch, self.LastLiquMsg = 0, 0, 0, 0
        self.SwapCounter = 1
        self.SleepTimer = 20
        self.prix, self.liqui = 0, 0
        self.schedule, self.TimeView, self.TimeViewOld, self.NomToken, self.TxH  = '', '', '', '', '' #, '', ''
        self.Connected = False
        self.timebasePRT, self.timebaseBUY, self.timebaseMSG = int(time()), int(time()), int(time())    # initialize timers for msgs + buy time gap limit
#
    ###################
    #   Send_MSG()
    ###################
    def Send_MSG(self, local, tg, msg):
        if local == 1:
            print(msg)
        if tg == 1:
            url = (f"https://api.telegram.org/bot{TgTOKEN}/sendMessage?chat_id={chat_id}&text={msg}")
            try:
                response = requests.get(url)
                print(f'Telegram sent: {response} \n')
            except Exception as e:
                print(f'Telegram sent error: {e} \n')
        return
#
    ###################
    #   Swap()
    ###################
    def Swap(self, quantiter):
    #
    # Create token Instance for Token
        contract = lqtc.web3.eth.contract(address=PcsRouter, abi=pcs_abi)
        sellTokenContract = lqtc.web3.eth.contract(The_Token, abi=pcs_sell_Abi)
        nonce = lqtc.web3.eth.get_transaction_count(mywallet)
    # Swaping
        #estimated_gas = lqtc.web3.eth.estimate_gas({'from': mywallet})
        pancakeswap2_txn = contract.functions.swapExactTokensForETH(amount,
                    0,
                    [The_Token, token_bnb],mywallet,(int(time()) +4)        # deadline in secondes for the swap transaction
                    ).build_transaction({'from': mywallet,'gasPrice': lqtc.web3.to_wei('3','gwei'),'nonce': nonce,})
        signed_txn = lqtc.web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=mykey)
        tx_token = lqtc.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        lqtc.TxH = lqtc.web3.to_hex(tx_token)                               # save transaction hash ID, no returned value or 0 if transaction fail ?
        return
#
    ##################
    # maj
    ##################
    def maj(self):
    #
    # Setup getReserves ABI & Create Pair Contract Instance
        getReserves_abi = {"constant":"true","inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":"false","stateMutability":"view","type":"function"},{"constant":"true","inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":"false","stateMutability":"view","type":"function"},{"constant":"true","inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":"false","stateMutability":"view","type":"function"}
        try:
            pair_contract = lqtc.web3.eth.contract(address=Token_Pair, abi=getReserves_abi)
            reserves = pair_contract.functions.getReserves().call()     # get epoch time & the amount of the 2 token (in Gwei INT) 
            Epoch = reserves[2]                                     # last blockchan event from pcs (Epoch time in secs INT no float)
            Event = ctime(Epoch)                                    # convert it to human time & date
        #
            if Event != lqtc.Event:     # new epoch time ? update datas.
                lqtc.Event = Event      # save for next loop
                token0 = pair_contract.functions.token0().call() # we dont know if token0 is bnb or token.
                if token0 == token_bnb:                          # check if reserve0 (token0) is token or bnb.
                    pool_token = reserves[1]
                    pool_bnb = reserves[0]
                else:                                               # get right token in right variable
                    pool_token = reserves[0]
                    pool_bnb = reserves[1]
        # make "Human Readable" pool value
                value_pool_bnb = float(pool_bnb/(10**18))       # convert value, 18 is bnb token decimals
                value_pool_token = float(pool_token/(10**18))   # convert value, 18 is bnb token decimals
        # Get BNB price in USDT
                routerContract = lqtc.web3.eth.contract(address=PcsRouter, abi=pcs_swap_abi)
                oneToken = lqtc.web3.to_wei(1, 'Ether')
                price = routerContract.functions.getAmountsOut(oneToken, [token_bnb, USDT]).call()
                BNBPRICE = float(lqtc.web3.from_wei(price[1], 'Ether'))     # convert value
        # compute token price & liquidity
                lqtc.prix = (value_pool_bnb/value_pool_token)*BNBPRICE                  # compute token price
                #lqtc.liqui = (value_pool_bnb*BNBPRICE)                               # BNB liquidity in usdt = pool 1
                lqtc.liqui = (value_pool_bnb*BNBPRICE)+(value_pool_token*lqtc.prix)     # OR Both liquidity in usdt = poo1 + pool2

        except Exception as e:
            message = (f'There is problem to get contract infos :\n {e}\n Local GmT {asctime(localtime())} \n')
            lqtc.Send_MSG(1,1,message)            
        return
#
##################
#           MAIN
##################
    def main(self):
        while True:
            lqtc.Connected = lqtc.web3.is_connected()   # check if still connected
            if lqtc.Connected is False:
                message = (f'Web3 connect is {lqtc.Connected}, reconnecting \n Local GmT {asctime(localtime())} \n')
                lqtc.Send_MSG(1,1,message)  # send msg cause we r disconnected
                
                lqtc.DoConnect()
                
                message =(f'Reconnected, last datas was: \n {lqtc.Gmessage} ')
                lqtc.Send_MSG(1,1,message)
            #
            lqtc.maj()      # update token datas
            #
            if lqtc.Event != lqtc.TimeViewOld:  # new event so update msgs timers
                lqtc.TimeViewOld = lqtc.Event   # save for next loop
                lqtc.TimeView = (f'{lqtc.Event}')    # update message time data
                Gmessage =(f'{lqtc.NomToken} Liquidity: {lqtc.liqui:.0f} price: {lqtc.prix:.4f} \n pcsTime: {lqtc.TimeView} GMT\n') # need to manual update generic message
                lqtc.Send_MSG(1,1,Gmessage)     # there is a change send msg despite of timers
            else:
                lqtc.TimeView = (f'-OLD- ') # {lqtc.Event}')  # no new event
                Gmessage =(f'{lqtc.NomToken} Liquidity: {lqtc.liqui:.0f} price: {lqtc.prix:.4f} \n pcsTime: {lqtc.TimeView} GMT\n') # need to manual update generic message
                #lqtc.Send_MSG(1,1,Gmessage)
#
            timeactu = int(time())         # get actual time in INT
#
# swap if price & liqui ok, but only every X secs gap (timer timebaseBUY -> for no swap each loop of 500 millis)
#           MaxSwap define quantity of swap and after that its off, default=4 (lqtc.SwapCounter compare to MaxSwap)
#
            if (lqtc.prix >= lqtc.schedule) and (lqtc.liqui >= liquidity) and ((timeactu - lqtc.timebaseBUY) >= 50) and (lqtc.SwapCounter <= MaxSwap):
            #
                BuyingTime = time()            # get time before and after swap, to see the timing   
        #-------------
                lqtc.Swap(quantiter)        # swap amount of token, (quantiter default=20000)
        #-------------
                BuyedTime = time()            # get time before and after swap, to see the timing
 
                message = (f'{quantiter} {lqtc.NomToken} SWAPED in {BuyedTime - BuyingTime:.3f} secs, swap {lqtc.SwapCounter} of {MaxSwap} Max \n TxH: {lqtc.TxH} \n') #{Gmessage} )
                lqtc.Send_MSG(1,1,message)
                lqtc.timebaseBUY = timeactu     # set actual time as ref at next loop
                lqtc.SwapCounter += 1               # add 1 , we will swap X time (see IF header infos). default=1
                lqtc.LastLiquMsg = 1            # set flag for "liquidity is high"
                lqtc.SleepTimer = 0.5            # set sleep timer to high check
#
# send messages if liquity has been down , but was up last loop. and set lqtc.sleeptimer for low check
#
            if (lqtc.liqui < liquidity) and (lqtc.LastLiquMsg == 1):    # if actual liquidity is low and flag is on mean last loop it was high liquidity
                lqtc.Send_MSG(1,1,Gmessage)
                lqtc.SleepTimer = 20            # set sleep timer to low check
                lqtc.LastLiquMsg = 0        # reset the flag for "liquidity is high"
#
# send messages every x secs if liquidy +10000 . OR by default every 3h (3h=10800) , act also like a 'keep alive msg' 
#
            if ((lqtc.liqui >= liquidity) and ((timeactu - lqtc.timebaseMSG) >=25)) or (timeactu - lqtc.timebaseMSG) >=10800:
                lqtc.Send_MSG(1,1,Gmessage)
                lqtc.timebaseMSG = timeactu      # set actual time as ref at next loop
#
# always msg to shell every x secs (10m=600) (30m=1800) (3h=10800) act also like a 'keep alive msg' 
#
            if (timeactu - lqtc.timebasePRT) >=3600:
                message= (f'CTRL - C for stop \n {Gmessage} Local GmT {asctime(localtime())} \n')
                lqtc.Send_MSG(1,0,message)
                lqtc.timebasePRT=timeactu       # set actual time as ref at next loop
                #
#
            sleep(lqtc.SleepTimer) #pause in SECONDES and restart the loop (default 20 secs, and 0.5 if high liquidity)
        return
#
    ##################
    #   INIT stuff
    ##################
    def init(self):
    # connect to 
        lqtc.DoConnect()           
    # get Token name 
        sellTokenContract = lqtc.web3.eth.contract(The_Token, abi=pcs_sell_Abi)  # get token info from contract sell abi
        lqtc.NomToken = sellTokenContract.functions.symbol().call()              # get Token name from contract
#
        lqtc.schedule = float(taux)     # convert token swap trigger value in float.
        
        #lqtc.maj()    # init token datas FIRST TIME
        #lqtc.TimeView = (f'{lqtc.Event}') # init timeview value
        return
#
    ##################
    # connect to chain
    ##################
    def DoConnect(self):          # managing re-connection: retrying with bigger waiting (x2) + msg user
        timeconnect = 30
        while True:     # like a do while loop
            lqtc.web3 = Web3(Web3.HTTPProvider(bsc))    # web3 connection
            lqtc.Connected = lqtc.web3.is_connected()   # check result
            if lqtc.Connected is True:
                message = (f'Init web3 connection, result is {lqtc.Connected} \n LocalTime GmT {asctime(localtime())} \n')
                lqtc.Send_MSG(1,1,message)
                break                   # break the while loop
            else:
                timeconnect =  timeconnect * 2
                message = (f'Not connected, retrying in {timeconnect/60:.0f} minutes \n')
                lqtc.Send_MSG(1,1,message)      #  send to Tg we r disconnected
                sleep(timeconnect)          # secs
        return
#
#
if __name__ == '__main__':
#
    lqtc = LQTC()   #instance
    lqtc.init()     #setup

    lqtc.main()     # go loop
#
#
#
# compilation error check: python3 -m py_compile fichier.py
# compile to EXE: pyinstaller -F --hide-console minimize-early .\LQTC_1.4.py
#
#version 1.54
# somes opti/cleaning
# add dynamic sleep, between loop is 20secs by defaut, 0.5 sec when there is liquidity
# add a send msg direct after a new BChain event change

#version 1.53
# add maxswap counter/limit, txh in msg, msg after liquidity has been removed 
# + littles optis like msg function with Send_MSG(local, tg, msg) options

#version 1.52
# add re-connection managing : each retry is 2x longer, first is half minute + msg user
#
#version 1.51
# add config file
#
#version 1.5
# get  infos from pancakeswap, no more web site API, creation of class
#------------------------------------------------------------------------
# pancake epoch = INT
# epoch = int(time.time()) # epoch of python = Float x,y (x secs) so convert to int.
# date = time.ctime(epoch) # python convert in txt format date et time
#
# -> bot to know your chat ID : https://t.me/get_myidbot
# prix gwei: https://tokentool.bitbond.com/gas-price/bsc
# https://bscscan.com/gastracker
#
#
