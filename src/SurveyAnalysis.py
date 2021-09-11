"""
SurveyAnalysis: 
"""
from flask import Flask, request
from config import db_conn,logger
from bson.json_util import dumps
import os # for Cwd path 
path = os.getcwd()

import simplejson as json

app = Flask(__name__)    # Construct an instance of Flask class for our webapp)

logger.info('Rest API Application started')    

'''
    Rest Endpoint to get survey Summary
    Req payload ex: http://127.0.0.1:5000/surveys
'''
@app.route('/surveys')
def computeSummary():
   
    print("Computing Survey Summary")
    logger.info("Calling /surveys API ****")
    sql_string = """
         SELECT
         survey_id,
         count(distinct(user_id)) as totalRespondents,
         count(distinct(question_id)) as totalQuestions,
         count(*) as totalSubmittedAnswers
         from survey_response GROUP BY survey_id;
         """
     
    with db_conn.cursor() as cursor:
        cursor.execute(sql_string)
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        json_data=[]
        for row in result:
            #print (dict(zip(columns, row))) 
            json_data.append(dict(zip(columns, row)))
        cursor.close()
        
        print(json.dumps(json_data, indent=4, sort_keys=True))
        logger.info(json.dumps(json_data, indent=4, sort_keys=True))
        return json.dumps(json_data),{'content-type':'application/json'}
    
    
'''
    Rest Endpoint to distribution of a specific survey
    Req payload ex: http://127.0.0.1:5000/survey_distribution?id=2
'''       
@app.route('/survey_distribution')
def find_benchmark_for_survey():         
    try:
        
        id = request.args.get('id', default = 1, type = int)
        logger.info("Calling /survey_distribution/id API for survey**** {}".format(id))
        print("Fetching distribution for survey =",id)
        sql_string = """
              SELECT
                  survey_id,question_id,
                  case when COUNT(question_id) OVER () > 50 then AVG (answer) else 0 end as average_score,
                  case when COUNT(question_id) OVER () > 50 then (SELECT AVG(answer) from survey_response where question_id=question_id)  else 0 end as benchmark, 
                  sum(case when (answer=4 OR answer=5) then 1 else 0 end) as favourable,
                  sum(case when (answer=2 OR answer=3) then 1 else 0 end) as neutral,
                  sum(case when answer =1 then 1 else 0 end) as unfavourable
                FROM survey_response where survey_id=%s GROUP BY question_id,survey_id having 
                count(question_id) > 50;
             """
         
        with db_conn.cursor() as cursor:
            cursor.execute(sql_string, [id])
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            json_data=[]
            for row in result:
                #print (dict(zip(columns, row))) 
                json_data.append(dict(zip(columns, row)))
            cursor.close()
            
            print(json.dumps(json_data, indent=4, sort_keys=True))
            logger.info(json.dumps(json_data, indent=4, sort_keys=True))
            return json.dumps(json_data),{'content-type':'application/json'}
    
    except Exception as e:
        print("exception"+e)
        logger.error(e)
        
        
'''
    Rest Endpoint to distribution of all surveys
    Req payload ex: http://127.0.0.1:5000/survey_distribution/all
'''    
@app.route('/survey_distribution/all')
def find_benchmark():
     print("Fetching distribution for all survey");
     logger.info("Calling /survey_distribution/all API **** ")
     sql_string = """
         SELECT
         question_id,survey_id,
          AVG (answer) AS average_score,
          (SELECT AVG(answer) from survey_response where question_id=question_id) as benchmark , 
          sum(case when (answer=4 OR answer=5) then 1 else 0 end) as favourable,
          sum(case when (answer=2 OR answer=3) then 1 else 0 end) as neutral,
          sum(case when answer =1 then 1 else 0 end) as unfavourable
          FROM survey_response GROUP BY question_id,survey_id  
          ORDER BY question_id ;
         """
     
     with db_conn.cursor() as cursor:
        cursor.execute(sql_string)
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        json_data=[]
        for row in result:
            #print (dict(zip(columns, row))) 
            json_data.append(dict(zip(columns, row)))
        
        cursor.close()
        print(json.dumps(json_data, indent=4, sort_keys=True))
        logger.info(json.dumps(json_data, indent=4, sort_keys=True))
        return json.dumps(json_data),{'content-type':'application/json'}
    
    
    
##Not used      
def computeDistributionForMoreThan50():

    sql_string = """
          SELECT
             question_id,survey_id,
              case when COUNT(question_id) OVER () > 50 then AVG (answer) else 0 end as average_score,
              case when COUNT(question_id) OVER () > 50 then (SELECT AVG(answer) from survey_response where question_id=question_id)  else 0 end as benchmark, 
              sum(case when (answer=4 OR answer=5) then 1 else 0 end) as favourable,
              sum(case when (answer=2 OR answer=3) then 1 else 0 end) as neutral,
              sum(case when answer =1 then 1 else 0 end) as unfavourable
            FROM survey_response GROUP BY question_id,survey_id having count(question_id) > 50;
         """
     
    with db_conn.cursor() as cursor:
        cursor.execute(sql_string)
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        for row in result:
            print (dict(zip(columns, row)))          
        cursor.close()
        
#print("Avg score and Score Distribution for more than 50 answered")
#computeDistributionForMoreThan50()


if __name__ == '__main__':  # Script executed directly?
    app.run()  # Launch built-in web server and run this Flask webapp
