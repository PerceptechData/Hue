from flask import Flask, render_template

from models import paye
from models import tax_bracket

app = Flask(__name__)


@app.route('/')
def index():
    method = paye.PAYE
    result = method(age_of_employee=35,
                    periods_per_annum=12,
                    ytd_non_bonus_taxable=1,
                    current_earnings=100000,
                    periods_to_date=1,
                    ytd_paye=25,
                    bonus_taxable=1000,
                    dependants=1)

    return render_template('index.html',
                           total_earnings=result.total_projected_annual_taxable_earnings(),
                           total_due=result.tax_due(),
                           bonus_tax_due=result.bonus_tax_due(),
                           net_due=result.net_due(),
                           tax_bracket=tax_bracket.get_tax_bracket(),
                           tax_dates=tax_bracket.get_tax_date(), )


if __name__ == '__main__':
    app.run()
