import streamlit as st
from pymongo import MongoClient

@st.cache_resource
def connect_to_db():
    uri = st.secrets["mongo"]["uri"]
    client = MongoClient(uri)
    db = client.ptg
    return db

def add_data_to_collection(collection_name, data):
    db = connect_to_db()
    collection = db[collection_name]
    result = collection.insert_one(data)
    return result.inserted_id

def get_collection(collection_name):
    db = connect_to_db()
    collection = db[collection_name]
    return collection