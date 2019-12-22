import pandas as pd


def get_data(file="Q:\ExternalData\Analizy\MB\prices_user\data_prices.txt"):
    """
    :param path: df source
    :return: df with data
    """
    print('Loading data for model...')
    data_temp = pd.read_csv(file, sep=',', nrows=0)
    col1 = data_temp.columns[0]
    data_set = pd.read_csv(file, sep=',', dtype={col1: 'str'})
    return data_set


def model_cus(df0, cus, m):
    cols = df0.columns
    df0 = df0.loc[(df0.iloc[:, 0] == cus) & (df0.iloc[:, 9] == m)]

    # shares for group
    df = df0.loc[:, [cols[0], cols[4], cols[7]]]
    grouped = df.groupby([df.iloc[:, 1]]).sum().reset_index()
    grouped['sh'] = (grouped.iloc[:, 1] / grouped.iloc[:, 1].sum()) * 100
    group_to_check = grouped.loc[grouped.iloc[:, 2] >= 20, cols[4]].tolist()  # check group >= 20 %-----------------------------------------------------------------------

    # shares for brand
    df2 = df0.loc[(df0.iloc[:, 0] == cus), [cols[5], cols[7]]]
    grouped_ = df2.groupby([df2.iloc[:, 0]]).sum().reset_index()
    grouped_['sh'] = (grouped_.iloc[:, 1] / grouped_.iloc[:, 1].sum()) * 100
    brand_to_check = grouped_.loc[grouped_.iloc[:, 2] >= 20, grouped_.columns[0]].tolist()  # check brand >= 20% ----------------------------------------------------------

    # avg_min price for sku
    df1 = df0.loc[(df0.iloc[:, 0] == cus) & (df0.iloc[:, 4].isin(group_to_check)) & (df0.iloc[:, 5].isin(brand_to_check)), [cols[2], cols[6], cols[7]]]
    df1['min'] = df1.iloc[:, 2] / df1.iloc[:, 1]

    sum_ = df1.groupby([df1.iloc[:, 0]]).agg({df1.columns[1]: "sum", df1.columns[2]: "sum", df1.columns[3]: "min"}).reset_index()
    sum_['avg_'] = sum_.iloc[:, 2] / sum_.iloc[:, 1]
    cus_df = sum_.loc[:, [sum_.columns[0], sum_.columns[1], sum_.columns[3], sum_.columns[4]]]
    return cus_df, cus_df.iloc[:, 0].tolist()


def model_all(df0, cus, skus, m):
    # avg_ price for sku
    team = df0.loc[(df0.iloc[:, 0] == cus), df0.columns[1]].drop_duplicates().values
    df1 = df0.loc[(df0.iloc[:, 0] != cus) & (df0.iloc[:, 2].isin(skus)) & (df0.iloc[:, 1].isin(team) & (df0.iloc[:, 9] == m)), [df0.columns[2], df0.columns[6], df0.columns[7]]]  # [df0.columns[2], df0.columns[6], df0.columns[7]] & (df0.iloc[:, 1].isin(team))
    df1['min'] = df1.iloc[:, 2] / df1.iloc[:, 1]

    sum_ = df1.groupby([df1.iloc[:, 0]]).agg({df1.columns[1]: "sum", df1.columns[2]: "sum", df1.columns[3]: "min"}).reset_index()
    sum_['avg_'] = sum_.iloc[:, 2] / sum_.iloc[:, 1]
    model_df = sum_.loc[:, [sum_.columns[0], sum_.columns[3], sum_.columns[4]]]
    return model_df


def campare_result(target_df, dta=get_data()):    #target_df  #cus_list, months_list,
    """
    :param target_df: df with ids and months to check
    :param dta: df with source, data with skus, prices, sales, year, month
    :return: df with campared avg and price min for sku, id
    """
    all_df = list()
    cus_list = target_df.iloc[:, 0].drop_duplicates().to_list()
    counter = list()

    for i in cus_list:
        months_list = target_df.loc[(target_df.iloc[:, 0] == i), target_df.columns[3]].to_list()
        counter.append(i)

        for m in months_list:
            cus_df, ids_to_check = model_cus(dta, i, m)
            avg_all = model_all(dta, i, ids_to_check, m)

            df_main = pd.merge(cus_df, avg_all, on=cus_df.columns[0], how='left', suffixes=('_df1', '_df2')).fillna(0)
            df_main['df_avg_'] = df_main.iloc[:, 3] - df_main.iloc[:, 5]
            df_main['df_min_'] = df_main.iloc[:, 2] - df_main.iloc[:, 4]
            df_main['id'] = i
            df_main['m_cam'] = m

            all_df.append(df_main.round(2))

        '#print progress'
        if len(counter) % 5 == 0:
            print('Camparing models for customer: {}/{}'.format(len(counter), len(cus_list)))
        else:
            pass
    return pd.concat(all_df, sort=False)



