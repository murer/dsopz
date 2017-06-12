FROM ruby:2.4

ENV DEBIAN_FRONTEND noninteractive

RUN sed -i "s/\/\/us\.archive\.ubuntu\.com/\/\/br.archive.ubuntu.com/g" /etc/apt/sources.list
RUN sed -i "s/\/\/archive\.ubuntu\.com/\/\/br.archive.ubuntu.com/g" /etc/apt/sources.list

# RUN apt-get -y update

RUN curl -sL https://deb.nodesource.com/setup_6.x | bash -
RUN apt-get install -y nodejs

RUN gem install bundler

ADD config /opt/config

RUN find /opt/config -name "*.sh" -exec chmod -v +x "{}" \;

WORKDIR /opt/config

RUN bundle update

WORKDIR /opt/dsopz/docs

CMD /opt/config/entry-point.sh
