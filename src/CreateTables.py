from __future__ import print_function
from config import db_conn,logger
import psycopg2

def create_tables():
    """ create tables in the PostgreSQL database"""
    logger.info("Table creation started... ")
    commands = (
        """
        CREATE TABLE survey_details (
            survey_id serial PRIMARY KEY,
            file_name VARCHAR ( 150 ),
            created_on TIMESTAMP NOT NULL,
            s3_last_modified_on VARCHAR ( 80 )
        )
        """,
        """
        CREATE TABLE survey_response (
               user_id integer,
                question_id integer,
                answer integer NOT NULL,
                survey_id integer,
                FOREIGN KEY (survey_id)
                REFERENCES survey_details (survey_id),
                created_on TIMESTAMP NOT NULL
        )
        """)
    
    try:
        cur = db_conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        db_conn.commit()
        print("Table creation successful")
        logger.info("Table creation successful")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        logger.error(error)

if __name__ == '__main__':
    create_tables()