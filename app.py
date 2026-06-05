import streamlit as st
import numpy as np
import os
from modules.pdf_loader import extract_text
from modules.text_cleaner import cleaner
from modules.chunker import splitter
from modules.embedding import get_embedding
from modules.vector_store import build_index
from modules.retriver import retrieve
from modules.answer_builder import build_answer

# تنظیمات اولیه صفحه سایت
st.set_page_config(page_title="pdf assistant", page_icon="📚")
st.title("📚 pdf Q&A")
st.write("choose your pdf and upload it")

# دریافت کلید API از کاربر در سایدبار
api_key = st.sidebar.text_input(" write down the api-key here:", type="password")

# بخش آپلود فایل
uploaded_file = st.file_uploader("UPLOAD PDF", type=["pdf"])

if uploaded_file and api_key:
    # ذخیره موقت فایل آپلود شده برای پردازش
    temp_path = "temp_uploaded.pdf"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # پردازش فایل (فقط یک بار انجام می‌شود)
    if 'index' not in st.session_state:
        with st.spinner("reading (قراره طول بکشه)"):
            pdf = extract_text(temp_path)
            all_chunks = []
            all_vectors = []
            chunk_id = 1

            for page in pdf:
                normals = cleaner(page['text'])
                chunks, chunk_id = splitter(normals, page['page_number'], chunk_id)

                for chunk in chunks:
                    # vectorization for every chunks
                    vector = get_embedding(chunk['text']).astype("float32")
                    chunk['embedding'] = vector
                    all_chunks.append(chunk)
                    all_vectors.append(vector)

            all_vectors = np.array(all_vectors, dtype="float32")

            # ذخیره متغیرها در session_state برای جلوگیری از پردازش مجدد با هر بار سوال پرسیدن
            st.session_state['index'] = build_index(all_vectors)
            st.session_state['all_chunks'] = all_chunks

            st.success("فایل با موفقیت پردازش شد! حالا می‌توانید سوال بپرسید.")
            os.remove(temp_path)  # حذف فایل موقت

    # question input
    query = st.text_input("❓ سوال خود را بپرسید")

    if query:
        with st.spinner("در حال جستجو و تولید پاسخ..."):
            # retrieving results using vector_store.py, embedding.py and retriver.py
            results = retrieve(
                query=query,
                index=st.session_state['index'],
                chunks=st.session_state['all_chunks'],
                k=3  # most related top 3
            )

            # ۲. ساخت پاسخ نهایی
            answer = build_answer(query, results, api_key)

            st.markdown("### 💡 پاسخ")
            st.info(answer)

            # show selected chunks
            with st.expander("🔍 مشاهده منابع بازیابی شده (Context)"):
                for idx, res in enumerate(results):
                    st.markdown(f"**صفحه {res['page_number']} (قطعه {idx + 1}):**\n {res['text']}")
                    st.divider()

elif not api_key:
    st.warning("before anything insert your api-key on the left sidebar")
