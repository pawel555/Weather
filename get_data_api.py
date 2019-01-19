from pyowm import OWM

class GetDataFromOWMApi:
    def __init__(self):
        self.API_key='f6fd2fa083372d167d6d68edf9aaa247'
        self.cities = ['Warsaw, PL','Gdansk, PL','Pila, PL','Torun, PL','Plock, PL','Poznan, PL','Opole, PL','Krakow, PL','Lublin, PL','Rzeszow, PL']


    def retrunWeatherForFiveDays(self):
        owm = OWM(self.API_key)
        dict_of_weather = {}
        for i in range (len(getDataFromOWMApi.cities)):            
            forecaster = owm.three_hours_forecast(getDataFromOWMApi.cities[i])
            dict_of_weather[getDataFromOWMApi.cities[i]]= forecaster.get_forecast()
        return dict_of_weather


getDataFromOWMApi= GetDataFromOWMApi() 


for city , forecast in getDataFromOWMApi.retrunWeatherForFiveDays().items():
    print('City '+city)
    for weather in forecast:
        print(weather.get_reference_time('iso'),weather.get_rain(), weather.get_pressure(), weather.get_temperature(unit='celsius'),weather.get_snow())


#owm = OWM(getDataFromOWMApi.API_key)
#for i in range (len(getDataFromOWMApi.cities)):
#    forecaster = owm.three_hours_forecast(getDataFromOWMApi.cities[i])
#    forecast = forecaster.get_forecast()
#    print('City '+getDataFromOWMApi.cities[i])
#    for weather in forecast:
#        print(weather.get_reference_time('iso'),weather.get_status())
#


#print(w.get_clouds())
#print(w.get_rain())
#print(w.get_wind())
#print(w.get_pressure())
