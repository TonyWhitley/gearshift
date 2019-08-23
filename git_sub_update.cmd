echo git bash commands to update submodules to latest
rem Automated login
git config --global credential.helper wincred

git submodule update --remote --merge --recursive pyDirectInputKeySend                                                 
git submodule update --remote --merge --recursive pyRfactor2SharedMemory                               
git push
