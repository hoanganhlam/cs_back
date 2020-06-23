from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests


class Command(BaseCommand):
    def handle(self, *args, **options):
        req = requests.get('https://cheatography.com/smoqwhite/cheat-sheets/minecraft/')
        soup = BeautifulSoup(req.text, "html5lib")
        h1 = soup.select("#pagetitle > div:nth-child(1) > ol > li:nth-child(2) > a > span")
        print(h1[0].string)
        # items = soup.select('.cheat_sheet_output_wrapper')
        # for item in items:
        #     print(item.select(".cheat_sheet_output_title")[0].string)
        #     print(item.select(".cheat_sheet_output_block table")[0])
