# -*- coding: utf-8 -*-

import sys
import sqlite3
import fire
# args = sys.argv
# id=args[1]
# start=args[2]
# end=args[3]

def update_data(id,start,end):
    status=0
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    insert_sql ='insert into tb_record values(?,?,?,?)'

    try:
        cursor.execute(insert_sql,(id,start,end,status))
    except Exception as e:
        print(e)
        print('Error')
    else:
        conn.commit()
        print("successfully insert")

if __name__ == '__main__':
    fire.Fire(update_data)
