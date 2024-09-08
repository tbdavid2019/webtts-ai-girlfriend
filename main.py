import json
import random
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import os

# 初始化 Flask 應用
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用於 session 的密鑰

# 加載環境變量
load_dotenv(find_dotenv())

# 從環境變量中讀取 OpenAI API 密鑰

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

# 使用 system roles 生成 AI 回應
def get_response_from_ai_gf(human_input):
    # 使用隨機變量生成 system prompt
    system_prompt = generate_system_prompt()

    # 生成 system message 設定 AI 行為
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": human_input}
    ]

    # 使用最新的 OpenAI ChatCompletion 調用方式
    response = client.chat.completions.create(model="gpt-4",  # 使用 GPT-4 模型
    messages=messages)

    return response.choices[0].message.content

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

    # 保存 session 變更
    session.modified = True

    # 重定向回主頁
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)