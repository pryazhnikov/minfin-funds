AVAILABLE_FUNDS = (
    {
        'name': 'FNB',
        'load': {
            'source_url_templates': {
                '2017-09-30': 'https://minfin.ru/common/upload/library/{year}/{month}/main/Tablitsa_FNB_01-{month}-{year}.xlsx',
                '2017-11-30': 'https://minfin.ru/common/upload/library/{year}/{month}/main/Tablitsa_FNB_01{month}{year}.xlsx',
                '2017-12-31': 'https://minfin.ru/common/upload/library/{year}/{month}/main/Tablitsa_FNB_01-{month}-{year}.xlsx',
                '2018-01-31': 'https://minfin.ru/common/upload/library/{year}/{month}/main/FNB_01-{month}-{year}.xlsx',
                '9999-99-99': 'https://minfin.ru/common/upload/library/{year}/{month}/main/Tablitsa_FNB_01-{month}-{year}_rus.xlsx',
            },
            'target_file_template': 'Tablitsa_FNB_01-{month}-{year}.xlsx',
        },
        'transform': {
            'input_file_pattern': 'Tablitsa_FNB_*.xlsx',
            'output_file': 'fnb.csv',
        },
    },
    {
        'name': 'Reserved fund',
        'load': {
            'source_url_templates': {
                '2017-09-30': 'https://minfin.ru/common/upload/library/{year}/{month}/main/Tablitsa_Rezervnyy_fond_01-{month}-{year}.xlsx',
                '2017-10-30': 'https://minfin.ru/common/upload/library/{year}/{month}/main/Tablitsa_Rezervnyy_fond_01{month}{year}.xlsx',
                '2017-12-31': 'https://minfin.ru/common/upload/library/{year}/{month}/main/Tablitsa_Rezervnyy_fond_01-{month}-{year}.xlsx',
                '2018-01-31': 'https://minfin.ru/common/upload/library/{year}/{month}/main/Rezervnyy_fond__01-{month}-{year}.xlsx',
            },
            'target_file_template': 'Tablitsa_Rezervnyy_fond_01-{month}-{year}.xlsx',
        },
        'transform': {
            'input_file_pattern': 'Tablitsa_Rezervnyy_fond_*.xlsx',
            'output_file': 'reserved.csv',
        },
    },
)
