# -*- coding: UTF-8 -*-

from base_module import RealEstate
from bs4 import BeautifulSoup
import requests


class Myto(RealEstate):

    estate_name = 'myto'
    pretty_name = 'Pri Mýte'

    def get_data(self):
        url = 'http://primyte.sk/byty'
        data = requests.get(url).text
        soup = BeautifulSoup(data, "html.parser")

        table_body = soup.find('section', {'class': 'flat_list'}).find('table').find('tbody')
        rows = table_body.find_all('tr')

        for row in rows:
            cells = row.find_all('td')
            self.data[cells[0].get_text()] = {'availability': self.translate(cells[10].get_text()), 'price': None}

    def translate(self, flat_status):
        flat_status = unicode(flat_status.lower())
        if flat_status == 'voľný'.decode('utf-8'):
            translation = self.free_const
        elif flat_status == 'rezervovaný'.decode('utf-8'):
            translation = self.reserved_const
        elif flat_status == 'predaný'.decode('utf-8') or flat_status == 'nie je v predaji'.decode('utf-8'):
            translation = self.sold_const
        else:
            raise ValueError('Translation failed. Unable to translate {0}'.format(flat_status))
        return translation
