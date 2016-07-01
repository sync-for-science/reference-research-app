FROM python:3
MAINTAINER Josh Mandel

# Install required packages
RUN apt-get update
RUN apt-get install -y supervisor cron
RUN apt-get clean

# Create the application directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Setup cron
COPY crontab /etc/cron.d/reference-research-app-cron
RUN chmod 0644 /etc/cron.d/reference-research-app-cron
RUN touch /var/log/cron.log

# Install python dependencies
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the codebase
COPY . /usr/src/app

# Configure the app
RUN pip install -e .
ENV ES_URL "https://search-s4s-logs-xsjsafiwd7vkpiucmjqmdjkp7y.us-west-2.es.amazonaws.com/reference-research-app/log/"
RUN cp development.ini.dist development.ini

CMD supervisord -c supervisord.conf
