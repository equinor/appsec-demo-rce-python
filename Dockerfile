# This docker container is used to emulate the machine where the 
# hypothetical reservoir simulation software is running.

FROM python:3.4

VOLUME /myapp

CMD ["bash"]