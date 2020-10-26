import socket
import datetime
from datetime import timedelta
from time import sleep
import pymysql
from string import ascii_uppercase
import subprocess

#Reading params for DB
db_param = {}
with open("DB Settings.txt") as dbset:
    db_param["host"] = dbset.readline()[:-1]
    db_param["user"] = dbset.readline()[:-1]
    db_param["password"] = dbset.readline()[:-1]
    db_param["DB"] = dbset.readline()

# Dicts with Local statistic
s1_all_letter_counter = {k: int(v) for k, v in zip(ascii_uppercase, "0" * 26)}
s2_first_letter_counter = {k: int(v) for k, v in zip(ascii_uppercase, "0" * 26)}


def local_insert(rand_str: str):
    for i in rand_str:
        s1_all_letter_counter[i] += 1
    s2_first_letter_counter[rand_str[0]] += 1

#Save info in the lockal dict and DB
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

# Сhecks the condition by first letters
def more_than_zerro_checker():
    cur.execute("""SELECT COUNT_FRST_LTRS FROM ozzy;""")
    res = cur.fetchall()[-1][-1]
    print(res)
    return all(map(int, res.split("-")))

# Make and Save statistic in file
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


# Connection to DB
con = pymysql.connect(
    host=db_param["host"],
    user=db_param["user"],
    password=db_param["password"],
    db=db_param["DB"],
)

# Create a cursor and new table
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

# Run the server
SERVER_ADDRESS = ("localhost", 8686)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDRESS)
server_socket.listen()
print("Server is running...")

# Run the client
if sys.platform == "linux" or sys.platform == "darwin":
    subprocess.Popen(["python3", "Client.py"])
elif sys.platform == "win32":
    subprocess.Popen(["python", "Client.py"])


# Main loop
while True:
    #Getiing the connection
    connection, address = server_socket.accept()
    print(f"new connection from {address}")
    while connection:
        # Send request and get new rand string
        connection.send(bytes("Honey, give me string, please", encoding="UTF-8"))
        data = connection.recv(1024)
        print(f'New data was recived - {str(data, "utf-8")}')

        # Insert to DB and check the condition
        insert_to_db(str(data, "utf-8"))
        sleep(2)
        if more_than_zerro_checker():
            break
    # Save statistic and close connection
    saver()
    connection.close()
    break
