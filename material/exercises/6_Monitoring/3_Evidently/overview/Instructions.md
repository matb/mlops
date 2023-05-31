# Instructions

Let build a report that could be scheduled e.g. with airflow.

Here we will simulate how to test data quality with the utility of evidently.

1. Get familiar with the code in the app.py
2. Execute the code - preferably function by function and whatch the results
3. Edit one of the current-columns and execute the report again. E.g. you can use:
   `current['AveBedrms'] = current['AveBedrms'].values + np.random.normal(0, 5, current.shape[0])`