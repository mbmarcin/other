import pandas as pd


def get_data(path="..\..\data_projects"):
    """
    id ,
    date_sales
    """
    print('Loading data...')
    data_temp = pd.read_csv(path + "\\" + "data_sales.txt", sep=';', nrows=0)
    col1 = data_temp.columns.values[0]
    data_set = pd.read_csv(path + "\\" + "data_sales.txt", sep=';', dtype={col1: 'str'})
    data_set = data_set.replace(',', '.', regex=True)
    data_set.iloc[:, 3] = pd.to_numeric(data_set.iloc[:, 3])
    return data_set


def add_prop(df):
    df['prop'] = (df.Sales / df.Sales.sum()) * 100
    return df


def add_cumsum(df):
    df['cumsum'] = df.sort_values(by=['prop'], ascending=False).prop.cumsum()
    return df


def shares_by_year(df):
    cols = df.columns.values
    group = df.groupby([cols[0], cols[1]], as_index=False)[cols[3]].sum()
    df0 = group.groupby([cols[1]]).apply(add_prop)
    df1 = df0.groupby([cols[1]]).apply(add_cumsum)
    pivot = df1.pivot(index=cols[0], columns=cols[1]).fillna(0)
    pivot.columns = pivot.columns.map(lambda x: '_'.join([str(i) for i in x]))  # for concat multiIndex
    df2 = pivot.reset_index(col_level=0)  # for remove multiIndex
    df2['d_sales'] = df2.iloc[:, 2] - df2.iloc[:, 1]
    df2['d_prop'] = df2.iloc[:, 4] - df2.iloc[:, 3]
    df2['d_cumsum'] = df2.iloc[:, 6] - df2.iloc[:, 5]
    print('Table with shares for a year saved')
    return df2.to_csv('id_share_by_year.txt', sep=';', index=False, header=True)


shares_by_year(get_data())
# )
