import requests
import json
import sys
from datetime import datetime, timedelta
from auth import getHeaders
from parks import Park
from entertainments import Entertainment
from attractions import Attraction


class Destination(object):

    def __init__(self, id = ''):
        """
        Constructor Function
        Gets all destination data available and stores various elements into variables.
        ID must be a string.
        """
        try:

            if id == '':
                raise ValueError
            elif id != None and type(id) != str:
                raise TypeError

            self.__id = id

            s = requests.get("https://api.wdpro.disney.go.com/facility-service/destinations/{}".format(self.__id), headers=getHeaders())
            self.__data = json.loads(s.content)

            self.__destination_name = self.__data['name'].replace(u"\u2019", "'").replace(u"\u2013", "-").replace(u"\u2122", "").replace(u"\u2022", "-").replace(u"\u00ae", "").replace(u"\u2014", "-").replace(u"\u00a1", "").replace(u"\u00ee", "i").strip()
            self.__type = self.__data['type']

        except ValueError:
            print('Destination object expects an id value. Must be passed as string.\n Usage: Entertainment(id = None)')
            sys.exit()
        except TypeError:
            print('Destination object expects a string argument.')
            sys.exit()
        except Exception:
            print('That point of interest or ID is not available. {}'.format(id))
            print('Full list of possible destinations and their ID\'s can be found here: https://scaratozzolo.github.io/MouseTools/destinations.txt')
            sys.exit()

    def getThemeParks(self):
        """
        Returns a list of theme park Park objects
        """
        parks = []

        s = requests.get(self.__data['links']['themeParks']['href'], headers=getHeaders())
        data = json.loads(s.content)

        for park in data['entries']:
            parks.append(Park(park['links']['self']['href'].split('/')[-1]))

        return parks

    def getWaterParks(self):
        """
        Returns a list of water park Park objects
        """
        parks = []

        s = requests.get(self.__data['links']['waterParks']['href'], headers=getHeaders())
        data = json.loads(s.content)

        for park in data['entries']:
            parks.append(Park(park['links']['self']['href'].split('/')[-1]))

        return parks

    def getEntertainments(self):
        """
        Returns a list of Entertainment objects
        """
        entertainments = []

        s = requests.get(self.__data['links']['entertainments']['href'], headers=getHeaders())
        data = json.loads(s.content)

        for enter in data['entries']:
            entertainments.append(Entertainment(enter['links']['self']['href'].split('/')[-1]))

        return entertainments

    def getAttractions(self):
        """
        Returns a list of Attraction objects
        """
        attractions = []

        s = requests.get(self.__data['links']['attractions']['href'], headers=getHeaders())
        data = json.loads(s.content)

        for attract in data['entries']:
            attractions.append(Attraction(attract['links']['self']['href'].split('/')[-1]))

        return attractions

    def __formatDate(self, month, day):
        """
        Formats month and day into proper format
        """
        if len(month) < 2:
            month = '0'+month
        if len(day) < 2:
            day = '0'+day
        return month, day

    def __str__(self):
        return 'Destination object for {}'.format(self.__destination_name)