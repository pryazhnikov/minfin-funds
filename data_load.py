#!/usr/bin/env python3
import config as cfg
import argparse
import urllib
import datetime
import os
import re
import requests
import sys


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


def get_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--count', help='Count of files to load',
                        action='store', type=int, default=1)
    parser.add_argument('--stop-on-success', help='Stop after first loaded file',
                        dest='stop_on_success', action='store_true', default=False)

    return parser.parse_args()


def main():
    is_success = True

    args = get_arguments()
    if args.count < 1:
        raise ValueError("Count value should be positive")

    now = datetime.date.today()
    for fund_info in cfg.AVAILABLE_FUNDS:
        is_file_found = False
        time = now
        for i in range(args.count):
            print("{} processing #{}\t({})".format(fund_info['name'], i + 1, time.isoformat()))
            result = download_fund_file(fund_info, time)
            if result:
                is_file_found = True
                print("\tSuccess!")
                if args.stop_on_success:
                    print("Processing stop due to successful file loading")
                    break
            else:
                print("\tFailed!")

            time -= datetime.timedelta(days=30)

        if not is_file_found:
            is_success = False

    return is_success


if __name__ == '__main__':
    is_success = main()
    exit_code = 0 if is_success else 1
    sys.exit(exit_code)
