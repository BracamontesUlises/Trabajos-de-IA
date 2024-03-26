import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, f1_score
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical

def main():
    while True:
        num_layers = int(input("Ingrese el número de capas ocultas: "))
        neurons_per_layer = []
        for i in range(num_layers):
            neurons = int(input(f"Ingrese el número de neuronas en la capa {i + 1}: "))
            neurons_per_layer.append(neurons)
        epochs = int(input("Ingrese el número de épocas: "))

        X, y, df, label_encoder = cargar_datos()
        analizar_separabilidad(X, y, label_encoder)

        porcentajes_entrenamiento = list(range(10, 91, 10))
        resultados = {'Entrenamiento': [], 'Efectividad': [], 'Precision': [], 'F1-Score': []}

        for porcentaje_entrenamiento in porcentajes_entrenamiento:
            X_train, X_test, y_train, y_test = split_datos(X, y, porcentaje_entrenamiento)
            model = crear_modelo(X_train, y_train, neurons_per_layer, epochs)

            y_pred_probs = model.predict(X_test)
            y_pred = np.argmax(y_pred_probs, axis=1)
            y_test_argmax = np.argmax(y_test, axis=1)

            efectividad = accuracy_score(y_test_argmax, y_pred)
            precision = precision_score(y_test_argmax, y_pred, average='weighted')
            f1 = f1_score(y_test_argmax, y_pred, average='weighted')

            resultados['Entrenamiento'].append(f"{porcentaje_entrenamiento}%")
            resultados['Efectividad'].append(efectividad)
            resultados['Precision'].append(precision)
            resultados['F1-Score'].append(f1)

        df_resultados = pd.DataFrame(resultados)
        print("\n----------------------------------Resultados----------------------------------\n")
        print(df_resultados)

        Intento = input("Deseas volver a ejecutar el programa (Si/No): ")
        if Intento.lower() != "si":
            break

def cargar_datos():
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    #df_wine = pd.read_csv("/content/drive/MyDrive/wine.data", header=None)
    df_wine = pd.read_csv("/content/wine.data", header=None)
    label_encoder = LabelEncoder()
    y = to_categorical(label_encoder.fit_transform(df_wine.iloc[:, 0]), num_classes=3)
    X = df_wine.iloc[:, 1:].values

    return X, y, df_wine, label_encoder

def analizar_separabilidad(X, y, label_encoder):
    for class1 in range(3):
        for class2 in range(class1 + 1, 3):
            verificar_separabilidad(X, y, class1, class2)

def verificar_separabilidad(X, y, class1, class2):
    class_indices = (y[:, class1] == 1) | (y[:, class2] == 1)
    X_filtered = X[class_indices]
    y_filtered = y[class_indices]

    clf = SVC(kernel='linear')
    clf.fit(X_filtered, np.argmax(y_filtered, axis=1))
    accuracy = clf.score(X_filtered, np.argmax(y_filtered, axis=1))
    return accuracy

def crear_modelo(X, y, neurons_per_layer, epochs):
    model = Sequential()
    model.add(Dense(neurons_per_layer[0], activation='relu', input_dim=13))

    for neurons in neurons_per_layer[1:]:
        model.add(Dense(neurons, activation='relu'))

    model.add(Dense(3, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X, y, epochs=epochs, verbose=1)

    return model

def split_datos(X, y, porcentaje_entrenamiento):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=(100 - porcentaje_entrenamiento) / 100, random_state=42)
    return X_train, X_test, y_train, y_test

def evaluar_modelo(model, X, y, df, label_encoder):
    loss, accuracy = model.evaluate(X, y)
    print(f"\nAccuracy del modelo de perceptrón: {accuracy}")

    y_predicted_probs = model.predict(X)
    y_predicted = np.argmax(y_predicted_probs, axis=1)
    y_real = np.argmax(y, axis=1)
    df["Ye"] = y.tolist()
    df["Yc"] = y_predicted_probs.tolist()
    df["Yc"] = df["Yc"].apply(lambda x: list(map(lambda val: float(f"{val:.6f}"), x)))

    efectividad = calcular_efectividad(y_real, y_predicted)

    print("\n-------------------------------------Resultados-------------------------------------\n")
    print(df.iloc[:, :15])
    print(f"\nPérdida: {loss}")
    print(f"Precisión: {accuracy}")
    print(f"Efectividad del modelo: {efectividad}\n")

def calcular_efectividad(y_real, y_pred):
    total_registros = len(y_real)
    aciertos = sum(y_real == y_pred)
    efectividad = aciertos / total_registros
    return efectividad

if __name__ == "__main__":
    main()

# este proyecto se ejecuto mediante Google Colab
# se uso una base de datos de vinos para la realizacion de este trabajo