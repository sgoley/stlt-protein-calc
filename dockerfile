FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt
COPY data/protein_table.csv ./data/protein_table.csv

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        netbase \
        && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt

EXPOSE 8501

COPY . .

ENTRYPOINT ["streamlit", "run"]

CMD ["streamlit_app.py"]