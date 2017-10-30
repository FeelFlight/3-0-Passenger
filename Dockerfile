FROM python:latest

ADD requirements.txt requirements.txt
RUN pip install -r   requirements.txt

ADD mcp.py       mcp.py
ADD passenger.py passenger.py

EXPOSE 8030

CMD ["python","-u","mcp.py"]
