import tensorflow as tf
from sklearn import datasets
from sklearn.model_selection import train_test_split

VERSION = 1


def main():
    iris = datasets.load_iris()
    features = iris.data
    labels = iris.target

    features_train, features_test, labels_train, labels_test = train_test_split(
        features, labels, test_size=0.2, random_state=42
    )

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(10, activation='relu', input_shape=(4,)),
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(3, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(features_train, labels_train, epochs=100, batch_size=32)

    loss, accuracy = model.evaluate(features_test, labels_test)
    print(f'Test loss: {loss}')
    print(f'Test accuracy: {accuracy}')

    # Step 6: Save the trained model
    model.save(f'models/iris/{VERSION}')

    print("Model saved successfully!")


if __name__ == '__main__':
    main()
