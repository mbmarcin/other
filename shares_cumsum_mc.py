import pandas as pd


def get_data(file="Q:\ExternalData\Analizy\MB\prices_user\data_sales.txt"):
    """
    id ,
    data_sales
    """
    print('Loading data...')
    data_temp = pd.read_csv(file, sep=',', nrows=0)
    col1 = data_temp.columns.values[0]
    data_set = pd.read_csv(file, sep=',', dtype={col1: 'str'})
    return data_set


def compare_shares_and_cumsum(df):
    """
    :param df: with id, date(campare two yers or months), sales
    :return: df with campared pareto
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
    # print('Table with shares for a year saved')
    # df2.to_csv('id_share_by_year.txt', sep=';', index=False, header=True)
    return df2


def ranking_per_month(df):
    """
    :param df: with id, months, sales // min 2 month
    :return: df with campared pareto per month
    """
    dfa = df.copy()
    dfa['m'] = dfa.iloc[:, 1].astype('str') + '_' + dfa.iloc[:, 2].astype('str')
    teams = dfa.iloc[:, 4].drop_duplicates().to_list()

    list_df = list()

    for team in teams:
        df1 = dfa.loc[dfa.iloc[:, 4] == team]
        months = df1.iloc[:, 2].sort_values().drop_duplicates().to_list()
        #months_ = [1,2,3,4,5,6,7, 8] #-------------------------------------------- do wywalenia

        if len(months) >= 2:
            for i in range(len(months) - 1):
                df2 = df1.loc[df1.iloc[:, 2].isin([months[i], months[i + 1]]), [df1.columns[0], df1.columns[5], df1.columns[3]]]
                compared = compare_shares_and_cumsum(df2)

                # condstions for check to prices sku--------------------------------------------------------------------------
                campared_condstions = compared.loc[(compared.iloc[:, 2] != 0) & (compared.iloc[:, 9] < -4.5)].sort_values(by=['d_cumsum']).reset_index(drop=True)

                campared_condstions['month'] = months[i + 1]
                list_df.append(campared_condstions.iloc[:, [0, 8, 9, 10]])
    main_t = pd.concat(list_df)
    main_t.to_csv('compared_pareto_per_month.txt', sep=';', index=False, header=True)
    print('plik z pareto zapisany')
    return main_t


def main():
    source = get_data()
    # df with max year
    df0 = source.loc[source.iloc[:, 1] == source.iloc[:, 1].drop_duplicates().max()]
    df_pareto = ranking_per_month(df0)

    if len(df_pareto.iloc[:, 0]) >= 1:

        import model_mc as m
        campare_sku = m.campare_result(df_pareto)
        campare_sku.to_csv('compared_prices_TEST_mc.txt', sep=';', index=False, header=True)
        print('compared_prices_TEST_mc.txt')

    else:
        print('compared_pareto_per_month.txt')



main()

"""
import model_mc as m
test_result_df = m.campare_result(test_df)

test_result_df.to_csv('campared_prices_TEST_mc.txt', sep=';', index=False, header=True) # ----------------------zapisanie danych
print('zapisane')
"""


"""
# klasyfikacja klientów po wzroście w pareto po miesiącach
dta = dta.loc[dta.y == y, [dta.columns[0], dta.columns[1], dta.columns[2], dta.columns[3]]]
dta['mc'] = dta.iloc[:, 1].astype('str') + '_' + dta.iloc[:, 2].astype('str')

months = dta.iloc[:, 2].sort_values().drop_duplicates().to_list()
months_ = [1, 2, 3]

list_df = list()

if len(months_) >= 2:
    for i in range(len(months_)-1):
        df1 = dta.loc[dta.iloc[:, 2].isin([months_[i], months_[i+1]]), [dta.columns[0], dta.columns[4], dta.columns[3]]]
        campared = campare_shares_and_cumsum(df1)
        campared_condstions = campared.loc[(campared.iloc[:, 2] != 0) & (campared.iloc[:, 9] < -4.5)].sort_values(by=['d_cumsum']).reset_index(drop=True)
        campared_condstions['month'] = months_[i+1]
        list_df.append(campared_condstions.iloc[:, [0, 8, 9, 10]])
else:
    pass

dfg = pd.concat(list_df, sort=False)
x = dfg.loc[dfg.id == '00009373']

print(
x
)
"""

"""
    for i in months[1:]:
        df = dta.loc[dta.iloc[:, 2].isin([i, i-1])]
        print(df)
        break
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

# TEST1
"""

#pd.to_datetime(dta.iloc[:,1], format='%Y-%m')
dta.iloc[:,1] = dta.iloc[:,1].dt.strftime('%Y-%m')
#dta.iloc[:,1] = pd.to_datetime(dta.iloc[:,1])
print(dta.info())
"""

# TEST2
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
