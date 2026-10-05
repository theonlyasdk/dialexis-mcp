FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .
ENV DIALEXIS_OUTPUT_DIR=/data
VOLUME ["/data"]
EXPOSE 8000
CMD ["dialexis-mcp", "--http", "--host", "0.0.0.0", "--port", "8000"]
