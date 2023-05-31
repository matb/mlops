from sklearn2pmml import sklearn2pmml , make_pmml_pipeline

from model import train_forest as train

def main():
    model = train()
    pmml = make_pmml_pipeline(model)
    # Convert the model to PMML format
    sklearn2pmml(pmml, 'model.pmml')


if __name__ == '__main__':
    main()