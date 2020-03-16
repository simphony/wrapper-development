ARG OSP_CORE_IMAGE=simphony/osp-core:latest
FROM $OSP_CORE_IMAGE
LABEL maintainer="your.name@domain.foo"
LABEL dockerfile.version="2.3"

ADD . /simphony/wrappers/simwrapper
WORKDIR /simphony/wrappers/simwrapper

# Install requirements
RUN apt-get update && apt-get install -y \
    <packages>

# Install engine
RUN echo "Install the engine here"
# If you use some library to connect to the engine via python, you might
#  want to install it too
RUN echo "also the python binding, when relevant (syntactic layer)"

# Install simwrapper
RUN python setup.py install
# Maybe you also need to install some ontology
RUN pico install ontology.simwrapper.yml
