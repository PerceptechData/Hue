import sqlite3

import pandas as pd


def get_rebate():
    """
    method connects to database and loads tax bracket where created at <= today and expires at >= today
    to get the relevant tax bracket
    :return: pandas dataframe of database tax bracket data
    """
    connector = sqlite3.connect('database.db')
    cursor = connector.cursor()
    data = pd.read_sql_query(
        'select * from rebates where date(created_at) <= current_date and date(expires_at) >= current_date',
        connector)
    cursor.close()
    return data


def get_primary_rebate():
    df = get_rebate()
    return df[df['rebate'] == 'primary']['value'][0]


def get_age_rebate(age):
    """
    returns age rebate to the relevant age consumed by the method
    :param age: employees age
    :return: rebate amount
    """
    df = get_rebate()
    if 65 <= age < 75:
        return df[df['rebate'] == 'secondary']['value'][0]
    elif age >= 75:
        return df[df['rebate'] == 'tertiary']['value'][0]
    else:
        return 0
