FROM ubuntu

ENV TZ=America/Argentina/Buenos_Aires \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y tzdata wget curl vim python3 pip
RUN apt-get install -y gdal-bin libgdal-dev
RUN apt-get install proj-bin libproj-dev
RUN apt-get install -y libgeos-dev
RUN pip install requests gdal 
RUN pip install django
RUN pip install djangorestframework
RUN pip install djangorestframework-gis
RUN pip install psycopg2-binary


