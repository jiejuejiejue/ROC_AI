import appbuilder
import streamlit as st
import os

#获取密钥和ID
os.environ['APPBUILDER_TOKEN'] = "bce-v3/ALTAK-n2XgeA6FS3Q5E7Jab6UwE/850b44ebec64c4cad705986ab0b5e3df4b05d407"
app_id = "df881861-9fa6-40b6-b3bd-26df5f5d4b9a"

#初始化agent实例
your_agent = appbuilder.AppBuilderClient(app_id)

#创建会话id
conversation_id = your_agent.create_conversation()

#创建网页
st.title("☁礼貌用语检测器")

#清空消息
clear = st.button("清除")
if clear:
    st.session_state.clear()

#输出内容
if "memory" not in st.session_state:
    st.session_state['memory'] = []
    st.session_state['message'] = [{"role": "ai",
                                "content": "你好！我是“礼貌用语检测器”。在这里，我能够帮助你检测中文语言中的冒犯性内容，维护一个文明、和谐的交流环境。请告诉我你的需求，我会尽力提供帮助。"}]

for message in st.session_state['message']:
    st.chat_message(message["role"]).write(message["content"])

#输入内容
text = st.chat_input()

#运行
if text:
    #将问题保存进message和memory
    st.session_state["message"].append({"role": "human", "content": text})
    st.session_state["memory"].append(text)
    st.chat_message("human").write(text)
    #得到回答
    with st.spinner("AI正在思考中，请稍等..."):
        msg = your_agent.run(conversation_id, text)
        answer = msg.content.answer

    #将回答保存进message和memory
    st.session_state["message"].append({"role": "ai", "content": answer})
    st.session_state["memory"].append(answer)
    st.chat_message("ai").write(answer)
    
    



