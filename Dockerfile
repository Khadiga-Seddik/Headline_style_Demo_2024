# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container to /NewsRecSurveyProject
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libc-dev \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*


# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the rest of your application
COPY . /app



# Run
#CMD ["gunicorn", "NEWSREC_survey.wsgi:application", "--bind", "0.0.0.0:8000"]

