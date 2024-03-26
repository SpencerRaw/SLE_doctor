# Code refactored from https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps

import openai
from openai import OpenAI
import streamlit as st



with st.sidebar:
    st.title('🤖💬 SLE Doctor Chatbot')
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        # openai.api_key = st.secrets['OPENAI_API_KEY']
        client = OpenAI(
            api_key=st.secrets['OPENAI_API_KEY'],
            base_url="https://api.moonshot.cn/v1",
        )
    else:
        # openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
        client = OpenAI(
            api_key=st.text_input('Enter OpenAI API token:', type='password'),
            base_url="https://api.moonshot.cn/v1",
        )
        # if not (openai.api_key.startswith('sk-') and len(openai.api_key)==51):
        #     st.warning('Please enter your credentials!', icon='⚠️')
        # else:
        st.success('Proceed to entering your prompt message!', icon='👉')

filename = 'rule_prompt.txt'

# 使用 with 语句打开文件，这样可以确保文件在读取后会被自动关闭
with open(filename, 'r', encoding='utf-8') as file:
    file_content = file.read()

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "system", "content": file_content})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] != "system":
            st.markdown(message["content"])

if prompt := st.chat_input("你好，请问有什么事情吗?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model="moonshot-v1-32k",
            messages=[{"role": m["role"], "content": m["content"]}
                      for m in st.session_state.messages], stream=True):
            # full_response += response.choices[0].delta.get("content", "")
            # full_response += response.choices[0].delta.content
            if response.choices[0].delta.content is not None:
                full_response += response.choices[0].delta.content
            else:
                # 如果是None，可以选择跳过或添加一个空字符串
                # full_response += ""  # 这行是可选的，因为如果不做任何操作，效果是一样的
                pass  # 直接跳过
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
