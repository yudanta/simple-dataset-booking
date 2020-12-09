FROM python:3.7-slim

RUN apt update 
RUN apt -y upgrade 

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# create user 
ARG user=fortress
ARG group=fortress
ARG uid=1000
ARG gid=1001
RUN adduser ${user}

USER ${user}
RUN mkdir /home/${user}/src
RUN mkdir /home/${user}/log

# cp project files 
ADD app/ /home/${user}/src/app/
ADD config.py /home/${user}/src/
ADD dbmigration.py /home/${user}/src/
ADD seeders/ /home/${user}/src/seeders
ADD fortress-gunicorn.sh /home/${user}/src/

EXPOSE 8000

WORKDIR /home/${user}/src
RUN python3 dbmigration.py SqlDB init 
RUN python3 dbmigration.py SqlDB migrate 
RUN python3 dbmigration.py SqlDB upgrade 
RUN python3 dbmigration.py do_seed_users

CMD ["sh", "/home/fortress/src/fortress-gunicorn.sh"]