import google.generativeai as genai


def build_answer(query: str, retrieved_chunks: list, api_key: str) -> str:
    genai.configure(api_key=api_key)
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
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"خطا در ارتباط با مدل: {str(e)}"


def summarize_document(full_text: str, api_key: str) -> str:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
    شما یک دستیار متخصص هستید. متن زیر محتوای کامل یک سند است.
    لطفاً آن را به صورت جامع، شامل نکات کلیدی و سرفصل‌های اصلی خلاصه کنید.

    متن سند:
    {full_text}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"خطا در خلاصه‌سازی: {str(e)}"