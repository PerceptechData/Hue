import sqlite3

import pandas as pd


def get_tax_bracket():
    """
    method connects to database and loads tax bracket where created at <= today and expires at >= today
    to get the relevant tax bracket
    :return: pandas dataframe of database tax bracket data
    """
    connector = sqlite3.connect('../database.db')
    cursor = connector.cursor()
    data = pd.read_sql_query(
        'select * from tax_bracket where date(created_at) <= current_date and date(expires_at) >= current_date',
        connector)
    cursor.close()
    return data


def get_tax_threshold():
    connector = sqlite3.connect('../database.db')
    cursor = connector.cursor()
    data = pd.read_sql_query(
        'select * from tax_threshold where date(created_at) <= current_date and date(expires_at) >= current_date',
        connector)
    cursor.close()
    return data


def get_rebates():
    connector = sqlite3.connect('../database.db')
    cursor = connector.cursor()
    data = pd.read_sql_query(
        'select * from rebates where date(created_at) <= current_date and date(expires_at) >= current_date',
        connector)
    cursor.close()
    return data


def get_medical_tax_credit():
    connector = sqlite3.connect('../database.db')
    cursor = connector.cursor()
    data = pd.read_sql_query(
        'select * from medical_tax_credit where date(created_at) <= current_date and date(expires_at) >= current_date',
        connector)
    cursor.close()
    return data
