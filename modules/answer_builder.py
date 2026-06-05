import google.generativeai as genai


def build_answer(query: str, retrieved_chunks: list, api_key: str) -> str:
    """
    دریافت متن و تولید پاسخ نهایی
    """
    genai.configure(api_key=api_key)

    # concatenating chunks
    context_text = "\n\n".join([chunk['text'] for chunk in retrieved_chunks])

    # ساخت پرامپت نهایی برای مدل
    # پرامپت بهینه‌شده برای پاسخ‌های دقیق‌تر
    prompt = f"""
        شما یک دستیار متخصص پژوهشی هستید. وظیفه شما پاسخ به سوالات کاربر بر اساس «متن مرجع» ارائه شده است.
        لطفاً برای پاسخ‌دهی به نکات زیر توجه کنید:
        1. فقط و فقط از اطلاعات موجود در متن مرجع استفاده کنید.
        2. پاسخ باید رسمی، دقیق و دارای ساختار علمی باشد.
        3. اگر پاسخ در متن نیست، بنویسید: «اطلاعات موجود در مستندات برای پاسخ به این پرسش کافی نیست.»
        4. اگر سوال نیاز به توضیح فنی دارد، آن را به صورت لیست‌های شماره‌دار خلاصه کنید.

        متن مرجع:
        {context_text}

        سوال کاربر:
        {query}
        """
    try:
        # model call
        model = genai.GenerativeModel('gemini-2-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print( f"خطا در ارتباط با مدل زبانی: {str(e)}")
