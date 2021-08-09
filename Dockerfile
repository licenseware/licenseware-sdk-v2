FROM python:3.8

WORKDIR /usr/src/ifmp-service/

RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD honcho start