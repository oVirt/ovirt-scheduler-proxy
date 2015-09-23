#!/bin/bash -xe
[[ -d exported-artifacts ]] \
|| mkdir -p exported-artifacts

[[ -d rpmbuild ]] \
|| mkdir -p rpmbuild

make dist
rpmbuild \
    --define "_topmdir $PWD/rpmbuild" \
    --define "_rpmdir $PWD/rpmbuild" \
    -ta *.tar.gz

# Move RPMs to exported artifacts
find rpmbuild -iname \*rpm -exec mv "{}" exported-artifacts/ \;
cp -l *.tar.gz exported-artifacts/