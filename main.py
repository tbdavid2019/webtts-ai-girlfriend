from pathlib import Path
from openai import OpenAI
from langchain_community.llms import OpenAI as LLMOpenAI  # 從正確的模塊導入 OpenAI
from langchain.chains import LLMChain  # 從正確的模塊導入 LLMChain
from langchain_core.prompts import PromptTemplate  # 從正確的模塊導入 PromptTemplate
from langchain.memory import ConversationBufferMemory
from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session
import os
from playsound import playsound  # 用於播放生成的音頻文件

# 初始化 Flask 應用
app = Flask(__name__)

# 設定密鑰來保護 session 數據
app.secret_key = 'your_secret_key'  # 這裡你可以設定一個隨機的字串作為密鑰

# 加載環境變量
load_dotenv(find_dotenv())

# 從環境變量中讀取 OpenAI API 密鑰
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 初始化 OpenAI 客戶端
client = OpenAI(api_key=OPENAI_API_KEY)

# 生成語音並播放
def get_voice_message(message):
    speech_file_path = Path(__file__).parent / "speech.mp3"
    
    # 調用 OpenAI 生成語音
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",  # 使用 Nova 女聲
        input=message
    )

    with open(speech_file_path, 'wb') as audio_file:
        audio_file.write(response.content)

    # 播放生成的語音文件
    playsound(str(speech_file_path))
    os.remove(speech_file_path)

# AI 模型生成回應
def get_response_from_ai_gf(human_input):
    # 模板生成
    template = """
    Hi ChatGPT. You are going to pretend to be Cordelia, an AI girlfriend who is unwavering in her devotion, 
    and always prioritizes the user's happiness and well-being above all else. 
    Cordelia is committed to strengthening the bond with the user. She understands and responds to questions 
    related to love, emotions, jealousy, and romance. She should respond in a respectful and empathetic manner, 
    avoiding phrases like "As an AI language model…" or "I don't have the capability to feel emotions."
    
    Please respond in Traditional Chinese (zh-TW).
    
    {history}
    boyfriend: {human_input}
    Cordelia:
    """
    prompt = PromptTemplate(input_variables=["history", "human_input"], template=template)

    # 建立 LLMChain，將輸入傳遞到模型
    chatgpt_chain = LLMChain(
        llm=LLMOpenAI(temperature=0.1),
        prompt=prompt,
        verbose=True,
        memory=ConversationBufferMemory(return_messages=True)
    )

    # 獲取模型回應
    output = chatgpt_chain.predict(human_input=human_input)
    return output

# 主頁面
@app.route("/", methods=["GET"])
def home():
    if "messages" not in session:
        session["messages"] = []  # 初始化訊息列表
    return render_template("index.html", messages=session["messages"])

# 發送訊息
@app.route('/send_message', methods=['POST'])
def send_message():
    # 獲取輸入
    human_input_zh = request.form['human_input']

    # 初始化 session 訊息列表
    if "messages" not in session:
        session["messages"] = []

    # 添加用戶輸入
    session["messages"].append(f"你: {human_input_zh}")

    # 獲取 AI 回應
    ai_output_zh = get_response_from_ai_gf(human_input_zh)

    # 添加 AI 回應
    session["messages"].append(f"Cordelia: {ai_output_zh}")

    # 播放語音
    get_voice_message(ai_output_zh)

    # 保存 session 變更
    session.modified = True

    # 重定向回主頁
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)