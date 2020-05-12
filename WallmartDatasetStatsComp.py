

import pandas as pd
import os #разобраться с этой штукой
import matplotlib.pyplot as plt
from numpy import datetime64 as datetime

CSVNAME = 'walmart.csv'
PERCENTDELETION = 0.6

def DownloadDS():
    df = pd.read_csv(os.getcwd()+'/'+CSVNAME)
    return df

def PreWork(df):
    print('Общая информация:')
    print ('Первые 5 записей:\n' + str(df.head()) + '\n')
    print ('Последние 5 записей:\n' + str(df.iloc[len(df)-5:len(df)]) + '\n')
    print ('Кол-во наблюдений:\n' + str(len(df)))
    
    print('Названия и типы переменных:\n')
    print(df.dtypes)
    print('\n')
    
def DateToDate(df):
    print('Изменяем тип переменной даты:')
    df['Date'] = pd.to_datetime(df['Date'])
    #print(str(type(df['Date'][0])))
    #print(str(type(df['Date'][len(df)-1])))
    print('Получившийся тип столбца - ' + str(df.Date.dtypes))
    print('\n')
    return df
    
def MissingFields(df):
    print('Информация о пустых полях:')
    
    for column in df:
        emptyFCount = df[column].isnull().sum()
        print('У переменной ' + column + ' ' + str(emptyFCount) + ' пустых полей')
        if (emptyFCount/len(df) > PERCENTDELETION):
            del df[column]
    
    print('\n')
    return df

def Sampling(df):
    print('Информация о выборке:')
    print('Магазинов в датасете ' + str(df.Store.value_counts().size))
    print('Отделов в датасете ' + str(df.Dept.value_counts().size))
    print('Охватывается промежуток в ' + str((df.Date.max()-df.Date.min()).days) + ' дней')
    print('\n')


def Dynamics(df):
    df = df[['Date', 'Weekly_Sales']]
    df = df.groupby('Date', as_index=False).aggregate(sum)
    df.plot(x='Date', y='Weekly_Sales')
    
def Corr(df):
    plt.matshow(df.corr())
    plt.show()
    
def TopSupp(df, mainfield, topcount):
    dfSel = df[[mainfield, "Weekly_Sales"]]
    dfSel = dfSel.groupby(mainfield, as_index=False).aggregate(sum)
    dfSel.sort_values(by=['Weekly_Sales'], inplace=True, ignore_index=True)
    df = df.loc[df[mainfield].isin(dfSel[mainfield].head(topcount))]
    l = [] #для хранения отдельных экземпляров датафреймов для каждого элемента mainfield
    for i in range(topcount):
        l.append(df[df[mainfield] == dfSel[mainfield][i]])
        l[i] = l[i][['Date', "Weekly_Sales"]]
        l[i] = l[i].groupby('Date', as_index=False).aggregate(sum)
        l[i] = [l[i], dfSel[mainfield][i]]
    for frame in l:
        plt.plot(frame[0]['Date'], frame[0]['Weekly_Sales'], label = frame[1])
    plt.legend()
    plt.show()
    
def Top5(df):
    TopSupp(df, 'Store', 5)

def Top10(df):
    df = df[df.Type == 'A']
    df = df[['Weekly_Sales', 'Date', 'Dept']]
    df = df[df.Date >= datetime('2011')]
    df = df[df.Date < datetime('2012')]
    
    TopSupp(df, 'Dept', 10)

    
def main():
    df = DownloadDS()
    PreWork(df)
    df = DateToDate(df)
    df = MissingFields(df)
    Sampling(df)
    Dynamics(df)
    Corr(df)
    Top5(df)
    Top10(df)

main()