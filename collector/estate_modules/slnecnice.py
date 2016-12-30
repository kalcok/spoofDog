# -*- coding: UTF-8 -*-

from base_module import RealEstate
from bs4 import BeautifulSoup
import requests
import os


class Slnecnice(RealEstate):

    estate_name = 'slnecnice'
    pretty_name = 'Slnečnice'

    def get_data(self):
        base_url = 'https://www.slnecnice.sk/mesto/ponuka-byvania/vsetky-byty'
        base_page = requests.get(base_url).text

        pagination_soup = BeautifulSoup(base_page, 'html.parser')
        paginator = pagination_soup.find('section', {'id': 'paginator'}).find('ul', {'class': 'pagination'})
        flat_list_pages = []
        for page in paginator.find_all('li'):
            flat_list_pages.append(page.get_text())

        for page in flat_list_pages:
            url = '{0}/page:{1}'.format(base_url, page)
            page_data = requests.get(url).text
            soup = BeautifulSoup(page_data, "html.parser")
            table_body = soup.find("table", {"class": "flats-list"}).find('tbody')

            rows = table_body.find_all("tr")
            for row in rows:
                cells = row.find_all("td")
                self.data[cells[3].get_text()] = self.translate(cells[12].get_text())

    def translate(self, flat_status):
        flat_status = unicode(flat_status.lower())
        if flat_status == 'voľná'.decode('utf-8'):
            translation = self.free_const
        elif flat_status == 'rezervovaná'.decode('utf-8') or flat_status == 'predrezervovaná'.decode('utf-8'):
            translation = self.reserved_const
        elif flat_status == 'predaná'.decode('utf-8'):
            translation = self.sold_const
        else:
            raise ValueError('Translation failed. Unable to translate {0}'.format(flat_status))
        return translation
