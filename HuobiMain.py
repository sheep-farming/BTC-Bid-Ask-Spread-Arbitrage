#coding=utf-8

'''
本程序在 Python 3.3.0 环境下测试成功
使用方法：python HuobiMain.py
'''

from Util import *
import HuobiService
import threading #导入threading包
import time
from time import sleep
amount="0.005"
c=0
ping=0
canned=0

Trade_Pass='YOUR TRADING PASSWORD HERE'
def sellit(sellat):
    print ("限价卖出:"+str(sellat))
    print (HuobiService.sell(1,str(sellat),amount,Trade_Pass,None,SELL))
def buyit(buyat):
    print ("限价买入:"+str(buyat))
    print (HuobiService.buy(1,str(buyat),amount,Trade_Pass,None,BUY))

if __name__ == "__main__":
    #print("获取所有正在进行的委托")
    print(HuobiService.getOrders(1,GET_ORDERS))
    while(1):
        sleep(0.3)
        price=HuobiService.getPrice()
        price=eval(price)
        ticker=price['ticker']
        sell=round(ticker['sell'],2)
        buy=round(ticker['buy'],2)
        print('Ask:'+str(sell))
        print('Bid:'+str(buy))
        sellat=round(sell-0.02,2)
        buyat=round(buy+0.02,2)
        spread=(sell*100-buy*100)/100
        print('Spread:'+str(spread))
        ordStatus=HuobiService.getOrders(1,GET_ORDERS)
        if(str(ordStatus)=='[]'):
            if spread>=0.15 and spread<=1:
                c=c+1
                print(c);
                if c>=3:
                    c=0

                    sellit(sellat)
                    buyit(buyat)
                    if False:
                        threads=[]
                        t1=threading.Thread(target=sellit, args=(sellat,))
                        threads.append(t1)
                        t2=threading.Thread(target=buyit, args=(buyat,))
                        threads.append(t2)
                        threads[0].start
                        threads[1].start
                        threads[0].join
                        threads[1].join
                        sleep(1)

                    while(1):
                        sleep(1)
                        ordStatus=HuobiService.getOrders(1,GET_ORDERS)
                        print(ordStatus)
                        if(str(ordStatus)=='[]'):
                            print("Done!")
                            c=0
                            ping=0
                            canned=0
                            break
                        ping=ping+1
                        if ping>=5:
                            if canned>=100:
                                price=HuobiService.getPrice()
                                price=eval(price)
                                ticker=price['ticker']
                                sell=round(ticker['sell'],2)
                                buy=round(ticker['buy'],2)
                                print('Ask:'+str(sell))
                                print('Bid:'+str(buy))
                                sellat=round(sell-0.11,2)
                                buyat=round(buy+0.11,2)
                            canned=canned+1
                            print('CANCEL')
                            ping=0
                            ordFeedback=eval(ordStatus)
                            if len(ordFeedback)==2:
                                print('取消买卖订单')
                                print (HuobiService.cancelOrder(1,ordFeedback[1]['id'],CANCEL_ORDER))
                                print (HuobiService.cancelOrder(1,ordFeedback[0]['id'],CANCEL_ORDER))
                            if len(ordFeedback)==1:
                                '''
                                ordType=ordFeedback[0]['type']
                                print (HuobiService.cancelOrder(1,ordFeedback[0]['id'],CANCEL_ORDER))
                                if ordType==1:
                                    print (HuobiService.buy(1,str(sellat),amount,Trade_Pass,None,BUY))
                                else:
                                    print (HuobiService.sell(1,str(buyat),amount,Trade_Pass,None,SELL))
                                '''


            else:
                c=0
        else:
            print(ordStatus)
            ping=ping+1
            if ping>=10:
                print('CANCEL')
                ping=0
                ordFeedback=eval(ordStatus)
                if len(ordFeedback)==2:
                    print('取消买卖订单')
                    print (HuobiService.cancelOrder(1,ordFeedback[0]['id'],CANCEL_ORDER))
                    print (HuobiService.cancelOrder(1,ordFeedback[1]['id'],CANCEL_ORDER))
                if len(ordFeedback)==1:
                    ordType=ordFeedback[0]['type']
                    print (HuobiService.cancelOrder(1,ordFeedback[0]['id'],CANCEL_ORDER))
                    if ordType==1:
                        print (HuobiService.buy(1,str(buyat),amount,Trade_Pass,None,BUY))
                    else:
                        print (HuobiService.sell(1,str(sellat),amount,Trade_Pass,None,SELL))

