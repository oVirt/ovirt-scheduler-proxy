#!/bin/bash -xe

# Set the location of the JDK that will be used for compilation:
export JAVA_HOME="${JAVA_HOME:=/usr/lib/jvm/java-11}"

[[ -d exported-artifacts ]] \
|| mkdir -p exported-artifacts

[[ -d rpmbuild ]] \
|| mkdir -p rpmbuild

make clean all
make dist
rpmbuild \
    --define "_topmdir $PWD/rpmbuild" \
    --define "_rpmdir $PWD/rpmbuild" \
    -ta *.tar.gz

# Move RPMs to exported artifacts
find rpmbuild -iname \*rpm -exec mv "{}" exported-artifacts/ \;
cp -l *.tar.gz exported-artifacts/
