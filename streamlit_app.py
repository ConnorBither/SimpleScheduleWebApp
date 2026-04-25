import streamlit as st
from openai import OpenAI
from st_chat_message import message
import keys
client = OpenAI(
    api_key = keys.key
)
st.title("AI Schedule Aide")
col1, col2 = st.columns(2)
with col1:
    unavailable = st.text_input("Busy Hours(e.g., School)")
with col2:
    sleeps = st.text_input("Sleep Hours:")

system_prompt = f"""
You are a scheduling aide. Your job is to help the user organize their tasks over the next week.

Rules:
- The user is unavailable from {unavailable}. Do NOT schedule anything during these times.
- The user sleeps from {sleeps}. Do NOT schedule anything during sleep unless absolutely critical.
- Always include unavailable and sleep blocks in each day's schedule so the user can see them.

You MUST respond with the follwing format, keep everthing on seperate lines so it is easy to read and replace the UNAVAILABLE TIME and SLEEP TIME with what times the user is unavailable and sleeping:

message: A SHORT FRIENDLY SUMMARY OR RESPONSE TO THE USER
Monday:
    Tasks: [INSERT THE TASKS FOR MONDAY WITH THE TIME : "HH:MM AM/PM, TASK NAME, AND THEN OPTIONAL NOTES]
    Busy: UNAVAILABLE TIME
    Sleep: SLEEP TIME


Tuesday:
    Tasks: [INSERT THE TASKS FOR TUESDAY WITH THE TIME : "HH:MM AM/PM, TASK NAME, AND THEN OPTIONAL NOTES]
    Busy: UNAVAILABLE BLOCK TIME
    Sleep: SLEEP BLOCK


Wednesday:
    Tasks: [INSERT THE TASKS FOR WEDNESDAY WITH THE TIME : "HH:MM AM/PM, TASK NAME, AND THEN OPTIONAL NOTES]
    Busy: UNAVAILABLE BLOCK TIME
    Sleep: SLEEP BLOCK


Thursday:
    Tasks: [INSERT THE TASKS FOR THURSDAY WITH THE TIME : "HH:MM AM/PM, TASK NAME, AND THEN OPTIONAL NOTES]
    Busy: UNAVAILABLE BLOCK TIME
    Sleep: SLEEP BLOCK


Friday:
    Tasks: [INSERT THE TASKS FOR FRIDAY WITH THE TIME : "HH:MM AM/PM, TASK NAME, AND THEN OPTIONAL NOTES]
    Busy: UNAVAILABLE BLOCK TIME
    Sleep: SLEEP BLOCK


Saturday:
    Tasks: [INSERT THE TASKS FOR SATURDAY WITH THE TIME : "HH:MM AM/PM, TASK NAME, AND THEN OPTIONAL NOTES]
    Busy: UNAVAILABLE BLOCK TIME
    Sleep: SLEEP BLOCK


Sunday:
    Tasks: [INSERT THE TASKS FOR SUNDAY WITH THE TIME : "HH:MM AM/PM, TASK NAME, AND THEN OPTIONAL NOTES]
    Busy: UNAVAILABLE BLOCK TIME
    Sleep: SLEEP BLOCK


suggestions: UP TO 2 OPTIONAL TIPS


"""
if 'convo' not in st.session_state:
    st.session_state["convo"] = [
        {"role": "system", "content": system_prompt}
    ]

for i, chat_message in enumerate(st.session_state["convo"]):
    if chat_message["role"] == "system":
        continue
    elif chat_message["role"] == "user":
        message(chat_message["content"], is_user=True, key=f"user_{i}")
    else:
        message(chat_message["content"], key = f"assisttant_{i}")

with st.form("input", clear_on_submit=True):
    user_input = st.text_input("What do you want to add to your schedule?")
    submitted = st.form_submit_button("Submit")
    if submitted and user_input != "":
        st.session_state["convo"].append({"role": "user", "content": user_input})

        api_call = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state["convo"],
        )

        bot_message = api_call.choices[0].message.content
        st.session_state["convo"].append({"role": "assistant", "content": bot_message})

        st.rerun()
