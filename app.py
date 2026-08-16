import streamlit as st
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

def predict(gender,age,embark,ticket_class):
    print("start prediction")
    df=pd.read_csv("titanic_train.csv")
    if gender=="male":
        gender=0
    else:
        gender=1
    if embark=="Southhampton":
        embark=0
    elif embark=="Queenstown":
        embark=1
    else:
        embark=2
    age_group = 0
    if age<21.75:
        age_group=0
    elif age <26.5:
        age_group=1
    elif age<36:
        age_group=2
    else:
        age_group=3
    df["Age1"]=df["Age"]
    df.loc[(df["Age1"].isnull()) & (df["Pclass"]==1) & (df["Sex"]=="male"),"Age1"]= df[(df["Pclass"]==1)&(df["Sex"]=="male")]["Age"].mean()
    df.loc[(df["Age1"].isnull()) & (df["Pclass"]==1) & (df["Sex"]=="female"),"Age1"]= df[(df["Pclass"]==1)&(df["Sex"]=="female")]["Age"].mean()
    df.loc[(df["Age1"].isnull()) & (df["Pclass"]==2) & (df["Sex"]=="male"),"Age1"]= df[(df["Pclass"]==2)&(df["Sex"]=="male")]["Age"].mean()
    df.loc[(df["Age1"].isnull()) & (df["Pclass"]==2) & (df["Sex"]=="female"),"Age1"]= df[(df["Pclass"]==2)&(df["Sex"]=="female")]["Age"].mean()
    df.loc[(df["Age1"].isnull()) & (df["Pclass"]==3) & (df["Sex"]=="male"),"Age1"]= df[(df["Pclass"]==3)&(df["Sex"]=="male")]["Age"].mean()
    df.loc[(df["Age1"].isnull()) & (df["Pclass"]==3) & (df["Sex"]=="female"),"Age1"]= df[(df["Pclass"]==3)&(df["Sex"]=="female")]["Age"].mean()
    df.loc[(df["Age1"]<21.75) ,"age count"]=0
    df.loc[(df["Age1"]>=21.75) & (df["Age1"]<26.5),"age count"]=1
    df.loc[(df["Age1"]>=26.5) & (df["Age1"]<36),"age count"]=2
    df.loc[(df["Age1"]>=36) ,"age count"]=3
    df["age count"]=df["age count"].astype("Int64")
    df["Embarked"]=df["Embarked"].fillna("S")
    mapping = {"S": 0, "C": 1, "Q": 2}
    df["Embarked"] = df["Embarked"].map(mapping).astype("Int64")
    mapping = {"male": 0, "female": 1}
    df["Sex"] = df["Sex"].map(mapping).astype("Int64")
    df1=df.drop(['PassengerId','Name','Age' ,'SibSp',"Parch","Ticket","Fare","Cabin","Age1"],axis=1)
    X=df1.drop("Survived",axis=1)
    y=df1["Survived"]
    X_train, X_test, y_train, y_test=train_test_split(X,y, test_size=0.2, random_state=101)
    lr=LogisticRegression()
    lr.fit(X_train, y_train)
    Survived=lr.predict([[ticket_class,gender,embark,age_group]])[0]
    print(Survived)
    if Survived==1:
        st.badge("You survived!!!")
        print("Survived")
    elif Survived==0:
        st.badge("You are DEAD", color="red")
        print("Not Survived")
    

def main():
    st.title("Titanic prediction")
    gender = st.selectbox("gender",("male","female"))
    age = st.slider("How old are you?", 0, 100, 25)
    

    
    

   

    embark = st.radio(
        "embarked location",
        ["Southhampton","Queenstown","Cherbourg"])
    
    ticket_class = st.selectbox("Ticket class",(1,2,3))
    if st.button("predict", type="primary"):
        predict(gender,age,embark,ticket_class)
    
   
    
main()