#!/usr/bin/env python3
import config as cfg
import argparse
import urllib
import datetime
import os
import re
import requests
import sys


def get_source_url(templates_list, dt):
    date_formatted = dt.strftime('%Y-%m-%d')
    for valid_till in sorted(templates_list.keys()):
        if date_formatted < valid_till:
            template = templates_list[valid_till]
            return template.format(year=dt.strftime('%Y'), month=dt.strftime('%m'))

    return None


def get_target_file(file_template, dt):
    abs_path = os.path.dirname(os.path.abspath(__file__))
    output_path = abs_path + '/data/input/'
    base_file = file_template.format(year=dt.strftime('%Y'), month=dt.strftime('%m'))
    return output_path + base_file


def download_fund_file(fund_info, now):
    url = get_source_url(fund_info['source_url_templates'], now)
    if url is None:
        print("\tCannot find url for date: {}".format(now))
        return False

    out_file = get_target_file(fund_info['target_file_template'], now)
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
    exit_code = 0

    args = get_arguments()
    if args.count < 1:
        raise ValueError("Count value should be positive")

    now = datetime.date.today()
    for fund_info in cfg.AVAILABLE_FUNDS:
        is_file_found = False
        time = now
        for i in range(args.count):
            print("{} processing #{}\t({})".format(fund_info['name'], i + 1, time.isoformat()))
            result = download_fund_file(fund_info['load'], time)
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
            exit_code = 1

    return exit_code


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
