import pandas as pd


def get_data(path="..\..\data_projects"):
    """id ,
    date_sales
    """
    print('Loading data...')
    data_temp = pd.read_csv(path+"\\"+"tableInput.txt", sep=';', nrows=0)
    col1 = data_temp.columns.values[0]
    data_set = pd.read_csv(path+"\\"+"tableInput.txt", sep=';', dtype={col1: 'str'})
    data_set.iloc[:, 1] = pd.to_datetime(data_set.iloc[:, 1])
    return data_set


def parametr0(df):
    """
    :param df0:
    :return: parametrs
    """
    print('Loading parameters...')
    col = df.columns.values
    list_id = df.iloc[:, 0].drop_duplicates().tolist()
    max_date = df.iloc[:, 1].max()
    max_year = df.iloc[:, 1].dt.year.max()
    max_year_month = df.loc[df.iloc[:, 1].dt.year == max_year, col[1]].dt.month.max()
    return list_id, max_date, max_year, max_year_month


def get_status_id(df0):
    """
    :param df0:
    :return: table with status(conditions by sales date) id
    """
    print('Start checking status...')
    col = df0.columns.values
    list_id_, max_date_, max_year_, max_year_month_ = parametr0(df0)

    t1 = pd.DataFrame(columns=('id', 'status', 'days', 'avg', 'std', 'activ'))
    row_num = 0
    counter = list()

    for i in list_id_:
        dta_all = df0.loc[df0.iloc[:, 0] == i, col[1]].sort_values(ascending=False).to_frame()  # data for user

        dta_all['date_new'] = dta_all.iloc[:, 0].shift(periods=1, freq=None, axis=0)
        dta_all = dta_all.iloc[1:]
        dta_all['df_date'] = (dta_all.loc[:, 'date_new'] - dta_all.iloc[:, 0]).dt.days.fillna(0).astype(int)

        '#data for max year and id'
        dta_max_year = dta_all.loc[dta_all.iloc[:, 1].dt.year == max_year_]

        avg = round(dta_max_year.df_date.mean(), 3)
        std = round(dta_max_year.df_date.std(), 3)
        activ = len(dta_max_year.iloc[:, 1].dt.strftime('%m%Y').drop_duplicates())

        '#max date - max date for id'
        days_from_max_days = (max_date_ - dta_all.iloc[:, 1].max()).days

        '#max date - max date for id without max month'
        days_from_max_days_ = (max_date_ - dta_all.loc[dta_all.iloc[:, 1].dt.month != max_year_month_, 'date_new'].max()).days

        '#check id neglacted'
        x = 0
        if dta_all.loc[(dta_all.iloc[:, 1].dt.year == max_year_) & (dta_all.iloc[:, 1].dt.month == max_year_month_), 'date_new'].count() == 0:

            for a in range(1, 4):
                if dta_all.loc[dta_all.iloc[:, 1].dt.strftime('%m%Y') == (max_date_ - pd.DateOffset(months=a)).strftime('%m%Y'), 'date_new'].count() > 0:
                    x += 1
                else:
                    break

        '#make status'
        dta = dta_all.iloc[:, 1]

        if int(dta[(dta.dt.year == max_year_) & (dta.dt.month == max_year_month_)].count()) >= 1 \
                and int(dta.count()) == 0:
                #and int(dta[(dta.dt.year == max_year_) & (dta.dt.month != max_year_month_)].count()) == 0:

            t1.loc[row_num] = [i, 'pierwszy_zakup', days_from_max_days, avg, std, activ]

        elif x == 3:
            t1.loc[row_num] = [i, 'zaniedbany', days_from_max_days, avg, std, activ]

        elif days_from_max_days >= 180:
            t1.loc[row_num] = [i, 'utracony_6mc', days_from_max_days, avg, std, activ]

        elif days_from_max_days >= 90:
            t1.loc[row_num] = [i, 'utracony_3mc', days_from_max_days, avg, std, activ]

        elif days_from_max_days >= 60:
            t1.loc[row_num] = [i, 'utracony_2mc', days_from_max_days, avg, std, activ]

        elif dta[(dta.dt.year == max_year_) & (dta.dt.month == max_year_month_)].count() > 0 and days_from_max_days_ >= 210:
            t1.loc[row_num] = [i, 'ożywiony_6mc', days_from_max_days, avg, std, activ]

        elif dta[(dta.dt.year == max_year_) & (dta.dt.month == max_year_month_)].count() > 0 and days_from_max_days_ >= 120:
            t1.loc[row_num] = [i, 'ożywiony_3mc', days_from_max_days, avg, std, activ]

        else:
            pass
            #t1.loc[row_num] = [i, 'normal', days_from_max_days, avg, std]

        row_num += 1
        counter.append(i)

        if len(counter) % 50 == 0:
            print("Qty_user: ", len(counter), "/", len(list_id_))
        else:
            continue

    print('end_process')
    return t1.to_csv('status_id_by_date.txt', sep=';', index=False, header=True)


if __name__ == "__main__":
    get_status_id(get_data())
