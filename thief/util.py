import pandas as pd


# only handle the case where the input file is .xlsx file and there are only two column
def process_file(filename):
    df = pd.read_excel(filename, header=None)
    df.drop_duplicates(inplace=True)
    df[1] = df[1].astype(str)
    df = df.groupby(0)[1].apply(', '.join).reset_index()
    df.to_excel(filename, index=False)


# process_file("总1.xlsx")

# combine two .xlsx that has exact same column names to a new .xlsx file with new column
# file_name would be xxx_ABC.xlsx and xxx_BCD.xlsx
def merge_files(filename1, filename2):
    # get ABC and BCD
    identifier1 = filename1.split('_')[1].split('.')[0]
    identifier2 = filename2.split('_')[1].split('.')[0]

    df1 = pd.read_excel(filename1)
    df2 = pd.read_excel(filename2)

    df1[identifier1] = 1
    df2[identifier2] = 1
    merged_df = pd.merge(df1, df2, how='outer', on='URL')
    merged_df = merged_df.fillna(0)

    merged_df.to_excel("总和.xlsx", index=False)


def modify_excel(small_file, large_file):
    small_df = pd.read_excel(small_file)
    large_df = pd.read_excel(large_file)
    merged_df = pd.merge(small_df, large_df, on='URL', how='left')
    merged_df.rename(columns={'Number': '电话号码', 'Shop Name': '商家名称'}, inplace=True)
    merged_df = merged_df[['URL', '商家名称', '电话号码']]
    merged_df.to_excel('第一次小尝试.xlsx', index=False)



def combine_excel(file1, file2):
    # Read the excel files
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    # Add a temporary 'source' column to each DataFrame to track where they come from
    df1['source'] = 1
    df2['source'] = 2
    df = pd.concat([df1, df2])

    # Check if "无" is in any column, create a new 'check' column for it
    df['check'] = df.apply(lambda row: "无" in row.values, axis=1)
    df = df.drop(columns=['check'])
    df['credit'] = df.duplicated(subset=df.columns.difference(['source']), keep=False).astype(int)

    df = df.drop(columns=['source'])

    df = df.drop_duplicates()

    df = df.sort_values(by='credit', ascending=False)

    df.to_excel("new_file.xlsx", index=False)



def modify_excel(file1, file2):
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    df1 = pd.merge(df1, df2[['URL', 'CompanyName']], on='URL', how='left')
    df1 = df1.rename(columns={'CompanyName': '公司名称'})
    df1 = df1[~((df1['Email'] == "无") & (df1['Phone'] == "无"))]
    df1.to_excel("确认公司信息.xlsx", index=False)

print(pd.__version__)
