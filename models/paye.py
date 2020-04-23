from models import rebate
from models import tax_bracket


class PAYE:
    def __init__(self, age_of_employee, periods_per_annum, ytd_non_bonus_taxable, current_earnings, periods_to_date,
                 ytd_paye):
        # total projected annual taxable earnings
        self.age_of_employee = age_of_employee
        self.periods_per_annum = periods_per_annum
        self.ytd_non_bonus_taxable = ytd_non_bonus_taxable
        self.current_earnings = current_earnings
        self.periods_to_date = periods_to_date

        # tax due
        self.ytd_paye = ytd_paye

        self.total_taxable_earnings = self.ytd_non_bonus_taxable + self.current_earnings
        self.average_taxable_earnings = self.total_taxable_earnings / self.periods_to_date

    def total_projected_annual_taxable_earnings(self):
        """
        calculates total projected annual taxable earnings per individual
        :return: average taxable earnings * periods per annum
        """
        return self.average_taxable_earnings * self.periods_per_annum

    def tax_due(self):
        bracket = tax_bracket.get_rate_of_tax_bracket(self.average_taxable_earnings * self.periods_per_annum)
        tax_bracket_excess = (self.average_taxable_earnings * self.periods_per_annum) - bracket
        taxable_percentage = tax_bracket.get_taxable_percentage(self.average_taxable_earnings * self.periods_per_annum)
        tax_excess = tax_bracket_excess * taxable_percentage
        standard_tax = tax_bracket.get_rate_of_tax_value(self.average_taxable_earnings * self.periods_per_annum)
        tax_total = (tax_excess + standard_tax) - rebate.get_primary_rebate()
        projected_annual_tax = ((tax_total - rebate.get_age_rebate(self.age_of_employee)) / self.periods_per_annum) * self.periods_to_date
        return projected_annual_tax - self.ytd_paye
