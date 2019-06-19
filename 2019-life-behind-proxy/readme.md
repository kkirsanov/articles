
## How to install Ubuntu on Windows WLS(Windows Linux Subsystem) behind proxy

1. Enable Windows Linux subsystem(WLS) - Win+S->"Turn windows Feautures On and Off"->Windows Linux subsystem
2. Install Ubuntu from Microsoft Store
3. ```echo "Acquire::http::Proxy \"http://your.proxy.address\";" | sudo tee -a /etc/apt/apt.conf.d/proxy.conf```
4. ```echo "http_proxy=http://your.proxy.address.net" | sudo tee -a /etc/enviroment```
5. ```echo "https_proxy=http://your.proxy.address.net" | sudo tee -a /etc/enviroment```
6. ```sudo apt install python3 python3-pip```



## How to install Docker on Windows behind proxy

1. Enable Hyper: Win+S->"Turn windows Features On and Off"->HyperV
2. Register on docker hub - https://hub.docker.com/ and install  Docker Desktop
3. During install uncheck "Create desktop shortcut".
4. Check proxy settings - правая ПКМ на иконке в Tray->Docker->settings->Proxy
5. Save environment variables into proxy.txt in home folder
```
http_proxy=http://your.proxy.address
https_proxy=http://your.proxy.address
ftp_proxy=
no_proxy=localhost,127.0.0.1
```
5. Run: ```docker run -it --env-file ./proxy.txt ubuntu```
6. Sometimes Credential Manager are buggy. In this case go ```Control Panel\User Accounts\Credential Manager```
and in ```Windows Credentionals``` remove all records with ```dokcer```
7. In docker settings check "Expose daemon on tcp://localhost:2375 without TLS"

## How to setup gitlab behind proxy
Change ```C:/users/User.Name/.gitconfig``` to 
```bash
[user]
    email = User.Name@rompany.com
    name = User Name
[http]
    proxy = http://your.proxy.address
[https]
    proxy = http://your.proxy.address
    sslVerify = false
[core]
    autocrlf = true
```

Sometimes Credential Manager are buggy. In this case go ```Control Panel\User Accounts\Credential Manager```
and in ```Windows Credentionals``` remove all records with ```gitlab```

## How to fix Haskell`s pthread problem
Copy```C:\Program Files\Haskell Platform\8.6.5\mingw\bin\libwinpthread-1.dll``` into pthread.dll in the same folder
