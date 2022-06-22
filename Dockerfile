FROM python:3.7.9
# Python docker images: https://github.com/docker-library/docs/tree/master/python/

USER root

# Copy the src
WORKDIR /app
COPY ML-Model-with-flask/ /app/
RUN ls -la /app

# Install python dependencies
RUN python3 --version

RUN pip3 install --no-cache-dir -r /app/ML-Model-with-flask/requirements.txt
RUN pip3 list --format=columns

USER 1001

# EXPOSE 5001
ENTRYPOINT ["python3", "/app/ML-Model-with-flask/run.py"]