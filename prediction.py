import numpy as np
from PIL import Image
from tensorflow.keras.models import model_from_json
from sklearn.preprocessing import LabelEncoder

def getPrediction(file_path):
    
    classes = ['NonDemented','VeryMildDemented','MildDemented','ModerateDemented']
    le = LabelEncoder()
    le.fit(classes)
    le.inverse_transform([2])
    
    
    #Load model
    with open('C:/Users/halo4/OneDrive/Up/Clases/Aprenizaje maquina 2/Proyecto/Irving/model.json', 'r') as json_file:
        loaded_model_json = json_file.read()
    my_model = model_from_json(loaded_model_json)
    my_model.load_weights('C:\\Users\\halo4\\OneDrive\\Up\\Clases\\Aprenizaje maquina 2\\Proyecto\\Irving\\model_cnnv2.h5')
    
    imagenes_array_train = []
    imagen_array = np.asarray(Image.open(file_path).convert("RGB").resize((176, 208)))       
    # Añadir el array NumPy a la lista
    imagenes_array_train.append(imagen_array)

    img = np.stack(imagenes_array_train)
    
    pred = my_model.predict(img) #Predict                    
    
    #Convert prediction to class name
    pred_class = le.inverse_transform([np.argmax(pred)])[0]
    # print("Diagnosis is:", pred_class)
    return pred_class

# print(getPrediction("C:\\Users\\halo4\\OneDrive\\Up\\Clases\\Aprenizaje maquina 2\\test\\NonDemented\\26 (71).jpg"))