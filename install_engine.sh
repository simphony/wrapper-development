#!/bin/bash
#
# Author: Contact info
#
# Description: This script installs some engine and its Python binding
#              Used as part of the installation for some wrapper.
#
# Run Information: This script is run manually.

###################################
### Install engine requirements ###
###################################
./install_engine_requirements.sh

################################
### Download necessary files ###
################################
git clone url_of_git_repository

############################
### Perform installation ###
############################
mkdir something_maybe

################
### Clean up ###
################
rm -rf something_maybe

#########################
### Test installation ###
#########################
echo "It works!" | echo "It doesn't!"