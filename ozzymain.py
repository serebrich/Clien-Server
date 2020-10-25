import argparse
import sys
import subprocess

#Database information save in file
with open("DB Settings.txt", "w") as file:
    print("Enter info about DataBase")
    host = input("Host: ")
    user = input("User: ")
    password = input("Password: ")
    DB = input("DataBase: ")
    file.write(f"{host}\n{user}\n{password}\n{DB}")

#Arguments for main file
parser = argparse.ArgumentParser()
parser.add_argument("-cs", "--clienserver", help="Client-Server Mod", action="store_true")
parser.add_argument("-th", "--threading", help="Threading Mod", action="store_true")

try:
    args = parser.parse_args()
except:
    sys.exit()

#Checking OS and run script
if args.clienserver:
    if sys.platform == "linux" or sys.platform == "darwin":
        subprocess.Popen(["python3", "Serv.py"])
    elif sys.platform == "win32":
        subprocess.Popen(["python", "Serv.py"])

if args.threading:
    if sys.platform == "linux" or sys.platform == "darwin":
        subprocess.Popen(["python3", "Threads.py"])
    elif sys.platform == "win32":
        subprocess.Popen(["python", "Threads.py"])
