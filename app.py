import streamlit as st
import numpy as np
import os
import uuid
from modules.pdf_loader import extract_text
from modules.text_cleaner import cleaner
from modules.chunker import splitter
from modules.embedding import get_embedding
from modules.vector_store import build_index
from modules.retriver import retrieve
from modules.answer_builder import build_answer, summarize_document

# ۱. تنظیمات صفحه (حالت عریض برای نمایش بهتر)
st.set_page_config(page_title="M.Amin P.Yeganeh", page_icon="🎓", layout="wide")

# RTL texts
st.markdown("""
    <style>
        * { font-family: Tahoma, 'Segoe UI', sans-serif; }
        p, h1, h2, h3, h4, h5, h6, li, .stMarkdown, .st-chat-message {
            text-align: right !important;
            direction: rtl !important;
        }
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# header
st.markdown("<h1>🎓 دستیار هوشمند و تحلیلگر اسناد</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='color: gray; font-size: 14px;'>فایل خود را آپلود کنید و با استفاده از هوش مصنوعی محتوای آن را تحلیل کنید.</p>",
    unsafe_allow_html=True)
st.divider()

# sidebar
with st.sidebar:
    st.header("⚙️ تنظیمات سیستم")

    # model provider
    provider = st.selectbox(
        "🌐 انتخاب سرویس‌دهنده هوش مصنوعی:",
        ["Gemini", "Ollama (Local models)", "OpenRouter"]
    )

    model_name = ""
    api_key = ""

    # options
    if provider == "Gemini":
        model_name = st.text_input("🤖 نام مدل جمنای:", value="gemini-2.5-flash")
        api_key = st.text_input("google 🔑 API-key: ", type="password")

    elif provider == "Ollama (Local)":
        model_name = st.text_input("🤖 نام مدل لوکال:", value="llama3")
        st.info("💡 مطمئن شوید نرم‌افزار Ollama روی سیستم شما در حال اجراست.")

    elif provider == "OpenRouter":
        model_name = st.text_input("🤖 نام مدل اوپن‌راوتر:", value="meta-llama/llama-3-8b-instruct:free")
        api_key = st.text_input("🔑 openrouter API-key: ", type="password")

    st.divider()

    if st.button("🗑️ پاکسازی و شروع مجدد", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.divider()
    st.markdown("💡 **راهنما:** ابتدا سرویس‌دهنده و تنظیمات را مشخص کرده، سپس فایل خود را آپلود کنید.")

# api check
if provider in ["Gemini", "OpenRouter"] and not api_key:
    st.info(f"👈 برای شروع، لطفاً API-key مربوط به {provider} را در منوی سمت چپ وارد کنید.")
    st.stop()

col1, col2 = st.columns([2, 1])

# upload
uploaded_file = st.file_uploader("📄 آپلود فایل PDF", type=["pdf"])

if uploaded_file is None:
    st.info("💡 منتظر آپلود فایل... لطفاً یک سند PDF انتخاب کنید.")
elif 'index' in st.session_state:
    st.success("✅ پردازش تمام شد! فایل شما آماده پرسش و پاسخ است.")

# writing file
if uploaded_file and 'index' not in st.session_state:
    temp_path = f"temp_{uuid.uuid4().hex}.pdf"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # showing states
    with st.status("در حال تحلیل و پردازش سند...", expanded=True) as status:
        st.write("🔍 استخراج متن از صفحات...")
        pdf = extract_text(temp_path)

        st.write("✂️ قطعه‌بندی و پاکسازی داده‌ها...")
        all_chunks = []
        all_vectors = []
        full_text_list = []
        chunk_id = 1

        for page in pdf:
            full_text_list.append(page['text'])
            normals = cleaner(page['text'])
            chunks, chunk_id = splitter(normals, page['page_number'], chunk_id)

            for chunk in chunks:
                vector = get_embedding(chunk['text']).astype("float32")
                chunk['embedding'] = vector
                all_chunks.append(chunk)
                all_vectors.append(vector)

        st.write("🧠 در حال ساخت پایگاه دانش...")
        st.session_state['index'] = build_index(np.array(all_vectors, dtype="float32"))
        st.session_state['all_chunks'] = all_chunks
        st.session_state['full_text'] = "\n".join(full_text_list)

        status.update(label="پردازش با موفقیت انجام شد!", state="complete", expanded=False)
        if os.path.exists(temp_path): os.remove(temp_path)

# chat & summarize
if 'index' in st.session_state:
    st.divider()
    tab_chat, tab_summary = st.tabs(["💬 گفتگوی هوشمند (Q&A)", "📝 خلاصه مدیریتی"])

    with tab_chat:
        # history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # last message
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("سوال خود را از متن فایل بپرسید..."):

            # answer
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            # generator
            with st.chat_message("assistant"):
                with st.spinner("در حال بررسی منابع..."):
                    results = retrieve(prompt, st.session_state['index'], st.session_state['all_chunks'], k=3)
                    # فراخوانی تابع با آرگومان‌های جدید
                    answer = build_answer(prompt, results, provider, model_name, api_key)
                    st.markdown(answer)

                    with st.expander("🔍 مشاهده منابع ارجاعی"):
                        for i, res in enumerate(results):
                            st.caption(f"صفحه {res['page_number']}: {res['text'][:150]}...")

            # save history
            st.session_state.messages.append({"role": "assistant", "content": answer})

    with tab_summary:
        st.info("این عملیات کل محتوای فایل را مطالعه کرده و یک چکیده ساختاریافته ارائه می‌دهد.")
        # استفاده از دکمه primary برای جلب توجه بیشتر
        if st.button("🚀 تولید خلاصه سند", type="primary"):
            with st.spinner("در حال پردازش کل متن (ممکن است کمی طول بکشد)..."):
                # فراخوانی تابع خلاصه ساز با آرگومان‌های جدید سرویس‌دهنده
                summary = summarize_document(st.session_state['full_text'], provider, model_name, api_key)
                st.markdown("---")
                st.markdown(summary)