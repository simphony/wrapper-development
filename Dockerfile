# This is a template Dockerfile in case you want to offer your users the
# possibility to run your wrapper using Docker (for example, this may be handy
# when the installation of a required simulation engine is complicated)

FROM python:3.10
LABEL org.opencontainers.image.authors="you@domain.org"

ADD . /simphony/wrappers/package-name
WORKDIR /simphony/wrappers/package-name

# Install requirements
RUN apt-get update && apt-get install -y \
    <packages>

# Install engine and engine dependencies (if not available via `apt-get`)
RUN echo "Install the engine here"

# Install your package. Dependencies, including `simphony-osp` will be
# automatically installed.
RUN pip install .
# Maybe you also need to install a specific ontology that your wrapper makes
# use of (like `package_name/ontology.yml` for this prototype wrapper example).
RUN pico install some_ontology_maybe.yml
