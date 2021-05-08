from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from flights.forms import FlightSearchForm
from django.contrib import messages
from flight_booking.scrapy import generate_codes as mgc
from flight_booking.ixigo import generate_codes as igc
from flight_booking.paytm import generate_codes as pay

source = ''
destination = ''
date = ''
order=''

name = 'lanka'
all_flights = []


def home(request):
    return render(request,'flights/home.html')


@login_required
def results(request):
    global all_flights,order
    if order == 'price':
        all_flights = sorted(all_flights, key=lambda i: i['price'])
    elif order == 'duration':
        for i in all_flights:
            hr=0
            min=0
            if 'h' in i['duration']:
                c = 0
                ind = i['duration'].find('hr')
                for j in range(ind, -1, -1):
                    if i['duration'][j].isdigit():
                        hr += int(i['duration'][j]) * pow(10, c)
                        c += 1
            if 'm' in i['duration']:
                c = 0
                ind = i['duration'].find('mi')
                while c != 2 and ind >= 0:
                    ind -= 1
                    if i['duration'][ind].isdigit():
                        min += int(i['duration'][ind]) * pow(10, c)
                        c += 1
            fduration = hr * 60 + min
            i['fduration']=fduration
        all_flights = sorted(all_flights, key=lambda i: i['fduration'])

    all_flights_p = sorted(all_flights, key = lambda i: i['price'])
    all_flights_t = sorted(all_flights, key = lambda i:i['duration'])
    # for i in all_flights_t:
        # print("all_flights_t time is")
        # print(i['duration'])
    min_price = int(all_flights_p[0]['price'])
    min_time = all_flights_t[0]['duration']
    hr = 0
    min = 0
    if 'h' in min_time:
        c = 0
        ind = min_time.find('hr')
        for j in range(ind,-1,-1):
            if min_time[j].isdigit():
                hr += int(min_time[j])*pow(10,c)
                c+=1
    if 'm' in min_time:
        c = 0
        ind = min_time.find('mi')
        while c!=2 and ind >= 0:
            ind-=1
            if min_time[ind].isdigit():
                min+=int(min_time[ind])*pow(10,c)
                c +=1
    min_time = hr*60+min
    # print("first hr and min and min time is ",hr,min,min_time)
    for i in all_flights:
        c = 0
        hr = 0
        min = 0
        if 'h' in i['duration']:
            c = 0
            ind = i['duration'].find('hr')
            for j in range(ind, -1, -1):
                if i['duration'][j].isdigit():
                    hr += int(i['duration'][j]) * pow(10, c)
                    c += 1
        if 'm' in i['duration']:
            c = 0
            ind = i['duration'].find('mi')
            while c != 2 and ind >=0:
                ind -= 1
                if i['duration'][ind].isdigit():
                    min += int(i['duration'][ind]) * pow(10, c)
                    c += 1
        time = (hr*60)+min
        # print("hr and min time and min time and price and min price")
        # print(hr,min,time,min_time,int(i['price']),min_price)
        i['flight-score']= 100 - (((int(i['price']) - min_price)*(100/int(i['price']))*1)+((time - min_time)*(100/time)*1.25))*0.05
        # i['time'] =time
    if order == 'score':
        all_flights = sorted(all_flights, key=lambda i: i['flight-score'],reverse=True)
    #pprint.pprint(all_flights)
    return render(request,'flights/results.html',{'flights':all_flights})


@login_required
def search_flights(request):
    global source,date,destination,all_flights,order
    all_flights=[]
    if request.method == "POST":
        form = FlightSearchForm(request.POST)
        if form.is_valid():
            # form.save()
            source = form.cleaned_data.get('source')
            destination = form.cleaned_data.get('destination')
            order = form.cleaned_data.get('sort_by')
            date = form.cleaned_data.get('date')
            date = str(date)
            all_flights = igc(source,destination,date,all_flights)
            # all_flights_i.append('ixigo')
            
            all_flights =  pay(source,destination,date,all_flights)
            #   all_flights_m.append('makemytrip')
           
            messages.success(request,f'{all_flights}')
            return redirect('flights-results')
    else:
        form = FlightSearchForm()
    return render(request,'flights/search_flights.html',{'form':form})
