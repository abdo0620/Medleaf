import streamlit as st
from pathlib import Path
from Rag import initialize_db
st.set_page_config(page_title="MedLeaf", page_icon="app/assets/images/Gemini_Generated_Image_8yo9v28yo9v28yo9.png", layout="centered")
st.logo("app/assets/images/Gemini_Generated_Image_pjw0i6pjw0i6pjw0.png",size="large")


st.title("Upload Your Documents",text_alignment="center")
uploaded_files = st.file_uploader(
    "Drop your leaflets here",
    type=["pdf", "txt"],
    accept_multiple_files=True,
    label_visibility="collapsed",
)


if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} file(s) ready to add")
    for f in uploaded_files:
        st.markdown(f"- **{f.name}** ({f.size / 1024:.1f} KB)")

    st.divider()

    if st.button("➕ Add to Mia's Database", use_container_width=True):
        with st.spinner("Processing, chunking, and embedding documents... Feel free to check out the 'About Me' section! 😊"):
                saved_paths = []
                tmp_dir = Path("files/documents_injected")
                for f in uploaded_files:
                    file_path = tmp_dir / f.name
                    saved_paths.append(str(file_path))
                    if f.name[-4:].lower()==".pdf":
                         file_path.write_bytes(f.getvalue())

                    if f.name[-4:].lower()==".txt":

                         text=f.getvalue().decode("utf-8")
                         file_path.write_text(text, encoding="utf-8")


                initialize_db.add_vector_db()
        st.success("Documents Uploaded Successfully")


  




else:
    st.info("No files uploaded yet.")



