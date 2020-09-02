# mongodb database

from pymongo import MongoClient
import json
from datetime import timedelta, datetime


class Database(object):
    def __init__(self, database):
        self.conn = MongoClient('mongodb://huaxin:inesa2014@10.200.43.5:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false')
        self.db = self.conn[database]

    def get_state(self):
        return self.conn is not None and self.db is not None

    def insert_one(self, collection, data):
        if self.get_state():
            ret = self.db[collection].insert_one(data)
            return ret.inserted_id
        else:
            return ""

    def insert_many(self, collection, data):
        if self.get_state():
            ret = self.db[collection].insert_many(data)
            return ret.inserted_ids
        else:
            return ""

    def update(self, collection, data):
        # data format:
        # {key:[old_data,new_data]}
        data_filter = {}
        data_revised = {}
        for key in data.keys():
            data_filter[key] = data[key][0]
            data_revised[key] = data[key][1]
        if self.get_state():
            return self.db[collection].update_many(data_filter, {"$set": data_revised}).modified_count
        return 0

    def find_one(self, col):
        if self.get_state():
            return self.db[col].find_one()
        else:
            return None

    def find(self, col, condition, column=None):
        if self.get_state():
            if column is None:
                return self.db[col].find(condition)
            else:
                return self.db[col].find(condition, column)
        else:
            return None

    def find_lastone(self, col):
        if self.get_state():
            return self.db[col].find_one(sort=[('_id', -1)])
        else:
            return None

    def find_last(self, col, condition, num, column=None):
        if self.get_state():
            if column is None:
                return self.db[col].find(condition).sort('_id', -1).limit(num)
            else:
                return self.db[col].find(condition, column).sort('_id', -1).limit(num)
        else:
            return None

    def find_time(self, col, condition, num, column=None):
        if self.get_state():
            if column is None:
                return self.db[col].find(condition).sort('Datetime', -1).limit(num)
            else:
                return self.db[col].find(condition, column).sort('Datetime', -1).limit(num)
        else:
            return None

    def delete(self, col, condition):
        if self.get_state():
            return self.db[col].delete_many(filter=condition).deleted_count
        return 0

    def close(self):
        self.conn.close()


def get_data_from_db():
    # 实例化db
    db = Database("huaxin")

    def json_usage(list, res):
        for item in res:
            list.append(item['usage'])
        return list

    def json_MD(list1, list2, res):
        for item in res:
            list1.append(item['MD'])
            list2.append(item['Datetime'])
        return list1, list2

    def get_energy_list(energy):
        col_his = "huaxin_" + energy + "_all_4h_anomaly"
        col_pre = "huaxin_" + energy + "_all_4h_pre"

        lastone = db.find_lastone(col_his)
        time_end = lastone['Datetime']
        week = datetime.strptime(time_end, "%Y-%m-%d %H:%M:%S").weekday() + 1

        dt = datetime.strptime(time_end, "%Y-%m-%d %H:%M:%S") + timedelta(days=-5)
        time_start = datetime(dt.year, dt.month, dt.day, dt.hour * 0).strftime('%Y-%m-%d %H:%M:%S')

        res = db.find(col_his, {"Datetime": {"$gte": time_start, "$lte": time_end}})

        if energy == 'energy':
            list_usage_his = []
            json_usage(list_usage_his, res)
        elif energy == 'MD':
            list_MD_his = []
            list_time = []
            json_MD(list_MD_his, list_time, res)

        tps = datetime.strptime(time_end, "%Y-%m-%d %H:%M:%S") + timedelta(hours=4)
        tn = datetime.strptime(time_end, "%Y-%m-%d %H:%M:%S") + timedelta(days=2)

        time_pre_start = tps.strftime('%Y-%m-%d %H:%M:%S')
        time_pre_end = datetime(tn.year, tn.month, tn.day, tn.hour * 0).strftime('%Y-%m-%d %H:%M:%S')

        res = db.find(col_pre, {"Datetime": {"$gte": time_pre_start, "$lte": time_pre_end}})

        if energy == 'energy':
            list_usage_pre = []
            list_usage_pre = list_usage_pre + list_usage_his
            json_usage(list_usage_pre, res)
            return list_usage_his, list_usage_pre, week, time_end
        elif energy == 'MD':
            list_MD_pre = []
            list_MD_pre = list_MD_pre + list_MD_his
            json_MD(list_MD_pre, list_time, res)
            return list_MD_his, list_MD_pre, list_time, week, time_end

    def get_huaxin_info():
        huaxin_info = db.find_one('huaxin_info')
        huaxin_info.pop('_id')
        huaxin_info.pop('id')
        return huaxin_info

    def get_energy_day(energy, time):
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

    def get_energy_month(time, num):
        dt = datetime.strptime(time, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m')
        res = db.find_time("huaxin_energy_month", {"Datetime": {"$lte": dt}}, num)
        month = []
        for item in res:
            month.append(item['usage'])
        month.reverse()
        return month

    def get_MD_time(time):
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

    # 获取历史最后一条数据的时间及星期、用电列表、MD列表、MD时间窗口
    list_usage_his, list_usage_pre, week_usage, time_usage = get_energy_list('energy')
    list_MD_his, list_MD_pre, list_time, week_MD, time_MD = get_energy_list('MD')

    # 获取充放电建议列表advise[]
    time_advise = get_MD_time(time_MD)
    advise = []
    for i in list_time:
        flag = 0
        for time in time_advise:
            if time == i:
                flag = 1
                break
        advise.append(flag)

    # 获取华鑫园区基本信息
    data = get_huaxin_info()

    db.close()

    usage = {'totally': get_energy_day('energy', time_usage), 'week': list_usage_his, 'week_forcast': list_usage_pre,
             'month': get_energy_month(time_usage, 6)}

    power = {'peak': get_energy_day('MD', time_MD), 'week': list_MD_his, 'week_forcast': list_MD_pre, 'advise': advise}

    data['usage'] = usage
    data['power'] = power

    summary = {'code': 200, 'time': time_usage, 'day_of_week': week_usage, 'data': data}
    return summary


if __name__ == '__main__':
    print(get_data_from_db())

