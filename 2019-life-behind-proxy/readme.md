
## How to install Ubuntu on Windows WLS(Windows Linux Subsystem) behind proxy

1. Enable Windows Linux subsystem(WLS) - Win+S->"Turn windows Feautures On and Off"->Windows Linux subsystem
2. Install Ubuntu from Microsoft Store
3. ```echo "Acquire::http::Proxy \"http://your.proxy.addres:80\";" | sudo tee -a /etc/apt/apt.conf.d/proxy.conf```
4. ```echo "http_proxy=http://your.proxy.addres.net" | sudo tee -a /etc/enviroment```
5. ```echo "https_proxy=http://your.proxy.addres.net" | sudo tee -a /etc/enviroment```
6. ```sudo apt install python3 python3-pip```



## How to install Docker on Windows behind proxy

1. Enable Hyper: Win+S->"Turn windows Features On and Off"->HyperV
2. Register on docker hub - https://hub.docker.com/ and install  Docker Desktop
3. During install uncheck "Create desktop shortcut".
4. Check proxy settings - правая ПКМ на иконке в Tray->Docker->settings->Proxy
5. Save environment variables into proxy.txt in home folder
```
http_proxy=http://your.proxy.addres
https_proxy=http://your.proxy.addres
ftp_proxy=
no_proxy=localhost,127.0.0.1
```
5. Run: ```docker run -it --env-file ./proxy.txt ubuntu```
6. Sometimes Credential Manager buggy. In this case go ```Control Panel\User Accounts\Credential Manager```
and in ```Windows Credentionals``` remove all records with ```dokcer```
7. In docker settings check "Expose daemon on tcp://localhost:2375 without TLS"

## Install Haskell
1. Download an install Haskell Platform - https://www.haskell.org/platform/
2. Copy```C:\Program Files\Haskell Platform\8.6.5\mingw\bin\libwinpthread-1.dll``` into pthread.dll in the same folder