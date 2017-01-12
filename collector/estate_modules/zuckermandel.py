from base_module import RealEstate
import requests
import simplejson


class Zuckermandel(RealEstate):

    estate_name = 'zuckermandel'
    pretty_name = "Zuckermandel"

    def __init__(self):
        super(Zuckermandel, self). __init__()

    def get_data(self):
        url = 'http://www.zuckermandel.sk/api/estate/get'
        data = requests.get(url).json()
        flat_data = data['list']['B']
        for flat in flat_data:
            name = '{0}{1}{2}{3}'.format(flat['block'], flat['entrance'], flat['floor'], flat['flat_no'])
            status = flat['status']
            self.data[name] = {'availability': self.translate(status), 'price': None}

    def translate(self, flat_status):
        if flat_status == '0':
            translation = self.free_const
        elif flat_status == '1':
            translation = self.reserved_const
        elif flat_status == '2':
            translation = self.sold_const
        else:
            raise ValueError('Translation failed. Unable to translate {0}'.format(flat_status))
        return translation
