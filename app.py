import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# -------- PAGE CONFIG --------
st.set_page_config(page_title="AI Legal Notice Generator", layout="wide")

st.title("⚖️ AI Legal Notice Generator")
st.write("Generate professional legal notices instantly.")

# -------- INPUT FORM --------

case_type = st.selectbox(
    "Select Case Type",
    ["Rental Dispute", "Cheque Bounce", "Property Issue", "Payment Recovery"]
)

sender = st.text_input("Sender Name")
receiver = st.text_input("Receiver Name")

details = st.text_area("Enter Issue Details")

language = st.selectbox(
    "Select Language",
    ["English", "Tamil"]
)

# Default values (NO placeholders)
sender_address = "Thoothukudi, Tamil Nadu"
receiver_address = "Chennai, Tamil Nadu"
sender_contact = "9876543210"
receiver_contact = "9123456780"

# Auto date
current_date = datetime.now().strftime("%d-%m-%Y")

generate_btn = st.button("Generate Notice")

# -------- LLM --------

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# -------- LANGUAGE CONTROL --------

if language == "Tamil":
    lang_instruction = """
    Write the entire legal notice strictly in formal legal Tamil.
    Do NOT use conversational Tamil.
    Do NOT include any English words.
    """
else:
    lang_instruction = "Write the entire legal notice strictly in English."

# -------- PROMPT --------

prompt = ChatPromptTemplate.from_template("""
You are a professional legal expert in India.

Generate a formal legal notice using proper structure.

Details:
Case Type: {case_type}
Date: {current_date}

Sender Name: {sender}
Sender Address: {sender_address}
Sender Contact: {sender_contact}

Receiver Name: {receiver}
Receiver Address: {receiver_address}
Receiver Contact: {receiver_contact}

Issue Details:
{details}

Instructions:
- Use proper legal notice format
- Include:
  1. Sender & Receiver details
  2. Date
  3. Subject
  4. Formal legal body
  5. Clear demand
  6. Time limit (15 days)
- Do NOT include placeholders like [Insert Date], [Address]
- Do NOT include "Translation"
- Keep it professional and structured

IMPORTANT:
{lang_instruction}
""")

chain = prompt | llm | StrOutputParser()

# -------- LOGIC --------

if generate_btn:

    if not sender or not receiver or not details:
        st.warning("⚠️ Please fill all fields")

    else:
        with st.spinner("Generating legal notice..."):
            result = chain.invoke({
                "case_type": case_type,
                "sender": sender,
                "receiver": receiver,
                "details": details,
                "sender_address": sender_address,
                "receiver_address": receiver_address,
                "sender_contact": sender_contact,
                "receiver_contact": receiver_contact,
                "current_date": current_date,
                "lang_instruction": lang_instruction
            })

        st.session_state["notice"] = result

# -------- OUTPUT --------

if "notice" in st.session_state:

    st.subheader("📄 Generated Legal Notice")

    # Clean document-style formatting
    st.markdown(f"```\n{st.session_state['notice']}\n```")

    # -------- DOWNLOAD --------
    st.download_button(
        label="📥 Download Legal Notice",
        data=st.session_state["notice"],
        file_name="legal_notice.txt",
        mime="text/plain"
    )