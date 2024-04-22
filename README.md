# Reddit ETL Pipe Line Project

This project provides a comprehensive data pipeline solution to ETL Reddit data into a AWS Redshift data warehouse. The pipeline leverages a combination of tools and services including Apache Airflow, Celery, PostgreSQL, Amazon S3, AWS Glue, Amazon Athena, and Amazon Redshift.

## Prerequisites
- AWS Account with appropriate permissions for S3, Glue, Athena, and Redshift.
- Reddit API Credentials, you need to get the own reddit_secret_key and reddit_client_id.
- Docker Installation
- Python 3.9, It might not work if the version is lower or higher.
- Apache Airflow Fernet Key (specific secret key)
- PostGreSQL

## How to get Apache Airflow Fernet Key
Open the Python and print the below code.
- Referecned by https://cryptography.io/en/latest/fernet/
- Once you run this code, you will get the fernet key and keep it in secured place!
```bash
from cryptography.fernet import Fernet

fernet_key = Fernet.generate_key()
print(fernet_key.decode())
```

## How to get Reddit API
https://www.geeksforgeeks.org/how-to-get-client_id-and-client_secret-for-python-reddit-api-registration/![image](https://github.com/kmpark70/Reddit_Project/assets/72221217/1f6d8697-d575-43e4-b266-9ff9e8b94871)

## How to change username and password in Apache Airflow
1. Go to Docker.compose.yml and find the below lines.
```bash
  airflow-init:
    <<: *airflow-common
    command: >
      bash -c "pip install -r /opt/airflow/requirements.txt && airflow db init && airflow db upgrade && airflow users create --username admin --firstname admin --lastname admin --role Admin --email airflow@airflow.com --password admin"
    restart: "no"
```
2. You can change the username and password. Initially, we set id and password are admin.

## System Setup
1. Clone the repository.
```bash
https://github.com/kmpark70/Reddit_Project.git
```
2. Create a virtual environment.
```bash
python-3 -m venv venv
```
3. Activate the virtual environment.
```bash
On windows:
myenv\Scripts\activate
```
```bash
On MacOS/Linux:
source venv/bin/activate
```
4. Install the dependencies.
```bash
pip install -r requirements.txt
```
5. Create a folder named config and place the config.conf.example file inside that folder.
- If Broken.DAG issue occurs
```bash
.../config/config.conf.example
```
6. Starting the containers
```bash
docker-compose up -d --build
```
7. Launch the Airflow web UI.
```bash
open http://localhost:8080
```
## AWS ETL Guidelines
### AWS S3
1. If you prefer to use terminal then install the lines below.
- Brew install awscli
```bash
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
```
2. Create a S3 bucket in AWS, then navigate to config.conf, and within [aws], add your created bucket under aws_bucket_name as cs4440-reddit-data-engineering.
   
3. Next, go to Apache Airflow, click Admin - Xcomps.
- The information of "return value", "reddit_extraction" is written in aws_S3_pipeline.py
  
4. Check if the CSV file has been successfully moved to the S3 bucket.
   
5. Create a folder in the location where raw files are stored and add Transformed_Data as a folder
6. Using AWS Glue, direct the transformed files to this location as the final destination.

### AWS Glue
<Part1>
  
1. Click on the orange button for Visual ETL.
  
2. Click on "Sources" and select "Amazon S3.
   
3. Click on "Targets" and select "Amazon S3.
   
4. Then, two boxes will be connected.
   
5. Click on the box above, then press "Browse," and choose the CSV file.
   
6. Click on "Infer schema".
   
7. The CSV file should be in the box above.
    
8. In the box below (destination schema), set the desired data format.
    
9. Click on "Job details," change the Name to "reddit_glue_job.
    
10. Click on "Advanced properties" to ensure it's set to "reddit_glue_job.py."
    
11. Click on "Script," press "-edit," confirm, and then add the code between AmazonS3_node and Amazon S3_node.
    
12. Click on "Save," then press "Run." Next, click on the "Runs" section.
    
13. Once you see the result marked as "Succeeded," go to the S3 bucket and check if it's in the "Transformed_" folder. Confirm that it's done properly.

<Part2>
1. Click on AWS Crawler and create a new one named "reddit_crawler". 
  
2. Next, click on "Add a data source" -> browse S3 -> Choose the Run file within the Transformed folder.
   
3. Click "Create new IAM role" and select AWSGlueServiceRole-reddit-glue-role.
 
4. Click on "Add database" -> reddit_db -> then click "Refresh" and select reddit_db.
 
5. Click on "Run crawler". It will take approximately 2 minutes. Wait until it shows "completed".
   
6. After that, go to AWS Glue -> Databases -> reddit_db -> Check the table data.
 
7. Athena screen will open. From there, go to Amazon Athena -> Query editor -> Manage Settings -> Browse S3 -> Add another folder named "athena_scripts" to the S3 Bucket -> Then choose and save.

### AWS Redshift
1. Create Workgroup: reddit-workgroup.
   
2. Associated IAM Roles - Click "Manage IAM roles" -> Choose S3.
  
3. Once this is completed, click on "Query data" in the top right corner.
   
4. You can view the CSV and Parquet files in AWS Redshift in a table format.

## Data Preparation and Setup
1. Specify the database system(s) and version(s) used, along with installation instructions (a link to official documentation will be enough).
- PostGreSQL, makesure the portnumber: 5432
- AWS S3, Redshift, referenced by https://pypi.org/project/s3fs/
2. Describe how to acquire project data. Include a small dataset sample (< 5 MB) or provide scripts to download/scrape/process the data.
3. How do we load this data into the database system?
- When you open the data folder, you'll find input and output as sub-folders. The input folder contains the raw log files, while the output folder contains the result of the ETL process, which is a CSV file.
- You can download those files.
4. Do you have some scripts to do that? If so, how do we execute them?
- Please follow the installation guide above.
5. Did you use some tools for loading? If so, provide appropriate details and links.
- We don't use any tools for loading, but when it comes to parquet file in AWS, you can download in AWS ecosystem.
If you are benchmarking different database systems, detail any configuration modifications made.
- You have to follow the port number and PostgreSQL due to our initial configuration.
If generating your own data, include a sample of the synthetic dataset/database.
- We don't use any our own data, The data is from the Real-time Reddit API.
