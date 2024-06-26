# app/Dockerfile

FROM python:3.9-slim

WORKDIR /emulsion_app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

#RUN git clone https://github.com/Vasichar11/emu_labs_status.git .
COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "Overview.py"]
