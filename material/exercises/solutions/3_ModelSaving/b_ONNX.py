from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import onnxmltools
from skl2onnx.common.data_types import FloatTensorType

from model import train_forest as train


def main():

    model = train()

    # Convert the model to ONNX format
    initial_type = [('float_input', FloatTensorType([None, 4])),]
    onnx_model = onnxmltools.convert_sklearn(model, initial_types=initial_type)
    # Save the ONNX model to a file
    onnxmltools.utils.save_model(onnx_model, 'model.onnx')

if __name__ == '__main__':
    main()