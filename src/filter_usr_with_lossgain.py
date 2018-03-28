import json


jsn = open('new_contest.json')
li = json.load(jsn)

to = open('updates.json', 'w')
change_log = open('lazy_users.json', 'w')
xhanges = {}
usr = {}
counter = 0

for i in li:
	if int(li[i][-1]):
		xhanges[str(i)] = li[i]
	else:
		usr[str(i)] = li[i][:-1]
	counter += 1
print(counter)
json.dump(xhanges, to, ensure_ascii=False, indent=4)
json.dump(usr, change_log, ensure_ascii=False, indent=4)
jsn.close()
to.close()
change_log.close()
