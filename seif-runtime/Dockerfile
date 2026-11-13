FROM python:3.12-slim
WORKDIR /app
COPY server.py index.html ./
RUN useradd --uid 10001 --create-home seif && mkdir /data && chown seif:seif /data
USER seif
ENV SEIF_BIND=0.0.0.0 SEIF_DATA_DIR=/data PYTHONUNBUFFERED=1
EXPOSE 8765
CMD ["python", "server.py"]
