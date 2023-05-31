# KubeFlow Pipelines 
## Hands-On

In this part we are taking a look into the pipelining KubeFlow offers. 
For this purpose we have prepared 2 files within the `example` folder
- example_pipeline.py 
- example_visuals.py 

Within the first file you will find a new dataset that is getting transformed, trained and evaluated. 
Note that the code to do so is not intended to be executed  directly or locally. 
Instead, the code will be compiled and the resulting yaml will be uploaded to KubeFlow. 

The second file is just to give you more inspiration on how to enrich the pipelines with visual output

### Task 1
1. Get familiar with the code at hand 
2. run the python code for each of the files 
   - As you can see - the compiler will be called and produces the output 
3. Move to the KubeFlow interface and upload the yaml-file. 
4. Run each of the new pipelines 
5. Now go to the Kubeflow Website
   - Under Pipelines - click ** + Upload pipeline** 
   - Put in the required information 
   - select Upload a file and click **chose a file** 
   - navigate to the created yaml and upload it 
6. Go to Experiment(KFP)
   - And create a new experiment  via ** + Create experiment** 
   - After you created it - fill out the details by choosing the pipeline you just created 
   - Watch it run and interact with the outputs 


### Task 2
Please navigate to the hands_on/pipeline.py and have a look at the code. 
Now please create one new pipelines with the model we have below.
Split the pipeline into different groups:

   1. the download
   2. training

The exact location is market in the code below

Help: a usefull annotation might be

    def download_data(features: OutputPath(str), target: OutputPath(str)) -> NamedTuple("output",
                                                                                    [("features", str),
                                                                                     ("target", str)]):
