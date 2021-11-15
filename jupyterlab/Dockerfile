# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG BASE_CONTAINER=jupyter/scipy-notebook:2ce7c06a61a1
FROM $BASE_CONTAINER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

USER root

# Spark dependencies
ENV APACHE_SPARK_VERSION 2.4.8
ENV HADOOP_VERSION 2.7

RUN apt-get -y update && \
    apt-get install --no-install-recommends -y openjdk-8-jre-headless ca-certificates-java && \
    rm -rf /var/lib/apt/lists/*

RUN cd /tmp && \
    wget -q http://mirrors.ukfast.co.uk/sites/ftp.apache.org/spark/spark-${APACHE_SPARK_VERSION}/spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
#    echo "E8B7F9E1DEC868282CADCAD81599038A22F48FB597D44AF1B13FCC76B7DACD2A1CAF431F95E394E1227066087E3CE6C2137C4ABAF60C60076B78F959074FF2AD *spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" | sha512sum -c - && \
    tar xzf spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -C /usr/local --owner root --group root --no-same-owner && \
    rm spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz
RUN cd /usr/local && ln -s spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} spark

# Mesos dependencies
# Install from the Xenial Mesosphere repository since there does not (yet)
# exist a Bionic repository and the dependencies seem to be compatible for now.
COPY mesos.key /tmp/
RUN apt-get -y update && \
    apt-get install --no-install-recommends -y gnupg && \
    apt-key add /tmp/mesos.key && \
    echo "deb http://repos.mesosphere.io/ubuntu xenial main" > /etc/apt/sources.list.d/mesosphere.list && \
    apt-get -y update && \
    apt-get --no-install-recommends -y install mesos=1.2\* && \
    apt-get purge --auto-remove -y gnupg && \
    rm -rf /var/lib/apt/lists/*

# Spark and Mesos config
ENV SPARK_HOME /usr/local/spark
ENV PYTHONPATH $SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.7-src.zip
ENV MESOS_NATIVE_LIBRARY /usr/local/lib/libmesos.so
ENV SPARK_OPTS --driver-java-options=-Xms1024M --driver-java-options=-Xmx4096M --driver-java-options=-Dlog4j.logLevel=info

USER $NB_UID

# Install pyarrow
RUN conda install --quiet -y 'pyarrow' && \
    conda clean --all -f -y && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

#####

ENV RSTUDIO_PKG=rstudio-server-1.2.1335-amd64.deb
ENV SHINY_PKG=shiny-server-1.5.9.923-amd64.deb

USER root

# APT packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-dejavu \
    tzdata \
    gfortran \
    gcc \
    scilab \
    tree \
    vim \
    pari-gp \
    libpari-dev \
    sagemath \
    sagemath-jupyter \
    libgmp-dev \
    # START needed for rstudio server
    libapparmor1 \
    libedit2 \
    lsb-release \
    psmisc \
    libssl1.0.0 \
    libclang-dev
    # END needed for rstudio server
#    && apt-get clean && \
#    rm -rf /var/lib/apt/lists/*

RUN wget -q https://download2.rstudio.org/server/bionic/amd64/${RSTUDIO_PKG}
RUN wget -q https://download3.rstudio.org/ubuntu-14.04/x86_64/${SHINY_PKG}
RUN dpkg -i ${RSTUDIO_PKG}
RUN dpkg -i ${SHINY_PKG}
RUN rm ${RSTUDIO_PKG}
RUN rm ${SHINY_PKG}

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Fix SageMath kernel, still as root
RUN sed -i 's/"\/usr\/bin\/sage"/"env", "PATH=\/usr\/local\/sbin:\/usr\/local\/bin:\/usr\/sbin:\/usr\/bin:\/sbin:\/bin", "\/usr\/bin\/sage"/' /usr/share/jupyter/kernels/sagemath/kernel.json

USER $NB_UID

# Conda packages
RUN conda install --quiet --yes \
    'pyspark~=2.4.3' \
    'r-base~=3.6.1' \
    'r-irkernel~=1.0.2' \
    'r-dplyr~=0.8.3' \
    'r-data.table~=1.12.2' \
    'r-devtools~=2.1.0' \
    'r-tidyverse~=1.2.1' \
    'r-shiny~=1.3.2' \
    'r-rmarkdown~=1.14' \
    'r-forecast~=8.7' \
    'r-rsqlite~=2.1.2' \
    'r-reshape2~=1.4.3' \
    'r-nycflights13~=1.0.0' \
    'r-caret=6.0*' \
    'r-rcurl=1.95*' \
    'r-crayon~=1.3.4' \
    'r-randomforest=4.6*' \
    'r-htmltools~=0.3.6' \
    'r-raster=2.9*' \
    'r-sf=0.7*' \
    'r-sparklyr~=1.0.2' \
    'r-tmap~=2.2' \
    'r-htmlwidgets~=1.3' \
    'r-hexbin~=1.27.3' \
    'julia~=1.0.3' && \
    conda clean -tipsy && \
    fix-permissions $CONDA_DIR

ENV CPATH=$CONDA_DIR/include

RUN pip install \
    pari_jupyter~=1.3.2 \
    libais~=0.17 \
    jupyter-rsession-proxy~=1.0b6 \
    scilab-kernel~=0.9.10 && \
    fix-permissions $CONDA_DIR

# jupyterlab-server-proxy in the repo is not yet compatible with jupyterlab 1.0, compiling from source.
# See https://github.com/jupyterhub/jupyter-server-proxy/issues/1394
RUN cd /tmp/ && \
    git clone --depth 1 https://github.com/jupyterhub/jupyter-server-proxy && \
    cd jupyter-server-proxy/jupyterlab-server-proxy && \
    npm install && npm run build && jupyter labextension link . && \
    npm run build && jupyter lab build

# The desktop package uses /usr/lib/rstudio/bin
ENV PATH="${PATH}:/usr/lib/rstudio-server/bin"
ENV LD_LIBRARY_PATH="/usr/lib/R/lib:/lib:/usr/lib/x86_64-linux-gnu:/usr/lib/jvm/java-7-openjdk-amd64/jre/lib/amd64/server:/opt/conda/lib/R/lib"

# Add conda env hook
COPY ./conda-activate.sh /usr/local/bin/before-notebook.d/

# The `work` folder is mounted on host, so we should be there by default
WORKDIR /home/$NB_USER/work
