import pandas as pd


# ['taxable_income_min', 'taxable_income_max', 'rate_of_tax_value','taxable_percentage']
def tax_bracket_measure(t):
    """
    collects internal csv file of current years income tax and returns
    relevant rate of tax for annual earnings per individual
    :param t: total projected annual taxable earnings
    :return: (rate of tax value, taxable percentage)
    """
    csv = pd.read_csv('../static/tax_brackets.csv')
    for i in range(0, 8):
        if csv['taxable_income_min'][i] < t <= csv['taxable_income_max'][i]:
            return {'rate_of_tax_value': csv['rate_of_tax_value'][i],
                    'taxable_percentage': csv['taxable_percentage'][i]}



