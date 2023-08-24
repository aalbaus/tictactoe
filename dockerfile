FROM python:latest

RUN mkdir /code
WORKDIR /code

ADD . /code/
RUN pip install -r requirements.txt --no-cache-dir

# ssh
# ENV SSH_PASSWD "root:Docker!"
# RUN apt-get update \
#         && apt-get install -y --no-install-recommends dialog \
#         && apt-get update \
#  && apt-get install -y --no-install-recommends openssh-server \
#  && echo "$SSH_PASSWD" | chpasswd 

# COPY sshd_config /etc/ssh/
# COPY init.sh /usr/local/bin/

# RUN chmod u+x /usr/local/bin/init.sh
EXPOSE 8000 2222

RUN cd /code/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["python", "-m" "uvicorn", "main:app", "--reload"]
# ENTRYPOINT ["init.sh"]
