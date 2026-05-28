# 使用官方 Python 3.14 輕量版作為基礎鏡像
FROM python:3.14-slim

# 設定環境變數
# 1. 避免 Python 寫入 .pyc 暫存檔，保持容器乾淨
ENV PYTHONDONTWRITEBYTECODE=1
# 2. 讓 Python 輸出（stdout/stderr）即時顯示，便於 Docker 收集日誌
ENV PYTHONUNBUFFERED=1
# 3. 預設運作環境為生產環境 (production)
ENV FLASK_ENV=production
# 4. 預設連接埠為 19191
ENV PORT=19191

# 設定工作目錄
WORKDIR /app

# 先複製 requirements.txt 以利利用 Docker cache 機制，加速後續構建
COPY requirements.txt .

# 安裝 Python 依賴套件（不使用快取以減小映像檔大小）
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案其餘的所有程式碼與檔案
COPY . .

# 宣告對外開放的連接埠（搭配 run.py 中的預設連接埠）
EXPOSE 19191

# 啟動應用程式
CMD ["python", "run.py"]
