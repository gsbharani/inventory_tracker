import streamlit as st
from db import get_connection

try:
    conn = get_connection()
    st.success("Connected to Supabase!")
except Exception as e:
    st.error(f"Connection failed: {e}")
