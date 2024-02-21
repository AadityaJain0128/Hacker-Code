import sqlite3

# def alter_database(db, args):
#     try:
#         x = sqlite3.connect(f"instance/{db}.db")
#         y = x.cursor()
#     except:
#         return "Error in DataBase"
#     try:
#         if db == "questions":
#             y.execute(f"insert into questions values ({args[0]}, '{args[1]}', '{args[2]}', '{args[3]}')")
#             x.commit()
#         elif db == "login-data":
#             y.execute(f"delete from 'login' where username = '{args[0]}'")
#             x.commit()
        # return "Operation Successful"
#     except:
#         return "Operation Failed"


def alter_database(qno, title, desc, difficulty):
    try:
        x = sqlite3.connect("questions.db")
        y = x.cursor()
    except:
        print("Error connecting to DataBase")
    try:
        y.execute(f"insert into questions values ({qno}, '{title}', '{desc}', '{difficulty}', 0)")
        x.commit()
        return "Operation Successful"
    except Exception as e:
        print(e)
        return "Error in inserting Values"


def update_solved(qno):
    data = fetch_login()
    count = 0
    for i in data:
        if i[0] != None:
            if str(qno) in i[0]:
                count += 1
    x = sqlite3.connect("questions.db")
    y = x.cursor()
    y.execute(f"update questions set solved = {count} where qno = {qno}")
    x.commit()
    y.close()
    x.close()


def update_all():
    data = fetch_questions()
    for q in data:
        update_solved(q[0])


def fetch_login():
    x = sqlite3.connect("login-data.db")
    y = x.cursor()
    y.execute("select completed from login")
    data = y.fetchall()
    return data


def fetch_questions():
    x = sqlite3.connect("questions.db")
    y = x.cursor()
    y.execute("select * from questions")
    data = y.fetchall()
    return data


def top_problems():
    x = sqlite3.connect("questions.db")
    y = x.cursor()
    y.execute("select * from questions order by solved desc, qno desc")
    top_q = y.fetchall()
    y.close()
    x.close()
    return top_q

def update_data():
    x = sqlite3.connect("questions.db")
    y = x.cursor()
    y.execute(f"update questions set desc = '{input()}' where qno = {int(input())}")
    x.commit()
    y.close()
    x.close()


def delete_data():
    x = sqlite3.connect("login-data.db")
    y = x.cursor()
    user = input()
    y.execute(f"DELETE from 'login' where username = '{user}';")
    x.commit()
    y.close()
    x.close()


def fetch_user(user):
    x = sqlite3.connect("login-data.db")
    y = x.cursor()
    y.execute(f"select completed from login where username = '{user}'")
    data = y.fetchall()[0][0]
    return data


if __name__ == "__main__":
    # update_solved(1)
    # print(top_problems())
    print(fetch_login())
    # update_data()
    # delete_data()