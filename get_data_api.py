from pyowm import OWM


class GetDataFromOWMApi:
    def __init__(self):
        self.API_key = 'f6fd2fa083372d167d6d68edf9aaa247'
        self.cities = ['Warsaw, PL', 'Gdansk, PL', 'Pila, PL', 'Torun, PL', 'Plock, PL', 'Poznan, PL', 'Opole, PL',
                       'Krakow, PL', 'Lublin, PL', 'Rzeszow, PL']

    def retrunWeatherForFiveDays(self):
        owm = OWM(self.API_key)
        dict_of_weather = {}
        for i in range(len(self.cities)):
            forecaster = owm.three_hours_forecast(self.cities[i])
            dict_of_weather[self.cities[i]] = forecaster.get_forecast()
        return dict_of_weather


    def main(self, city, date):
        get_data_from_api = GetDataFromOWMApi()

        my_dict = get_data_from_api.retrunWeatherForFiveDays()
        fore = my_dict[city]
        fore_modi = []

        for weather in fore:
            ref_time = weather.get_reference_time('iso')
            if date in ref_time:
                fore_modi.append([ref_time.split(' ')[1].split('+')[0], weather.get_rain(), weather.get_pressure(),
                    weather.get_temperature(unit='celsius'), weather.get_snow(), weather.get_wind(), weather.get_clouds()])

        return fore_modi

    # for weather in fore:
    #     print(weather.get_reference_time('iso'), weather.get_rain(), weather.get_pressure(),
    #           weather.get_temperature(unit='celsius'), weather.get_snow(), weather.get_wind())

# for city, forecast in getDataFromOWMApi.retrunWeatherForFiveDays().items():
#     print('City '+city)
#     for weather in forecast:
#         print(weather.get_reference_time('iso'),weather.get_rain(), weather.get_pressure(), weather.get_temperature(unit='celsius'),weather.get_snow())


# owm = OWM(getDataFromOWMApi.API_key)
# for i in range (len(getDataFromOWMApi.cities)):
#    forecaster = owm.three_hours_forecast(getDataFromOWMApi.cities[i])
#    forecast = forecaster.get_forecast()
#    print('City '+getDataFromOWMApi.cities[i])
#    for weather in forecast:
#        print(weather.get_reference_time('iso'),weather.get_status())
#


# print(w.get_clouds())
# print(w.get_rain())
# print(w.get_wind())
# print(w.get_pressure())
