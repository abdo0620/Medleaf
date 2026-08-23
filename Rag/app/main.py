import streamlit as st

Home=st.Page("pages/app.py",title="Talk To Mia", icon="🩺")
Upload=st.Page("pages/Upload_docs.py",title="Upload Your Documents",icon="📃")
about=st.Page("pages/About_me.py",title="About me",icon="🌿")

pg=st.navigation([Home,Upload,about])
pg.run()

