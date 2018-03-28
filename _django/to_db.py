from json import load
from codechef.models import User

if __name__ == '__main__':
    db_file = open('db.json')
    jsn = load(db_file)
    for info in jsn.values():
        try:
            user = User()
            user.username = info[0]
            user.country = info[1]
            user.state = info[2]
            user.city = info[3]
            user.usr_type = info[4]
            user.global_rank = info[5]
            user.country_rank = info[6]
            user.ratings = info[7]
        except ValueError:
            with open('log.txt', 'w') as f:
                f.write(user.username)
        user.save()
