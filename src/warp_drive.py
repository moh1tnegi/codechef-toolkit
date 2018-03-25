from json import load


if __name__ == '__main__':
    UAK_database = 'fabric_of_space_time.json'
    CAK_database = 'city_db.json'

    UAK_file = open(UAK_database)
    CAK_file = open(CAK_database)
    
    UAK_json = load(UAK_file)
    CAK_json = load(CAK_file)


    def is_alive():
        uname = input('Enter your handle: ')
        try:
            print("You are alive {}.".format(UAK_json[uname]))
        except KeyError:
            print("You are a ghost!")

    def city_chefs():
        city = input('Enter the city: ')
        try:
            print("City chefs:\n{}".format((CAK_json[city])))
        except KeyError:
            print("I think you are from Area 51.")

    usr_interaction = input('1. Check you alive?\n2. Your city chefs. \n')

    if int(usr_interaction) is 1:
        is_alive()
    elif int(usr_interaction) is 2:
        city_chefs()

    UAK_file.close()
    CAK_file.close()
