# -*- coding: UTF-8 -*-

from base_module import RealEstate
from bs4 import BeautifulSoup
import requests

class Blumental(RealEstate):

    estate_name = 'blumental'
    pretty_name = 'Blumentál'

    def get_data(self):
        url = 'http://blumental.eu/en/pricelist.php'
        data = requests.get(url).text
        blocks = ['A', 'B', 'C', 'D', 'E', 'F', "G", 'H', 'J', 'K']
        soup = BeautifulSoup(data, "html.parser")

        for block in blocks:
            table = soup.find('table', {'id': 'blok{0}'.format(block)})
            if not table:
                continue
            bodies = table.find('tbody')
            if not bodies:
                continue
            rows = bodies.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                self.data[cells[1].get_text()] = {'availability': self.translate(cells[8].get_text()), 'price': None}

    def translate(self, flat_status):
        if flat_status == 'Available':
            translation = self.free_const
        elif flat_status == 'Reserved**' or flat_status == 'Pre-Booked*':
            translation = self.reserved_const
        elif flat_status == 'Sold':
            translation = self.sold_const
        else:
            raise ValueError('Translation failed. Unable to translate {0}'.format(flat_status))
        return translation
