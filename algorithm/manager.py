# -*- coding=utf-8 -*
import CF
import cool
import itemCool
from model import model

class rsManager:
    def __init__(self):
        self.itemCF = self.get_itemCF()
        self.userCF = self.get_userCF()
        self.user_cool = self.get_user_cool()
        self.item_cool = self.get_item_cool()

    def get_itemCF(self, k=8):
        return CF.CF(k)

    def get_userCF(self, k=8):
        return CF.CF(k, 'item')

    def get_item_cool(self):
        return itemCool.itemCool()

    def get_user_cool(self):
        return cool.cool()

    def update(self, new_manager):
        self.itemCF = new_manager.itemCF
        self.userCF = new_manager.userCF
        self.user_cool = new_manager.user_cool
        self.item_cool = new_manager.item_cool

    # user is list
    def recommend(self, old_user):
        user = {}
        user['id'] = old_user[0]
        user['age'] = old_user[2]
        user['sex'] = old_user[3]
        user['job'] = old_user[4]
        user_id = user["id"]
        print model.is_new_user(user_id)
        res = []
        if model.is_new_user(user_id):
            title = "根据你的特征，猜测你喜欢"
            movies = self.user_cool.recommend(user)
            res.append((title, movies))
        else:
            title = "与你相似的人都喜欢"
            res.append((title, self.userCF.recommend(user_id)))
            title = "你喜欢过相似的电影"
            res.append((title, self.itemCF.recommend(user_id)))
        item_cool_rec = self.item_cool.recommend(user_id)
        if len(item_cool_rec):
            title = "你可能喜欢"
            res.append((title, item_cool_rec))
        return res

    def test(self):
        print self.item_cool.recommend(61)


rs_manager = rsManager()