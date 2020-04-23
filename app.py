from flask import Flask

from models import paye

app = Flask(__name__)


@app.route('/')
def hello_world():
    method = paye.PAYE

    result = method(age_of_employee=35,
                    periods_per_annum=12,
                    ytd_non_bonus_taxable=1,
                    current_earnings=100000,
                    periods_to_date=1,
                    ytd_paye=25)

    total_earnings = result.total_projected_annual_taxable_earnings()
    tax_due = result.tax_due()
    return 'Total Projected Annual Taxable Earnings: {} \n ' \
           'Total Tax Earnings: {}'.format(total_earnings, tax_due)


if __name__ == '__main__':
    app.run()
