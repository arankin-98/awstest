import datetime, xlrd
import decimal
import requests
from collections import OrderedDict
import boto3

dynamodb = boto3.resource("dynamodb", region_name = "us-west-2", endpoint_url = "http://localhost:8000")
table = dynamodb.Table("Natural_Gas_Price")


downloadSheet = requests.get("https://www.eia.gov/dnav/ng/hist_xls/RNGWHHDd.xls")
savedSheet = open("lng_prices.xls", "wb")
savedSheet.write(resp.content)
savedSheet.close()

workbook = xlrd.open_workbook("lng_prices.xls")
prices_sheet = workbook.sheet_by_name("Data 1")
historicalGasSet = OrderedDict()

for cells in range(3, 5286):
    
    date = prices_sheet.cell_value(cells,0)
    dateForm = datetime.datetime(*xlrd.xldate_as_tuple(date, workbook.datemode))

    arrFormDate = str(dateForm).split()
    reducedDate = arrFormDate[0].split("-")

    saveDate = ".".join(list(reversed(reducedDate)))
    historicalGasSet[saveDate] = prices_sheet.cell_value(cells,1)
        

for k,v in (historicalGasSet.items()):

    table.put_item(
        Item = {
            "date": (str(k)),
            "price": (Decimal(str(v))),
        }
    )
