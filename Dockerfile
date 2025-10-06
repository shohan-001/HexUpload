FROM nanthakps/kpsmlx:heroku

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

RUN apt update && apt install -y ffmpeg

COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["bash", "start.sh"]
