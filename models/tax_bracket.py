import sqlite3

import pandas as pd

connector = sqlite3.connect('../database.db')
cursor = connector.cursor()


def get_tax_bracket():
    """
    method connects to database and loads tax bracket where created at <= today and expires at >= today
    to get the relevant tax bracket
    :return: pandas dataframe of database tax bracket data
    """
    return pd.read_sql_query(
        'select * from tax_bracket where date(created_at) <= current_date and date(expires_at) >= current_date',
        connector)


# ['taxable_income_min', 'taxable_income_max', 'rate_of_tax_value','taxable_percentage', 'created_at', 'expires_at']
def get_rate_of_tax_value(t):
    """
    returns rate of tax value relative to the annual income passed to the method
    :param t: total projected annual taxable earnings
    :return:
    """
    csv = get_tax_bracket()
    for i in range(0, 8):
        if csv['taxable_income_min'][i] < t <= csv['taxable_income_max'][i]:
            return csv['rate_of_tax_value'][i]


def get_taxable_percentage(t):
    """
    returns taxable percentage relative to the annual income passed to the method
    :param t: total projected annual taxable earnings
    :return: taxable percentage
    """
    csv = get_tax_bracket()
    for i in range(0, 8):
        if csv['taxable_income_min'][i] < t <= csv['taxable_income_max'][i]:
            return csv['taxable_percentage'][i]
