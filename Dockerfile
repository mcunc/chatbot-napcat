FROM python:3.12.11-trixie

COPY ./ /chatbot-napcat/
RUN pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple --root-user-action=ignore -r /chatbot-napcat/requirements.txt
WORKDIR /chatbot-napcat
ENTRYPOINT PYTHONPATH="${PYTHONPATH}:/chatbot-napcat/control:/chatbot-napcat/model" && cp /config/config.toml /chatbot-napcat && python /chatbot-napcat/main.py
