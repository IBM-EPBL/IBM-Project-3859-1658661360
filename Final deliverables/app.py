from flask import Flask, render_template,request
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import requests
from flask_sqlalchemy import SQLAlchemy
from cloudant.client import Cloudant 

app=Flask(__name__)

client = Cloudant.iam("3ee50175-428c-485a-bc07-a2a2f168570f-bluemix", "rveYiwft6107kLBtVLDCboinURgJmcCdziMRtMnlVYtk", connect=True)
session = client.session()

print('Databases: {0}'.format(client.all_dbs()))
my_database = client.create_database('nutrition')

# You can check that the database exists
if my_database.exists():
    print('SUCCESS!!')
model=load_model(r"model_ibm.h5")
def predict(img):
    index=['Banana', 'Banana Lady Finger', 'Banana Red', 'Guava', 'Mango', 'Mango Red', 'Papaya', 'Pineapple', 'Pineapple Mini', 'Pomogranate']
    img=image.load_img(img,target_size=(64,64))
    x=image.img_to_array(img)
    x=np.expand_dims(x,axis=0)
    pred=np.argmax(model.predict(x), axis=1)
    result=str(index[pred[0]])
    return result
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')
@app.route('/submit',methods=['POST','GET'])
def posts():
    temp='mmm'
    sources=''
    index=['Banana', 'Banana Lady Finger', 'Banana Red', 'Guava', 'Mango', 'Mango Red', 'Papaya', 'Pineapple', 'Pineapple Mini', 'Pomogranate']

    if request.method=='POST':
        image=request.files['inputfile']
        path="C:\\project\\fruit_classification\\static\\images\\"+image.filename
        image.save(path)
        temp=predict(path)
    dic={'Mango Red':'40c4589d30d04b0b230558d823b9b8b3','Banana Red':'4ae378dbb8b01e948b7477ec3d3573df','Pomogranate':'774621b077fa5ca2a9adb8791be0c789','Banana':'9ae0516f0058418c6e87c4d4a051c01d','Banana Lady Finger':'bbd7a4670c2426da8a32cc69f6d43af2','Papaya':'bbd7a4670c2426da8a32cc69f6f2b324','Guava':'cb4b81a9cc440f01bb203da2d1644a89','Pineapple Mini':'cb4b81a9cc440f01bb203da2d17028cf','Pineapple':'ea79ebc176c73a6719dce0d69d21b577','Mango':'d9d76f57c53207af1cdaebdb35b8137f'}
    #my_document =my_database['40c4589d30d04b0b230558d823b9b8b3']['name']
    name =my_database[dic[temp]]['name']
    calories =my_database[dic[temp]]['calories']
    fiber =my_database[dic[temp]]['fiber']
    carbohydrates =my_database[dic[temp]]['carbohydrates']
    Protein =my_database[dic[temp]]['Protein']
    Sugar =my_database[dic[temp]]['Sugar']
    Others=my_database[dic[temp]]['Others']
    Tips =my_database[dic[temp]]['Tips']

    

    
    
        
    return render_template('processing.html',answer=temp,filename=image.filename,name=name,calories=calories,fiber=fiber,carbohydrates=carbohydrates,Protein=Protein,Sugar=Sugar,Others=Others,Tips=Tips)

if __name__=='__main__':
    app.run(debug=True)