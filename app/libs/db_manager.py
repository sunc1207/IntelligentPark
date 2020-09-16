from app.libs.db import *
from datetime import timedelta, datetime

def json_usage_his(list1, list2, res):
    for item in res:
        list1.append(item['usage'])
        list2.append(item['anomaly'])
    return list1, list2


def json_MD_his(list1, list2, list3, res):
    for item in res:
        list1.append(item['MD'])
        list2.append(item['Datetime'])
        list3.append(item['anomaly'])
    return list1, list2, list3


def json_usage_pre(list, res):
    for item in res:
        list.append(item['usage'])
    return list


def json_MD_pre(list1, list2, res):
    for item in res:
        list1.append(item['MD'])
        list2.append(item['Datetime'])
    return list1, list2

def get_energy_list(db, col, energy):
    col_his = col + "_4h_anomaly"
    col_pre = col + "_4h_pre"

    lastone = db.find_lastone(col_his)
    if lastone ==  None:
        col_his = '180_11_' + energy + "_4h_anomaly"
        col_pre = '180_11_' + energy + "_4h_pre"
        lastone = db.find_lastone(col_his)
    # print(lastone)
    time_end = lastone['Datetime']
    week = datetime.strptime(time_end, "%Y-%m-%d %H:%M:%S").weekday() + 1

    dt = datetime.strptime(time_end, "%Y-%m-%d %H:%M:%S") + timedelta(days=-5)
    time_start = datetime(dt.year, dt.month, dt.day, dt.hour * 0).strftime('%Y-%m-%d %H:%M:%S')

    res = db.find(col_his, {"Datetime": {"$gte": time_start, "$lte": time_end}})

    if energy == 'energy':
        list_usage_his = []
        list_usage_ano = []
        json_usage_his(list_usage_his, list_usage_ano, res)
    elif energy == 'MD':
        list_MD_his = []
        list_time = []
        list_MD_ano = []
        json_MD_his(list_MD_his, list_time, list_MD_ano, res)

    tps = datetime.strptime(time_end, "%Y-%m-%d %H:%M:%S") + timedelta(hours=4)
    tn = datetime.strptime(time_end, "%Y-%m-%d %H:%M:%S") + timedelta(days=2)

    time_pre_start = tps.strftime('%Y-%m-%d %H:%M:%S')
    time_pre_end = datetime(tn.year, tn.month, tn.day, tn.hour * 0).strftime('%Y-%m-%d %H:%M:%S')

    res = db.find(col_pre, {"Datetime": {"$gte": time_pre_start, "$lte": time_pre_end}})

    if energy == 'energy':
        list_usage_pre = []
        list_usage_pre = list_usage_pre + list_usage_his
        json_usage_pre(list_usage_pre, res)
        return list_usage_his, list_usage_pre, list_usage_ano, week, time_end
    elif energy == 'MD':
        list_MD_pre = []
        list_MD_pre = list_MD_pre + list_MD_his
        json_MD_pre(list_MD_pre, list_time, res)
        return list_MD_his, list_MD_pre, list_MD_ano, list_time, week, time_end

def get_last_time(db):
    col = "180_11_energy_4h_anomaly"
    lastone = db.find_lastone(col)
    # print(lastone)
    time_end = lastone['Datetime']
    return time_end

def get_huaxin_info(db):
    huaxin_info = db.find_one('huaxin_info')
    huaxin_info.pop('_id')
    huaxin_info.pop('id')
    return huaxin_info


def get_company_info(db):
    company_info = {}
    col = "huaxin_company"
    res = db.find(col)
    for item in res:
        co_num = item['co_num']
        company = item['company']
        introduction = item['introduction']
        business_scope = item['business_scope']
        entry_date = item['entry_date']
        ed = datetime.strptime(entry_date, "%Y.%m.%d").strftime('%Y-%m-%d')
        co_info = {}
        co_info['name'] = company
        co_info['entry_date'] = ed
        co_info['introduction'] = introduction
        co_info['business_scope'] = business_scope
        company_info[co_num] = co_info

    return company_info


def get_energy_day(db, energy, time):
    dt = datetime.strptime(time, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d')
    if energy == 'energy':
        res = db.find('huaxin_energy_all_1d_pre', {'Datetime': dt})
        for item in res:
            totally = item['usage']
        return totally
    elif energy == 'MD':
        res = db.find('huaxin_MD_all_1d_pre', {'Datetime': dt})
        for item in res:
            md = item['MD']
        return md


def get_energy_month(db, time, num):
    dt = datetime.strptime(time, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m')
    res = db.find_time("huaxin_energy_month", {"Datetime": {"$lte": dt}}, num)
    month = []
    for item in res:
        month.append(item['usage'])
    month.reverse()
    return month


def get_co_energy_month(db, time, co_num, num):
    dt = datetime.strptime(time, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m')
    res = db.find_time("huaxin_co_energy_month", {"Datetime": {"$lte": dt}, "co_num": co_num}, num)
    month = []
    for item in res:
        month.append(item['usage'])
    month.reverse()
    return month


def get_MD_time(db, time):
    tn = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    dt = datetime(tn.year, tn.month, tn.day, tn.hour * 0).strftime('%Y-%m-%d %H:%M:%S')
    res = db.find('huaxin_MD_all_1d_time_pre', {"Datetime": {"$gte": dt}})
    time_advise = []

    for item in res:
        time_advise.append(item['Datetime'])
        dt_st = datetime.strptime(item['Datetime'], "%Y-%m-%d %H:%M:%S") + timedelta(hours=-4)
        dt_st = dt_st.strftime('%Y-%m-%d %H:%M:%S')
        time_advise.append(dt_st)
    return time_advise


def get_floor_company(db):
    res = db.find('floor_company')
    floor_company = {}
    for item in res:
        floor = item['floor']
        co_num_set = item['co_num_set']
        floor_company[floor] = co_num_set

    return floor_company

def get_all():
    # 实例化db
    db = Database("huaxin", "huaxin")
    col_energy = 'huaxin_energy_all'
    col_MD = 'huaxin_MD_all'

    # 获取历史最后一条数据的时间及星期、用电列表、MD列表、MD时间窗口
    list_usage_his, list_usage_pre, list_usage_ano, week_usage, time_usage = get_energy_list(db, col_energy, 'energy')
    list_MD_his, list_MD_pre, list_MD_ano, list_time, week_MD, time_MD = get_energy_list(db, col_MD, 'MD')

    # 获取充放电建议列表advise[]
    time_advise = get_MD_time(db, time_MD)
    advise = []
    for i in list_time:
        flag = 0
        for time in time_advise:
            if time == i:
                flag = 1
                break
        advise.append(flag)

    # 获取华鑫园区基本信息
    data = get_huaxin_info(db)



    usage = {'totally': get_energy_day(db, 'energy', time_usage), 'anomaly': list_usage_ano, 'week': list_usage_his, 'week_forcast': list_usage_pre,
             'month': get_energy_month(db, time_usage, 6)}

    power = {'peak': get_energy_day(db, 'MD', time_MD), 'anomaly': list_MD_ano, 'week': list_MD_his, 'week_forcast': list_MD_pre, 'advise': advise}

    db.close()

    data['usage'] = usage
    data['power'] = power

    all_data = {'code': 200, 'time': time_usage, 'day_of_week': week_usage, 'data': data}
    return all_data

def get_company():
    db = Database("zyyjy", "huaxin_energy")
    company_info = {'code': 200, 'time': get_last_time(db), 'data': get_company_info(db)}
    db.close()
    return company_info

def get_floor():
    db = Database("zyyjy", "huaxin_energy")
    floor_info = {'code': 200, 'time': get_last_time(db), 'data': get_floor_company(db)}
    db.close()
    return floor_info

def get_co_num(co_num='180_11'):
    db = Database("zyyjy", "huaxin_energy")
    company_info = get_company_info(db)
    # print(company_info[co_num])

    try:
        name = company_info[co_num]['name']
    except:
        co_num = '180_11'
        name = company_info[co_num]['name']

    col_energy = co_num + '_energy'
    col_MD = co_num + '_MD'

    list_usage_his, list_usage_pre, list_usage_ano, week_usage, time_usage = get_energy_list(db, col_energy, 'energy')
    list_MD_his, list_MD_pre, list_MD_ano, list_time, week_MD, time_MD = get_energy_list(db, col_MD, 'MD')

    usage = {'week': list_usage_his, 'week_forcast': list_usage_pre, 'anomaly': list_usage_ano, 'month': get_co_energy_month(db, time_usage, co_num, 6)}
    power = {'week': list_MD_his, 'week_forcast': list_MD_pre, 'anomaly': list_MD_ano}

    db.close()

    data = {'id': co_num, 'name': name, 'usage': usage, 'power': power}

    co_num_data = {'code': 200, 'time': time_usage, 'data': data }
    return co_num_data

if __name__ == '__main__':
    print(get_all())
    print(get_company())
    print(get_floor())
    print(get_co_num())
