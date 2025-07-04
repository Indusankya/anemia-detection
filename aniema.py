# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 04:14:20 2025

@author: indus
"""


pip install tensorflow
import pandas as pd # categorical
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


data = pd.read_csv(r"C:\Users\indus\Downloads\children anemia.csv")


columns_to_drop = [
    'Highest educational level', 
    'Wealth index combined', 
    'Have mosquito bed net for sleeping (from household questionnaire)',
    'Smokes cigarettes', 
    'Current marital status', 
    'Currently residing with husband/partner',
    'When child put to breast', 
    'Type of place of residence', 
    'Births in last five years', 
    
    
    
    
    'Age of respondent at 1st birth'
]
data.drop(columns=columns_to_drop, inplace=True)


data.dropna(inplace=True)


label_encoders = {}
for column in data.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column])
    label_encoders[column] = le



X = data.drop('Anemia level', axis=1)  
y = data['Anemia level']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)


y_pred = model.predict(X_test)


accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

print(classification_report(y_test, y_pred))



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)


y_pred = model.predict(X_test)


accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

print(classification_report(y_test, y_pred))



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)


model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)


y_pred = model.predict(X_test)


accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

print(classification_report(y_test, y_pred))

# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['Not Anemic', 'Anemic'], yticklabels=['Not Anemic', 'Anemic'])
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.title('Confusion Matrix')
plt.show()

# Data Visualization
plt.figure(figsize=(10, 6))
sns.countplot(data=data, x='Anemia level')
plt.title('Distribution of Anemia Levels')
plt.xlabel('Anemia Level')
plt.ylabel('Count')
plt.show()


importances = model.feature_importances_
feature_names = X.columns
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(10, 6))
plt.title("Feature Importances")
plt.bar(range(X.shape[1]), importances[indices], align="center")
plt.xticks(range(X.shape[1]), feature_names[indices], rotation=90)
plt.xlim([-1, X.shape[1]])
plt.show()


plt.figure(figsize=(8, 8))
data['Anemia level'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
plt.title('Distribution of Anemia Levels')
plt.ylabel('')  
plt.show()

mobilenet_model = MobileNetV2(weights='imagenet')

def load_and_preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))  # Resize image to 224x224
    img_array = image.img_to_array(img)  # Convert image to array
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = preprocess_input(img_array)  # Preprocess the image
    return img_array


img_path = r'C:\Users\indus\Downloads\anemia.jpg' 


img_array = load_and_preprocess_image(img_path)


predictions = model.predict(img_array)

decoded_predictions = decode_predictions(predictions, top=3)[0]


print("Predictions:")
for i, (imagenet_id, label, score) in enumerate(decoded_predictions):
    print(f"{i + 1}: {label} ({score:.2f})")


plt.imshow(image.load_img(img_path))
plt.axis('off')
plt.show()

