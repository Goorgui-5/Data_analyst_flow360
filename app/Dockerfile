FROM python:3.11-slim

# set workdir
WORKDIR /app

# copy requirements (we will create it)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy app
COPY . /app

# streamlit port
EXPOSE 8501

ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_PORT=8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.headless=true"]
