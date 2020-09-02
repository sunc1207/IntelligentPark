# mongodb database

from pymongo import MongoClient


class Database(object):
    def __init__(self, user, database):
        url = "mongodb://%s:inesa2014@10.200.43.5:27017/?authSource=admin&readPreference=primary&appname=MongoDB" % (user) +"%20Compass&ssl=false"
        self.conn = MongoClient(url)
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

    def find(self, col, condition=None, column=None):
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

