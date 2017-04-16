#!/usr/bin/env python3
import config as cfg
import urllib
import datetime
import os
import re
import requests


def get_source_url(template, dt):
    return template.format(year=dt.strftime('%Y'), month=dt.strftime('%m'))


def get_target_file(url):
    abs_path = os.path.dirname(os.path.abspath(__file__))
    output_path = abs_path + '/data/input/'
    base_file = re.sub(r'^.+/', '', url)
    return output_path + base_file


def download_fund_file(fund_info, now):
    url = get_source_url(fund_info['source_url_template'], now)
    out_file = get_target_file(url)
    print("\tProcessing: {} -> {}".format(url, out_file))

    r = requests.get(url)
    print("\tResponse code: {:d}".format(r.status_code))
    result = False
    if r.status_code == 200:
        f = open(out_file, 'wb')
        f.write(r.content)
        result = True
    return result


def main():
    now = datetime.date.today()
    for fund_info in cfg.AVAILABLE_FUNDS:
        print("{} processing start".format(fund_info['name']))
        result = download_fund_file(fund_info, now)
        if result:
            print("\tSuccess!")
        else:
            print("\tFailed!")

if '__main__' == __name__:
    main()
