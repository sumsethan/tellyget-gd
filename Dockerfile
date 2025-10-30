FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --no-cache-dir  beautifulsoup4 requests requests-toolbelt pycryptodome netifaces
RUN python ./setup.py install
ENV TZ Asia/Shanghai
ENV USER=
ENV PASSWORD=
ENV MACADDR=
ENV INTERFACE=
  
RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
    && sed -i 's/security.debian.org/mirrors.163.com/g' /etc/apt/sources.list.d/debian.sources
RUN apt-get update && apt-get install -y tzdata
COPY start.sh /start.sh
RUN chmod +x /start.sh
CMD /start.sh
