import os, re
from setuptools import setup, find_packages
from functools import reduce

# https://packaging.python.org/guides/distributing-packages-using-setuptools/?highlight=setup.py#setup-py
# Distribute py wheels
# python3 setup.py bdist_wheel sdist
# twine check dist/*
# cd dist
# twine upload *


with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.readlines()
    
    
    
VERSION = '2.0.2'


if os.path.exists("./CHANGELOG.md"):
    
    with open("CHANGELOG.md", "r") as f:
        changelog = f.read()

    if '# Changelog' in changelog:    
        version_match = re.match(f'#\s+Changelog\n+#+\s*\[((\d+\.\d+\.\d+))\]\(', changelog)
        if version_match:
            VERSION = version_match.group(1)


EXTRAS = {
    "tracing": [
        "opentelemetry-distro==0.26b1",
        "opentelemetry-instrumentation==0.26b1",
        "opentelemetry-exporter-otlp==1.7.1",
    ],
}
# NOTE: remove this when you find how to make the SDK private
EXTRAS_TMP_HACK = reduce(lambda lst1, lst2: lst1 + lst2, EXTRAS.values(), [])


setup(
    name="licenseware",
    version=VERSION,
    description="Common utilities for licenseware.",
    url="https://licenseware.io/",
    author="Licenseware",
    author_email="contact@licenseware.io",
    license='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=REQUIREMENTS + EXTRAS_TMP_HACK,
    packages=find_packages(
        where=".",
        exclude=["tests"]
    ),
    include_package_data=True,
    package_data={"": ["*"]},
    entry_points={
        'console_scripts': [
            'licenseware=licenseware.cli:cli_entrypoint',
        ],
    },
    # extras_require=EXTRAS,
)
