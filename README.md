# Survey_Data_Analysis_Python

Designing RESTful API with Python-Flask and posgres using survey response dataset    

This example project demonstrate reading data stored in S3, storing it in local DB for analysis, return the analysis via RESTful API with Python-Flask,      

### The steps done for this project are
  1) Creating DB tables needed for the project
  2) Reading survey response loaded in CSV format from AWS S3 and incrementally ingesting to local database postgresDB (skipping the data injestion, if the file is already in DB)       
  3) Analysing the data in postgres to find, average score, benchmark and the score distribution    
  4) Creating an API that provides access to the data analysis results, (average score, benchmark and the score distribution)   
  5) Dockering the application    

### The task performed by various python files (.py) present in the src folder are :-    
      
 configuration.env  --> For storing environment variables needed for the project (configuration.bat if the application is run via conda environment)
  1) config.py   --> Centralized configuration to inialize DB connection, logging which will be imported by other python classes     
  2) CreateTables.py  --> Creating the DB tables need for the project
  3) ReadS3AndPopulateDB.py   -->  ingest the csv files from S3 and store relevant data in the Postgres database   
  4) SurveyAnalysis.py  --> computiing the average score and the score distribution, benchmark and Creation of Flask API for the same


 You can download this project by cloning the repository:  
  
# Get the project code
git clone https://github.com/padmapria/Survey_Data_Analysis_Python.git  
NOTE: While working with Python, its recommended to use virtual environment to keep all the project's dependencies isolated from other projects.    

# To automate creating conda environment and deploying the project,
1) Clone this git repository in a folder, for example to the folder,  C:/Survey_Data_Analysis_Python 

2) Edit the startup.bat located in the scripts folder of this git project.
   Modify the venv_root_dir     
     set venv_root_dir="D:\Survey_Data_Analysis_Python\scripts"      
     to     
      set venv_root_dir="C:\Survey_Data_Analysis_Python\scripts"    
      
      save the changes
      
 3) Edit the start_app.bat located in the scripts folder of this git project. Modify the path pointing to the python file.      
      python D:\Survey_Data_Analysis_Python\src\config.py     
      python D:\Survey_Data_Analysis_Python\src\CreateTables.py    
      python D:\Survey_Data_Analysis_Python\src\ReadS3AndPopulateDB.py     
      python D:\Survey_Data_Analysis_Python\src\SurveyAnalysis.py    
      
      to    
      python C:\Survey_Data_Analysis_Python\src\config.py    
      python C:\Survey_Data_Analysis_Python\src\CreateTables.py    
      python C:\Survey_Data_Analysis_Python\src\ReadS3AndPopulateDB.py     
      python C:\Survey_Data_Analysis_Python\src\SurveyAnalysis.py 
      
      save the changes
      
  4) Run the startup.bat located in the scripts folder    
        
  The above steps will automatically   
        1) create a local conda environment    
        2) installing the dependencies given in the requirements.txt located in the scipts folder    
        3) Injesting data from s3 to postgresDB   
        4) Starting the application   
      
## Test the application
Once the application is started, go to localhost on Postman to test the API.

### To get Survey Summary (Get Request).      
127.0.0.1:5000/surveys   
[![surveys.jpg](https://i.postimg.cc/xTBD6kdZ/surveys.jpg)](https://postimg.cc/YhNs9CYN)
     
      
### To get survey_distribution, benchmark for a specific survey (Get Request)
http://127.0.0.1:5000/survey_distribution?id=2
[![survey-distri-id.jpg](https://i.postimg.cc/rmf7xsbQ/survey-distri-id.jpg)](https://postimg.cc/MMjs86zQ)
     
      
### To get survey_distribution, benchmark for all surveys (Get Request)
http://127.0.0.1:5000/survey_distribution/all
[![survey-distri-all.jpg](https://i.postimg.cc/FK5fXsTW/survey-distri-all.jpg)](https://postimg.cc/YvR21kKY)

           
# To manually perform the tasks given in the steps 1 to 4 are: 
## Create your local environment 
conda init
conda create -n Survey_Data_Analysis_Python python=3.7 anaconda     # To create the environment    
activate Survey_Data_Analysis_Python     # To activate the environment    

## Install dependencies    
pip install -r requirements.txt    
Start posgres Server    
    
## Config the application and deploy the application    
Change the DBNAME in the config file (configuration.env/configuration.bat) according to the database name you are using.    

Start the application to test locally using the below command  
python config.py    

## Test the application    
Once the application is started, go to localhost on Postman to test the API, using the endpoint given above.

