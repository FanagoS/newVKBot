import os, random, time
from plugins import workFiles

users_dir = os.path.join(r"users/")

def check_user_mention(from_id):
    get_data = workFiles.loadjson(users_dir + str(from_id) + ".json")
    return get_data

def saveUserData(from_id, data):
    workFiles.dumpjson(data, users_dir + str(from_id) + ".json")

def reg(from_id):
    user_id = str(from_id)

    bonus_money = 50000
    profileList = {"Name": "",
                   "ID": '{}'.format(str(user_id)), "balance": '{}'.format(int(bonus_money)),
                   "Status": "СтартовоеМеню", "Room_id": "0",
                   "data_reg": '{}'.format(str(time.strftime("%d.%m.%Y", time.localtime())))}
    workFiles.dumpjson(profileList, users_dir + str(user_id) + ".json")
