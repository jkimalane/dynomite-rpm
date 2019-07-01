# dynomite-rpm
Bits and pieces for packaging Netflix Dynomite into RPM package

### Notes
* The release tarball from Netflix/dynomite repo needs to be repacked to include file `VERSION` otherwise compiled version will not include valid version number. By default the version related data is fetched from the project's git tag. The release tarball is a clean export and does not contain git repo.
