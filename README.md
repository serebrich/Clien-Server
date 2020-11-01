# Usage
### Install PyMySQL
```python
pip install pymysql
```
### Clone repository
```python
$git clone https://github.com/serebrich/Ozzy_Test.git
```
### Create new DB or use the old one
```sql
CREATE DATABASE databasename;
```
## Run
### 1. Open terminal
### 2. Go to directory with repository
```
$cd PATH/TO/REPO/Ozzy_Test
```
### 3. Run script with two ways
### Way 1 Client-Server
```
python ozzymain.py -cs
```
### Way 2 Threading
```
python ozzymain.py -th
```
### 4. Script ask you about DB information
For this test script use:
```
Host: localhost
User: *your username for DB*
Password: *your pass for DB*
DB: *Name of your choosen DB*
```
### 5. Enjoy
