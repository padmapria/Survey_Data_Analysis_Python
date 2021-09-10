from __future__ import print_function
import boto3
import boto
import csv
import os
from smart_open import smart_open
from datetime import datetime as dt
from config import db_conn,env,logger


#Loading the environment variables
BUCKET_NAME = env['BUCKET_NAME']
PREFIX=env['PREFIX']

      
def download_s3_file():
    logger.info("Downloading file from  s3")
    client = boto3.client('s3', aws_access_key_id='', aws_secret_access_key='')
    client._request_signer.sign = (lambda *args, **kwargs: None)

    bucket_list = []
    lastModified = []
    
    #https://stackoverflow.com/questions/35803027/retrieving-subfolders-names-in-s3-bucket-from-boto3
    response  = client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX )
    
    #Fetching the list of files that are already in DB, to skip adding the files again
    fetch_fileNames_sql="SELECT file_name from survey_details;"
    with db_conn.cursor() as cursor:
        cursor.execute(fetch_fileNames_sql)
        result = cursor.fetchall()
        existing_files=(list(sum(result, ())))      
        cursor.close()

    #Fetching the list of files from S3    
    for object in response['Contents']:
        if(object['Key'].find(".csv")!=-1):
            if(object['Key'] in existing_files):
                print("Contents of the file are already in DB, skipping re-adding the file **",object['Key'])
            else:
                print("New File found in s3 **",object['Key'])
                bucket_list.append(object['Key'])
                lastModified.append(object['LastModified'])
            
    print("List of Files to create entry in DB are **",bucket_list[0:10])
    
    for i in range(len(bucket_list)):
        BUCKET_FILE_NAME= bucket_list[i]
        S3_LastModified=lastModified[i]
        
        #https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
        head, LOCAL_FILE_NAME = os.path.split(BUCKET_FILE_NAME)
    
        #Downloading the file to local file system
        client.download_file(BUCKET_NAME, BUCKET_FILE_NAME, LOCAL_FILE_NAME)
        store_survey_details(BUCKET_FILE_NAME,S3_LastModified,LOCAL_FILE_NAME)
    
            
                  
def store_survey_details(BUCKET_FILE_NAME, S3_LastModified,LOCAL_FILE_NAME):
    
    print("To create Survey details in DB for the file ** ",BUCKET_FILE_NAME)
    logger.info("To create Survey details in DB for the file")
    with db_conn.cursor() as cur:
        survey_id= None
        sql_string = """INSERT INTO survey_details (file_name,created_on,s3_last_modified_on) 
        VALUES (%s,%s,%s) RETURNING survey_id;"""
        
        try:
            cur.execute(sql_string, (BUCKET_FILE_NAME,dt.now(),S3_LastModified))
            survey_id = cur.fetchone()[0]
            db_conn.commit()
            
            print("Survey details created in DB for the file ** ",BUCKET_FILE_NAME)
            cur.close()
            
            #Parse the file and store the contents to DB
            with open(LOCAL_FILE_NAME, 'r') as csvfile:
                csv_data = csv.reader(csvfile) 
                store_survey_response(csv_data,survey_id)
                print("Survey response added in DB for the file ** ",BUCKET_FILE_NAME)
                
        except Exception as e:
                print("exception"+cur.fetchall())
                logger.error(e)



def store_survey_response(csv_data, survey_id):
    print("To add survey response to DB")
    logger.info("To add survey response to DB")
    sql_string ="""INSERT INTO survey_response (question_id, user_id, answer, survey_id,created_on) 
                VALUES(%s,%s,%s,%s,%s);"""
    with db_conn.cursor() as cur:
        for idx, row in enumerate(csv_data):
            try:
                if (row[0]) != 'questionId':
                    cur.execute(sql_string, (row[0], row[1], row[2],survey_id,dt.now()))
                    db_conn.commit()
                else:
                    print("Header found..Skipping the header !!")
                    logger.info(row)
            except Exception as e:
                print("exception"+cur.fetchall())
                logger.error(e)
        cur.close()        
                    
  
if __name__ == '__main__':       
    download_s3_file()


      
'''
Not used as this method need access key and secret access 
'''
def download_s3_file_with_aws_key():
    #If we have access key then we can use the below method"
    #https://www.sqlservercentral.com/articles/reading-a-specific-file-from-an-s3-bucket-using-python
    s3_client =boto3.client('s3')
    s3_bucket_name=BUCKET_NAME
    s3 = boto3.resource('s3', aws_access_key_id='xxxxxxxx', aws_secret_access_key='yyyyyy')

    my_bucket=s3.Bucket(s3_bucket_name)
    bucket_list = []
    for file in my_bucket.objects.filter(Prefix = 'analytics_assessment'):
        file_name=file.key
        if file_name.find(".csv")!=-1:
            bucket_list.append(file.key)
    length_bucket_list=print(len(bucket_list))
    print(bucket_list[0:10])
    
    
'''
Not used as this method need access key and secret access 
'''
def read1(bucket_name,region, remote_file_name, aws_access_key_id, aws_secret_access_key):
    #https://stackoverflow.com/questions/30818341/how-to-read-a-csv-file-from-an-s3-bucket-using-pandas-in-python/46323684
    path = 's3://{}:{}@{}/{}'.format(aws_access_key_id, aws_secret_access_key, bucket_name, remote_file_name)

    df = pd.read_csv(smart_open(path))
    x = df.head()  
    print(x)

#read1("er-public-assets","ap-southeast-1","analytics_assessment/1_1.csv","xxxxxxxx","yyyyyy")