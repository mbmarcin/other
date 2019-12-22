import pandas as pd


def get_data(path="..\..\data_projects"):
    """
    id ,
    data_sales
    """
    print('Loading data for model....')
    data_temp = pd.read_csv(path + "\\" + "data_prices.txt", sep=',', nrows=0)
    col1 = data_temp.columns[0]
    data_set = pd.read_csv(path + "\\" + "data_prices.txt", sep=',', dtype={col1: 'str'})
    data_set = data_set.replace(',', '.', regex=True)
    data_set.iloc[:, 6] = pd.to_numeric(data_set.iloc[:, 6])  # errors='coerce'
    data_set.iloc[:, 7] = pd.to_numeric(data_set.iloc[:, 7])  # errors='coerce'
    # data_set = data_set[pd.to_numeric(data_set.cena, errors='coerce').isnull()] # sprawdzajka do błedów w formacie
    return data_set



def model_cus(df0, cus):
    cols = df0.columns
    df0 = df0.loc[df0.iloc[:, 0] == cus]

    # shares for group
    df = df0.loc[:, [cols[0], cols[4], cols[7]]]
    grouped = df.groupby([df.iloc[:, 1]]).sum().reset_index()
    grouped['sh'] = (grouped.iloc[:, 1] / grouped.iloc[:, 1].sum()) * 100
    group_to_check = grouped.loc[grouped.iloc[:, 2] >= 20, cols[4]].tolist()  # check group >= 20 %

    # shares for brand
    df2 = df0.loc[(df0.iloc[:, 0] == cus), [cols[5], cols[7]]]
    grouped_ = df2.groupby([df2.iloc[:, 0]]).sum().reset_index()
    grouped_['sh'] = (grouped_.iloc[:, 1] / grouped_.iloc[:, 1].sum()) * 100
    brand_to_check = grouped_.loc[grouped_.iloc[:, 2] >= 20, grouped_.columns[0]].tolist()  # check brand >= 20 %

    # avg_min price for sku
    df1 = df0.loc[(df0.iloc[:, 0] == cus) & (df0.iloc[:, 4].isin(group_to_check)) & (df0.iloc[:, 5].isin(brand_to_check)), [cols[2], cols[6], cols[7]]]
    df1['min'] = df1.iloc[:, 2] / df1.iloc[:, 1]

    sum_ = df1.groupby([df1.iloc[:, 0]]).agg({df1.columns[1]: "sum", df1.columns[2]: "sum", df1.columns[3]: "min"}).reset_index()
    sum_['avg_'] = sum_.iloc[:, 2] / sum_.iloc[:, 1]
    cus_df = sum_.loc[:, [sum_.columns[0], sum_.columns[1], sum_.columns[3], sum_.columns[4]]]
    return cus_df, cus_df.iloc[:, 0].tolist()


def model_all(df0, cus, skus):
    # avg_ price for sku
    team = df0.loc[(df0.iloc[:, 0] == cus), df0.columns[1]].drop_duplicates().values
    df1 = df0.loc[(df0.iloc[:, 0] != cus) & (df0.iloc[:, 2].isin(skus)) & (df0.iloc[:, 1].isin(team)), [df0.columns[2], df0.columns[6], df0.columns[7]]]  # [df0.columns[2], df0.columns[6], df0.columns[7]] & (df0.iloc[:, 1].isin(team))
    df1['min'] = df1.iloc[:, 2] / df1.iloc[:, 1]

    sum_ = df1.groupby([df1.iloc[:, 0]]).agg({df1.columns[1]: "sum", df1.columns[2]: "sum", df1.columns[3]: "min"}).reset_index()
    sum_['avg_'] = sum_.iloc[:, 2] / sum_.iloc[:, 1]
    model_df = sum_.loc[:, [sum_.columns[0], sum_.columns[3], sum_.columns[4]]]
    return model_df


def campare_result(cus_list, dta=get_data()):
    all_df = list()

    for i in cus_list:
        cus_df, ids_to_check = model_cus(dta, i)
        avg_all = model_all(dta, i, ids_to_check)

        df_main = pd.merge(cus_df, avg_all, on=cus_df.columns[0], how='left', suffixes=('_df1', '_df2')).fillna(0)
        df_main['df_avg_'] = df_main.iloc[:, 3] - df_main.iloc[:, 5]
        df_main['df_min_'] = df_main.iloc[:, 2] - df_main.iloc[:, 4]
        df_main['id'] = i

        all_df.append(df_main.round(2))

        '#print progress'
        if len(all_df) % 5 == 0:
            print('Camparing models for customer: {}/{}'.format(len(all_df), len(cus_list)))
        else:
            pass

    return pd.concat(all_df, sort=False)



print(get_data().head())

#print(campare_result(x, dta))

