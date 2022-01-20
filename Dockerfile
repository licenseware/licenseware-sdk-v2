# STAGE 0: base image
FROM python:3.8-slim-buster AS base

LABEL author="Meysam Azad <meysam@licenseware.io>"

ARG WHEELDIR=/wheelhouse
ARG BUILDDIR=/build
ARG REQUIREMENTS=requirements.txt

ENV BUILDDIR=${BUILDDIR}
ENV WHEELDIR=${WHEELDIR}
ENV REQUIREMENTS=${REQUIREMENTS}

RUN pip install -U pip && apt update && apt install -y curl gcc


# STAGE 1: fetch dependencies
FROM base AS build

COPY ${REQUIREMENTS} ${BUILDDIR}/
RUN pip wheel -r ${BUILDDIR}/${REQUIREMENTS} -w ${WHEELDIR}


# STAGE 2: ready to run the server
FROM base AS run

ARG ENV=development
ARG USER=licenseware
ARG SERVICEDIR=/home/${USER}
ARG PORT=5000
ARG DUMB_INIT='https://github.com/Yelp/dumb-init/releases/download/v1.2.5/dumb-init_1.2.5_x86_64'
ARG APP_DIR=${SERVICEDIR}/app

RUN curl -Lo /usr/local/bin/dumb-init ${DUMB_INIT} && \
    chmod +x /usr/local/bin/dumb-init

RUN useradd -m ${USER}

ENV USER=${USER} \
    PORT=${PORT} \
    ENV=${ENV} \
    PYTHONUNBUFFERED=1

EXPOSE ${PORT}
WORKDIR ${SERVICEDIR}

COPY --from=build ${BUILDDIR} ${BUILDDIR}
COPY --from=build ${WHEELDIR} ${WHEELDIR}

RUN pip install -U --no-cache-dir -f ${WHEELDIR} -r ${BUILDDIR}/${REQUIREMENTS} && \
    rm -rf ${BUILDDIR} ${WHEELDIR}

COPY --chown=${USER} . ${APP_DIR}
RUN pip install ${APP_DIR} && rm -rf ${APP_DIR}

USER ${USER}

ENTRYPOINT [ "/usr/local/bin/dumb-init", "--" ]
