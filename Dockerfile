# STAGE 0: base image
FROM python:3.8-slim-buster AS base

LABEL author="Meysam Azad <meysam@licenseware.io>"

ARG WHEELDIR=/wheelhouse
ARG BUILDDIR=/build
ARG REQUIREMENTS=requirements.txt

ENV BUILDDIR=${BUILDDIR}
ENV WHEELDIR=${WHEELDIR}
ENV REQUIREMENTS=${REQUIREMENTS}

RUN pip install -U pip && apt update && apt install -y curl gcc libexpat1


# STAGE 1: fetch dependencies
FROM base AS build

COPY ${REQUIREMENTS} ${BUILDDIR}/
RUN pip wheel -r ${BUILDDIR}/${REQUIREMENTS} -w ${WHEELDIR}


# STAGE 2: ready to run the server
FROM base AS pre-run

ARG ENV=development
ARG USER=licenseware
ARG SERVICEDIR=/home/${USER}
ARG PORT=5000
ARG DUMB_INIT='https://github.com/Yelp/dumb-init/releases/download/v1.2.5/dumb-init_1.2.5_x86_64'
ARG APP_DIR=${SERVICEDIR}/app
ARG FILE_UPLOAD_PATH=/tmp/lware

RUN curl -sLo /usr/local/bin/dumb-init ${DUMB_INIT} && \
    chmod +x /usr/local/bin/dumb-init

RUN useradd -m ${USER} && \
    mkdir -p ${FILE_UPLOAD_PATH} && \
    chown ${USER}:${USER} ${FILE_UPLOAD_PATH}

ENV USER=${USER} \
    PORT=${PORT} \
    ENV=${ENV} \
    PYTHONUNBUFFERED=1

EXPOSE ${PORT}
WORKDIR ${SERVICEDIR}

VOLUME ${FILE_UPLOAD_PATH}

COPY --from=build ${BUILDDIR} ${BUILDDIR}
COPY --from=build ${WHEELDIR} ${WHEELDIR}

RUN pip install ${WHEELDIR}/* && \
    rm -rf ${BUILDDIR} ${WHEELDIR}

COPY --chown=${USER} . ${APP_DIR}
RUN pip install ${APP_DIR} && \
    rm -rf ${APP_DIR} 

USER ${USER}

ENTRYPOINT [ "/usr/local/bin/dumb-init", "--" ]


FROM pre-run AS odbc

USER root

RUN apt install -y gnupg && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt update && \
    apt install -y build-essential unixodbc-dev && \ 
    ACCEPT_EULA=Y apt install -y msodbcsql18

USER ${USER}

RUN pip install pyodbc==4.0.32


FROM pre-run AS run

RUN echo ready!
