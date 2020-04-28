from models import get_data

"""
How SARS Calculates Tax:
1. Gross Annual Income
2. Annualized Taxable Income (multipy by tax periods, 12, 26, 52)
3. Determine which bracket taxable income falls
4. Reduce Taxable Income with the min bracket amount
5. Multiply by % of Tax
6. Add rate of tax amount
7. Deduct Rebate
8. Divide tax by periods (12, 26, 52)
9. Deduct Medical Aid Tax Credit
"""


class PAYECalculator:
    def __init__(self, fixed_salary, *income, period, raf, pension, provident, monthly_travel_allowance,
                 travel_allowance_percentage, age):
        self.fixed_salary = fixed_salary
        self.income = income
        self.period = period
        self.raf = raf
        self.pension = pension
        self.provident = provident
        self.monthly_travel_allowance = monthly_travel_allowance
        self.travel_allowance_percentage = travel_allowance_percentage
        self.age = age

    def gross_annual_salary(self):
        """
        When calculating PAYE, start by computing the total annual or gross salary/income
        inclusive of benefits before any deductions.

        i. Fixed salaries This calculation should be more straightforward for employees who receive fixed salaries.
        In such a case, the gross pay is calculated as follows: Employee's gross annual salary = monthly salary * 12

        i. Variable salaries It is more involving but still simple to compute PAYE for employees who receive variable
        incomes. Below is a brief to use in this computation: Employee gross annual salary = (sum of monthly
        remuneration to the current date/number of remuneration months) * 12
        :return: integer. gross annual salary
        """
        if self.fixed_salary:
            return self.income[0] * self.period
        else:
            return (sum(self.income) / len(self.income)) * self.period

    def monthly_deductions(self):
        """
        It is advisable to factor in regular deductions such as provident funds and RAF using this procedure;
        Deductions = (Sum of monthly RAF, pension)*12
        :return: integer. monthly deductions
        """
        return (self.raf + self.pension + self.provident) * self.period

    def travel_allowance(self):
        """
        i. More than 80% travel rate Travel allowance deduction = (monthly travel allowance*12)*20%
        ii. Less than 80% travel rate Travel allowance deduction= (monthly travel allowance*12)*80%
        :return: integer. travel allowance
        """
        return (self.monthly_travel_allowance * self.period) * self.travel_allowance_percentage

    def tax_rebates(self):
        """
        Employers should determine the age of the employer before further tax rebate deduction. Below is a
        comprehensive rebate deduction guide for individuals in the order of category of rebate, the employee's age, and amount:
        :return: integer. tax rebate
        """
        df = get_data.get_rebates()
        value = df['value'].tolist()
        if self.age < 65:
            return value[0]
        elif 65 <= self.age < 75:
            return value[0] + value[1]
        elif self.age >= 75:
            return value[0] + value[1] + value[2]

    def tax_threshold(self):
        """
        Tax thresholds serve as a relief for low-income earners specifying the limits for tax-free income level.
        Provided below is a tax threshold guide for the year 2018 in the order of age limits followed by the thresholds.
        :return: integer. tax threshold
        """
        df = get_data.get_tax_threshold()
        ages = df['age'].tolist()
        value = df['threshold'].tolist()
        if self.age < ages[0]:
            return value[0]
        elif ages[0] <= self.age < ages[1]:
            return value[1]
        elif self.age >= ages[2]:
            return value[2]
        else:
            return 0

    def taxable_income(self):
        """
        i. Taxable income
        Sum of annual salary – (Travel allowance deduction + pension or RAF or provident fund deductions)
        :return: integer. taxable income
        """
        return (self.gross_annual_salary() - (
                    self.travel_allowance() + self.monthly_deductions())) - self.tax_threshold()


class PAYEOLD:
    def __init__(self, fixed_period, period, income, raf, pension, provident, travel_allowance,
                 travel_allowance_percentage, age):
        self.fixed_period = fixed_period
        self.period = period
        self.income = income
        self.raf = raf
        self.pension = pension
        self.provident = provident
        self.travel_allowance = travel_allowance
        self.travel_allowance_percentage = travel_allowance_percentage
        self.age = age

    def gross_annual_salary(self):
        """
        Work out your employee’s gross or total annual salary before deductions and including benefits:

        In the case of fixed salaries, this is simple:
        Total monthly salary X 12

        In the case of variable income, use a calculation to estimate the annual total income, e.g.
        If your employee has earned R10 000 in March, R12 000 in April and now R15 000 in May, you would add all amounts
        together, divide by the number of months you have figures for – in this case 3 – and multiply by 12 months in the
        year to receive an estimated total annual income:
        ((Add total monthly remunerations amounts to date) / number of remuneration amounts ) x 12
        :param fixed_period: Boolean. True: fixed 12 month salary. False: list of all incomes for period
        :param period: Integer. 12, 26, 52
        :param income: List: list of all income values
        :return:
        """
        if self.fixed_period:
            return self.income[0] * self.period
        else:
            return (sum(self.income) / len(self.income)) * self.period

    def raf_pension_provident_contribution(self):
        """
        Contributions to RAF, pension or provident funds:
        Total Monthly RAF or pension or provident fund contributions x 12

        This deduction is limited to a % of the employee’s total income.
        :param raf: Integer. Employee Retirement Annuity Fund contribution
        :param pension: Integer. Employee pension contribution
        :param provident_fund: Integer. Employee provident contribution
        :param period: Integer. Period as 12, 26, 52
        :return: Integer. Total contribution
        """
        return (self.raf + self.pension + self.provident) * self.period

    def travel_allowance(self):

        return (self.travel_allowance() * self.period) * self.travel_allowance_percentage

    def tax_rebates(self):
        """
        Tax rebates are amounts by which SARS will reduce the actual taxes owing based on certain
        conditions or circumstances.
        :param age: Integer. Employee Age
        :return: Integer. tax_rebate
        """
        df = get_data.get_rebates()
        value = df['value'].tolist()
        if self.age < 65:
            return value[0]
        elif 65 <= self.age < 75:
            return value[0] + value[1]
        elif self.age >= 75:
            return value[0] + value[1] + value[2]

    def tax_threshold(self):
        """
        Tax Thresholds offer tax relief to low income earners and specify the ceilings for tax-free income.
        :param age: Integer. Employee age
        :return: Integer. relief amount
        """
        df = get_data.get_tax_threshold()
        ages = df['age'].tolist()
        value = df['threshold'].tolist()
        if self.age < ages[0]:
            return value[0]
        elif ages[0] <= self.age < ages[1]:
            return value[1]
        elif self.age >= ages[2]:
            return value[2]

    def paye_statutory_rate(self):
        """
        Find out which tax bracket your employee’s taxable income falls into and work out the total tax payable.
        This results in the gross annual income deducted by the minimum of the tax bracket
        :param gross_annual_income: Integer. Employees gross annual income
        :return: Integer. PAYE statutory rate
        """
        df = get_data.get_tax_bracket()
        for i in range(0, 8):
            if df['taxable_income_min'][i] < self.gross_annual_salary() <= df['taxable_income_max'][i]:
                return self.gross_annual_salary() - df['taxable_income_min'][0]

    def threshold_percentage(self):
        """
        Find out which tax bracket your employee’s taxable income falls into and work out the total tax payable.
        This results in the gross annual income deducted by the minimum of the tax bracket
        :param gross_annual_income: Integer. Employees gross annual income
        :return: Integer. Rate of Tax Percentage
        """
        df = get_data.get_tax_bracket()
        for i in range(0, 8):
            if df['taxable_income_min'][i] < self.gross_annual_salary() <= df['taxable_income_max'][i]:
                return df['taxable_percentage'][0]

    def rate_of_tax(self):
        """
        Find out which tax bracket your employee’s taxable income falls into and work out the total tax payable.
        This results in the gross annual income deducted by the minimum of the tax bracket
        :param gross_annual_income: Integer. Employees gross annual income
        :return: Integer. Rate of Tax
        """
        df = get_data.get_tax_bracket()
        for i in range(0, 8):
            if df['taxable_income_min'][i] < self.gross_annual_salary() <= df['taxable_income_max'][i]:
                return df['rate_of_tax_value'][0]

    def tax_payable(self):
        """
        the PAYE your employee needs to submit for the month:
        PAYE = (Total tax payable – total rebates) / 12
        :return: Integer. PAYE Total
        """
        total_tax_payable = ((self.gross_annual_salary() - self.paye_statutory_rate()) *
                             self.threshold_percentage()) + self.rate_of_tax()
        tot_rebates = self.tax_rebates()
        return (total_tax_payable - tot_rebates) / self.period


dirk = PAYE(fixed_period=True, period=12, income=[420000], raf=0, pension=0,
            provident=0, travel_allowance=0, travel_allowance_percentage=0, age=26).tax_payable()

print(dirk)
