### To build the docker image,
```
$ sudo docker build -t kuanpern/dstat_server:latest .
```


### To run the server, do
```
$ sudo docker run -dt --name dstat  --restart unless-stopped \
  -p 7770:80 \
 kuanpern/dstat_server:latest \
  --refresh 86400 \
  --average 10 \
  --maxfiles 1000 \
  --password foobar
```
all arguments are optional
