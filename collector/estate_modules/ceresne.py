# -*- coding: UTF-8 -*-

from base_module import RealEstate
import requests


class Ceresne(RealEstate):

    estate_name = 'ceresne'
    pretty_name = 'Čerešne'

    def get_data(self):

        ceresne_data = requests.get('https://cr.itb.sk/api/public/v1/pricelist/ceresne/desktop').json()
        flat_list = ceresne_data.get('data')

        for flat in flat_list:
            self.data[flat[2]] = { 'availability': self.translate(flat[12]), 'price': None}

    def translate(self, flat_status):
        if flat_status == 'V':
            translation = self.free_const
        elif flat_status == 'R':
            translation = self.reserved_const
        elif flat_status == 'P':
            translation = self.sold_const
        else:
            raise ValueError('Translation failed. Unable to translate {0}'.format(flat_status))
        return translation
