AVAILABLE_FUNDS = (
    {
        'name': 'FNB',
        'source_url_template': 'http://minfin.ru/common/upload/library/{year}/{month}/main/Tablitsa_FNB_01-{month}-{year}.xlsx',
        'input_pattern': 'Tablitsa_FNB_*.xlsx',
        'output_file': 'fnb.csv',
    },
    {
        'name': 'Reserved fund',
        'source_url_template': 'http://minfin.ru/common/upload/library/{year}/{month}/main/Tablitsa_Rezervnyy_fond_01-{month}-{year}.xlsx',
        'input_pattern': 'Tablitsa_Rezervnyy_fond_*.xlsx',
        'output_file': 'reserved.csv',
    },
)
