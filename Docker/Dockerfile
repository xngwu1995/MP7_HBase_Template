# Fetch ubuntu 16.04 LTS docker image
FROM ubuntu:16.04

#Make a copy of ubuntu apt repository before modifying it. 
RUN mv /etc/apt/sources.list /sources.list
#Now change the default ubuntu apt repositry, which is VERY slow, to another mirror that is much faster. It assumes the host already has created a sources.list.
COPY sources.list /etc/apt/sources.list

#uncomment this line to find the fastest ubuntu repository at the time. Probably overkill, so disabling for now
#Note that this functionality is untested and might need debugging a bit.

# Update apt, and install Java + curl + wget on your ubuntu image.
RUN \
  apt-get update && \
  apt-get install -y curl vim wget maven expect git zip unzip libboost-dev libboost-test-dev libboost-program-options-dev libboost-filesystem-dev libboost-thread-dev libevent-dev automake libtool flex bison pkg-config g++ libssl-dev telnet net-tools && \
  apt-get install -y openjdk-8-jdk 

RUN \
  apt-get install -y python && \
  apt-get install -y python-pip

RUN pip install happybase

ENV JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64
RUN pwd
RUN curl -s "https://archive.apache.org/dist/hadoop/common/hadoop-2.9.0/hadoop-2.9.0.tar.gz" | tar -xz -C /usr/local/
RUN cd /usr/local && ln -s ./hadoop-2.9.0 hadoop
#COPY hadoop-2.9.0.tar.gz /usr/local/
#RUN cd /usr/local/ && tar xzf hadoop-2.9.0.tar.gz && ln -s ./hadoop-2.9.0 hadoop

ENV HADOOP_PREFIX /usr/local/hadoop
ENV HADOOP_COMMON_HOME /usr/local/hadoop
ENV HADOOP_HDFS_HOME /usr/local/hadoop
ENV HADOOP_MAPRED_HOME /usr/local/hadoop
ENV HADOOP_YARN_HOME /usr/local/hadoop
ENV HADOOP_CONF_DIR /usr/local/hadoop/etc/hadoop
ENV YARN_CONF_DIR $HADOOP_PREFIX/etc/hadoop
ENV HADOOP_CLASSPATH $JAVA_HOME/lib/tools.jar
ENV PATH="/usr/local/hadoop/bin:${PATH}"

RUN sed -i "/^export JAVA_HOME/ s:.*:export JAVA_HOME=$JAVA_HOME\nexport HADOOP_PREFIX=/usr/local/hadoop\nexport HADOOP_HOME=/usr/local/hadoop\n:" $HADOOP_PREFIX/etc/hadoop/hadoop-env.sh
RUN sed -i '/^export HADOOP_CONF_DIR/ s:.*:export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop/:' $HADOOP_PREFIX/etc/hadoop/hadoop-env.sh

RUN \
  apt-get update && \
  apt-get install -y --no-install-recommends net-tools vim sudo expect ssh openssh-server zip unzip wget openjdk-8-jdk python python-pip python-setuptools gcc python-dev && \
  apt-get autoremove -qq -y --purge && \
  apt-get clean && \
  rm -rf /var/cache/apt /var/lib/apt/lists && \
  cd /usr/local/ && \
  wget "https://archive.apache.org/dist/zookeeper/zookeeper-3.4.13/zookeeper-3.4.13.tar.gz" &&\
  tar -xvf zookeeper-3.4.13.tar.gz && \
  ln -s ./zookeeper-3.4.13 zookeeper &&  \
  rm -rf /usr/local/zookeeper-3.4.13.tar.gz && \
  mkdir /usr/local/zookeeper/data && \
  mkdir /usr/local/zookeeper/log && \
  rm -rf /usr/local/zookeeper/docs && \
  bash -c "echo '1' >> /usr/local/zookeeper/data/myid" && \
  chmod a+rwx -R /usr/local/zookeeper/ && \
  wget "https://archive.apache.org/dist/hbase/1.6.0/hbase-1.6.0-bin.tar.gz" && \
  tar -xzf hbase-1.6.0-bin.tar.gz && \
  rm -rf /usr/local/hbase-1.6.0-bin.tar.gz && \
  mv /usr/local/hbase-1.6.0* /usr/local/hbase && \
  rm -rf /usr/local/hbase/docs && \
  chmod a+rwx -R /usr/local/hbase/ && \
  pip install wheel happybase && \
  cd /usr/local/ && \
  wget "https://archive.apache.org/dist/phoenix/phoenix-4.16.1/phoenix-hbase-1.6-4.16.1-bin.tar.gz" && \
  tar -xzf phoenix-hbase-1.6-4.16.1-bin.tar.gz && \
  rm -rf /usr/local/phoenix-hbase-1.6-4.16.1-bin.tar.gz && \
  mv /usr/local/phoenix-hbase-1.6-4.16.1* /usr/local/phoenix && \
  rm -rf /usr/local/phoenix/docs && \
  chmod a+rwx -R /usr/local/phoenix/ && \
  cp /usr/local/phoenix/phoenix-server-hbase-1.6-4.16.1.jar /usr/local/hbase/lib/

ENV CLASSPATH=$CLASSPATH:/usr/local/phoenix/phoenix-client-hbase-1.6-4.16.1.jar

COPY zoo.cfg /usr/local/zookeeper/conf/zoo.cfg
COPY hbase-site.xml /usr/local/hbase/conf/hbase-site.xml
COPY hbase-env.sh /usr/local/hbase/conf/hbase-env.sh

COPY auto* /usr/local/bin/
RUN chmod 777 /usr/local/bin/auto*
RUN adduser hadoopuser --disabled-password --gecos ""
RUN echo 'hadoopuser:hadooppass' | chpasswd && usermod -aG sudo hadoopuser
RUN sh -c "echo 'hadoopuser ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers"

ENV HBASE_HOME /usr/local/hbase
ENV PATH="/usr/local/hbase/bin:${PATH}"
RUN chmod a+rwx -R /usr/local/hbase/


# Make vim nice
RUN echo "set background=dark" >> ~/.vimrc

