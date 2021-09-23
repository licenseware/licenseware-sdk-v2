FROM python:3.8

WORKDIR /usr/src/{{ app_id }}/

RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip uninstall -y licenseware && pip install -r requirements.txt 


COPY . .
CMD ["sh", "docker-entrypoint.sh"]