from wxpy import *
from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import json

url="https://www.xiaoniu88.com/product/list"

headers={"Host": "www.xiaoniu88.com",
"Connection": "keep-alive",
"Content-Length": "75",
"Accept": "*/*",
"Origin": "https://www.xiaoniu88.com",
"X-Requested-With": "XMLHttpRequest",
"User-Agent":"******",
"Accept-Encoding": "gzip, deflate",
"Accept-Language": "zh-CN,zh;q=0.8"}

data={"type":"5",
      "termMode":"2",
      "pageNum":"1",
      "pageSize":"10",
      "tsfProfitSort":"0",
      "minTerm": "0",
      "maxTerm":"3"}
#参数pagenmu：页数 pagesize:每页条数 tsfprofitsort 0为让利高到低排序，1为低到高排序，minterm maxterm 为月份选择。

def message():
      r= requests.post(url=url,headers=headers,data=data)
      jsontext=r.text
      text=json.loads(jsontext)
      product_list=text["data"]["data"]
      for i in range(len(product_list)):
                name = product_list[i]["productName"]
                # 产品名称
                amount=product_list[i]["leftAmount"]
                #剩余金额
                remaining_time=product_list[i]["productTerm"]
                #剩余天数
                tsf_amount=product_list[i]["tsfProfitAmount"]
                #让利金额
                normal_rate=product_list[i]["annualRate"]
                #正常利率
                tsf_rate=product_list[i]["tsfProfitAmountRatio"]
                #让利比例
                repay=product_list[i]["repayModeEnum"]
                #还款方式参数，一次性还本付息：ONE_CAPITAL 先息后本：XXHB_CAPITAL 每月还本付息：MONTHLY_REPAY 按期还本付息：ONSCHEDULE_REPAY
                rate_year=round(tsf_rate/(remaining_time/365)*100,2)
                #计算年化收益率，因为我只爬取0-90天内的标，只算个大概就行，所以就没去区别还款方式了，还款方式不同年化计算也不同。
                if rate_year>50:
                      mess="产品名称："+name+"，剩余天数："+str(remaining_time)+"，剩余金额："+str(amount)+",让利比率为："+str(tsf_rate)+"，计算年化收益："+str(rate_year)+"%。"
                      #选取年化大于50%的标
                      return mess
                #else:
                      #print("暂时没有年化大于50%的产品")
                #return mess

def send_mess():
      my_friend=bot.friends().search("我还在")[0]
      text=message()
      my_friend.send(text)
      sleep(0.1)
      # bot.file_helper.send(text)
      #发送给文件传输助手

def my_scheduler():
      scheduler=BackgroundScheduler()
      scheduler.add_job(send_mess,"interval",minutes=5)
      #设置每隔五分钟执行一次
      scheduler.start()

if __name__=="__main__":
      bot=Bot()
      my_scheduler()
      embed()




