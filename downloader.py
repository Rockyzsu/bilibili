# @Time : 2019/1/28 14:19
# @File : youtube_downloader.py

import logging
import os
import subprocess
import sys
import datetime
import re
import codecs
import sqlite3
import time
from config import START, END, ID, YOU_GET_PATH,MINS
CMD = 'python {} {}'
filename = 'url.txt'


class SQLite():
    def __init__(self):
        self.conn = sqlite3.connect('history.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        create_sql = 'create table if not exists tb_download (url varchar(100),status tinyint,crawltime datetime)'
        create_record_tb = 'create table if not exists tb_record (idx varchar(100) PRIMARY KEY,start tinyint,end tinyint,status tinyint)'
        self.cursor.execute(create_record_tb)
        self.conn.commit()
        self.cursor.execute(create_sql)
        self.conn.commit()

    def exists(self,url):
        querySet = 'select * from tb_download where url = ? and status = 1'
        self.cursor.execute(querySet,(url,))
        ret = self.cursor.fetchone()
        return True if ret else False

    def insert_history(self,url,status):
        query = 'select * from tb_download where url=?'
        self.cursor.execute(query,(url,))
        ret = self.cursor.fetchone()
        current = datetime.datetime.now()

        if ret:
            insert_sql='update tb_download set status=?,crawltime=? where url = ?'
            args=(status,status,current,url)
        else:
            insert_sql = 'insert into tb_download values(?,?,?)'
            args=(url,status,current)

        try:
            self.cursor.execute(insert_sql,args)
        except:
            self.conn.rollback()
            return False
        else:
            self.conn.commit()
            return True

    def get(self):
        sql = 'select idx,start,end from tb_record where status=0'
        self.cursor.execute(sql)
        ret= self.cursor.fetchone()
        return ret

    def set(self,idx):
        print('set status =1')
        sql='update tb_record set status=1 where idx=?'
        self.cursor.execute(sql,(idx,))
        self.conn.commit()

def llogger(filename):
    logger = logging.getLogger(filename)  # 不加名称设置root logger

    logger.setLevel(logging.DEBUG)  # 设置输出级别

    formatter = logging.Formatter(
        '[%(asctime)s][%(filename)s][line: %(lineno)d]\[%(levelname)s] ## %(message)s)',
        datefmt='%Y-%m-%d %H:%M:%S')

    # 使用FileHandler输出到文件
    prefix = os.path.splitext(filename)[0]
    fh = logging.FileHandler(prefix + '.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    # 使用StreamHandler输出到屏幕
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    # 添加两个Handler
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger


logger = llogger('download.log')
sql_obj = SQLite()

def run():
    while 1:
        result = sql_obj.get()
        print(result)
        if result:
            idx=result[0]
            start=result[1]
            end=result[2]
            try:
                download_bilibili(idx,start,end)
            except:
                pass
            else:
                sql_obj.set(idx)
        else:
            time.sleep(MINS*60)

def download_bilibili(id,start_page,total_page):
    global doc
    # 填入id和页面
    #id = ID
    #start_page = START
    #total_page = END

    bilibili_url = 'https://www.bilibili.com/video/{}?p={}'
    for i in range(start_page, total_page+1):

        next_url = bilibili_url.format(id, i)
        if sql_obj.exists(next_url):
            print('have download')
            continue

        try:
            command = CMD.format(YOU_GET_PATH, next_url)
            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 shell=True)

            output, error = p.communicate()

        except Exception as e:
            print('has execption')
            sql_obj.insert_history(next_url,status=0)
            logger.error(e)
            continue
        else:
            output_str = output.decode()
            if len(output_str) == 0:
                sql_obj.insert_history(next_url,status=0)
                logger.info('下载失败')
                continue

            logger.info('{} has been downloaded !'.format(next_url))
            sql_obj.insert_history(next_url,status=1)

#download_bilibili()
run()
