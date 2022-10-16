import json

import requests


class APIHandler(object):
    """
    class containing getter functions for the API.
    TODO: should really store data as database on local machine.
    """

    def __init__(self, candidateNr: int, url=None):

        self.number = candidateNr

        self.url = url
        if self.url is None:
            self.url = "http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api/"

        self.cities = None

    def get_cities(self) -> list:
        """
        returns the list of valid cities from the API
        :return: list
        """
        request = requests.get(f"{self.url}/cities/")
        # throw traceback if there was an error in the request.
        request.raise_for_status()
        return json.loads(request.text)["cities"]

    def get_weather(self, city: str) -> dict:
        """
        returns the weather for a given city as a dict
        :return: dict. format {weekday:list}.
        """

        # ignore upper case letters
        city = city.lower()

        if city not in self.get_cities():
            raise Exception(
                f"{city} is not one of the cities listed in the database: {self.url}cities/")
        request = requests.get(
            f"{self.url}weather/{self.number}/{city}/")
        request.raise_for_status()
        return json.loads(request.text)

    def get_val(self, city: str, key: str, weekday=None,
                timeint=-1) -> list:
        """
        gets the given metric for a city. If weekday is None will return
        the val for the entire week. if timeint is -1, will return
        all the data for a given key for given day. All vals are non
        case sensitive.
        :param city: str, name of city
        :param key: str, pressure,temperature ...etc
        :param weekday: str
        :return: list
        """

        data = self.get_weather(city)
        key = key.lower()

        if weekday is not None:
            weekday = weekday.lower()
            if weekday not in data:
                raise KeyError(f"{weekday} is not a valid weekday")
            # look on just this weekday
            weekdays = [weekday]
        else:
            # look on all the weekdays (that are listed in the data)
            weekdays = list(data.keys())
        res = []
        for day in weekdays:
            if timeint != -1:
                # look at timeinterval given
                res.append(data[day][timeint][key])
            else:
                for dct in data[day]:
                    res.append(dct[key])
        return res
