from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pprint
import time


def generate_codes(source,destination,date,all_flights):
    url = 'https://www.prokerala.com/travel/airports/india/'
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data,'html.parser')
    names=[]
    codes=[]

    airport_names = soup.findAll('a',{'class':'airport-name'})
    for airport_name in airport_names:
        names.append(airport_name.text)
    airport_codes = soup.findAll('td',{'class':'tc td-width-60'})
    for airport_code in airport_codes:
        codes.append(airport_code.text)
    all_flights = generate_url(source,destination,date,names,codes,all_flights)
    return all_flights


def return_code(airport,names,codes):
    count = 0
    all_airports = {}
    for name in names:
        all_airports[name.lower()] = codes[count]
        count += 2
    # airport = input('enter an airport').lower()
    ind = [i for i in all_airports if airport in i]
    return all_airports[ind[0]]


def get_formatted_date(date):
    datey = date[0:4]
    datem = date[5:7]
    dated = date[8:10]
    date = datey + '-' +datem + '-' +dated 
    return date


def generate_url(source,destination,date,names,codes,all_flights):
    source_code = return_code(source,names,codes)
    destination_code = return_code(destination,names,codes)
    date = get_formatted_date(date)
    # print('source is ',source,'destination is',destination)
    url ='https://www.paytm.com/flights/flightSearch/' + source_code +'-'+source + '/' + destination_code + '-' + destination   + '/1/0/0/E/'+ date 
    all_flights = browse(url,all_flights)
    return all_flights


def browse(url,all_flights):
    #driver = webdriver.Chrome(executable_path="C:\Projects\flight_booking\chromedriver.exe")
    driver = webdriver.Firefox(executable_path='C:\Projects\geckodriver.exe')
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(16)
    time.sleep(15)

    body = driver.find_element_by_tag_name("body").get_attribute("innerHTML")
    soup = BeautifulSoup(body, 'html.parser')

    

    flights = soup.findAll('div', {'class': '_3215 row'})

    print(flights)
    all_flights = find_flights(flights,all_flights,url)

    # all_flights = sorted(all_flights, key=lambda i: i['price'])
    # pprint.pprint(all_flights)
    # print(len(all_flights))
    driver.quit()
    return all_flights


def find_flights(flights,all_flights,url):
    for flight in flights:
        flag = 0
        flight_name= flight.find('div', {'class': '_3H-S _1Eia'}).text
        #print(flight_name)
        #flight_name = flight_name_temp.find('div',{'class' : 'u-uppercase u-text-ellipsis'}).text
        flight_code_temp = flight.find('div',{'class':'NqXj _2GoO'}).text
        # print('flight code temp is ',flight_code_temp)
        #flight_code_temp1 = flight_code_temp.findAll('div',{'class':'u-text-ellipsis'})
        # print('flight code temp 1 is ', flight_code_temp1)
        flight_code = ''
        for i in flight_code_temp:
            if i!=' ' and i!='-':
                flight_code+=i
        # print('flight code is ',flight_code)
        dept_time_temp = flight.find('div', {'class': '_3Lds _1OV0'})
        dept_time = dept_time_temp.find('div',{'class':'_3H-S'}).text

        #dept_time = dept_time_temp.find('div', {'class': 'time'}).text
        duration = flight.find('div',{'class':'vY4t'}).text
        duration = duration.replace('h','hr')
        duration = duration.replace('m','min')
        #print(duration,flight_code,dept_time)
        
        if 'h' not in duration:
            duration = "00 hr "+duration
        arr_time = flight.find('div', {'class': '_3H-S _1wD5'}).text
        arr_time = arr_time[:5]

        #arr_time = arr_time_temp.find('div', {'class': 'time'}).text
        price = flight.find('div',{'class':'_1cxG'}).text
        #price = price_temp.findAll('span')
        #price = price[1].text
        price = price.replace(',','')
        price = int(price)
        for i in all_flights:
            if (i['flight_name']).lower()==(flight_name).lower() and i['dept_time']==dept_time and i['arr_time']==arr_time:
                if int(price) < int(i['price']):
                    del all_flights[i]
                    all_flights.append({'flight_name':flight_name,'flight_code':flight_code,'dept_time':dept_time,'duration':duration,'arr_time':arr_time,'price':price,'website':"PAYTM",'website-URL':url})
                    # all_flights.append({'flight_name':flight_name,'flight_code':flight_code,'dept_time':dept_time,'duration':duration,'arr_time':arr_time,'price':price,'website':"IXIGO"})
                flag = 1
                break
        if flag == 0:
            all_flights.append({'flight_name': flight_name, 'flight_code': flight_code, 'dept_time': dept_time, 'duration': duration,'arr_time': arr_time, 'price': price, 'website': "PAYTM",'website-URL':url})
            # all_flights.append({'flight_name': flight_name, 'flight_code': flight_code, 'dept_time': dept_time, 'duration': duration,'arr_time': arr_time, 'price': price, 'website': "IXIGO"})
        # print("flight name is",flight_name,"flight code is",flight_code,"dept time is ",dept_time,"duration is",duration,"arrival is",arr_time,"price is",price)
    return all_flights


# generate_codes('vija','hydera','2020-04-20')