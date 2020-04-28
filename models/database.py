import sqlite3

connector = sqlite3.connect('../database.db')
cursor = connector.cursor()

# tax bracket schema
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tax_bracket (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        taxable_income_min INTEGER NOT NULL,
        taxable_income_max INTEGER NOT NULL,
        rate_of_tax_value INTEGER NOT NULL,
        taxable_percentage INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        expires_at TEXT NOT NULL
    )
""")

# rebates schema
cursor.execute("""
    CREATE TABLE IF NOT EXISTS rebates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rebate TEXT NOT NULL,
        value INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        expires_at TEXT NOT NULL
    )
""")

# rebates schema
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tax_threshold (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER NOT NULL,
        calculation TEXT NOT NULL,
        threshold INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        expires_at TEXT NOT NULL
    )
""")

# medical tax credit schema
cursor.execute("""
    CREATE TABLE IF NOT EXISTS medical_tax_credit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        credit_value INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        expires_at TEXT NOT NULL
    )
""")

connector.close()




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
