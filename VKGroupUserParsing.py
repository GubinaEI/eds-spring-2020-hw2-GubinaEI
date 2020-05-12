

import vk_api
import pandas as pd
import matplotlib.pyplot as plt

USRCOUNT = 10000 #ориентировочное кол-во пользователей для отбора
USRSTEP = 1000 #шаг проверки пользователей, от 1 до 1000
BDAYCHECKS = 3 #сколько различных комбинаций из 50-и человек проверяем на совпадение дней рождения

def TokenLogin():
    print('...token authorization...\n')
    #https://oauth.vk.com/authorize?client_id=***&display=page&scope=friends,news,groups&response_type=token&v=5.103&state=123456
    link = '139923997' #id паблика (femalememes)
    print('input token')
    tokenstring = input()
    vk_session = vk_api.VkApi(token=tokenstring)
    return [vk_session.get_api(), link]

def ReadAndFilter(vk, groupname, df):
    print('...reading and filtration...\n')
    offs= 0
    thatsall = 0
    maxcount = vk.groups.getById(group_id = groupname, fields = 'members_count')[0]['members_count']
    dfsize = 0
    
    while thatsall != 1:
        temp = vk.groups.getMembers(group_id=groupname, offset = offs, count = USRSTEP)
        offs += USRSTEP
        usrDict = vk.users.get(user_ids = temp['items'], fields = 'bdate')
        for i in usrDict:
            if ('bdate' in i):
                fulldate = i['bdate'].split('.')
                df = df.append({'name': i['first_name'], 'surname':i['last_name'], 'id':i['id'], 'bdateday':fulldate[0], 'bdatemonth':fulldate[1]}, ignore_index=True)
                dfsize +=1
        if (dfsize >= USRCOUNT or offs >= maxcount):
            thatsall = 1
    return df


def GetUsersList(vk, groupname):
    print('...getting users...\n')
    column_names = ['name', 'surname', 'id','bdateday','bdatemonth']
    df = pd.DataFrame(columns = column_names)
    df = ReadAndFilter(vk, groupname, df)
    #print(df.to_string())
    return df


def UsersStats(df): #гистограмма, посмотреть похоже ли на равномерное распределение
    print('...stats solving...\n')
    lstats = []
    for i in range(12):
        lstats.append(0)
    for i in df['bdatemonth']:
        lstats[int(i)-1] +=1 #кол-во родившихся в каждом месяце
    plt.figure()
    plt.bar([1,2,3,4,5,6,7,8,9,10,11,12], lstats) #на равномерное распределение похоже, столбики примерно одинаковые


def UsersProbab(df): #вероятность совпадения дней рождения из 50-и произвольных людей
    print('...probability solving...\n')
    counter = 0
    matchlist = []
    k = 0
    while k != BDAYCHECKS:
        df = df.sample(frac=1).reset_index(drop=True)
        i = 0
        while i != 49:
            j=i+2
            while j != 50:
                if (df['bdatemonth'][i]==df['bdatemonth'][j] and df['bdateday'][i]==df['bdateday'][j]):
                    if not ([df['id'][i], df['id'][j]] in matchlist or [df['id'][j], df['id'][i]] in matchlist):
                        matchlist.append([df['id'][i], df['id'][j]])
                        counter+=1
                j+=1
            i+=1 
        k+=1
    
    print('в ', BDAYCHECKS, ' экспериментах произошло ', counter, ' совпадений дней рождения у пользователей с id:')
    for i in matchlist:
        print(i[0], ' и ', i[1], '\n')

def main():
    session = TokenLogin()
    usrdf = GetUsersList(session[0], session[1])
    UsersStats(usrdf)
    UsersProbab(usrdf)

main()