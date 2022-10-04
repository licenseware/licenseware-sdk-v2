import os

from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.readlines()


VERSION = os.getenv("PACKAGE_VERSION", "2.0.3")


EXTRAS = {
    "honcho": [
        "honcho==1.0.1",
    ],
    "mongita": [
        "mongita==1.1.1",
    ],
    "opentelemetry": [
        "opentelemetry-distro==0.26b1",
        "opentelemetry-instrumentation==0.26b1",
        "opentelemetry-exporter-otlp==1.7.1",
    ],
    "kafka": [
        "confluent-kafka==1.9.0",
    ],
    "trend-app": [
        "trend-app-protect==4.6.2",
    ],
    "watchdog": [
        "dramatiq[watch]",
    ],
}

setup(
    name="licenseware",
    version=VERSION,
    description="Common utilities for licenseware.",
    url="https://licenseware.io/",
    author="Licenseware",
    author_email="contact@licenseware.io",
    license="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=REQUIREMENTS,
    packages=find_packages(where=".", exclude=["tests"]),
    include_package_data=True,
    package_data={"": ["*"]},
    entry_points={
        "console_scripts": [
            "licenseware=licenseware.cli:cli_entrypoint",
        ],
    },
    extras_require=EXTRAS,
)
