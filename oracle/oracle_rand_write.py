import cx_Oracle
import multiprocessing
import random

conn = cx_Oracle.connect('sys', 'oracle', '10.10.200.1:1521/adminrac', cx_Oracle.SYSDBA)
c = conn.cursor()

def worker():
    while True:
        c.execute("update bigtab set a='asdf',b='qwer',c='zxcv',d='fdsa' where id = :id", id=random.randint(0, 1000000))
        conn.commit()

if __name__ == '__main__':
    for i in range(32):
        process = multiprocessing.Process(target=worker,)
        process.start()