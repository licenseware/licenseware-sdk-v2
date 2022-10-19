# base image
FROM python:3.8-slim-buster AS base

LABEL author="Meysam Azad <meysam@licenseware.io>"

ARG BUILDDIR=/build
ARG WHEELDIR=/wheelhouse
ARG REQUIREMENTS=requirements.txt
ARG USER=licenseware
ARG UID=1000
ARG GID=1000
ARG HOMEDIR=/home/${USER}

ENV BUILDDIR=${BUILDDIR} \
    WHEELDIR=${WHEELDIR} \
    REQUIREMENTS=${REQUIREMENTS} \
    USER=${USER} \
    UID=${UID} \
    GID=${GID} \
    PATH=${HOMEDIR}/.local/bin:${PATH} \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

RUN pip install -U pip && \
    apt update && \
    apt install -y gcc libexpat1

RUN groupadd -g ${GID} ${USER} && \
    useradd -u ${UID} -g ${GID} -m ${USER}

FROM curlimages/curl AS entrypoint

ARG DUMB_INIT='https://github.com/Yelp/dumb-init/releases/download/v1.2.5/dumb-init_1.2.5_x86_64'

USER root
RUN curl -sSLo /usr/local/bin/dumb-init ${DUMB_INIT} && \
    chmod +x /usr/local/bin/dumb-init

# fetch dependencies
FROM base AS build

COPY ${REQUIREMENTS} ${BUILDDIR}/
RUN pip wheel -r ${BUILDDIR}/${REQUIREMENTS} -w ${WHEELDIR}

# final image
FROM base AS run

ARG HOMEDIR
ARG SDKDIR=${HOMEDIR}/sdk
ARG SERVICEDIR=${HOMEDIR}/service
ARG FILE_UPLOAD_PATH=/tmp/lware
ARG PORT=5000

EXPOSE ${PORT}
VOLUME ${FILE_UPLOAD_PATH}

COPY --from=entrypoint /usr/local/bin/dumb-init /usr/local/bin/dumb-init
COPY --from=build ${BUILDDIR} ${BUILDDIR}
COPY --from=build ${WHEELDIR} ${WHEELDIR}

RUN mkdir -p ${FILE_UPLOAD_PATH} ${SERVICEDIR} && \
    chown ${USER}:${USER} ${FILE_UPLOAD_PATH} ${SERVICEDIR} && \
    pip install ${WHEELDIR}/* && \
    rm -rf ${BUILDDIR} ${WHEELDIR}

COPY --chown=${USER} . ${SDKDIR}
RUN pip install ${SDKDIR} && \
    rm -rf ${SDKDIR}

WORKDIR ${SERVICEDIR}
USER ${USER}

ENTRYPOINT [ "/usr/local/bin/dumb-init", "--" ]
