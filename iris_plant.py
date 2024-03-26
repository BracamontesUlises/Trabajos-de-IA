import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.svm import SVC
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical

def main():
    while True:
        # Solicitar al usuario la configuración del modelo
        num_layers = int(input("Ingrese el número de capas ocultas: "))
        neurons_per_layer = []
        for i in range(num_layers):
            neurons = int(input(f"Ingrese el número de neuronas en la capa {i + 1}: "))
            neurons_per_layer.append(neurons)
        epochs = int(input("Ingrese el número de épocas: "))

        X, y, df, label_encoder = cargar_datos()
        analizar_separabilidad(X, y, label_encoder)

        model = crear_modelo(X, y, neurons_per_layer, epochs)
        evaluar_modelo(model, X, y, df, label_encoder)

        Intento = input("Deseas volver a ejecutar el programa (Si/No): ")
        if Intento.lower() != "si":
            break

def cargar_datos():
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    df_iris = pd.read_csv("/content/bezdekIris.data", sep=",", header=None, names=["LS", "AS", "LP", "AP", "Class"])
    class_mapping = {'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2}
    df_iris["EncodedClass"] = df_iris["Class"].map(class_mapping)

    label_encoder = LabelEncoder()
    df_iris["EncodedClass"] = label_encoder.fit_transform(df_iris["Class"])

    y_one_hot = to_categorical(df_iris["EncodedClass"], num_classes=3)
    X = df_iris[["LS", "AS", "LP", "AP"]].values
    y = y_one_hot

    return X, y, df_iris, label_encoder

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
    model.add(Dense(neurons_per_layer[0], activation='relu', input_dim=4))

    for neurons in neurons_per_layer[1:]:
        model.add(Dense(neurons, activation='relu'))

    model.add(Dense(3, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X, y, epochs=epochs, verbose=1)

    return model

def evaluar_modelo(model, X, y, df, label_encoder):
    loss, accuracy = model.evaluate(X, y)
    print(f"\nAccuracy del modelo de perceptrón: {accuracy}")

    y_predicted_probs = model.predict(X)
    y_predicted = np.argmax(y_predicted_probs, axis=1)
    y_predicted_classes = label_encoder.inverse_transform(y_predicted)
    df["Ye"] = y.tolist()
    df["Yc"] = y_predicted_probs.tolist()
    df["Yc"] = df["Yc"].apply(lambda x: list(map(lambda val: float(f"{val:.6f}"), x)))

    print("\n-------------------------------------Resultados-------------------------------------\n")
    print(df[["LS", "AS", "LP", "AP", "Ye", "Yc"]])
    print(f"\nPérdida: {loss}")
    print(f"Precisión: {accuracy}\n")

if __name__ == "__main__":
    main()

# Este programa se ejecuto en Google Colab
# este es su direccion: https://colab.research.google.com/drive/16s19PdEO609V4oar8cMeVOAB1EMIuOWS?usp