# -*- coding=utf-8 -*
import model


class cool:
    def __init__(self, n=6):
        self.N = n
        self.age_feature = {'teen': set([]), 'midlife': set([]), 'old': set([])}
        self.sex_feature = {'girl': set([]), 'boy': set([])}
        self.job_feature = {}
        self.item_behavior = {}
        self.pfi_age = {}
        self.pfi_sex = {}
        self.pfi_job = {}

        self.__feature_init()
        self.calc()

    def __feature_init(self):
        users = model.get_all_user()
        for user in users:
            if int(user[2]) < 20:
                self.age_feature['teen'].add(user[0])
            elif int(user[2]) > 50:
                self.age_feature['old'].add(user[0])
            else:
                self.age_feature['midlife'].add(user[0])
            if user[3] == 'F':
                self.sex_feature['girl'].add(user[0])
            else:
                self.sex_feature['boy'].add(user[0])
            self.job_feature.setdefault(user[4], set([])).add(user[0])

        behaviors = model.get_all_behavior()
        for behavior in behaviors:
            self.item_behavior.setdefault(behavior[2], set([])).add(behavior[1])

    def calc(self):
        alpha = 100
        pfi_age = {'teen': {}, 'midlife': {}, 'old': {}}
        pfi_sex = {'girl': {}, 'boy': {}}
        pfi_job = {}
        for movie_id in self.item_behavior.keys():
            pfi_age['teen'][movie_id] = 1.0*len(self.item_behavior[movie_id] & self.age_feature['teen'])/(len(self.item_behavior[movie_id]) + alpha)
            pfi_age['midlife'][movie_id] = 1.0*len(self.item_behavior[movie_id] & self.age_feature['midlife'])/(len(self.item_behavior[movie_id]) + alpha)
            pfi_age['old'][movie_id] = 1.0*len(self.item_behavior[movie_id] & self.age_feature['old'])/(len(self.item_behavior[movie_id]) + alpha)
            pfi_sex['girl'][movie_id] = 1.0*len(self.item_behavior[movie_id] & self.sex_feature['girl'])/(len(self.item_behavior[movie_id]) + alpha)
            pfi_sex['boy'][movie_id] = 1.0 * len(self.item_behavior[movie_id] & self.sex_feature['boy'])/(len(self.item_behavior[movie_id]) + alpha)

            for job in self.job_feature.keys():
                pfi_job.setdefault(job, {})[movie_id] = \
                    1.0 * len(self.item_behavior[movie_id] & self.job_feature[job]) / (
                        len(self.item_behavior[movie_id]) + alpha
                    )

        for age, pfi in pfi_age.items():
            pfi = sorted(pfi.items(), key=lambda x:x[1], reverse=True)
            self.pfi_age[age] = pfi[:10]
        for sex, pfi in pfi_sex.items():
            pfi = sorted(pfi.items(), key=lambda x: x[1], reverse=True)
            self.pfi_sex[sex] = pfi[:10]
        for job, pfi in pfi_job.items():
            pfi = sorted(pfi.items(), key=lambda x: x[1], reverse=True)
            self.pfi_job[job] = pfi[:10]
        # print self.pfi_sex
        # print self.pfi_age

    def get_age_type(self, age):
        type = "midlife"
        if age < 20:
            type = "teen"
        elif age > 50:
            type = 'old'
        return type

    def get_sex_type(self, sex):
        if sex == 'F':
            type = 'girl'
        else:
            type = 'boy'
        return type

    # user = {age, sex, job}
    def recommend(self, user):
        age = self.get_age_type(user['age'])
        sex = self.get_sex_type(user['sex'])
        res = dict(self.pfi_age[age])
        for movie_id, rate in self.pfi_sex[sex]:
            res[movie_id] = res.setdefault(movie_id, 0) + rate
        for movie_id, rate in self.pfi_job[user['job']]:
            res[movie_id] = res.setdefault(movie_id, 0) + rate
        return sorted(res.items(), key=lambda x:x[1], reverse=True)[:self.N]






