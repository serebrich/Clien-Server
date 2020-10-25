from threading import Thread, Lock
import datetime
from datetime import timedelta
from time import sleep
import pymysql
from string import ascii_uppercase
import random

s1_all_letter_counter = {k: int(v) for k, v in zip(ascii_uppercase, "0" * 26)}
s2_first_letter_counter = {k: int(v) for k, v in zip(ascii_uppercase, "0" * 26)}

lock = Lock()

rand_strings = []


def random_string():
    with lock:
        rand_strings.append("".join(random.sample(ascii_uppercase, 16)))


def get_rand_str():
    t = Thread(target=random_string)
    t.start()


def local_insert(rand_str: str):
    for i in rand_str:
        s1_all_letter_counter[i] += 1
    s2_first_letter_counter[rand_str[0]] += 1


def insert_to_db(rand_str: str):
    local_insert(rand_str)
    cur.execute(
        f"""INSERT INTO ozzy(
        RAND_STR,
        TIME_OF_RCV,
        COUNT_ALL_LTRS,
        COUNT_FRST_LTRS)
        VALUES(
        '{rand_str}',
        '{datetime.datetime.now().strftime('%X')}',
        '{'-'.join(map(str, s1_all_letter_counter.values()))}',
        '{'-'.join(map(str, s2_first_letter_counter.values()))}');"""
    )
    con.commit()


def more_than_zerro_checker():
    cur.execute("""SELECT COUNT_FRST_LTRS FROM ozzy;""")
    res = cur.fetchall()[-1][-1]
    print(res)
    return all(map(int, res.split("-")))


def saver():
    cur.execute(
        """SELECT time_of_rcv FROM ozzy
                   WHERE id = (SELECT MIN(id) FROM ozzy) or
                   id = (SELECT MAX(id) FROM ozzy);"""
    )

    start_time, finish_time = cur.fetchall()

    start_time = list(map(int, start_time[0].split(":")))
    finish_time = list(map(int, finish_time[0].split(":")))

    td_st = timedelta(hours=start_time[0], minutes=start_time[1], seconds=start_time[2])
    td_fn = timedelta(
        hours=finish_time[0], minutes=finish_time[1], seconds=finish_time[2]
    )
    time_delta = str(td_fn - td_st)

    with open("statictic.txt", "w") as file:
        file.write(f"Working time - {time_delta}\n")

        file.write(f"\nRecived strings - {sum(s2_first_letter_counter.values())}\n")

        file.write("\nStatistic of all letters:\n")
        for k, v in s1_all_letter_counter.items():
            file.write(f"{k}: {v}\n")

        file.write("\nStatistic of first letters:\n")
        for k, v in s2_first_letter_counter.items():
            file.write(f"{k}: {v}\n")

        print('\nSTATISTIC WAS SAVED IN "statistic.txt *(Hire Me)*"')


con = pymysql.connect(
    host="localhost", user="root", password="Rocknrolla22", db="strings"
)

cur = con.cursor()
cur.execute(
    """CREATE TABLE IF NOT EXISTS ozzy(
    ID int NOT NULL AUTO_INCREMENT,
    RAND_STR char(16),
    TIME_OF_RCV varchar(128),
    COUNT_ALL_LTRS varchar(255),
    COUNT_FRST_LTRS varchar(255),
    PRIMARY KEY (ID)
                    );"""
)
con.commit()

while True:
    get_rand_str()
    string = rand_strings.pop()
    print(f"New data was recived - {string}")

    insert_to_db(string)
    sleep(0.5)
    if more_than_zerro_checker():
        break
saver()
