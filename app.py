from flask import Flask, render_template, request
import sqlite3
import time

from models import paye

app = Flask(__name__)
conn = sqlite3.connect('database.db')


@app.route('/')
def hello_world():
    method = paye.PAYE

    result = method(age_of_employee=35,
                    periods_per_annum=12,
                    ytd_non_bonus_taxable=1,
                    current_earnings=1,
                    periods_to_date=1,
                    ytd_paye=25).total_projected_annual_taxable_earnings()
    return 'Total Projected Annual Taxable Earnings: {}'.format(result)


if __name__ == '__main__':
    app.run()
