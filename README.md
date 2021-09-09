# Survey_Data_Analysis_Python
Survey_Data_Analysis_Python

Designing RESTful API with Python-Flask and posgres using survey response dataset    

This example project demonstrate reading data stored in S3, storing it in local DB for analysis, return the analysis via RESTful API with Python-Flask,      

The steps done for this project are
  1) Reading survey response loaded in CSV format from AWS S3 and incrementally ingesting to local database postgresDB     
  2) Analysing the data in postgres to find, average score, benchmark and the score distribution    
  3) Creating an API that provides access to the data analysis results, (average score, benchmark and the score distribution)   
  4) Dockering the application    

 You can download this project by cloning the repository:     

# Get the project code
git clone https://github.com/padmapria/Survey_Data_Analysis_Python.git  
NOTE: While working with Python, its recommended to use virtual environment to keep all the project's dependencies isolated from other projects.    

# To automate creating conda environment and deploying the project,
1) Clone this git repository in a folder, for example to the folder,  C:/survey_data_analysis 

2) Edit the startup.bat located in the scripts folder of this git project.
   Modify the venv_root_dir     
     set venv_root_dir="D:\Survey_Data_Analysis_Python\scripts"      
     to     
      set venv_root_dir="C:\survey_data_analysis\scripts"    
      
      save the changes
      
 3) Edit the start_app.bat located in the scripts folder of this git project. Modify the path pointing to the python file.      
      python D:\Survey_Data_Analysis_Python\src\config.py     
      python D:\Survey_Data_Analysis_Python\src\CreateTables.py    
      
      to    
      python C:\survey_data_analysis\src\config.py    
      python C:\survey_data_analysis\src\CreateTables.py    
      
      save the changes
      
  4) Run the startup.bat located in the scripts folder    
        
  The above steps will automatically   
        1) create a local conda environment    
        2) installing the dependencies given in the requirements.txt located in the scipts folder    
        3) Injesting data from s3 to postgresDB   
        4) Starting the application   
      
## Test the application
Once the application is started, go to localhost on Postman to test the API.

### To get Summary (Get Request).      
127.0.0.1:5000/summary    




### To get benchmark (Get Request)
127.0.0.1:5000/benchmark 


      
# To manually do the steps given in the steps 1 to 4, follow the below
## Create your local environment 
conda init
conda create -n survey_data_analysis python=3.7 anaconda     # To create the environment    
activate survey_data_analysis     # To activate the environment    

## Install dependencies    
pip install -r requirements.txt    
Start posgres Server    
    
## Config the application and deploy the application    
Change the DBNAME in the config file according to the database name you are using.    

Start the application to test locally using the below command  
python config.py    

## Test the application    
Once the application is started, go to localhost on Postman to test the API, using the endpoint given above.

