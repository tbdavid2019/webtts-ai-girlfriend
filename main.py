import json
import random
import threading  # 導入 threading 模組
from quart import Quart, render_template, request, redirect, url_for, session
from dotenv import find_dotenv, load_dotenv
from openai import OpenAI
import os
from pathlib import Path
from playsound import playsound

# 初始化 Quart 應用
app = Quart(__name__)
app.secret_key = 'your_secret_key'  # 用於 session 的密鑰

# 加載環境變量
load_dotenv(find_dotenv())

# 初始化 OpenAI 客戶端
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 讀取 system prompt 模板
def load_system_prompt():
    with open('prompt.json', 'r') as file:
        data = json.load(file)
    return data['system_prompt']

# 讀取變量
def load_variables():
    with open('variables.json', 'r') as file:
        data = json.load(file)
    return data

# 隨機選擇變量
def select_random_variables(variables):
    selected_vars = {}
    for key, value in variables.items():
        selected_vars[key] = random.choice(value)
    return selected_vars

# 生成最終的 system prompt
def generate_system_prompt():
    prompt_template = load_system_prompt()  # 讀取 JSON 模板
    variables = load_variables()  # 讀取變量
    selected_vars = select_random_variables(variables)  # 隨機選擇變量
    return prompt_template.format(**selected_vars)  # 用變量填充模板

# 使用 streaming 生成 AI 回應
async def get_response_from_ai_gf(human_input):
    # 使用隨機變量生成 system prompt
    system_prompt = generate_system_prompt()

    # 生成 system message 設定 AI 行為
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": human_input}
    ]

    # 使用 Streaming API 進行實時輸出
    stream = client.chat.completions.create(
        model="gpt-4o-mini",  # 使用 GPT-4 模型
        messages=messages,
        stream=True,
    )

    # 實時流式處理並獲取回應
    full_response = ""
    for chunk in stream:
        # 檢查 content 是否為 None，防止拼接 NoneType 和 str
        content = getattr(chunk.choices[0].delta, 'content', None)
        if content:
            full_response += content
            print(content, end="")
    
    return full_response

# 異步生成語音並播放
def get_voice_message(message):
    speech_file_path = Path(__file__).parent / "speech.mp3"
    
    # 使用 OpenAI 最新的 TTS 調用
    response = client.audio.speech.create(
        model="tts-1",  # 使用合適的語音模型
        voice="nova",  # 使用 Nova 女聲
        input=message
    )

    # 將生成的語音保存為 mp3 文件
    with open(speech_file_path, 'wb') as audio_file:
        audio_file.write(response.content)

    # 播放生成的語音文件
    playsound(str(speech_file_path))
    os.remove(speech_file_path)

# 啟動新的線程來播放語音
def start_voice_thread(message):
    thread = threading.Thread(target=get_voice_message, args=(message,))
    thread.start()

# 主頁面
@app.route("/", methods=["GET"])
async def home():
    if "messages" not in session:
        session["messages"] = []  # 初始化訊息列表
    return await render_template("index.html", messages=session["messages"])

# 發送訊息
@app.route('/send_message', methods=['POST'])
async def send_message():
    # 獲取輸入
    human_input_zh = (await request.form)['human_input']

    # 初始化 session 訊息列表
    if "messages" not in session:
        session["messages"] = []

    # 添加用戶輸入
    session["messages"].append(f"你: {human_input_zh}")

    # 獲取 AI 回應
    ai_output_zh = await get_response_from_ai_gf(human_input_zh)

    # 添加 AI 回應
    session["messages"].append(f"女友: {ai_output_zh}")

    # 保存 session 變更
    session.modified = True

    # 啟動語音播放的線程，文字會先顯示出來
    start_voice_thread(ai_output_zh)

    # 重定向回主頁
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)