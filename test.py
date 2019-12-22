import pandas as pd
from datetime import datetime
from status_id_by_date import get_data, parametr0

"""
'#check id neglacted'
x = 0

if dta_all.loc[(dta_all.iloc[:, 1].dt.year == max_year_) & (dta_all.iloc[:, 1].dt.month == max_year_month_), 'data'].count() == 0:
    #print('yes')
    for a in range(1, 4):
        if dta_all.loc[dta_all.iloc[:, 1].dt.strftime('%m%Y') == (max_date_ - pd.DateOffset(months=a)).strftime('%m%Y'), 'data'].count() > 0:
            x += 1
            #print(dta_all.loc[dta_all.iloc[:, 1].dt.strftime('%m%Y') == (max_date_ - pd.DateOffset(months=a)).strftime('%m%Y'), ['data', 'idCus']])
        else:
             break
#df['DOB1'] = df['DOB'].dt.strftime('%m/%d/%Y')

print(dta_all)
#print(dta_all.iloc[:, 1].dt.strftime('%m%Y'))
"""
"""
if dta_all.loc[(dta_all.iloc[:, 1].dt.year == max_year_) & (dta_all.iloc[:, 1].dt.month == max_year_month_), 'date_new'].count() == 0:

    for a in range(1, 4):
        if dta_all.loc[dta_all.iloc[:, 1].dt.month == (max_date_ - pd.DateOffset(months=a)).month, 'date_new'].count() > 0:
            x += 1
        else:
             break
"""
"""
#print(dta_all - pd.DateOffset(months=1))
def myFun(arg1, arg2, arg3):
    print("arg1:", arg1)
    print("arg2:", arg2)
    print("arg3:", arg3)

# Now we can use *args or **kwargs to
# pass arguments to this function :
args = ("Geeks", "for", "Geeks")
myFun(*args)

kwargs = {"arg1": "Geeks", "arg2": "for", "arg3": "Geeks"}
myFun(**kwargs)
myFun("Hi", first='Geeks', mid='for', last='Geeks')

    #grouped['mod_mode'] = grouped.apply(lambda i: check_mode(i['cena_median']), axis=1)
    #grouped['mod_mode'] = grouped.apply(lambda i: sum(i.cena_median)/len(i.cena_median) if i.cena_median == list() else i.cena_median, axis=1)

    #grouped['mod_mode'] = grouped.iloc[:, 5].apply(lambda i: sum(i)/len(i) if i == list else float(i))
    #grouped['mod_mode'] = grouped.iloc[:, 5].apply(check_mode)

    #gg = grouped.groupby([grouped.iloc[:, 0]])[['cena_mode']]
    #gg.apply(check_mode)
    #grouped['mod_mode'] = grouped.apply(check_mode(grouped.iloc[:, 5]))
    #gg.apply(check_mode(grouped.iloc[:, 5]))
"""

"""
for cus in fg:
    df0 = dta.loc[dta.iloc[:, 0] == cus]
    months = df0.iloc[:, 2].sort_values().drop_duplicates().to_list()
    print(months)

    if len(months) >= 2:
        for i in range(len(months)-1):
            df1 = df0.loc[df0.iloc[:, 2].isin([months[i], months[i+1]])]
            x = df1.iloc[:, 2].sort_values().to_list()
            print(x, cus)
    else:
        pass
"""
"""
a = ['a','b','c','d']
#b = [1,1,2,2,3,3,4,4,5,5]
b = [1.1,4,[1,2],[5,6,7]]
#b = [3,3,3,3,4]
df = pd.DataFrame({'a':a,'b':b})
#k = float(df.kurtosis())
#m = float(df.mean())
#l = len(b)

for row in df.iloc[:, 0]:
    print(type(row), row)
    if isinstance(row, list):
        print(sum(row) / len(row), sum(row))
    else:
        print(row)

x = df['b'].apply(pd.Series)
x_ = pd.concat([df[:], x[:]], axis=1)

x.loc[:, 'total'] = x.mean(axis=1)
len(x.columns)
xc = x.copy()
print(x.loc[:, x.columns[3]])
"""

# sum or mean by row
"""
dfz = pd.DataFrame(
    {
        "Undergraduate": {"Straight A's": 240, "Not": 3_760},
        "Graduate": {"Straight A's": 60, "Not": 440},
    }
)
dfz.loc[:,'Total'] = dfz.mean(axis=1)
print(dfz)
"""

# OBMICRW19STDEN1
# HWSHARFS123W2PL

"""
def wag(df):
    df.groupby()
    df['x'] = df.iloc[:, 5].sum()/df.iloc[:, 11].sum()
    return df
#df0.iloc[:, 5]
grouped = df0.groupby(df0.iloc[:, 4])
df1 = grouped.apply(wag)
"""

"""
#backUP
def model_price_qty(df0, list_sku):
    #przerobić funkcje na kolumny tylko potrzebne do przetworzenia

    def median(s):
        return s.sort_values().median()

    df1 = df0.loc[df0.iloc[:, 4].isin(list_sku)]
    grouped = df1.groupby([df1.iloc[:, 4]]).agg({df1.columns[6]: ['min', 'mean', 'std', 'max',  median, pd.Series.kurtosis, pd.Series.mode]}).fillna(0)
    grouped.columns = grouped.columns.map(lambda x: '_'.join([str(i) for i in x]))  # for concat multiIndex
    df1 = grouped.reset_index()

    #avg for mode
    md = df1.loc[:, df1.columns[7]].apply(pd.Series)
    md.loc[:, 'avg_mode'] = round(md.mean(axis=1), 2) # MOŻE mediane zastosowac lepiej

    df2 = pd.concat([df1.iloc[:, :], md.loc[:, 'avg_mode']], axis=1)
    return df2
"""
"""
df1 = pd.DataFrame({'id': [23, 24, 25, 26, 22], 'a': [1, 2, 3, 4, 5], 'b': [5, 4, 3, 2, 1]})
df1.set_index('a', inplace=True)
df2 = pd.DataFrame({'id': [23, 24, 25, 26, 22], 'a': [6, 7, 8, 9, 10], 'b': [10, 9, 8, 7, 6]})
df2.set_index('id', inplace=True)


def dfDiff(oldFrame, newFrame):
    dfBool = (oldFrame != newFrame).stack()
    diff = pd.concat([oldFrame.stack()[dfBool],
                      newFrame.stack()[dfBool]], axis=1)
    diff.columns = ["Old", "New"]
    return diff


x = dfDiff(df1, df2)  # .reset_index()
print(x)

#print(df1.stack().reset_index(), df1)

print(df1.stack())
"""

"""
x = 'test'
df2 = pd.DataFrame({'id': [23, 24, 25, 26, 22], 'a': [6, 7, 8, 9, 10], 'b': [10, 9, 8, 7, 6]})
print(df2.where(df2 >= 7).dropna())
"""

"""
df_A = pd.DataFrame({'start_date':['2017-03-27','2017-01-10','2019-01-01'],'end_date':['2017-04-20','2017-02-01','2019-01-02']})
df_B = pd.DataFrame({'event_date':['2017-01-20','2017-01-27','2019-01-02'],'price':[100,200,50]})

df_A['end_date'] = pd.to_datetime(df_A.end_date)
df_A['start_date'] = pd.to_datetime(df_A.start_date)
df_B['event_date'] = pd.to_datetime(df_B.event_date)

df_A = df_A.assign(key=1)
df_B = df_B.assign(key=1)
df_merge = pd.merge(df_A, df_B, on='key').drop('key',axis=1)

df_merge = df_merge.query('event_date >= start_date and event_date <= end_date')
df_out = df_A.merge(df_merge, on=['start_date','end_date'], how='left').fillna('').drop('key', axis=1)
print(df_out)
"""


"""
def gg():
    val = 7
    x = [i*val for i in range(val)][1:]
    return x

x = 10
def foo(x):
    x += 1
    print(x)

foo(x)
"""

"""
result = to_group_dta.groupby([to_group_dta.iloc[:, 0]]).agg(
            {to_group_dta.columns[1]: pd.Series.nunique,
             to_group_dta.columns[2]: pd.Series.nunique,
             to_group_dta.columns[3]: pd.Series.count,
             to_group_dta.columns[4]: ['min', 'max']})
result.columns = result.columns.map(lambda x: '_'.join([str(i) for i in x]))  # for concat multiIndex
"""

"""

months = ['Jan','Apr','Mar','June']
days = [31, 0, 31, 30]
sku = [1, 2, 3, 4]

d = {'skus':sku, 'Month':months,'Day':days}
#df = pd.DataFrame(d, columns=['Month','Day'])
df = pd.DataFrame(d)
data_tuples = list(zip(df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2]))

new_df = pd.DataFrame(data_tuples)

x = new_df.loc[new_df.isin([1]).any(1)]
"""
#x.loc[df.isin([1]).any(1)]

"""
dict = {'name':["aparna", "pankaj", "sudhir", "Geeku"],
        'degree':["MBA", "BCA", "M.Tech", "MBA"],
        'score':[90, 40, 80, 98],
        'id':[1, 90, 3, 4]}
"""

# dict = {'par':["aparna", "pankaj", "sudhir", "Geeku"],
#         'degree':["MBA", "BCA", "M.Tech", "MBA"],
#         'score':[90, 50, 80, 98],
#         'id':[1, 90, 8, 4]}
#
# df = pd.DataFrame(dict)
# #print(df.iloc[:, 1].count())
#
# df['par'] = df['id']
#
# print(df.iloc[:, 0].count())

list = [(1,2),(1,3),(1,6),(1,9), (1,2), (1,2),(1,2),(1,2),(1,2),(1,2),(1,2),(1,2),(1,2)]

# car = {
#   "brand":[]
# }
#
# #car.update({"color": "Red"})
#
list.append((3,4))
x = pd.DataFrame(list)
# c = pd.DataFrame({"brand": [5],
#                   'alert':[8]})
#
# s = x.append(c, sort=False)



print(x.drop_duplicates(inplace=False))

"""
x = [[1,2,3,4,5,6,7,8,9], [10]]

flattened  = [val for sublist in x for val in sublist]
print(flattened)
"""

# x = car['brand']
# x.append(8)
# print(x)

"""
months = ['Jan','Apr','Mar','June']
days = [31, 0, 31, 30]
sku = [1, 2, 3, 4]

d = {'skus':sku, 'Month':months,'Day':days}
#df = pd.DataFrame(d, columns=['Month','Day'])
df = pd.DataFrame(d)
data_tuples = list(zip(df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2]))

new_df = pd.DataFrame(data_tuples)
print(new_df)
"""



"""
ml = list()
for i, j in df.iterrows():
    if j[2] >= 90:
        x = list()
        for val in range(2):
            x.append(j[val])
        #print(j)
        ml.append(x)
x = pd.DataFrame(ml)
print(x)
"""
"""
for col, dta_col in df.iteritems():
    #print(col)
    print(dta_col)
"""

"""
for col in df.loc[:, df.columns[[2, 3]]]:
    for row in col:
        print(col[row])
    #print(df[df[col] >= 90])
"""

"""
for key, value in df.iteritems():
    print(key)
"""

"""
m = list()

for col in df.loc[:, df.columns[[2, 3]]]:
    for row in range(df.iloc[:, 1].count()):
        if df.loc[row, col] >= 90:
            #print(df.columns[1] + 'ok' + df.loc[row, df.columns[1]])
            m.append(df.loc[row, df.columns[0]] + '_' + df.columns[0] + '_' + df.loc[row, df.columns[1]])

        else:
            pass


dfx = pd.DataFrame({'allert':m})
print(dfx)
"""
#df.loc[row, df.columns[2]]
#df[col][row]
#print(df[col][row])
#df['name'][row]
#x = list(range(4))
#print(x)

"""
dict = {'key1':'geeks', 'key2':'for'}
print("Current Dict is: ", dict)

dict.update({'key3':'geeks'})
print("Updated Dict is: ", dict)
"""









