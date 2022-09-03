# URLs
Sale_URL ='https://www.britishairways.com/en-gb/offers/sale'
Flight_URL = 'https://www.britishairways.com/travel/book/public/en_gb/flightList?onds=LHR-DEN_2023-02-13,DEN-LHR_2023-02-16&ad=1&yad=0&ch=0&inf=0&cabin=J&flex=LOWEST&ond=1'
Flight_URL_ECON = 'https://www.britishairways.com/travel/book/public/en_gb/flightList?onds=LHR-DEN_2023-02-13,DEN-LHR_2022-02-16&ad=1&yad=0&ch=0&inf=0&cabin=M&flex=LOWEST&ond=1'
Sale_URL = 'https://www.britishairways.com/en-gb/offers/sale'
Title = 'British Airways Price Scanner'
database = '/home/nuc/BritishAirways/BA.db'
OP = '/home/nuc/BritishAirways/Outbound_Price.png'
IP = '/home/nuc/BritishAirways/Inbound_Price.png'
SALE = '/home/nuc/BritishAirways/Sale.png'
ERROR = '/home/nuc/BritishAirways/ERROR.png'

import pyautogui
import sys
import os
import cv2
import pytesseract
import sqlite3
from datetime import datetime
from time import sleep
from random import randint
from sqlite3 import Error

# Signal numbers
SRC = "+############"
DST = "+############"

def get_sale():
    try:
        # Click mouse - sale tab
        pyautogui.click(666,44)

        sleep(1)

        # Click mouse - Refresh
        pyautogui.click(160,82)

        sleep(10)

        # Take screenshot and save
        Sale_page = pyautogui.screenshot(region=(378,105,1218,807))
        Sale_page.save(SALE)

        # send signal message
        msg = 'Sale Page'
        send_signal(SRC,DST,msg,SALE)

        # delete sale image
        os.remove(SALE)
    except:
        return

    return

def get_data_economy():
    # create worked
    worked = False

    # Timestamps
    timestamp = int(datetime.timestamp(datetime.now()))

    try:
        # Click mouse - flight economy tab
        pyautogui.click(430,44)

        sleep(1)

        # Click mouse - Refresh
        pyautogui.click(160,82)

        sleep(10)

        # Screenshots
        Outbound_Price = pyautogui.screenshot(region=(995,689,80,50))
        Outbound_Price.save(OP)

        # select economy
        pyautogui.click(1051,717)

        sleep(2)

        # select economy again
        pyautogui.click(668,1094)

        sleep(10)

        # Screenshot
        #Inbound_Route = pyautogui.screenshot(region=(495,635,500,157))
        Inbound_Price = pyautogui.screenshot(region=(1300,635,200,157))
        #Inbound_Route.save(IR)
        Inbound_Price.save(IP)

        # Load Images
        Outbound_Price_CV = cv2.imread(OP)
        Inbound_Price_CV = cv2.imread(IP)

        # Process Images
        Outbound_Price_CV = cv2.cvtColor(Outbound_Price_CV, cv2.COLOR_BGR2GRAY)
        Outbound_Price_CV = cv2.bitwise_not(Outbound_Price_CV)
        Outbound_Price_Result = pytesseract.image_to_string(Outbound_Price_CV)

        #Inbound_Route_Result = pytesseract.image_to_string(Inbound_Route_CV)
        Inbound_Price_CV = cv2.cvtColor(Inbound_Price_CV, cv2.COLOR_BGR2GRAY)
        Inbound_Price_CV = cv2.bitwise_not(Inbound_Price_CV)
        Inbound_Price_Result = pytesseract.image_to_string(Inbound_Price_CV)

        # Process Text
        outbound = int(Outbound_Price_Result.strip().strip('£').replace(',',''))
        inbound = int(Inbound_Price_Result.strip().strip('£').replace(',',''))
        total = outbound + inbound

        worked = True
    except:
        worked = False

    if worked:
        msg = {
            'timestamp': timestamp,
            'class': 'economy',
            'outbound': outbound,
            'inbound': inbound,
            'total': int(total)
            }
        with open('/home/nuc/BritishAirways/log.txt', 'a') as f:
            f.write(f'{msg}\r\n')
    else:
        msg = {
            'timestamp': timestamp
            }
        with open('/home/nuc/BritishAirways/log.txt', 'a') as f:
            f.write(f'{msg}\r\n')

    # Clean up images
    os.remove(OP)
    os.remove(IP)

    return msg,worked

def get_data_business():
    # create worked
    worked = False

    # Timestamps
    timestamp = int(datetime.timestamp(datetime.now()))

    try:
        # Click mouse - flight tab
        pyautogui.click(184,44)

        sleep(1)

        # Click mouse - Refresh
        pyautogui.click(160,82)

        sleep(10)

        # Screenshots
        Outbound_Price = pyautogui.screenshot(region=(1300,635,200,157))
        Outbound_Price.save(OP)

        pyautogui.click(1162,712)

        sleep(2)

        pyautogui.click(679,1101)

        sleep(10)

        # Screenshot
        Inbound_Price = pyautogui.screenshot(region=(1300,635,200,157))
        Inbound_Price.save(IP)

        # Load Images
        Outbound_Price_CV = cv2.imread(OP)
        Inbound_Price_CV = cv2.imread(IP)

        # Process Images
        Outbound_Price_CV = cv2.cvtColor(Outbound_Price_CV, cv2.COLOR_BGR2GRAY)
        Outbound_Price_CV = cv2.bitwise_not(Outbound_Price_CV)
        Outbound_Price_Result = pytesseract.image_to_string(Outbound_Price_CV)

        Inbound_Price_CV = cv2.cvtColor(Inbound_Price_CV, cv2.COLOR_BGR2GRAY)
        Inbound_Price_CV = cv2.bitwise_not(Inbound_Price_CV)
        Inbound_Price_Result = pytesseract.image_to_string(Inbound_Price_CV)

        # Process Text
        outbound = int(Outbound_Price_Result.strip().strip('£').replace(',',''))
        inbound = int(Inbound_Price_Result.strip().strip('£').replace(',',''))
        total = outbound + inbound

        worked = True
    except:
        worked = False

    if worked:
        msg = {
            'timestamp': timestamp,
            'class': 'business',
            'outbound': outbound,
            'inbound': inbound,
            'total': int(total)
            }
        with open('/home/nuc/BritishAirways/log.txt', 'a') as f:
            f.write(f'{msg}\r\n')
    else:
        msg = {
            'timestamp': timestamp
            }
        with open('/home/nuc/BritishAirways/log.txt', 'a') as f:
            f.write(f'{msg}\r\n')

    # Clean up images
    os.remove(OP)
    os.remove(IP)

    return msg,worked

def send_signal(src,dst,msg,attachment):
    os.system(f'signal-cli --config /home/nuc/.local/share/signal-cli -u {src} send -m "{msg}" {dst} -a {attachment} > /dev/null 2>&1')

def create_connection(database):
    conn = None
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print(e)

    return conn

def write_query_prices(conn, data):
    cur = conn.cursor()

    sql = f'''SELECT * FROM Prices WHERE class = '{data["class"]}' ORDER BY id DESC LIMIT 1'''
    cur.execute(sql)
    previous_price = cur.fetchone()

    sql = f'''INSERT INTO Prices
                          (timestamp, class, outbound, inbound, total)
                           VALUES
                          ({data["timestamp"]},'{data["class"]}',{data["outbound"]},{data["inbound"]},{data["total"]})'''

    cur.execute(sql)
    conn.commit()

    return previous_price[5]

def main():
    conn = create_connection(database)
    counter = 0
    failure = 0

    while True:
        # Update counter
        counter += 1

        # Sleep between 2 and 5 minutes
        sleep(randint(120,300))

        # get data
        data_business,business_worked = get_data_business()
        data_economy,economy_worked = get_data_economy()

        # get data failed so try again!
        if not business_worked or not economy_worked:
            failure += 1
            if failure == 5:
                try:
                    Error_Screenshot = pyautogui.screenshot()
                    Error_Screenshot.save(ERROR)

                    msg_time = datetime.fromtimestamp(data_economy['timestamp']).strftime('%H:%M:%S %d-%m-%Y')
                    msg = f'Failure: {counter}\r\nTime: {msg_time}\r\nBusiness: {business_worked}\r\nEconomy: {economy_worked}'
                    send_signal(SRC,DST,msg,ERROR)

                    os.remove(ERROR)
                    failure = 0
                except:
                    msg = f'Serious Failure'
                    send_signal(SRC,DST,msg,ERROR)

            continue

        with conn:
            previous_business_price = write_query_prices(conn, data_business)
            previous_economy_price = write_query_prices(conn, data_economy)

        if data_business['total'] != previous_business_price or data_economy['total'] != previous_economy_price:
            business_time = datetime.fromtimestamp(data_business["timestamp"]).strftime("%H:%M:%S %d-%m-%Y")
            economy_time = datetime.fromtimestamp(data_business["timestamp"]).strftime("%H:%M:%S %d-%m-%Y")
            msg = f'PRICE CHANGE\r\nTime: {business_time}\r\nClass: {data_business["class"].title()}\r\nOutbound: £{data_business["outbound"]}\r\nInbound: £{data_business["inbound"]}\r\nTotal: £{data_business["total"]} (£{previous_business_price})\r\n\r\nTime: {economy_time}\r\nClass: {data_economy["class"].title()}\r\nOutbound: £{data_economy["outbound"]}\r\nInbound: £{data_economy["inbound"]}\r\nTotal: £{data_economy["total"]} (£{previous_economy_price})'

            send_signal(SRC,DST,msg,'')
        else:
            if counter % 500 == 0:
                business_time = datetime.fromtimestamp(data_business["timestamp"]).strftime("%H:%M:%S %d-%m-%Y")
                economy_time = datetime.fromtimestamp(data_business["timestamp"]).strftime("%H:%M:%S %d-%m-%Y")
                msg = f'SCHEDULED\r\nTime: {business_time}\r\nClass: {data_business["class"].title()}\r\nOutbound: £{data_business["outbound"]}\r\nInbound: £{data_business["inbound"]}\r\nTotal: £{data_business["total"]} (£{previous_business_price})\r\n\r\nTime: {economy_time}\r\nClass: {data_economy["class"].title()}\r\nOutbound: £{data_economy["outbound"]}\r\nInbound: £{data_economy["inbound"]}\r\nTotal: £{data_economy["total"]} (£{previous_economy_price})'
                send_signal(SRC,DST,msg,'')

                get_sale()

if __name__ == '__main__':
    main()
