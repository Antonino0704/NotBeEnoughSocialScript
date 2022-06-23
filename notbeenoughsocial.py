from urllib import response
import requests
import sys
import random
import string
from colorama import Fore, init

def five_number_random():
    ALPHANUMERIC_CHARS = string.ascii_lowercase + string.digits
    return "".join(random.choice(ALPHANUMERIC_CHARS) for _ in range(5))

def login(user, passw):
    response = requests.post("https://notbeenoughsocial.herokuapp.com/api-rest-auth/login/", data={"username": user, "password": passw})
    if response.status_code == 200:
        return  response.json()['key']



def create():
    num = five_number_random()
    data = {"username": 'User' + num,
            "email": f'User{num}@gmail.com',
            "password1": "defaultPassword" + num,
            "password2": "defaultPassword" + num}

    response = requests.post("https://notbeenoughsocial.herokuapp.com/api-rest-auth/registration/", data=data)
    if response.status_code == 201:
        return {"username": 'User' + num,
                "password": 'defaultPassword' + num}

    return f"{Fore.RED} error: {response.status_code} {response.json()}"


def delete():
    user = input("enter username: ")
    passw = input("enter password: ")
    token = "Token " + str(login(user, passw))
    response = requests.delete(f"https://notbeenoughsocial.herokuapp.com/api/profiles/{user.lower()}/", headers={"Authorization": token})
    if response.status_code == 204:
        return "204 all ok profile deleted"

    return f"{Fore.RED} error: {response.status_code} {response.json()}"


def createCustom():
    data = {}
    data['username'] = input("enter username: ")
    data['email'] = input("enter email: ")
    data['password1'] = input("enter password: ")
    data['password2'] = input("confirm password: ")

    response = requests.post("https://notbeenoughsocial.herokuapp.com/api-rest-auth/registration/", data=data)
    if response.status_code == 201:
        return {"username": data['username'],
                "password": data['password1']}

    return f"{Fore.RED} error: {response.status_code} {response.json()}"


def createMore(size):
    super_data = {}
    for i in range(int(size)):
        num = five_number_random()
        data = {"username": 'User' + num,
                "email": f'User{num}@gmail.com',
                "password1": "defaultPassword" + num,
                "password2": "defaultPassword" + num}

        response = requests.post("https://notbeenoughsocial.herokuapp.com/api-rest-auth/registration/", data=data)
        if response.status_code == 201:
            super_data[i] = {"username": 'User' + num,
                             "password": 'defaultPassword' + num}

        else:
            return f"{Fore.RED} error: {response.status_code} {response.json()}"

    return super_data


def updateDescription(description):
    user = input("enter username: ")
    email = input("enter email: ")
    passw = input("enter password: ")
    token = "Token " + str(login(user, passw))
    data = {"username": user,
            "email": email,
            "description": description}

    response = requests.put(f"https://notbeenoughsocial.herokuapp.com/api/profiles/{user.lower()}/", data=data, headers={"Authorization": token})
    if response.status_code == 200:
        return "200 all ok, description update"

    return f"{Fore.RED} error: {response.status_code} {response.json()}"


def createPost(content):
    user = input("enter username: ")
    passw = input("enter password: ")
    token = "Token " + str(login(user, passw))

    response = requests.post(f"https://notbeenoughsocial.herokuapp.com/api/profiles/{user.lower()}/post/", data={"content": content}, headers={"Authorization": token})
    if response.status_code == 201:
        return "201 all ok, post upload"
    
    return f"{Fore.RED} error: {response.status_code} {response.json()}"


def main():
    init(convert=True)
    if sys.argv[1] == 'create' and len(sys.argv) == 2:
        msg = create()
        print(f"{Fore.GREEN} {msg}")

    elif sys.argv[1] == "delete" and len(sys.argv) == 2:
        msg = delete()
        print(f"{Fore.GREEN} {msg}")

    elif sys.argv[1] == "create" and sys.argv[2] == '-c' and len(sys.argv) == 3:
        msg = createCustom()
        print(f"{Fore.GREEN} {msg}")

    elif sys.argv[1] == "create" and sys.argv[2] == '-m' and len(sys.argv) == 4:
        msg = createMore(sys.argv[3])
        print(f"{Fore.GREEN} {msg}")

    elif sys.argv[1] == "update" and sys.argv[2] == "-d" and len(sys.argv) == 4:
        msg = updateDescription(sys.argv[3])
        print(f"{Fore.GREEN} {msg}")

    elif sys.argv[1] == "create" and sys.argv[2] == "-p" and len(sys.argv) == 4:
        msg = createPost(sys.argv[3])
        print(f"{Fore.GREEN} {msg}")

if __name__ == "__main__":
    main()
