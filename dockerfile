FROM python:3.12
WORKDIR /mental-connect-algorithm
COPY . .

RUN pip install -r docker-requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 8090
EXPOSE 8091

WORKDIR /mental-connect-algorithm/Service

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8090", "--reload", "--log-config", "logging_config.json"]