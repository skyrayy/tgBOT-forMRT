from keras.models import load_model  
from PIL import Image, ImageOps 
import numpy as np


#Переменные
TOKEN = 'токен бота'
mozg = 'айди специалиста, которому будут приходить мрт мозга'
bruho = 'айди специалиста, которому будут приходить мрт брюшной полости'
addmin = 'айди админа, который в случае уверенности ии менее 60% будет сам решать какому специалисту отправлять данные'
channel = 'ссылка на телеграмм канал'

#Функция, которая определяет объект на фотографии
def get_class(image_path):

    np.set_printoptions(suppress=True)

    model = load_model("keras_model.h5", compile=False)

    class_names = open("labels.txt", "r").readlines()

    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    image = Image.open(image_path).convert("RGB")

    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    image_array = np.asarray(image)

    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    data[0] = normalized_image_array

    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    if confidence_score<=0.6:
        return ('notsure')
    else:
        return class_name[2:-1]

