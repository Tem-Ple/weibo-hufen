import cx_Oracle
import multiprocessing
import random

conn = cx_Oracle.connect('sys', 'oracle', '10.10.200.1:1521/adminrac', cx_Oracle.SYSDBA)
c = conn.cursor()

def worker():
    while True:
        c.execute("SELECT * from bigtab where id = :id", id=random.randint(0, 1000000))

if __name__ == '__main__':
    for i in range(120):
        process = multiprocessing.Process(target=worker,)
        process.start()