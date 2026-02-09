# 軽量なもの
FROM python:3.12-slim

# 環境変数の設定
# .pycファイルを作らない/標準出力をバッファリング(一時的な記憶)をしないで出す
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# コンテナ内の作業ディレクトリ
WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# ローカルのbackend/appディレクトリをcode/appにコピー
COPY ./app ./app

RUN useradd -m myuser
# ここでコマンドを実行するユーザーの指定
USER myuser

# app.main:app appフォルダのapp.mainモジュール
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]