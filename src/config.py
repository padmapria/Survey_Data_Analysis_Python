"""This module is to configure app to connect with database."""

import psycopg2
import logging
import os
import sys,io
from decouple import config
from os import environ as env
from dotenv import load_dotenv as load_dotenv

#https://stackoverflow.com/questions/41546883/what-is-the-use-of-python-dotenv
load_dotenv(dotenv_path='configuration.env')

#Loading the environment variables
t_host = env['DB_HOST']
t_port = env['DB_PORT']
t_dbname = env['DB_NAME']
t_user = env['DB_USER']
t_pw = env['DB_PASS']

#Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#https://stackoverflow.com/questions/10598002/how-do-i-get-tables-in-postgres-using-psycopg2
try:
    db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw, connect_timeout=5)
    cursor = db_conn.cursor()
    cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
    existing_tables=(list(sum(cursor.fetchall(), ())))
    print("Tables present in the Db are ** ",existing_tables)
    cursor.close()
    
except Exception as e:
    logger.error("ERROR: Unexpected error: Could not connect to postgres instance.")
    logger.error(e)
    sys.exit()

print("SUCCESS: Connection to RDS mysql instance succeeded")
logger.info("SUCCESS: Connection to RDS mysql instance succeeded")
