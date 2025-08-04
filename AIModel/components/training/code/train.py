import argparse
import os
from glob import glob
import random
import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix
from azureml.core import Run
from utils import *

SEED = 42
INITIAL_LEARNING_RATE = 0.01
BATCH_SIZE = 32
PATIENCE = 11
model_name = 'flower-cnn'

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--training_folder', type=str, dest='training_folder', help='training folder mounting point')
    parser.add_argument('--testing_folder', type=str, dest='testing_folder', help='testing folder mounting point')
    parser.add_argument('--output_folder', type=str, dest='output_folder', help='Output folder')
    parser.add_argument('--epochs', type=int, dest='epochs', help='The amount of Epochs to train')
    parser.add_argument("--seed", type=int)
    parser.add_argument("--initial_learning_rate", type=float)
    parser.add_argument("--batch_size", type=int)
    parser.add_argument("--patience", type=int)
    parser.add_argument("--model_name", type=str)
    args = parser.parse_args()


    print(" ".join(f"{k}={v}" for k, v in vars(args).items()))

    training_folder = args.training_folder
    print('Training folder:', training_folder)

    testing_folder = args.testing_folder
    print('Testing folder:', testing_folder)

    output_folder = args.output_folder
    print('Testing folder:', output_folder)

    MAX_EPOCHS = args.epochs

    training_paths = glob(training_folder + "/*.jpg", recursive=True)
    testing_paths = glob(testing_folder + "/*.jpg", recursive=True)

    print("Training samples:", len(training_paths))
    print("Testing samples:", len(testing_paths))

    random.seed(SEED)
    random.shuffle(training_paths)
    random.seed(SEED)
    random.shuffle(testing_paths)

    print(training_paths[:3])
    print(testing_paths[:3])

    X_train = getFeatures(training_paths)
    y_train = getTargets(training_paths)

    X_test = getFeatures(testing_paths)
    y_test = getTargets(testing_paths)

    print('Shapes:')
    print(X_train.shape)
    print(X_test.shape)
    print(len(y_train))
    print(len(y_test))

    LABELS, y_train, y_test = encodeLabels(y_train, y_test)
    
    print('One Hot Shapes:')

    print(y_train.shape)
    print(y_test.shape)

    print(f"y_train type: {type(y_train)}, shape: {y_train.shape}, example:\n{y_train[:3]}")
    print(f"y_test type: {type(y_test)}, shape: {y_test.shape}, example:\n{y_test[:3]}")

    model_directory = os.path.join(output_folder, model_name)
    os.makedirs(os.path.dirname(model_directory), exist_ok=True)
    model_path = os.path.join(model_directory, "model.keras")

    cb_save_best_model = keras.callbacks.ModelCheckpoint(filepath=model_path,
                                                            monitor='val_loss', 
                                                            save_best_only=True, 
                                                            verbose=1)

    cb_early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', 
                                                patience= PATIENCE,
                                                verbose=1,
                                                restore_best_weights=True)

    cb_reduce_lr_on_plateau = keras.callbacks.ReduceLROnPlateau(factor=.5, patience=4, verbose=1)
    lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
        initial_learning_rate=INITIAL_LEARNING_RATE,
        decay_steps=MAX_EPOCHS,
        decay_rate=0.5,
        staircase=True 
    )

    opt = tf.keras.optimizers.SGD(
        learning_rate=lr_schedule,
        momentum=0.0,
        nesterov=False
    )

    print("Building model")
    model = buildModel((64, 64, 3), 5)

    model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

    aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
                            height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
                            horizontal_flip=True, fill_mode="nearest")


    history = model.fit( aug.flow(X_train, y_train, batch_size=BATCH_SIZE),
                            validation_data=(X_test, y_test),
                            steps_per_epoch=len(X_train) // BATCH_SIZE,
                            epochs=MAX_EPOCHS,
                            callbacks=[cb_save_best_model, cb_early_stop, cb_reduce_lr_on_plateau] )

    print("[INFO] evaluating network...")
    predictions = model.predict(X_test, batch_size=32)
    print(classification_report(y_test.argmax(axis=1), predictions.argmax(axis=1), target_names=['tulip', 'sunflower', 'rose', 'dandelion', 'daisy']))


if __name__ == "__main__":
    main()