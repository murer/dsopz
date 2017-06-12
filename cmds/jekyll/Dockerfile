FROM ruby:2.4

# ENV DEBIAN_FRONTEND noninteractive

# RUN sed -i "s/\/\/us\.archive\.ubuntu\.com/\/\/br.archive.ubuntu.com/g" /etc/apt/sources.list
# RUN sed -i "s/\/\/archive\.ubuntu\.com/\/\/br.archive.ubuntu.com/g" /etc/apt/sources.list

# RUN apt-get -y update

RUN gem install jekyll

ADD config /opt/config

RUN find /opt/config -name "*.sh" -exec chmod -v +x "{}" \;

WORKDIR /opt/dsopz/docs

CMD /opt/config/entry-point.sh
