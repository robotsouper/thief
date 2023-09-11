import pandas as pd

# Read the Excel file
df = pd.read_excel('111111.xlsx')

# Filter rows where the 'Email' column is '无', and select the 'URL' column
df_filtered = df.loc[df['Email'] == '无', 'URL']

# Convert to DataFrame for saving to excel
df_filtered = pd.DataFrame(df_filtered)

# Save the filtered 'URL' values to a new Excel file
df_filtered.to_excel('filtered_urls.xlsx', index=False)
