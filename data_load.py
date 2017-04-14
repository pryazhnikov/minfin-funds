#!/usr/bin/env python3
import urllib
import datetime
import os
import re
import requests

def get_url_templates():
    """
    Источник данных: http://minfin.ru/ru/statistics/fonds/
    """
    return (
        'http://minfin.ru/common/upload/library/{year}/{month}/main/Tablitsa_FNB_01-{month}-{year}.xlsx',
        'http://minfin.ru/common/upload/library/{year}/{month}/main/Tablitsa_Rezervnyy_fond_01-{month}-{year}.xlsx',
    )

def get_url(template, dt):
    return template.format(year=dt.strftime('%Y'), month=dt.strftime('%m'))

def get_target_file(url):
    abs_path = os.path.dirname(os.path.abspath(__file__))
    output_path = abs_path + '/data/input/'
    base_file = re.sub(r'^.+/', '', url)
    return output_path + base_file

def main():
    now = datetime.date.today()
    for tmpl in get_url_templates():
        url = get_url(tmpl, now)
        out_file = get_target_file(url)
        print("Processing: {} -> {}".format(url, out_file))

        r = requests.get(url)
        print("\tResponse code: {:d}".format(r.status_code))
        if r.status_code == 200:
            f = open(out_file, 'wb')
            f.write(r.content)
            print("\tSuccess!")

if '__main__' == __name__:
    main()
