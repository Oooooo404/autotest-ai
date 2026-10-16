from faker import Faker
import random

from requests.utils import from_key_val_list

fk = Faker("zh_CN")

def new_user():
    """生成随机用户数据"""
    return{
        "username":f"autotest_{fk.user_name()}{random.randint(1000,9999)}",
        "password":"123456",
        "nickname":fk.name(),
    }