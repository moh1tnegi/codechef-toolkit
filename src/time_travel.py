""" Travel with time! The script gathers information for usernames
    provided in a file """

from requests import get
from lxml.html import fromstring


def clear_file():
    with open('fabric_of_space_time.txt', 'w'):
        pass


if __name__ == '__main__':
    user_file = 'path/to/usernames'
    user_logs = 'path/to/logs_of_not_found_usernames'
    user_info = 'fabric_of_space_time.txt'

    f = open(user_file)
    store = open(user_info, 'a')
    log = open(user_logs, 'a')

    link = 'https://www.codechef.com/users/'
    path = '/html/body/main/div/div/div/div/div/section[1]/ul'
    sentinel = 1
    
    for line in f:
        for usr in line.split():
            user_link = link+usr
            user_response = get(user_link)
            user_content = user_response.content
            user_elements = fromstring(user_content)
            try:
                user_tree = user_elements.xpath(path)[0]
                user_dict = dict()
                user_list = [0, 0, 0, 0, 0, 0]
                for li in range(len(user_tree)):
                    lhs = user_tree[li][0].text_content()
                    rhs = user_tree[li][1].text_content()
# {'usr': ['user', 'Country', 'state', 'city, 'student', 'insti']}
                    if lhs == 'Username:':
                        user_list[0] = usr
                    elif lhs == 'Country:':
                        user_list[1] = rhs[2:]
                    elif lhs == 'State:':
                        user_list[2] = rhs
                    elif lhs == 'City:':
                        user_list[3] = rhs
                    elif lhs == 'Student/Professional:':
                        user_list[4] = rhs
                    elif lhs == 'Institution:':
                        user_list[5] = rhs
                user_dict[usr] = user_list
                print(sentinel, usr)
                store.write(str(user_dict)+', '+'\n')
            except IndexError:
                log.write(usr+'\n')
                print(sentinel, 'username not found:', usr)
            sentinel += 1
    f.close()
    store.close()
    log.close()
