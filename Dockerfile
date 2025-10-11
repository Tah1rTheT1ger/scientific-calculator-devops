FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN useradd -m app && chown -R app:app /app
USER app
RUN pip install --no-cache-dir pytest
ENV PYTHONPATH=/app
CMD ["python", "main.py"]
