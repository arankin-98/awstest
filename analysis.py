from bs4 import BeautifulSoup as BS
from collections import OrderedDict

import boto3
import math
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import decimal
import requests

dynamodb = boto3.resource("dynamodb", region_name = "us-west-2", endpoint_url = "http://localhost:8000")
lngPrices = dynamodb.Table("Natural_Gas_Prices")

enumMonths = {
    "Jan." : 1,
    "Feb." : 2,
    "Mar." : 3,
    "Apr." : 4,
    "May." : 5,
    "Jun." : 6,
    "Jul." : 7,
    "Aug." : 8,
    "Sep." : 9,
    "Oct." : 10,
    "Nov." : 11,
    "Dec." : 12
    }

dates = []
historicalStockSet = OrderedDict()

def retrieve_stock_hist(stock):
    url = "https://au.finance.yahoo.com/quote/" + stock + "/history?p=" + stock
    page = requests.get(url)

    text = page.content
    page.close()
    soupInst = BS(text, "html.parser")
    inRead = soupInst.find_all("span")

    startMark = False
    dateTick = 0
    tempDate = ""
    tempClose = 0

    for line in inRead:
        if line.text == "Volume":
            startMark = True
        elif startMark == True:
            if dateTick == 0:
                tempSep = line.text.split()
                try:
                    float(tempSep[0])
                    tempSep[1] = str(enumMonths[tempSep[1]])
                    tempDate = ".".join(tempSep)
                    dates.append(tempDate)
                    dateTick += 1
                except ValueError:
                    break;
            elif dateTick == 5:
                tempClose = line.text
                dateTick += 1
            elif dateTick == 6:
                try:
                    historicalStockSet[tempDate] = float(tempClose)
                except ValueError:
                    break;
                dateTick = 0
                tempDate = ""
                tempClose = 0
            else:
                dateTick += 1
        
    for k, v in (historicalStockSet.items()):
        print("Date: " + str(k) + " Close: " + str(v))
    
    return

def lng_stock_analysis():
    lngStockDict = {}
    for date in dates:
        try:
            response = lngPrices.get_item(
                Key = {
                    "date": str(date)
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            lngItem = response['Item']
            tempDate = lngItem["date"]
            lngClose = lngItem["price"].split("(")[1]
            stockClose = historicalStockSet[tempDate]
            lngStockDict[tempDate] = [stockClose, lngClose]

    stockPerTot = 0
    lngPerTot = 0

    initDate = dates[0]
    stockPrev = lngStockDict[initDate][0]
    lngPrev = lngStockDict[initDate][1]
    stockPercentChange = []
    lngPercentChange =[]

    for i in range(1, len(lngStockDict)):
        stockPerTot += stockPercentChange[i - 1] = (lngStockDict[dates[i]][0] - stockPrev)/(stockPrev*100)
        lngPerTot += lngPercentChange[i - 1] = (lngStockDict[dates[i]][1] - lngPrev)/(lngPrev*100)
        stockPrev = lngStockDict[dates[i]][0]
        lngPrev = lngStockDict[dates[i]][1]
    
    stockPerAve = stockPerTot/(len(lngStockDict))
    lngPerAve = lngPerTot/(len(lngStockDict))

    stockVarTot = 0
    lngVarTot = 0
    covTot = 0
    
    for i in range(1, len(lngStockDict)):
        stockVarTot += (stockPercentChange[i - 1] - stockPerAve)**2
        lngVarTot += (lngPercentChange[i - 1] - lngPerAve)**2
        covTot += (stockPercentChange[i - 1] - stockPerAve)*(lngPercentChange[i - 1] - lngPerAve)


    stockVar = stockVarTot/(len(lngStockDict))
    lngVar = lngVarTot/(len(lngStockDict))
    covar = covTot/(len(lngStockDict) - 1)
    corr = covar/(sqrt(stockVar)*sqrt(lngVar))
    beta = covar/lngVar

    print("Stock-LNG Beta: " + beta + " Correlation: " + corr)
    return
