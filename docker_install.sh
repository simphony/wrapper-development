# Extract osp-version
osp_tag="v"
osp_tag+="$(python3 -c 'import packageinfo; print(packageinfo.OSP_CORE_MIN)')"
osp_tag+="-beta"
rm -rf temp_osp-core | true
# Download osp-core to temporary folder
git clone git@gitlab.cc-asp.fraunhofer.de:simphony/osp-core.git temp_osp-core
cd temp_osp-core
git checkout ${osp_tag}
docker build -t simphony/osp-core:${osp_tag} .
cd ..

# Build docker image
if docker build -t simphony/simwrapper --build-arg OSP_CORE_IMAGE=simphony/osp-core:${osp_tag} .
  then
    echo "Run 'docker run -ti simphony/simwrapper' to start the container"
  else
    echo "Something went wrong in the docker build. Check the error output."
fi
