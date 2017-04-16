#!/usr/bin/env python3
import config as cfg

import numpy as np
import pandas as pd
import glob
import os
import re
import sys

class FundLoader:
    column_codes = {
        '1':      ('Объем на начало периода', 'AmountTotalBeforeRub'),
        '1.1.':   ('Поступления', 'IncomeTotalRub'),
        '1.1.1.': ('в т.ч. доходы от размещения', 'IncomeEarningsRub'),
        '1.2.':   ('Изъятия', 'WithdrawalTotalRub'),
        '1.3.':   ('Курсовая разница от переоценки активов в иностранной валюте', 'CurrencyRateDiffRub'),
        '2':      ('Объем на конец периода', 'AmountTotalAfterRub'),
        '2.1.':   ('в т.ч. в процентах к ВВП', 'AmountTotalAfterGDPPercent'),
        '3':      ('Справочно: ', np.nan),
        '3.1.':   ('Объем средств фонда на конец периода (млрд. долларов США)', 'AmountTotalAfterUsd'),
        '3.2.':   ('Доходы от размещения, зачисленные в федеральный бюджет', 'AmountIncomeBudget'),
        '3.3.':   ('Расчетная сумма дохода от размещения на счетах в Банке России на конец периода', 'AmountIncomeCbr'),
        '4':      ('Валютная структура средств фонда на счетах в Банке России на конец периода (в соответствующей валюте)**', np.nan),
        '4.1.':   ('доллары США', 'CurrencyUsdAfter'),
        '4.2.':   ('евро', 'CurrencyEurAfter'),
        '4.3.':   ('фунты стерлингов', 'CurrencyGbpAfter'),
        '4.4.':   ('рубли', 'CurrencyRubAfter'),
        '5':      ('Размещено в иные разрешенные активы на конец периода', 'OtherTotalAfter'),
        '5.1.':   ('рубли', 'OtherRubAfter'),
        '5.2.':   ('иностранная валюта', 'OtherForeignAfter'),
    }

    def __init__(self, file_name):
        self.input_file = str(file_name)

    def _columns_input_names(self):
        return {k: v[0] for k, v in self.column_codes.items()}

    def _columns_output_names(self):
        return {k: v[1] for k, v in self.column_codes.items()}

    def verify_headers(self, df):
        df.copy().rename(columns={0: 'code', 1: 'value'})
        input_columns = self._columns_input_names()
        for index, row in df.iterrows():
            if row['Code'] in self.column_codes:
                expected_value = input_columns[row['Code']]
                if expected_value != row['Attribute']:
                    raise NameError('Attribute #{} has value "{}" ("{}" is expected)'.format(row['Code'], row['Attribute'], expected_value))

    def verify_values(self, df):
        # Размер фонда на начало периода должен быть равен размеру на конец предыдущего
        border_amounts_df = df[['AmountTotalBeforeRub', 'AmountTotalAfterRub']]
        last_after_amount = None
        for key, series in border_amounts_df.iterrows():
            if last_after_amount and (series['AmountTotalBeforeRub'] != last_after_amount):
                raise ValueError('Wrong AmountTotalAfterRub at previous rate for {} (expected: {}, got: {})'.format(key, last_after_amount, series['AmountTotalBeforeRub']))
            last_after_amount = series['AmountTotalAfterRub']

    def load(self):
        input_df = pd.read_excel(self.input_file, skiprows=2)

        # * 30 января 2008 г. средства Стабилизационного фонда были зачислены на счета Федерального казначейства
        # в Банке России по учету средств Резервного фонда и Фонда национального благосостояния.
        input_df.rename(columns={'Январь 2008*': '2008-01-30'}, inplace=True)
        input_df.dropna(thresh=100, inplace=True)

        # Проверка структуры human readable показателей
        headers_df = input_df.iloc[:, 0:2].copy()
        headers_df.columns = ['Code', 'Attribute']
        self.verify_headers(headers_df)

        # Приведение к machine readable названий показателей
        column_code_names_dict = self._columns_output_names()
        header_names = headers_df['Code'].astype(str).map(column_code_names_dict)

        # Спиливаем ненужные строки и делаем показатели столбцами
        result_df = input_df[header_names.notnull()].T
        result_df.rename(columns=header_names, inplace=True)

        # Спиливаем служебные строки с исходными кодами и названиями показателей
        result_df = result_df.iloc[2:]

        # Ключи должны быть датой
        result_df.index = result_df.index.to_datetime()

        # Проверка корректности полученных значений
        self.verify_values(result_df)

        # Формируем дополнительные поля для удобства чтения
        result_df['AmountTotalDiffRub'] = result_df['AmountTotalAfterRub'] - result_df['AmountTotalBeforeRub']

        return result_df


def get_sort_date(name):
    match = re.search(r'(\d{2})-(\d{2})-(\d{4})', name)
    if match:
        return match.group(3) + '-' + match.group(2) + '-' + match.group(1)
    else:
        return None


def get_last_source_file(pattern, offset):
    abs_path = os.path.dirname(os.path.abspath(__file__))
    files_list = glob.glob(abs_path + '/data/input/' + pattern)

    sorted_files_list = sorted(files_list, key=get_sort_date)
    return sorted_files_list[-1 - offset]


def get_target_file_name(basename):
    abs_path = os.path.dirname(os.path.abspath(__file__))
    return abs_path + '/data/output/' + os.path.basename(basename)


def main():
    pd.set_option('display.width', 160)

    source_offset = 0

    for fund_info in cfg.AVAILABLE_FUNDS:
        print(fund_info['name'] + " processing start")
        df_file = get_last_source_file(fund_info['input_pattern'], source_offset)
        print("Datafile loading {}".format(df_file))
        fund_loader = FundLoader(df_file)
        fund_df = fund_loader.load()

        target_file = get_target_file_name(fund_info['output_file'])
        print("Saving CSV data into {}".format(target_file))

        save_result = fund_df.to_csv(target_file)
        print("Done! Saving result: {}".format(save_result))

if '__main__' == __name__:
    main()
