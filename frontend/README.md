##Local

```
$ npm i
$ npm run dev
$ browser http://localhost:8080

```

##SERVER

###Start server from zero
```
$ cd /home/project/tvtracking
$ sudo npm i
$ sudo pm2 start prodServer.js
$ sudo pm2 logs prodServer

check 8080 port
```

###Restart server
```
$ cd /home/project/tvtracking
$ sudo npm i
$ sudo pm2 delete prodServer
$ sudo pm2 start prodServer.js
$ sudo pm2 logs prodServer

check 8080 port
```
