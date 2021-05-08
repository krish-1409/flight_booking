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
    date = dated + datem + datey
    return date


def generate_url(source,destination,date,names,codes,all_flights):
    source = return_code(source,names,codes)
    destination = return_code(destination,names,codes)
    date = get_formatted_date(date)
    # print('source is ',source,'destination is',destination)
    url = "https://www.ixigo.com/search/result/flight/" + source + "/" + destination + "/" + date + "//1/0/0/e?source=Search%20Form"
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

    flights = soup.findAll('div', {'class': 'summary-section'})
    all_flights = find_flights(flights,all_flights,url)

    # all_flights = sorted(all_flights, key=lambda i: i['price'])
    # pprint.pprint(all_flights)
    # print(len(all_flights))
    driver.quit()
    return all_flights


def find_flights(flights,all_flights,url):
    for flight in flights:
        flag = 0
        flight_name_temp = flight.find('a', {'class': 'flight-name'})
        flight_name = flight_name_temp.find('div',{'class' : 'u-uppercase u-text-ellipsis'}).text
        flight_code_temp = flight.find('div',{'class':'u-text-ellipsis'})
        # print('flight code temp is ',flight_code_temp)
        flight_code_temp1 = flight_code_temp.findAll('div',{'class':'u-text-ellipsis'})
        # print('flight code temp 1 is ', flight_code_temp1)
        flight_code = flight_code_temp1[1].text
        # print('flight code is ',flight_code)
        dept_time_temp = flight.find('div', {'class': 'left-wing'})
        dept_time = dept_time_temp.find('div', {'class': 'time'}).text
        duration_temp = flight.find('div',{'class':'c-timeline-wrapper horizontal'})
        duration = duration_temp.find('div', {'class', "label tl"}).text
        if 'h' not in duration:
            duration = "00 hr "+duration
        arr_time_temp = flight.find('div', {'class': 'right-wing'})
        arr_time = arr_time_temp.find('div', {'class': 'time'}).text
        price_temp = flight.find('div',{'class':'c-price-display u-text-ellipsis'})
        price = price_temp.findAll('span')
        price = price[1].text
        price = int(price)
        for i in all_flights:
            if (i['flight_name']).lower()==(flight_name).lower() and i['dept_time']==dept_time and i['arr_time']==arr_time:
                if int(price) < int(i['price']):
                    del all_flights[i]
                    all_flights.append({'flight_name':flight_name,'flight_code':flight_code,'dept_time':dept_time,'duration':duration,'arr_time':arr_time,'price':price,'website':"IXIGO",'website-URL':url})
                    # all_flights.append({'flight_name':flight_name,'flight_code':flight_code,'dept_time':dept_time,'duration':duration,'arr_time':arr_time,'price':price,'website':"IXIGO"})
                flag = 1
                break
        if flag == 0:
            all_flights.append({'flight_name': flight_name, 'flight_code': flight_code, 'dept_time': dept_time, 'duration': duration,'arr_time': arr_time, 'price': price, 'website': "IXIGO",'website-URL':url})
            # all_flights.append({'flight_name': flight_name, 'flight_code': flight_code, 'dept_time': dept_time, 'duration': duration,'arr_time': arr_time, 'price': price, 'website': "IXIGO"})
        # print("flight name is",flight_name,"flight code is",flight_code,"dept time is ",dept_time,"duration is",duration,"arrival is",arr_time,"price is",price)
    return all_flights


# generate_codes('vija','hydera','2020-04-20')