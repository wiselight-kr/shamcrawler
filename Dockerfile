# ./Dockerfile
FROM python:3.7
WORKDIR /srv/donghadongha

# CHROME
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/goodle.list'
RUN apt-get update
RUN apt-get install -y google-chrome-stable

# CHROME_DRIVER
RUN apt-get install -yqq unzip
RUN apt-get install -y curl
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /srv/donghadongha/driver
#ENV DISPLAY=:99

# TODO rabbitmq


## Install packages
COPY requirements.txt ./
RUN pip install -r requirements.txt

## Copy all src files
COPY . .

## Run the application on the port 8080
EXPOSE 8000

# gunicorn 배포 명령어
# CMD ["gunicorn", "--bind", "허용하는 IP:열어줄 포트", "project.wsgi:application"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["python", "test.py"]
# , "donghadongha.wsgi:application"
