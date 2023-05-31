# Demo

This is an introduction to evidently if used in production.
Will simulate a fast batchprocessing of data which will be sent to a Flask API to be monitored.
The API itself will expose the functionality of evidently and connect it to prometheus.
Finally, we will visualize the results using Grafana

To get started just execute `run_example.py`

- you can then view Grafana using http://localhost:3000 and login with "admin:admin"
- you find pre-mounted dashboard under Dashboard -> General

### Alerts 
Grafana is great at whatching your data and alerting you in case something is wrong - and we will create such an alert now. 

1. In Grafana - start by clicking on the hamburger menu and go down to "Alerting"
2. On this new page you find a hyperlink "Manage alert rules" 
3. Here you can see a big blue button "Create alert rule"
4.  Now you can define the alert you want to have 
5. Give your alert explanatory name 
6. in step 2 we  need to define the rules what we want to whatch out for. This is based on the same metrics we can use for visualizations. 
- lets take evidently:cat_target_drift:drift as example 
7. The  "B" Reduce part tells us what we want to do with our timeseries - e.g. take the maximum
8. Then we define the threshold - when should the trigger go off - we can take >0.4 
9. Now we  either chose or create the Folder were Grafana should save and organize the alert. The Group is important for grafana on how to evaluate multiple alerts -e.g. every minute (1m).
10. Finally, we can finetune our alert by editing the message that we receive and how we receive it. 


Now go up to the start again and hit "Save" - Done!
Now you have a woriking alert that can post your alerts 