echo git bash commands to update submodules to latest
rem Automated login
git config --global credential.helper wincred

git submodule init pyDirectInputKeySend                                                 
git submodule init pyRfactor2SharedMemory                               
git push
