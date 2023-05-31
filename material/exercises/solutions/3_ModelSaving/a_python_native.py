import pickle

import dill

from model import train_forest as train


def save_pickle(model):
    with open("model.pckl", "wb") as f:
        pickle.dump(model, f)


def save_dill(model):
    with open('model.dill', 'wb') as f:
        dill.dump(model, f)


def main():
    model = train()
    save_pickle(model)
    save_dill(model)


if __name__ == '__main__':
    main()
