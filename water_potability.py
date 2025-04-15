import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import pickle

df= pd.read_csv('C:\\Users\\punee\\OneDrive\\Desktop\\IBM-HACK\\water_potability.csv')
df.head()

df.describe()   #statistics
df.duplicated().any()
#fill null values with mean
df['ph']=df['ph'].fillna(df['ph'].mean())
df['Trihalomethanes']=df['Trihalomethanes'].fillna(df['Trihalomethanes'].mean())
df['Sulfate']=df['Sulfate'].fillna(df['Sulfate'].mean())

df.isnull().sum()
corr_matrix=df.corr()
corr_matrix

plt.figure(figsize=(18,16))
sns.heatmap(corr_matrix,annot=True,cmap='coolwarm')

corr_matrix1=corr_matrix.abs()
upper_tri=corr_matrix1.where(np.triu(np.ones(corr_matrix1.shape),k=1).astype(np.bool_))

#diff btw columns and target
for col in df.columns:
  sns.histplot(data=df,x=col,hue='Potability',kde=True)
 
sns.countplot(df['Potability'])
df['Potability'].value_counts()

corr_matrix = df.corr()

# Extracting the correlation values for potability
potability_corr = corr_matrix['Potability'].drop('Potability')  # Exclude self-correlation

# Finding the feature with the highest correlation with potability
highest_corr_feature = potability_corr.abs()  # Get the feature name with the highest absolute correlation
# highest_corr_value = potability_corr[highest_corr_feature]  # Get the correlation value

print("Feature with the highest correlation with potability:")
print(f"{highest_corr_feature}: {highest_corr_feature}")

x=df.drop('Potability',axis=1)
y=df['Potability']

x.head()
y.head()

from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
x_scaled=sc.fit_transform(x)

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42,stratify=y)

x_train.shape, x_test.shape

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostClassifier

LR=LogisticRegression()
SVM=SVC()
KNN=KNeighborsClassifier()
DT=DecisionTreeClassifier()
RF=RandomForestClassifier()
ETC=ExtraTreesClassifier()
GBC=GradientBoostingClassifier()
NB=GaussianNB()
ABC=AdaBoostClassifier()

from sklearn.model_selection import cross_val_score

models=[LR,SVM,KNN,DT,RF,ETC,GBC,NB,ABC]
features=x_scaled
labels=y
cv=5
accu_list=[]
ModelName=[]

for model in models:
  model_name=model.__class__.__name__
  accuracies=cross_val_score(model,features,labels,cv=cv, scoring='accuracy')
  accu_list.append(accuracies.mean()*100)
  ModelName.append(model_name)

model_acc_df=pd.DataFrame({'Model':ModelName,'Cross_Val_Accuracy':accu_list})
model_acc_df

SVM.fit(x_train,y_train)
ETC.fit(x_train,y_train)
RF.fit(x_train,y_train)
y_pred_SVM=SVM.predict(x_test)
y_pred_ETC=ETC.predict(x_test)
y_pred_RF=RF.predict(x_test)

from sklearn.metrics import classification_report
print(classification_report(y_test,y_pred_SVM))
print(classification_report(y_test,y_pred_RF))
print(classification_report(y_test,y_pred_ETC))

from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.model_selection import StratifiedKFold

params_RF={"min_samples_split":[2, 6],
           "min_samples_leaf":[1, 4],
           "n_estimators":[100, 200, 300],
           "criterion":["gini", "entropy"]
           }

cv_method=StratifiedKFold(n_splits=3)
GridSearchCV_RF=GridSearchCV(estimator=RandomForestClassifier(),
                             param_grid=params_RF,
                             cv=cv_method,
                             verbose=1,
                             n_jobs=2,
                             scoring="accuracy",
                             return_train_score=True
                             )

GridSearchCV_RF.fit(x_train,y_train)
best_params_RF=GridSearchCV_RF.best_params_
print("Best Hyperparameters for Random Forest are = ",best_params_RF)

from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier

# Define the parameter grid for Random Forest
params_RF = {
    "min_samples_split": [2, 6],
    "min_samples_leaf": [1, 4],
    "n_estimators": [100, 200, 300],
    "criterion": ["gini", "entropy"]
}

# Define the cross-validation method
cv_method = StratifiedKFold(n_splits=3)

# Set up the GridSearchCV
GridSearchCV_RF = GridSearchCV(
    estimator=RandomForestClassifier(),
    param_grid=params_RF,
    cv=cv_method,
    verbose=1,
    n_jobs=2,
    scoring="accuracy",
    return_train_score=True
)

# Fit the GridSearchCV on the training data
GridSearchCV_RF.fit(x_train, y_train)

# Get the best hyperparameters
best_params_RF = GridSearchCV_RF.best_params_
print("Best Hyperparameters for Random Forest are =", best_params_RF)

# Access the best estimator from GridSearchCV
best_rf = GridSearchCV_RF.best_estimator_

# Ensure that df.x_train.columns (or df.columns if you're using the entire dataframe) contains the feature names
feature_names = df.columns  # Adjust this if your feature names are stored differently

# Print the feature importances
for score, name in zip(best_rf.feature_importances_, feature_names):
    print(name, round(score, 2))

GridSearchCV_RF.score(x_test,y_test)

best_estimator = GridSearchCV_RF.best_estimator_
best_estimator

best_estimator = GridSearchCV_RF.best_estimator_
best_estimator.fit(x_train, y_train)
y_pred_best = best_estimator.predict(x_test)
print(classification_report(y_test, y_pred_best))

from sklearn.metrics import accuracy_score
print(f"Accuracy of Random Forest Model ={round(accuracy_score(y_test, y_pred_best)*100,2)}%")

df.columns

list1=df.iloc[2:3, 0:9].values.flatten().tolist()
list1

ph = float(input('Enter the Ph Value = '))
Hardness = float(input('Enter the Hardness Value = '))
Solids = float(input('Enter the Solids Value = '))
Chloramines = float(input('Enter the Chloramines Value = '))
Sulfate = float(input('Enter the Sulfate Value = '))
Conductivity = float(input('Enter the Conductivity Value = '))
Organic_carbon = float(input('Enter the Organic_carbon Value = '))
Trihalomethanes = float(input('Enter the Trihalomethanes Value = '))
Turbidity = float(input('Enter the Turbidity Value = '))

input_data = [ph,Hardness,Solids,Chloramines,Sulfate,Conductivity,Organic_carbon,Trihalomethanes,Turbidity]

from sklearn.preprocessing import StandardScaler
std_scalar = StandardScaler()

std_scalar.fit(x_train,y_train)

water_data_input=std_scalar.transform([[ph,Hardness,Solids,Chloramines,Sulfate,Conductivity,Organic_carbon,Trihalomethanes,Turbidity]])
water_data_input

model_prediction = best_estimator.predict(water_data_input)
print(model_prediction)

if model_prediction == 0:
  print('Water is not safe for Consumption')
else:
  print('Water is Potable, Safe for Consumption')
  
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score


# Training the model with best hyperparameters
GridSearchCV_RF.fit(x_train, y_train)
best_params_RF = GridSearchCV_RF.best_params_
best_estimator = GridSearchCV_RF.best_estimator_

# Define WQI categories (adjust ranges and labels based on your chosen WQI formula)
wqi_categories = {
    "Excellent": (90, 100),
    "Good": (70, 89),
    "Fair": (50, 69),
    "Poor": (0, 49)
}

# Assuming best_estimator is your trained classification model (from previous code)
# Assuming user_data is a list containing preprocessed water quality parameters

# Predict the class label (assuming "safe" or "unsafe") using the existing model
# Reshape the input to 2D: (samples, features)
predicted_class = best_estimator.predict(water_data_input.reshape(1, -1))[0]

# Find the corresponding WQI category based on predicted class (modify logic if needed)
if predicted_class == "Safe":  # Assuming "Safe" corresponds to higher WQI
    for category, (lower_bound, upper_bound) in wqi_categories.items():
        if predicted_class == "Safe" and lower_bound <= 100:  # Assuming all safe values fall within WQI range
            wqi_category = category
            break
else:
    wqi_category = "Poor"  # Assuming "Unsafe" implies poor water quality

# Interpretation
print(f"Predicted WQI Category: {wqi_category}")
print(f"WQI Range for {wqi_category}: {wqi_categories[wqi_category][0]} - {wqi_categories[wqi_category][1]}")

import random
import string
import numpy as np

sentence=input(print('Enter the sentence : '))

# sentence = "There present an average ph value, water has high hardness, contains average solids and low chloramines and low sulphur which has high conductivity. The water has average turbidity due to presence of moderate organic_carbon molecules. Predict the Potability."

# Remove punctuation for better word matching
translator = str.maketrans('', '', string.punctuation)
sentence = sentence.translate(translator)

# Split the sentence into words
ws = sentence.split()

# Initialize variables
phb = pha = hardb = harda = solb = sona = clb = cla = sbf = sfa = conb = cona = ocb = oca = thb = tha = turb = tuba = None

for i in range(len(ws)):
    if ws[i] == 'ph':
        phb = ws[i-1]
        if i + 2 < len(ws):
            pha = ws[i+2]

    if ws[i] == 'hardness':
        hardb = ws[i-1]
        if i + 2 < len(ws):
            harda = ws[i+2]

    if ws[i] == 'solids':
        solb = ws[i-1]
        if i + 2 < len(ws):
            sona = ws[i+2]

    if ws[i] == 'chloramines':
        clb = ws[i-1]
        if i + 2 < len(ws):
            cla = ws[i+2]

    if ws[i] == 'sulfate':
        sbf = ws[i-1]
        if i + 2 < len(ws):
            sfa = ws[i+2]

    if ws[i] == 'conductivity':
        conb = ws[i-1]
        if i + 2 < len(ws):
            cona = ws[i+2]

    if ws[i] == 'organic_carbon':
        ocb = ws[i-1]
        if i + 2 < len(ws):
            oca = ws[i+2]

    if ws[i] == 'trihalomethanes':
        thb = ws[i-1]
        if i + 2 < len(ws):
            tha = ws[i+2]

    if ws[i] == 'turbidity':
        turb = ws[i-1]
        if i + 2 < len(ws):
            tuba = ws[i+2]

if phb == "high":
    ph = random.uniform(8.6, 14)
elif phb == "moderate" or phb == "average":
    ph = random.uniform(6, 9)
elif phb == "low":
    ph = random.uniform(0, 7.4)
elif pha == "high":
    ph = random.uniform(8.6, 14)
elif pha == "moderate" or pha == "average":
    ph = random.uniform(6.5, 9.5)
elif pha == "low":
    ph = random.uniform(0, 7.4)
else:
    ph = np.mean([ph])

if hardb == "high":
    Hardness = random.uniform(197, 324)
elif hardb == "moderate" or hardb == "average":
    Hardness = random.uniform(47.3, 197)
elif hardb == "low":
    Hardness = random.uniform(0, 47.3)
elif harda == "high":
    Hardness = random.uniform(197, 324)
elif harda == "moderate" or harda == "average":
    Hardness = random.uniform(47.3, 197)
elif harda == "low":
    Hardness = random.uniform(0, 47.3)
else:
    Hardness = np.mean([Hardness])

if solb == "high":
    Solids = random.uniform(20928, 61226.196)
elif solb == "moderate" or hardb == "average":
    Solids = random.uniform(320, 20929)
elif solb == "low":
    Solids = random.uniform(0, 321)
elif sona == "high":
    Solids = random.uniform(20928, 61226.196)
elif sona == "moderate" or harda == "average":
    Solids = random.uniform(320, 20929)
elif sona == "low":
    Solids = random.uniform(0, 321)
else:
    Solids = np.mean([Solids])

if clb == "high":
    Chloramines = random.uniform(7.13, 14.13)
elif clb == "moderate" or hardb == "average":
    Chloramines = random.uniform(0.352, 7.13)
elif clb == "low":
    Chloramines = random.uniform(0, 0.353)
elif cla == "high":
    Chloramines = random.uniform(7.13, 14.13)
elif cla == "moderate" or harda == "average":
    Chloramines = random.uniform(0.352, 7.13)
elif cla == "low":
    Chloramines = random.uniform(0, 0.353)
else:
    Chloramines	 = np.mean([Chloramines])

if sbf == "high":
    Sulfate = random.uniform(334, 482)
elif sbf == "moderate" or hardb == "average":
    Sulfate = random.uniform(129, 335)
elif sbf == "low":
    Sulfate = random.uniform(0, 130)
elif sfa == "high":
    Sulfate = random.uniform(334, 482)
elif sfa == "moderate" or harda == "average":
    Sulfate = random.uniform(129, 335)
elif sfa == "low":
    Sulfate = random.uniform(0, 130)
else:
    Sulfate	 = np.mean([Sulfate])

if conb == "high":
    Conductivity = random.uniform(421.88, 754.34)
elif conb == "moderate" or hardb == "average":
    Conductivity = random.uniform(181.48, 422.88)
elif conb == "low":
    Conductivity = random.uniform(0, 182.48)
elif cona == "high":
    Conductivity = random.uniform(421.88, 754.34)
elif cona == "moderate" or harda == "average":
    Conductivity = random.uniform(181.48, 422.88)
elif cona == "low":
    Conductivity = random.uniform(0, 182.48)
else:
    Conductivity = np.mean([Conductivity])

if ocb == "high":
    Organic_carbon = random.uniform(14.21, 29.30)
elif ocb == "moderate" or hardb == "average":
    Organic_carbon = random.uniform(2.20, 15.21)
elif ocb == "low":
    Organic_carbon = random.uniform(0, 3.20)
elif oca == "high":
    Organic_carbon = random.uniform(14.21, 29.30)
elif oca == "moderate" or harda == "average":
    Organic_carbon = random.uniform(2.20, 15.21)
elif oca == "low":
    Organic_carbon = random.uniform(0, 3.20)
else:
    Organic_carbon = np.mean([Organic_carbon])

if thb == "high":
    Trihalomethanes = random.uniform(66.39, 254)
elif thb == "moderate" or hardb == "average":
    Trihalomethanes = random.uniform(0.738, 67.39)
elif thb == "low":
    Trihalomethanes = random.uniform(0, 0.738)
elif tha == "high":
    Trihalomethanes = random.uniform(66.39, 254)
elif tha == "moderate" or harda == "average":
    Trihalomethanes = random.uniform(0.738, 67.39)
elif tha == "low":
    Trihalomethanes = random.uniform(0, 0.738)
else:
    Trihalomethanes = np.mean([Trihalomethanes])

if turb == "high":
    Turbidity = random.uniform(3.955, 7.739)
elif turb == "moderate" or hardb == "average":
    Turbidity = random.uniform(1.45, 4.955)
elif turb == "low":
    Turbidity = random.uniform(0, 2.45)
elif tuba == "high":
    Turbidity = random.uniform(3.955, 7.739)
elif tuba == "moderate" or harda == "average":
    Turbidity = random.uniform(1.45, 4.955)
elif tuba == "low":
    Turbidity = random.uniform(0, 2.45)
else:
    Turbidity = np.mean([Turbidity])

input_data = [ph, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic_carbon, Trihalomethanes, Turbidity]

std_scalar = StandardScaler()
std_scalar.fit(x_train, y_train)
water_data_input = std_scalar.transform([[ph, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic_carbon, Trihalomethanes, Turbidity]])

# Prediction with probability
model_prediction_proba = best_estimator.predict_proba(water_data_input)

# Assuming positive class (index 1) represents safe water
safe_water_proba = model_prediction_proba[0][1]  # Probability of class 1 (safe)

print(f"Probability of water being safe for consumption: {safe_water_proba:.2f}")

# Interpretation (modify based on your model's interpretation of classes)
if safe_water_proba > 0.8:
    print("Water is likely safe for consumption.")
elif safe_water_proba > 0.5:
    print("Water might be safe for consumption, but consider further testing.")
else:
    print("Water is likely unsafe for consumption. Recommend further testing.")

from sklearn.feature_selection import RFE
rfe = RFE(best_estimator, n_features_to_select=2)
rfe.fit(x_train, y_train)
ranking = rfe.ranking_


lst=[ph, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic_carbon, Trihalomethanes, Turbidity]
for i in range(len(ranking)):
  if ranking[i]>3:
    lst[i]=0
water_data_input = std_scalar.transform([lst])

# Prediction with probability
model_prediction_proba = best_estimator.predict_proba(water_data_input)

# Assuming positive class (index 1) represents safe water
safe_water_proba = model_prediction_proba[0][1]  # Probability of class 1 (safe)

print(f"Probability of water being safe for consumption: {safe_water_proba:.2f}")
rfe.predict(water_data_input)
ranking = rfe.ranking_
features_affecting=list()
for i in range(len(list(ranking))):
  if int(ranking[i])<3:
    features_affecting.append(df.columns[i]+",")
print("Features causing water issue:",str(features_affecting))  


pickle.dump(best_estimator, open('model.pkl', 'wb'))