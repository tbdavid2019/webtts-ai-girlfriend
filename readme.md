# AI Girlfriend Project / AI 女友專案

This project is an AI-powered virtual girlfriend named **Cordelia** that generates text and speech responses using OpenAI's API. The application is built with Flask for web interaction, and it uses OpenAI for generating text responses and text-to-speech (TTS) for voice output.

本專案是一個由 AI 驅動的虛擬女友，名為 **Cordelia**，使用 OpenAI 的 API 生成文字和語音回應。應用程式使用 Flask 作為網頁互動介面，並使用 OpenAI 來生成文本回應與文字轉語音 (TTS)。

## Features / 功能
- AI-generated conversation / AI 生成對話
- Text-to-speech (TTS) responses using OpenAI's speech model / 使用 OpenAI 語音模型進行文字轉語音 (TTS)
- Cordelia can respond in Traditional Chinese (zh-TW) / Cordelia 可使用繁體中文 (zh-TW) 回應
- Flask-based web interface / 基於 Flask 的網頁介面
- Temporary MP3 files are auto-deleted after playback to save disk space / 臨時 MP3 文件播放後自動刪除以節省磁碟空間

## Technologies Used / 使用技術
- Python
- Flask
- OpenAI API (GPT & TTS)
- Langchain for managing conversation flow / 使用 Langchain 管理對話流程
- Playsound for playing generated MP3 files / 使用 Playsound 播放生成的 MP3 文件
- HTML & CSS for the web interface / 網頁介面的 HTML 和 CSS

## Setup & Installation / 設置與安裝

1. **Clone the repository / 克隆此倉庫**:

    ```bash
    git clone https://github.com/yourusername/ai-girlfriend.git
    cd ai-girlfriend
    ```

2. **Set up a virtual environment / 建立虛擬環境** (optional but recommended / 可選，但建議):

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required dependencies / 安裝所需依賴項**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables / 設置環境變量**:

    Create a `.env` file in the root directory with your OpenAI API key:
    
    在根目錄中建立 `.env` 文件，並添加你的 OpenAI API 金鑰：
    
    ```bash
    OPENAI_API_KEY=your_openai_api_key
    ```

5. **Run the Flask application / 運行 Flask 應用程式**:

    ```bash
    python3 main.py
    ```

6. **Access the app / 訪問應用程式**:

    Open your browser and go to / 打開瀏覽器並進入：
    
    ```
    http://127.0.0.1:5000
    ```

## Usage / 使用說明
1. Start a conversation with Cordelia via the web interface.
2. Input a message, and Cordelia will respond in both text and voice.
3. After the response is played, the temporary MP3 file will be deleted automatically.

1. 通過網頁介面與 Cordelia 開始對話。
2. 輸入訊息，Cordelia 將以文字和語音形式回應。
3. 回應播放完畢後，臨時 MP3 文件將自動刪除。

## File Structure / 文件結構
```bash
├── main.py              # Flask web app and main logic / Flask 網頁應用程式及主要邏輯
├── templates
│   └── index.html       # HTML for the web interface / 網頁介面的 HTML 文件
├── requirements.txt     # Python dependencies / Python 依賴項
├── .env                 # Environment variables (not included in the repo) / 環境變量（不包含在倉庫中）
└── README.md            # Project README file / 專案說明文件
```

## How it Works / 如何運作
- **Cordelia's Text Response**: The AI girlfriend responds based on user input using the OpenAI GPT model. The conversation history is maintained using `ConversationBufferMemory` from Langchain.
  
  **Cordelia 的文字回應**：虛擬女友 Cordelia 根據使用者輸入使用 OpenAI 的 GPT 模型進行回應。對話歷史記錄由 Langchain 的 `ConversationBufferMemory` 來維護。

- **Voice Generation**: The text response is converted to speech using OpenAI's TTS model (`tts-1`). The audio is played using the `playsound` package.
  
  **語音生成**：文本回應使用 OpenAI 的 TTS 模型（`tts-1`）轉換為語音。音頻使用 `playsound` 套件進行播放。

- **File Management**: The MP3 files generated are temporary and are automatically deleted after being played.
  
  **文件管理**：生成的 MP3 文件是臨時文件，播放後會自動刪除。

## Dependencies / 依賴項
- Flask
- OpenAI Python Library / OpenAI Python 庫
- Langchain
- Playsound
- Python-Dotenv

## License / 授權協議
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

此專案基於 MIT 授權協議。詳見 [LICENSE](LICENSE) 文件。
