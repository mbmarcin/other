import pandas as pd
#import model as m


def get_data(path="..\..\data_projects"):
    """
    id ,
    data_sales
    """
    print('Loading data...')
    data_temp = pd.read_csv(path + "\\" + "data_sales.txt", sep=';', nrows=0)
    col1 = data_temp.columns.values[0]
    data_set = pd.read_csv(path + "\\" + "data_sales.txt", sep=';', dtype={col1: 'str'})
    data_set = data_set.replace(',', '.', regex=True)
    data_set.iloc[:, 3] = pd.to_numeric(data_set.iloc[:, 3])
    return data_set


def campare_shares_and_cumsum(df):
    """
    :param df: with id, date(campare two yers or months), sales
    :return: df with id
    """

    def _add_prop(df):
        df['prop'] = (df.iloc[:, 2] / df.iloc[:, 2].sum()) * 100
        return df

    def _add_cumsum(df):
        df['cumsum'] = df.sort_values(by=['prop'], ascending=False).prop.cumsum()
        return df

    cols = df.columns
    df0 = df.groupby([cols[1]]).apply(_add_prop)
    df1 = df0.groupby([cols[1]]).apply(_add_cumsum)
    pivot = df1.pivot(index=cols[0], columns=cols[1]).fillna(0)
    pivot.columns = pivot.columns.map(lambda x: '_'.join([str(i) for i in x]))  # for concat multiIndex
    df2 = pivot.reset_index(col_level=0)  # for remove multiIndex
    df2['d_sales'] = df2.iloc[:, 2] - df2.iloc[:, 1]
    df2['d_prop'] = df2.iloc[:, 4] - df2.iloc[:, 3]
    df2['d_cumsum'] = df2.iloc[:, 6] - df2.iloc[:, 5]
    print('Table with shares for a year saved')
    #df2.to_csv('id_share_by_year.txt', sep=';', index=False, header=True)
    return df2

"""
def _basket(df0):

    #:param df0:
    #:return: df with id, max, min

    # shares and cum_sam-------------------------------------------------------------
    cols = df0.columns.values
    df = df0.sort_values(by=cols[3], ascending=False)
    df['prop'] = (df.iloc[:, 3] / df.iloc[:, 3].sum()) * 100
    df['cumsum'] = df.sort_values(by=['prop'], ascending=False).prop.cumsum()

    # bins----------------------------------------------------------------------------
    bins = [0, 20, 40, 60, 80, 101]
    labels = [2, 24, 46, 68, 81]
    df['basket_'] = pd.cut(df['cumsum'], bins=bins, labels=labels).astype(int)
    return df


def max_min_basket(df0, y):
    df1 = df0.loc[df0.iloc[:, 1] == y]
    df = df1.groupby([df0.iloc[:, 1], df0.iloc[:, 2]], group_keys=False).apply(_basket)
    df = df.groupby([df0.iloc[:, 0]]).agg({"basket_": ['min', 'max']})
    df.columns = ["_".join(x) for x in df.columns]
    df = df.reset_index()
    df['diff'] = df['basket__max'] - df['basket__min']

    #dorzucić sortowanie i zastanowić sie nad kierunkiem wzrost/spadek

    return df.sort_values('diff', ascending=False)
"""
"""
# dane do klasyfikcji klientów według wzrostu pareto-------------------------------
df = get_data()
# ----------------------------------------------------------------------------------F?
cols = df.columns
group = df.groupby([cols[0], cols[1]], as_index=False)[cols[3]].sum()  # data for  2 years
df2 = campare_shares_and_cumsum(group)
dta = df2.loc[(df2.iloc[:, 2] != 0) & (df2.iloc[:, 9] < -4.5)].sort_values(by=['d_cumsum'])

ids = dta.iloc[:, 0].tolist()
# -----------------------------------------------------------------------------------------------

# -------------------------------------sprawdzanie cen dla określonych w/w warunkach
x = m.campare_result(ids)
x.to_csv('campared_prices.txt', sep=';', index=False, header=True) # ----------------------zapisanie danych
print('koniec!')
"""

#TEST1
"""
dta = get_data2()
#pd.to_datetime(dta.iloc[:,1], format='%Y-%m')
dta.iloc[:,1] = dta.iloc[:,1].dt.strftime('%Y-%m')
#dta.iloc[:,1] = pd.to_datetime(dta.iloc[:,1])
print(dta.info())
"""


#TEST2
"""
#cus = ['10946661', '10334905', '00063639', '10643892']
#x = ['10643892', '10334905']
def main(df0):  # różne agregacje dla roku, miesiąca R/R, 
    df = get_data()
    max_year = df.iloc[:, 1].drop_duplicates().max()
    max_month_1 = df.loc[df.iloc[:, 1] == max_year, df.columns[2]].max() - 1
    cols = df.columns.values
    group = df.groupby([cols[0], cols[1]], as_index=False)[cols[3]].sum()  # data for  2 years
    df['mc'] = df.iloc[:, 1].astype('str') + df.iloc[:, 2].astype('str')
    # df.columns
    df_ = df.loc[df.iloc[:, 2] == 5, df.columns[[0, 4, 3]]]  # data set for one month 2018,2019
    # df_y = df.loc[(df.iloc[:, 1] == max_year) & (df.iloc[:, 1] == max_year)]
    print(group.head()) 
    pass
"""