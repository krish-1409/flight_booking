from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pprint
import time


def generate_codes(source,destination,date,all_flights):

    url ='https://www.prokerala.com/travel/airports/india/'
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
    date = dated + '/' + datem + '/' + datey
    return date


def generate_url(source,destination,date,names,codes,all_flights):
    source = return_code(source,names,codes)
    destination = return_code(destination,names,codes)
    date = get_formatted_date(date)
    # print('source is ',source,'destination is',destination)
    url = "https://www.makemytrip.com/flight/search?itinerary=" + source + "-" + destination + "-" + date + "&tripType=O&paxType=A-1_C-0_I-0&intl=false&=&cabinClass=E"
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

    flights = soup.findAll('div', {'class': 'dept-options-section clearfix'})
    all_flights = find_flights(flights,all_flights,url)

    # all_flights = sorted(all_flights, key=lambda i: i['price'])
    # pprint.pprint(all_flights)
    # print(len(all_flights))
    driver.close()
    return all_flights


def find_flights(flights,all_flights,url):
    for flight in flights:
        price_int = ''
        flight_name = flight.find('span', {'class': 'airways-name'}).text
        flight_code = flight.find('p', {'class': 'fli-code'}).text
        dept_time = flight.find('div', {'class': 'dept-time'}).text
        duration = flight.find('p', {'class', "fli-duration"}).text
        if 'h' not in duration:
            duration =  "00 hr "+duration
        arr_time = flight.find('p', {'class', "reaching-time append_bottom3"}).text
        arr_time = arr_time[:5]
        price = flight.find('span', {'class': 'actual-price'}).text
        for i in price:
            if i.isdigit():
                price_int+=i
        price_int = int(price_int)
        all_flights.append({'flight_name':flight_name,'flight_code':flight_code,'dept_time':dept_time,'duration':duration,'arr_time':arr_time,'price':price_int,'website':'MAKE-MY-TRIP','website-URL':url})
        # all_flights.append({'flight_name':flight_name,'flight_code':flight_code,'dept_time':dept_time,'duration':duration,'arr_time':arr_time,'price':price_int,'website':'MAKE-MY-TRIP'})
        # all_flights[flight_code] = [flight_name, dept_time, duration, arr_time, price]
        # print("flight name is",flight_name,"flight code is",flight_code,"dept time is ",dept_time,"duration is",duration,"arrival is",arr_time,"price is",price)
    return all_flights

