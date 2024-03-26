import numpy as np
from sklearn import preprocessing
from keras.utils import to_categorical
from tensorflow import random
from keras import Sequential
from keras.layers import Dense, Activation
import pandas as pd

def execute_logical_operation(X, Y, entrada, operation_name):
    print(f"\n {operation_name}")
    model_perceptron(X, Y, entrada)

def execute_exercise(X, Y, entrada, exercise_name):
    print(f"\n {exercise_name}")
    model_perceptron(X, Y, entrada)

def model_perceptron(X, Y, entrada):
    num_hidden_layers = int(input("Ingrese el número de capas ocultas: "))
    neurons_per_layer = []
    for i in range(num_hidden_layers):
        neurons = int(input(f"Ingrese el número de neuronas en la capa {i + 1}: "))
        neurons_per_layer.append(neurons)
    epochs = int(input("Ingrese el número de épocas: "))

    random.set_seed(20)
    model = Sequential()

    for i, neurons in enumerate(neurons_per_layer):
        if i == 0:
            model.add(Dense(neurons, activation='relu', input_dim=entrada))
        else:
            model.add(Dense(neurons, activation='relu'))

    model.add(Dense(1, activation='linear'))

    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

    model.fit(X, Y, epochs=epochs)

    loss, accuracy = model.evaluate(X, Y, verbose=0)
    print(f"Pérdida: {loss}")
    print(f"Precisión: {accuracy}")

    y_predicted = model.predict(X)

    results_df = pd.DataFrame(data=np.concatenate((X, y_predicted, Y.reshape(-1, 1)), axis=1),
                              columns=[f'X{i}' for i in range(1, entrada + 1)] + ['Yc', 'Ye'])

    print("Resultados:")
    print(results_df.to_string(index=False))

def main_menu():
    while True:
        print("Menú:")
        print("1. AND")
        print("2. OR")
        print("3. XOR")
        print("4. Ejercicio1")
        print("5. Mayoria Simple")
        print("6. Paridad")
        print("7. Salir")
        option = int(input("Elige una opción: "))

        if option == 1:
            execute_logical_operation(np.array([[0, 0], [0, 1], [1, 0], [1, 1]], "float32"),
                                       np.array([0, 0, 0, 1], "float32"), 2, "OPERACIÓN AND")
        elif option == 2:
            execute_logical_operation(np.array([[0, 0], [0, 1], [1, 0], [1, 1]], "float32"),
                                       np.array([0, 1, 1, 1], "float32"), 2, "OPERACIÓN OR")
        elif option == 3:
            execute_logical_operation(np.array([[0, 0], [0, 1], [1, 0], [1, 1]], "float32"),
                                       np.array([0, 1, 1, 0], "float32"), 2, "OPERACIÓN XOR")
        elif option == 4:
            execute_exercise(np.array([[2, 0], [0, 0], [2, 2], [0, 1], [1, 1], [1, 2]], "float32"),
                             np.array([1, 0, 1, 0, 1, 0], "float32"), 2, "EJERCICIO 1")
        elif option == 5:
            execute_exercise(np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]], "float32"),
                             np.array([0, 0, 0, 1, 0, 1, 1, 1], "float32"), 3, "MAYORÍA SIMPLE")
        elif option == 6:
            execute_exercise(np.array([
                [0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 1],
                [0, 1, 0, 0], [0, 1, 0, 1], [0, 1, 1, 0], [0, 1, 1, 1],
                [1, 0, 0, 0], [1, 0, 0, 1], [1, 0, 1, 0], [1, 0, 1, 1],
                [1, 1, 0, 0], [1, 1, 0, 1], [1, 1, 1, 0], [1, 1, 1, 1]
            ], "float32"),
                             np.array([1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1], "float32"), 4, "PARIDAD")
        elif option == 7:
            break
        else:
            print("Opción no válida. Por favor, elige 1, 2, 3, 4, 5, 6 o 7.")


main_menu()

# Programa Creado en Equpio por:
# Bracamontes Ordoñez Ulises
# Robert González Jesús Israel
# ESIME-ZACATENCO ICE, Especialidad computacion 