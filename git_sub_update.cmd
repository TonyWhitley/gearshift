echo git bash commands to update submodules to latest
rem Automated login
git config --global credential.helper wincred

git submodule update --remote --merge pyDirectInputKeySend                                                 
git submodule update --remote --merge pyRfactor2SharedMemory                               
git push
