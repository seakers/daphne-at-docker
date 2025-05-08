# FROM python:3.7-slim-stretch

# # The working directory where daphne_brain is placed is /usr/src/app/daphne_brain
# WORKDIR /usr/src/app/daphne_brain


# # Copy everything in the daphne_brain directory to /usr/src/app/daphne_brain
# COPY ./. /usr/src/app/daphne_brain/.


# # Update apt-get package manager -- Install daphne_brain dependencies
# RUN apt-get -y update &&\
#     apt-get -y upgrade &&\
#     apt-get -y install build-essential manpages-dev &&\
#     pip3 install --no-cache-dir -r ./requirements.txt


# # Commands to start daphne_brain
# RUN python3 manage.py migrate --run-syncdb &&\
#     python3 manage.py collectstatic --clear --noinput
# CMD daphne -b 0.0.0.0 -p 8001 daphne_brain.asgi:application

FROM python:3.9.19

# Set working directory
WORKDIR /usr/src/app

# Create logs directory 
RUN mkdir -p /usr/src/app/logs && chmod 777 /usr/src/app/logs

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    manpages-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY temp_requirements.txt .
RUN pip install --no-cache-dir -r temp_requirements.txt

# Copy project files
COPY . .

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=daphne_brain.settings \
    PYTHONUNBUFFERED=1 \
    POSTGRES_DB=daphne \
    POSTGRES_USER=daphne \
    POSTGRES_PASSWORD=daphnetest \
    POSTGRES_HOST=db \
    POSTGRES_PORT=5432\
    REDIS_HOST=redis \
    REDIS_PORT=6379 

RUN python3 manage.py collectstatic --clear --noinput

EXPOSE 8002

CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]
