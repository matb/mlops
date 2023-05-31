# Apache Airflow - Instructions

We are going through a standard installation of apache airflow for local usage and development, have a look at some examples and then create one new dag. 

## Getting started with Apache Airflow 

For this we will create a virtual environment with python, install the required libraries, start the server and look into the UI 

1. create a virtual environment with python
	1.  `python3 -m venv --prompt airflow venv`
2. Install apache airflow 
	1. Activate the environment we just created `source venv/bin/activate`
	2. Ensure that your prompt has changed  and now start with `airflow`
	3. Install the necessary packages using `python -m pip install apache-airflow`
3. Start airflow 
	1.  set the home path for airflow to use via `export AIRFLOW_HOME=~/airflow`
	2.  start all of the components in one go using `airflow standalone`
	3.  Grab the credentials by using either of these methods 
		1. Follow the logs a little until the point when the webserver started and shows you the credientials 
		2. Alternatively you can find the credentials in your airflow home e.g.  with `cat ~/airflow/standalone_admin_password.txt`
4. Navigate to the UI with <host-ip>:8080


## Example Dags 

beside all of the example dags already visible in the airflow UI have a look at the two examples we provide in the folder :
- 0_example.py
- 1_jinja.py  

Both of them define a simple example workflow with 3 Tasks:
1. Log the start of the execution in a log file in the tmp folder 
2. Create a pipeline file 
3. Use python to read that pipeline file and modify it

The only logical difference is that one of them is using static file names while the second one is using a templating engine called jinja to make these files dynamic. 

Task: 
- Move the file into Airflow dags folder your can find in its home directory you defined via the environment variable
```
cp engineering/material/exercises/1_Airflow/0_example.py ~/airflow/dags
cp engineering/material/exercises/1_Airflow/1_jinja.py ~/airflow/dags
```
- Trigger of both – are there any differences in their execution?
	- *Hint: there is a difference in the default_args*



