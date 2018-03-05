import requests
from lxml import html


if __name__ == '__main__':
    pointer = 1
    # with open('user_names.txt', 'w'):
    #     pass
    f = open('nothing.txt', 'w')
    flag = 0
    for pages in range(1, 3):  # 7898
        link = 'https://discuss.codechef.com/users/?sort=reputation&page='+str(pages)
        chef = 'https://www.codechef.com/users/'
        data = requests.get(link)
        page = data.content
        tree = html.fromstring(page)
        pointer = pages
        try:
            for usr in range(35):
                path = '//*[@id="main-body"]/div/div[' \
                       + str(usr+1) + ']/ul/li[2]/span/a'
                info = tree.xpath(path)
                u_name, *_ = info[0].text_content().split()
                if 'class' in info[0].attrib:
                    if info[0].attrib['class'] == 'suspended-user':
                        flag += 1
                        break
                u_page = requests.get(chef+u_name)
                u_data = u_page.content
                u_tree = html.fromstring(u_data)
                u_info = u_tree.xpath(u_path)
                try:
                    if u_info[0][0].text_content() == 'City:':
                        f.write(u_info[0][1].text_content()+': '+u_name+', ')
                        print(u_name+': '+u_info[0][1].text_content())
                except IndexError:
                    pass
        except IndexError:
            pass
        f.write('\n')
        if flag:
            break
    f.write('\nPage: '+str(pointer)+'\n')
    f.close()
