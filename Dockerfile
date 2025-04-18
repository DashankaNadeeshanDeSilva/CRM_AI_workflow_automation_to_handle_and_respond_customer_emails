# use python base images
FROM python:3.10

# set working dir inside the container
WORKDIR /app

# install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install--no-cache-dir -r /app/requirements.txt

# copy all files and dirs to /app dir in the container
COPY . /app

# expose
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]