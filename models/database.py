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

connector.close()
