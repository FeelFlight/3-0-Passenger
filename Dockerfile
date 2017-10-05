FROM python:latest

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD mcp.py mcp.py
EXPOSE 5000

CMD python mcp.py
