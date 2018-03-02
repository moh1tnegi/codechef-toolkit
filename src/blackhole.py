import requests
from lxml import html


if __name__ == '__main__':
    pointer = 1
    # with open('log.txt', 'w'):
    #     pass
    f = open('log.txt', 'a')
    for pages in range(1, 7900):  # 7908
        link = 'https://discuss.codechef.com/users/?sort=reputation&page='+str(pages)
        data = requests.get(link)

        page = data.content
        tree = html.fromstring(page)
        pointer = pages
        try:
            for usr in range(35):
                path = '//*[@id="main-body"]/div/div['\
                        + str(usr+1) + ']/ul/li[2]/span/a'
                info = tree.xpath(path)
                if 'class' in info[0].attrib:
                    break
                else:
                    f.write(info[0].text_content()+' ')
        except IndexError:
            break
        f.write('\n')
    f.write('\nPointer:'+str(pointer)+'\n')
    f.close()
