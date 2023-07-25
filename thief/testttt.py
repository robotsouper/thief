import pandas as pd

# Read the Excel files
df1 = pd.read_excel('统一.xlsx')
df2 = pd.read_excel('汇总.xlsx')

# Merge the two dataframes on the "URL" column
df_merged = pd.merge(df1, df2, on='URL')

# Write the merged dataframe to a new Excel file
df_merged.to_excel('shuiaah.xlsx', index=False)
