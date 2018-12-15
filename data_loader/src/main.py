import json
import zipfile
import sqlite3
import datetime
import sys
import re

DATA_PATH = '/tmp/data/data.zip'


def main():
    start = datetime.datetime.now()
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    create_tables(cursor)

    with zipfile.ZipFile(DATA_PATH, 'r') as zip_ref:
        for filename in zip_ref.namelist():
            if re.match(r'accounts_\d+.json$', filename):
                content_str = zip_ref.read(filename).decode('utf-8')
                content_data = json.loads(content_str).get('accounts', [])

                load_accounts_data(content_data, cursor, conn)
    conn.close()

    finish = datetime.datetime.now()
    delta = finish - start
    print(delta.total_seconds())


def create_tables(cursor):
    cursor.execute("""CREATE TABLE accounts
            	                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
            	                  email text, fname text,
            	                  sname text, status text,
            	                  country text, city text,
            	                  phone text, sex text,
            	                  joined integer, birth integer,
            	                  ext_id integer)
            	               """)

    cursor.execute("""CREATE TABLE accounts_like
            	                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
            	                   like_id integer,
            	                   like_ts integer,
            	                   acc_id integer,
            	                   FOREIGN KEY(acc_id) REFERENCES accounts(ext_id))
            	               """)

    cursor.execute("""CREATE TABLE accounts_premium
                	                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                	                  start integer,
                	                  finish integer,
                	                  acc_id integer,
                	                  FOREIGN KEY(acc_id) REFERENCES accounts(ext_id))
                	               """)

    cursor.execute("""CREATE TABLE accounts_interest
            	                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
            	                  interest text,
            	                  acc_id integer,
                	              FOREIGN KEY(acc_id) REFERENCES accounts(ext_id))
            	               """)


def load_accounts_data(content_data, cursor, conn):
    account_cache = []
    interest_cache = []
    like_cache = []
    premium_cache = []
    for obj in content_data:
        account_cache.append((obj.get('email'), obj.get('fname'), obj.get('sname'), obj.get('status'),
                              obj.get('country'), obj.get('city'), obj.get('phone'), obj.get('sex'),
                              obj.get('joined'), obj.get('birth'), obj.get('id')))

        for interest in obj.get('interests', []):
            interest_cache.append((obj.get('id'), interest))

        for like in obj.get('likes', []):
            like_cache.append((obj.get('id'), like.get('like_id'), like.get('like_ts')))

        premium = obj.get('premium', {})
        if premium:
            premium_cache.append((obj.get('id'), premium.get('start'), premium.get('finish')))

        if len(account_cache) == 1000:
            load_slice(account_cache, interest_cache, like_cache, premium_cache, cursor, conn)

            account_cache = []
            interest_cache = []
            like_cache = []
            premium_cache = []


def load_slice(account_cache, interest_cache, like_cache, premium_cache, cursor, conn):
    try:
        cursor.executemany("""INSERT INTO accounts
                            (email, fname, sname, status, country, city, phone, sex, joined, birth, ext_id)
                            VALUES (?,?,?,?,?,?,?,?,?,?,?)""", account_cache)
        conn.commit()
        cursor.executemany("INSERT INTO accounts_interest (acc_id, interest) VALUES (?,?)", interest_cache)
        cursor.executemany("INSERT INTO accounts_like (acc_id, like_id, like_ts) VALUES (?,?,?)", like_cache)
        cursor.executemany("INSERT INTO accounts_premium (acc_id, start, finish) VALUES (?,?,?)", premium_cache)
        conn.commit()
    except sqlite3.Error:
        sys.stdout.write('E')
        sys.stdout.flush()
    sys.stdout.write('+')
    sys.stdout.flush()


if __name__ == '__main__':
    main()
