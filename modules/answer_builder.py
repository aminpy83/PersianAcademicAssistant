import google.generativeai as genai
import requests


def _call_llm(provider: str, model_name: str, api_key: str, prompt: str, default_model: str) -> str:
    """
    تابع مرکزی و هوشمند برای مدیریت درخواست‌ها به سرویس‌دهنده‌های مختلف
    """
    # ۱. حالت گوگل جمنای
    if provider == "Gemini":
        try:
            genai.configure(api_key=api_key)
            selected_model = model_name if model_name else default_model
            model = genai.GenerativeModel(selected_model)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"خطا در ارتباط با جمنای: {str(e)}"

    # ۲. حالت مدل‌های محلی اولاما (Ollama)
    elif provider == "Ollama (Local)":
        selected_model = model_name if model_name else "llama3"
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": selected_model,
            "prompt": prompt,
            "stream": False
        }
        try:
            res = requests.post(url, json=payload, timeout=90)
            return res.json().get("response", "خطا در دریافت پاسخ از اولاما")
        except Exception as e:
            return f"❌ خطا: آیا Ollama روی سیستم شما در حال اجراست؟ نسخه خطا: {str(e)}"

    # (OpenRouter)
    elif provider == "OpenRouter":
        selected_model = model_name if model_name else "openai/gpt-oss-120b:free"
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": selected_model,
            "messages": [{"role": "user", "content": prompt}]
        }
        try:
            res = requests.post(url, json=payload, headers=headers, timeout=90)
            if res.status_code == 200:
                return res.json()['choices'][0]['message']['content']
            else:
                return f"خطا از OpenRouter (کد {res.status_code}): {res.text}"
        except Exception as e:
            return f"خطا در ارتباط با OpenRouter: {str(e)}"

    return "سرویس‌دهنده انتخاب شده معتبر نیست."


def build_answer(query: str, retrieved_chunks: list, provider: str, model_name: str, api_key: str) -> str:
    context_text = "\n\n".join([chunk['text'] for chunk in retrieved_chunks])

    prompt = f"""
    شما یک دستیار متخصص پژوهشی هستید. با استفاده از «اطلاعات مرجع» زیر، به «سوال» کاربر پاسخ دقیق و علمی بدهید.
    - فقط از اطلاعات متن استفاده کنید.
    - پاسخ را به صورت لیست‌بندی شده و ساختاریافته بنویسید.
    - اگر اطلاعات کافی نیست، اعلام کنید.

    اطلاعات مرجع:
    {context_text}

    سوال کاربر:
    {query}
    """
    return _call_llm(provider, model_name, api_key, prompt, default_model='gemini-2.5-flash')


def summarize_document(full_text: str, provider: str, model_name: str, api_key: str) -> str:
    prompt = f"""
    شما یک دستیار متخصص هستید. متن زیر محتوای کامل یک سند است.
    لطفاً آن را به صورت جامع، شامل نکات کلیدی و سرفصل‌های اصلی خلاصه کنید.

    متن سند:
    {full_text}
    """
    return _call_llm(provider, model_name, api_key, prompt, default_model='gemini-2.5-flash')
