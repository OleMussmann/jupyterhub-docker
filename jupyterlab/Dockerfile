FROM jupyter/scipy-notebook:2ce7c06a61a1

LABEL maintainer="Luca De Feo <https://defeo.lu/>"

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
