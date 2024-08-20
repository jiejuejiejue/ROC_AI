<script setup>
import { ref ,nextTick} from 'vue';

const messages = ref([]);
const userInput = ref('');
const currentChat = ref(null); // 初始化当前对话为空

// 后端地址
const API_URL = 'http://localhost:5000/predict';

// 存储最近聊天记录
const recentChats = ref([

]);

// 初始化新对话
const initNewChat = () => {
    const today = new Date();
    const formattedDate = today.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    }).replace(/\//g, '-'); 

    const newChat = {
        id: today.getTime(),
        title: formattedDate,
        messages: []
    };

    recentChats.value.push(newChat);
    currentChat.value = newChat;
    messages.value = currentChat.value.messages;
};

// 页面加载时初始化新对话
initNewChat();


// 加载聊天记录
const loadChat = (chat) => {
    messages.value = chat.messages; // 加载已存储的消息到聊天界面
};

// 发送消息
const sendMessage = async () => {
    if (!userInput.value.trim()) return;

    // 如果有用户输入的内容，将其加入消息列表
    if (userInput.value.trim()) {
        messages.value.push({ role: 'user', content: userInput.value });
    }

    try {
        const text = userInput.value;
        const response = await fetch(API_URL,{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({text: text})
            })

        if (response.ok) {
            const data = await response.json();
            const assistantReply = data.prediction;
            messages.value.push({ role: 'assistant', content: assistantReply });
        } else {
            messages.value.push({ role: 'assistant', content: 'AI 无法响应，请稍后再试。' });
        }
    } catch (error) {
        messages.value.push({ role: 'assistant', content: '请求失败，请检查网络连接或稍后再试。' });
    }

    userInput.value = '';

    nextTick(scrollToBottom);
};


const scrollToBottom = () => {
    const chatBox = document.querySelector('.chat-box');
    chatBox.scrollTop = chatBox.scrollHeight;
};
</script>
 
<template>
    <div class="chat-container">
        <div class="menu">
            <el-scrollbar>
                <el-text>历史聊天记录</el-text>
                <div v-for="chat in recentChats" :key="chat.id" class="menu-item" @click="loadChat(chat)">
                    {{ chat.title }}
                </div>
            </el-scrollbar>
        </div>
        <div class="chat-content">
            <div class="chat-header">
                <h2>你好，<br>我是攻击性和偏见语言检测模型</h2>
                <p>我可以回答你的问题，为你提供有用信息，帮助你判断句子是否含有攻击性或偏见。</p>
            </div>
            <el-scrollbar class="chat-box">
                <div v-for="(message, index) in messages" :key="index" class="message" :class="message.role">
                    <el-card class="box-card" :body-style="{ padding: '16px' }">
                        <div class="message-content">
                            <p>{{ message.content }}</p>
                        </div>
                    </el-card>
                </div>
            </el-scrollbar>
            <div class="input-container">
                <el-input v-model="userInput" placeholder="请输入你的消息..." :input-style="{ height: '108px'}"
                    class="input-field" @keyup.enter="sendMessage">

                    <template #append>
                        <el-button @click="sendMessage" class="send-button">发送</el-button>
                    </template>

                </el-input>
            </div>
        </div>
    </div>
</template>

<style scoped>
.chat-container {
    display: flex;
    height: 80vh; /* 占满整个页面高度 */
    background: #eef2f7;
    color: #333;
}

.menu {
    width: 300px;
    background: #ffffff;
    border-radius: 12px;
    margin: 10px;
    padding: 10px;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
    /* flex-shrink: 0; */
}

.menu-item {
    padding: 10px 20px;
    border-radius: 6px;
    background: #f7f7f7;
    margin-bottom: 10px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.menu-item:hover {
    background: #e6e6e6;
}

.chat-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    background: #eef2f7;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.05);
    height: calc(92vh - 24px);
    margin: 20px 100px;
}

.chat-header {
    text-align: left;
    padding: 20px;
    background: #fff;
    border-radius: 12px;
    margin-bottom: 20px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    flex-shrink: 0;
}

.chat-header h2 {
    font-size: 1.5rem;
    margin-bottom: 10px;
}

.chat-header p {
    font-size: 1rem;
    color: #555;
}

.prompt-tip {
    background: #eef5ff;
    border-radius: 8px;
    padding: 10px;
    margin-top: 10px;
    color: #4a90e2;
}

.chat-box {
    flex: 1;
    padding: 10px 20px;
    overflow-y: auto;
    background: #eef2f7;
    display: flex;
    flex-direction: column-reverse; /* 新消息会出现在底部 */
}

.message {
    margin-bottom: 15px;
}

.message.user {
    text-align: right;
    align-self: flex-end;
    border-radius: 12px;
}

.message.assistant {
    text-align: left;
    align-self: flex-start;
    border-radius: 12px;
}

.box-card {
    max-width: 70%;
    margin: 0 auto;
    border-radius: 12px;
    background: #ffffff;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.message-content {
    color: #1f1f1f;
}

.input-container {
    padding: 20px 0;
    background: #eef2f7;
    display: flex;
    align-items: center;
    border-top: 1px solid #dcdcdc;
    position: sticky;
    bottom: 0; /* 输入框固定在底部 */
    background-color: #eef2f7;
    z-index: 10;
}

.input-field {
    background: #ffffff;
    border: 1px solid #dcdcdc;
    border-radius: 30px;
    color: #1f1f1f;
    flex: 1;
}

.send-button {
    background: #4a90e2;
    color: #fff;
    border: none;
    border-radius: 30px;
    padding: 0 20px;
    cursor: pointer;
}

.send-button:hover {
    background: #357ab8;
}

</style>