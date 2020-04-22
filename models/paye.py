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
        total_projected_annual_taxable_earnings = self.average_taxable_earnings * self.periods_per_annum
        tx_brckt = tax_bracket.tax_bracket_measure(total_projected_annual_taxable_earnings)

        tax_bracket_excess = total_projected_annual_taxable_earnings - tx_brckt['rate_of_tax_value']
        tax_excess = tax_bracket_excess * tx_brckt['taxable_percentage']
        total_tax_from_bracket = tax_excess +
