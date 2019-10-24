#!/bin/bash
#
# Author: Contact info
#
# Description: This script install the requirements for some engine
#              Used as part of the installation for some wrapper.
#
# Run Information: This script is called by install_engine.sh

echo "Installing necessary requirements for the engine"
platform=$(python -mplatform)

case $platform in
  *"Ubuntu"*)
    sudo apt-get update
    # Add commands for Ubuntu here
  ;;
  # Add other platforms here
esac