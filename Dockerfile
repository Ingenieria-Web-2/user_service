FROM python:3.13

WORKDIR /usr/src/user_service

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies - this layer will be cached unless requirements.txt changes
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]