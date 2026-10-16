import streamlit as st
from groq import Groq

# إعدادات الصفحة
st.set_page_config(
    page_title="أنـس AI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 وكيل أنس الذكي")
st.caption("مدعوم بقوة وسرعة Groq ⚡")

# القائمة الجانبية للإعدادات
with st.sidebar:
    st.header("⚙️ الإعدادات")
    api_key = st.text_input("أدخل مفتاح Groq API:", type="password")
    
    model_choice = st.selectbox(
        "اختر نموذج الذكاء الاصطناعي:",
        [
            "llama-3.3-70b-versatile",
            "llama-3.2-11b-vision-preview",
            "mixtral-8x7b-32768"
        ]
    )
    st.markdown("---")
    st.markdown("💡 **تنبيه:** يحفظ الوكيل سياق المحادثة أثناء الجلسة.")

if not api_key:
    st.info("👋 مرحباً بك! يرجى إدخال مفتاح Groq API في القائمة الجانبية للبدء.")
    st.stop()

# تهيئة العميل
client = Groq(api_key=api_key)

# ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال المستخدم
if prompt := st.chat_input("اسأل وكيلك الذكي أي شيء..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            messages_payload = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
            
            chat_completion = client.chat.completions.create(
                model=model_choice,
                messages=messages_payload,
                temperature=0.7,
                max_tokens=2048,
            )
            
            full_response = chat_completion.choices[0].message.content
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            full_response = f"⚠️ حدث خطأ: {e}"
            message_placeholder.error(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
