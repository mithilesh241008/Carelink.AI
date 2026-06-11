import streamlit as st

st.title("CareLink AI v2")

name = st.text_input("Enter your name")

if name:
    st.write(f"Hello {name}")