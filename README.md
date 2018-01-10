# awstest
Short Test of AWS DynamoDB Tables with Python.

Requires 'dbTableCreator.py' to be run intially providing a DynamoDB table is active through command line prompt prior, creating an instance of a DynamoDB table which historical LNG Prices will 
be added to. 'lngPriceRetrival' populates this table using data from .xls spreadsheet, owned by US Energy Information
Administration. 'analysis'.py has two functions, the first necessary to run, to determine which stock is being compared is 
'retrieve_stock_hist', which takes a string and returns nothing. Stocks must be entered in all capitals and Australian stocks
require '.AX' following their identifying code, eg; "CBA.AX".

Following the entry of a legitimate stock code, when 'lng_stock_analysis' is run it will return the beta and correlation 
values of the stock w.r.t. historical LNG prices. 'lng_stock_analysis' takes no arguments and returns nothing.

Code concerning the creation and querying of the AWS DynamoDB table was produced using aid from AWS "10 Minute Tutorials" 
available at https://aws.amazon.com/getting-started/tutorials/. 

Dependencies required:
  xlrd,
  AWS Python SDK (boto3),
  bs4 (BeautifulSoup),
  Requests
  
