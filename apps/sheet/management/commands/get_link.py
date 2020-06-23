from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from apps.sheet.models import CheatSheet
from apps.general.models import HashTag
import requests
from datetime import timedelta
import uuid


def remove_attrs(soup, whitelist=tuple()):
    if soup is None:
        return None
    for attr in [attr for attr in soup.attrs if attr not in whitelist]:
        del soup[attr]
    return str(soup)


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(36):
            req = requests.get("https://cheatography.com/programming/" + str(i + 1))
            soup = BeautifulSoup(req.text, "html5lib")
            a_list = soup.select("div.triptychdblr > div > strong > a")
            for a in a_list:
                url = "https://cheatography.com" + a["href"]
                print(url)
                d_req = requests.get(url)
                d_soup = BeautifulSoup(d_req.text, "html5lib")
                tag = d_soup.select("#pagetitle > div:nth-child(1) > ol > li:nth-child(2) > a > span")
                taxonomy = tag[0].string if len(tag) > 0 else None
                if len(a.select("span")) > 0:
                    title = a.select("span")[0].string
                    sheets = []
                    items = d_soup.select('.cheat_sheet_output_wrapper')
                    for item in items:
                        label = item.select(".cheat_sheet_output_title")[0].string
                        value = item.select(".cheat_sheet_output_block table")[0]
                        rows = []
                        for tr in value.select("tr"):
                            td = tr.select("td div")
                            rows.append(
                                {
                                    "label": remove_attrs(td[0] if len(td) > 0 else None),
                                    "value": remove_attrs(td[1] if len(td) > 1 else None)
                                }
                            )
                        sheets.append({
                            "id": str(uuid.uuid4()),
                            "title": label,
                            "rows": rows
                        })
                    cs = CheatSheet.objects.filter(title=title).first()
                    if cs is None:
                        last = CheatSheet.objects.order_by('-id').first()
                        last_time = last.date_published + timedelta(hours=0.07)
                        cs = CheatSheet(title=title, sheets=sheets, date_published=last_time, user_id=1)
                        cs.save()
                        if taxonomy is not None:
                            tag = HashTag.objects.filter(title=taxonomy).first()
                            if tag is None:
                                tag = HashTag(title=taxonomy)
                                tag.save()
                            cs.taxonomies.add(tag)
                        print(cs.id)
