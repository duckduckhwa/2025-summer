import streamlit as st
import google.generativeai as genai
import fitz
import os

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def get_gemini_summary(text, model_name="models/gemini-2.5-flash"):
    model = genai.GenerativeModel(model_name)
    prompt = f"다음 텍스트를 핵심 내용 위주로 명확하고 간결하게 한국어로 요약해줘.\n\n{text}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"요약 중 오류가 발생했습니다: {e}"
        
def get_gemini_translation(text, lang, model_name="models/gemini-2.5-flash"):
    model = genai.GenerativeModel(model_name)

    if lang == "English":
        prompt = f"Translate the following text into English:\n\n{text}"
    elif lang == "日本語":
        prompt = f"以下のテキストを日本語に翻訳してください:\n\n{text}"
    else:
        prompt = f"Translate the following text:\n\n{text}"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"번역 중 오류가 발생했습니다: {e}"

st.title("PDF 요약 및 번역 서비스 📄")
st.markdown("---")

api_key = st.text_input("여기에 Gemini API 키를 입력하세요:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    st.success("API 키가 성공적으로 설정되었습니다!")

    st.header("1. PDF 파일 업로드")
    uploaded_file = st.file_uploader("여기에 PDF 파일을 드래그하거나 클릭하여 업로드하세요.", type=["pdf"])

    if uploaded_file is not None:
        st.success(f"'{uploaded_file.name}' 파일이 성공적으로 업로드되었습니다.")
        
        st.header("2. 기능 선택")
        
        if st.button("문서 요약 (한국어)"):
            with st.spinner("문서 요약 중..."):
                extracted_text = extract_text_from_pdf(uploaded_file)
                summary_text = get_gemini_summary(extracted_text)
            
            st.subheader("💡 요약 결과")
            st.info("요약이 완료되었습니다.")
            st.write(summary_text)

        st.markdown("---")
        translation_lang = st.selectbox(
            "번역할 언어를 선택하세요:",
            ("English", "日本語")
        )
        if st.button("문서 번역 시작"):
            with st.spinner("문서 번역 중..."):
                extracted_text = extract_text_from_pdf(uploaded_file)
                translation_text = get_gemini_translation(extracted_text, translation_lang)
            
            st.subheader("💡 번역 결과")
            st.info(f"{translation_lang} 번역이 완료되었습니다.")
            st.write(translation_text)
else:
    st.info("시작하려면 Gemini API 키를 입력하세요.")
