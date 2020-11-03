import json
import requests
import sqlite3
conn = sqlite3.connect('database.db', check_same_thread=False)
c = conn.cursor()


def authLogin(username, userpin):
    chechUser = checkUserExists(username)

    print(chechUser)

    if chechUser is True:
        c.execute(
            f"SELECT username,userpin FROM users WHERE username='{username}'")
        result = c.fetchone()
        if(userpin != '' and int(result[1]) == int(userpin)):
            return True

        else:
            return False

    else:
        return False


def authSign(username, userpin):

    c.execute(f"INSERT INTO users VALUES('{username}',{int(userpin)})")
    conn.commit()


def checkUserExists(username):

    c.execute(f"SELECT username FROM users WHERE username='{username}'")
    result = c.fetchone()

    if result == None:
        return False

    else:
        return True


def createuserbase(username):

    c.execute(f'''CREATE TABLE USER_{username}(stock TEXT)''')
    conn.commit()


def getstocks(username):

    c.execute(f"SELECT stock FROM USER_{username}")
    data = c.fetchall()
    result = []
    for i in range(len(data)):
        result.append(data[i][0])

    return result


def addstock(stock, username):

    c.execute(f"INSERT INTO USER_{username} VALUES('{stock}')")
    conn.commit()


def deletestock(stock, username):

    c.execute(f"DELETE FROM USER_{username} WHERE stock='{stock}'")
    conn.commit()


def getStockData(stock):
    req = requests.get(f"http://stonksapi.herokuapp.com/getdata/{stock}")
    print(stock)
    data = json.loads(req.content)
    return data
