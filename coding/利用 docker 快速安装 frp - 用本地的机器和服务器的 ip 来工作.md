

项目地址:
- [frp](https://github.com/fatedier/frp)        

## 一些参考

- [【1】Expose Local Server by FRP (Fast Reverse Proxy)](https://tofu.icu/archives/14)  
- [【2】基于 Docker 搭建 FRP 内网穿透开源项目（很简单哒）](https://linux.do/t/topic/494309)
- [【3】Exposing your local server to the internet over NAT using FRP](https://gabrieltanner.org/blog/port-forwarding-frp/)  
- [【4】frp 教程](https://www.xbfast.com/22/)    

由于考虑到引用链接可能会挂掉，我这里还是简单的记录一下自己的配置。

## frp 用来做什么

你有一个程序，你的服务器算力不足，无法运行或者速度无法接受。

你本地的机器能跑起来，你非常希望能向别人演示这样一个软件，但是你的本地机器没有公网 ip。

这个时候就可以利用 frp 将你本地端口穿透至公网端口，来实现用“服务器的 ip + 本地的算力”这样的组合。

皆大欢喜。

## frp 局限

目前我用的碰到的主要都是网络方面的局限。

因为不同于直接运行于服务器，数据交换为 A - B，frp 是 A - C - B 。仅仅只是多了一个中转，就对三方的上下行带宽都有比较高的要求。本地机器和服务器只要有一方上下行受限，就会导致传输文件慢。且如果是国内机器，国外服务器，可能还需要挂梯子，考虑因素更多。


## frp 快速安装

标题提到，这里会介绍用 docker 来部署的方式。我之前一直都是到 release 下载压缩包，解压，然后 systemctl 编写自动运行服务的。那样的确也可行，可以参考【4】。但是 docker 是更优雅的解法，如果服务器可以访问 dockerhub。

```shell
cd /opt
mkdir frp
cd frp
vim docker-compose.yml
```

> 你可以选择任何你喜欢的位置！

然后写入 docker-compose.yml

```yaml
services:
  frps:
    image: snowdreamtech/frps:0.61.2
    container_name: frps
    restart: always
    network_mode: host
    volumes:
      - ./frps.toml:/etc/frp/frps.toml
```


只需要注意修改 `frps:0.61.2` 的版本号即可，注意 frps 和 frpc 同版本。

之后 `docker-compose pull`:

```shell
root@xnne:/opt/frp# docker-compose pull
[+] pull 0/1
 ⠙ Image snowdreamtech/frps:0.61.2 Pulling                                         
```


## frp 配置

分为 frps.toml 和 frpc.toml, 分别代表 server 和 client, 即服务器和本地机器。

frps.toml:

```toml
# 客户端与服务连接端口
bindPort = 7000
# 客户端连接服务端时认证的密码
auth.token = "xnnehang"
# http协议监听端口,也是要反向代理的端口
vhostHTTPPort = 28080
# web界面配置
webServer.addr = "0.0.0.0"
webServer.port = 7500
webServer.user = "admin"
webServer.password = "admin"
```

之前我多服务反代 28080 端口时并不冲突，具体为什么我给忘了。等我部署完再补充。

frpc.toml:

```toml
serverAddr = "106.55.197.32"
serverPort = 7000
auth.token = "xnnehang"

[[proxies]]
name = "ollama"
type = "http"
customDomains = ["ollama.xnnehang.top"]
localIP = "0.0.0.0"
localPort = 11434

[[proxies]]
name = "ollama-server"
type = "tcp"
localIP = "0.0.0.0"
localPort = 11434
remotePort = 11434
```


这里演示了 `http` 和 `tcp` 两种穿透方式，如果给别人使用公网那么可以考虑用 http ，反代更友好。自己用可以 ip + port 访问，这样延迟和传输会更快。

## 运行 frps

```shell
root@xnne:/opt/frp# docker compose up
Attaching to frps
frps  | 2026-01-05 07:41:06.974 [I] [frps/root.go:105] frps uses config file: /etc/frp/frps.toml
frps  | 2026-01-05 07:41:07.158 [I] [server/service.go:237] frps tcp listen on 0.0.0.0:7000
frps  | 2026-01-05 07:41:07.159 [I] [server/service.go:305] http service listen on 0.0.0.0:28080
frps  | 2026-01-05 07:41:07.159 [I] [frps/root.go:114] frps started successfully
frps  | 2026-01-05 07:41:07.159 [I] [server/service.go:351] dashboard listen on 0.0.0.0:7500
```

访问 ip:7500 看看服务页面，登录时输入 user 和 password。

![服务面板](https://cdn.xnnehang.top/MrXnneHang/blog_img/refs/heads/main/BlogHosting/img/25/11/202601050945829.png)

反代参考 [# Termix - 一个很酷而且很方便的 Web-Based ssh 连接工具。](https://xnnehang.top/posts/default/termix)

反代 28080 端口，根据 frps.toml 里的配置。

## 演示和多服务

![lab.xnnehang.top](https://cdn.xnnehang.top/MrXnneHang/blog_img/refs/heads/main/BlogHosting/img/25/11/202601060926968.png)

另外可能好奇，frps 中只留了一个端口，会不会端口冲突。这里的结论是并不会。

因为在 http 连接的时候一般会自定义一个 `custom_domain`。只要这个不冲突， frp 就能正确链路到你的网页。

比如我再运行一个一样的程序，然后把它部署到 `test.xnnehang.top`。

![test.xnnehang.top](https://cdn.xnnehang.top/MrXnneHang/blog_img/refs/heads/main/BlogHosting/img/25/11/202601060954172.png)

```toml
[[proxies]]
name = "lab"
type = "http"
customDomains = ["lab.xnnehang.top"]
localIP = "0.0.0.0"
localPort = 8051


[[proxies]]
name = "test"
type = "http"
customDomains = ["test.xnnehang.top"]
localIP = "0.0.0.0"
localPort = 8050
```

这是我 proxy 的配置，反代的也都是 28080, 最后可以看到它们并没有端口冲突。

之后可以尽情专注于开发了！只要本地能跑，服务器上也不必担心受到算力限制。

