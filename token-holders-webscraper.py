import requests
from bs4 import BeautifulSoup
import csv
import time
from selenium import webdriver

RESULTS = "results.csv"
TOKEN_CONTRACT = "0x8d2bffcbb19ff14a698c424fbcdcfd17aab9b905"
URL = "https://etherscan.io/token/generic-tokenholders2?a=" + TOKEN_CONTRACT + "&s=0&p="

def getData(sess, page):
    url = URL + page
    print("Retrieving page", page)
    soup = BeautifulSoup(sess.get(url).text, 'html.parser')
    
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(3)

    html = browser.page_source
    soup = BeautifulSoup(html, "lxml")

    browser.close()

    return soup

def getPage(sess, page):
    table = getData(sess, str(int(page))).find('table')

    try:
        data = [[X.text.strip() for X in row.find_all('td')] for row in table.find_all('tr')]
    except Exception as e: 
        print(e)
    finally:
        return data

def main():
    resp = requests.get(URL)
    sess = requests.Session()

    with open(RESULTS, 'w', newline='') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        wr.writerow(map(str, "Rank Address Quantity Percentage".split()))
        page = 0
        while True:
            page += 1
            data = getPage(sess, page)

            if len(data[1]) == 1:
                break
            else:
                for row in data:
                    if len(row) != 0:
                        wr.writerow(row)
                time.sleep(1)

if __name__ == "__main__":
    main()
