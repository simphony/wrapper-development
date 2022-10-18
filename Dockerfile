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
# Maybe you also need to install an ontology
RUN pico install some_ontology_maybe.yml
