FROM ghcr.io/licenseware/licenseware-sdk-v2:latest

COPY . .
RUN opentelemetry-bootstrap --action=install

CMD ["./docker-entrypoint.sh"]
