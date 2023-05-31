# Instructions  

In the file here you can find multiple ways to save a trained model to disk. 

1. Uncomment and execute each of these files 
2. Have a look into each of the generated files - what can you observe?
3. add the following function to  model.py
```python 
    def train_forest():
        iris = datasets.load_iris()
        X = iris.data
        y = iris.target
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
        #Create a Gaussian Classifier
        clf=RandomForestClassifier(n_estimators=100)
        #Train the model using the training sets y_pred=clf.predict(X_test)
        clf.fit(X_train,y_train)
        return clf
```
4.Use "ls -l" in the terminal and note the size of the models as they are 
5.Rewrite all files to now store the new model instead - which do you expect to change the most