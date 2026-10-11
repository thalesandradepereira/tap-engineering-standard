FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8080
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && groupadd -g 10001 tap && useradd -u 10001 -g tap -s /usr/sbin/nologin tap && mkdir /data && chown tap:tap /data
COPY server/ ./server/
COPY web/ ./web/
USER 10001:10001
EXPOSE 8080
VOLUME /data
CMD ["python","server/studio.py"]
