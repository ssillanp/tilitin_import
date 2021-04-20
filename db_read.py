import pandas as pd
import sqlite3

dbt_reader = sqlite3.connect('SVTK.sqlite')
qry = 'SELECT * FROM entry'
entry_df = pd.read_sql(qry, dbt_reader)
entry_df.set_index('id', inplace=True)
print(entry_df)