FROM continuumio/miniconda3
 
WORKDIR /app
 
# Create the environment:
COPY ENV.yml /app
RUN conda env create -f ENV.yml
 
# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "awm_env", "/bin/bash", "-c"]
 
# Copy everything in your Django project to the image.
COPY . /app
ENV PYTHONPATH="/app"
 
# for entry point
RUN chmod +x docker-entrypoint.sh
# Install uWSGI
RUN pip install uwsgi
 
# Expose the port uWSGI will run on
EXPOSE 8000
 
# Run uWSGI
CMD ["uwsgi", "--ini", "/app/uwsgi.ini"]