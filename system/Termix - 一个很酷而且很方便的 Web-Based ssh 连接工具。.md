## 前言（一些废话）

前几天我的室友给我看了一个在网页部署的类似 Termius 的应用，当时看了之后感到非常惊奇，功能非常完整， sftp 也支持， upload 和 download 均可，而且可视化完全仿照了 termius，但是它可以运行在本地端口并且在网页端访问。

仓库地址：

https://github.com/Termix-SSH/Termix

这意味把它公网部署着不少方便之处：

- 更换到新设备或者新的系统不需要费力安装软件，并且不用再看一遍 ip 与密码。
- 如果使用别人的设备不必留痕。
- 最重要的是不用被 termius 的偶尔抽风自己卸载自己而烦恼。

我先后用过宝塔面板的 ssh 连接和 Termius，当然运营商自带的就不提了，腾讯服务器扫码都快扫吐了。

初用 Termius 会觉得它设计得很漂亮，光是终端风格的选择就够我玩半天，以及许多 UI 元素都很现代化和优美，看得很舒服，这是我一直坚持使用它的原因。但是前面提到过，它有时候会自己抽风，把自己卸载掉，而且是清空所有缓存的那种写在，所有机器都得再导入一次。就像百度网盘那样。

当然，这里也有一个悖论。如果我部署 Termix 的服务器内部错误，然后我的 Termix 用不了，我依然得用 termius 来连，这没得避。

喜新厌旧，始乱终弃这一块。

让我们开始部署环节。

如果你希望先看看部署后的结果，可以看看最后的 `一些截图`, 以及如果你放心，你甚至可以直接用我部署的面板 =-=//(我能有什么坏心思呢)。

## 超简单的本地部署过程。

如果你曾经用过 docker 和 docker-compose 。

那么部署它就非常容易，如果没有用过，那么请稍等，我简单补充一下 docker 和 docker-compose 的安装。

### 准备工作：docker 和 docker-compose 安装

摘自 [Mix-Space部署最新后端Core](https://www.vlo.cc/posts/jc/mix-deploy)

> 若服务器在国外且需要使用1Panel，可以直接运行1Panel安装脚本，一把梭安装1Panel和Docker / Docker-Compose

首先，安装一些必要的软件包：

```shell
apt updateapt upgrade -yapt install curl vim wget gnupg dpkg apt-transport-https lsb-release ca-certificates
```

然后加入 Docker 的 GPG 公钥和 apt 源：

```shell
curl -sSL https://download.docker.com/linux/debian/gpg | gpg --dearmor > /usr/share/keyrings/docker-ce.gpgecho "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-ce.gpg] https://download.docker.com/linux/debian $(lsb_release -sc) stable" > /etc/apt/sources.list.d/docker.list
```

国内机器可以用清华 TUNA 的国内源：

```shell
curl -sS https://download.docker.com/linux/debian/gpg | gpg --dearmor > /usr/share/keyrings/docker-ce.gpgecho "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-ce.gpg] https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/debian $(lsb_release -sc) stable" > /etc/apt/sources.list.d/docker.list
```

然后更新系统后即可安装 Docker CE

```shell
apt updateapt install docker-ce docker-ce-cli containerd.io
```

我们可以使用 Docker 官方发布的 Github 直接安装最新版本docker-compose：

```shell
curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-Linux-x86_64 > /usr/local/bin/docker-composechmod +x /usr/local/bin/docker-compose
```

此时可使用 `docker-compose version` 命令检查是否安装成功

### 正式工作

在一个想存放的目录，比如 `/opt/termix`。写入 `compose.yml` :

```yaml
services:
  termix:
    image: ghcr.io/lukegus/termix:latest
    container_name: termix
    restart: unless-stopped
    ports:
      - "8080:8080"
    volumes:
      - termix-data:/app/data
    environment:
      PORT: "8080"

volumes:
  termix-data:
    driver: local
```

然后拉取镜像:

```shell
root@ser351791695801:/opt/termix# docker compose pull
[+] pull 19/19
 ✔ Image ghcr.io/lukegus/termix:latest Pulled    
```

最后运行镜像:

```shell
root@ser351791695801:/opt/termix# docker compose up
[+] up 3/3
 ✔ Network termix_default    Created                                                                             0.1s 
 ✔ Volume termix_termix-data Created                                                                             0.0s 
 ✔ Container termix          Created                                                                             0.1s 
Attaching to termix
termix  | Configuring web UI to run on port: 8080
termix  | SSL disabled - using HTTP-only configuration (default)
termix  | Starting nginx...
termix  | Starting backend services...
termix  | [7:35:12 AM] [INFO] [📦] Termix Backend starting - Version: 1.9.0 [op:startup]
termix  | [7:35:12 AM] [SUCCESS] [🗄️] JWT secret auto-generated and saved to .env [op:jwt_auto_generated]
termix  | [7:35:12 AM] [SUCCESS] [🗄️] Database key auto-generated and saved to .env [op:db_key_auto_generated]
termix  | [7:35:12 AM] [SUCCESS] [🗄️] Internal auth token auto-generated and saved to .env [op:internal_auth_auto_generated]
termix  | [7:35:12 AM] [INFO] [🚀] SSL not enabled - skipping certificate generation [op:ssl_disabled_default]
termix  | [7:35:12 AM] [INFO] [🗄️] Initializing SQLite database [op:db_init]
termix  | [7:35:12 AM] [SUCCESS] [🗄️] Schema migration completed [op:schema_migration]
termix  | [7:35:14 AM] [INFO] [📡] Found 0 autostart hosts and 0 total hosts for endpointHost resolution
Gracefully Stopping... press Ctrl+C again to force
```

如果没有报错信息抛出。就可以 Ctrl+C 中断然后进行后台运行:

```shell
root@ser351791695801:/opt/termix# docker compose up -d
[+] up 1/1
 ✔ Container termix Running    
```

这样程序就会在终端关闭时保活。


> 我当时挺好奇，为什么有的人会写 compose.yml, 有的人会写 compose.yaml, 有的人写 docker-compose.yml。但似乎都能被 `docker compose pull` 识别。

然后经 gemini 提醒，是因为它会根据优先级自动搜寻:

![compose file 搜索机制](https://cdn.xnnehang.top/MrXnneHang/blog_img/refs/heads/main/BlogHosting/img/25/11/202512291042933.png)

这样也避免了两个以上 compose 文件冲突的问题。

## 公网部署

这里我仅仅演示我最常用的一种方式：

1panel 反向代理。你也可以用你自己的方式进行部署。

1panel 安装：

```shell
https://1panel.cn/
```

它的在线安装脚本不支持很多旧系统，我的 ubuntu 20.04 都不行，可能和地区有关。然后幽默地给我发了个付费把安装包发到邮箱的选项。

- 1panel 应用商店安装 openresty
- 新建 DNS 记录。 A 记录，主机记录 ssh， 记录值为所部署服务器公网 ip。
- 网站创建反向代理，代理 127.0.0.1:8080, 如果 compose.yml 没改端口的话。域名写 `ssh.xnnehang.top`, 取决于你的 DNS 记录和自己的域名。
- 申请证书，需要绑定 DNS 账户，如果是在腾讯买的， 可以在这里新建或者查看 ACESS KEY 和 ACESS ID。[API 密钥管理](https://console.cloud.tencent.com/cam/capi)

![添加 DNS 账户](https://cdn.xnnehang.top/MrXnneHang/blog_img/refs/heads/main/BlogHosting/img/25/11/202512291043494.png)


随后申请证书时勾选跳过 DNS 校验即可。

![申请证书](https://cdn.xnnehang.top/MrXnneHang/blog_img/refs/heads/main/BlogHosting/img/25/11/202512291043854.png)

- 最后在网站出开启 HTTPS 并且选择 ACME 账户（一般无需创建）和对应域名的证书即可。

![开启 https](https://cdn.xnnehang.top/MrXnneHang/blog_img/refs/heads/main/BlogHosting/img/25/11/202512291043299.png)

唯一注意点是**记得保存**。

相当喂饭了已经，主要也是想测一下"图床"稳定性。

## 一些截图

之后你就可以直接公网访问了，似乎是注册机制的，如果你想要用，也无不可 =-=，如果你放心，我欢迎。

![登录界面](https://cdn.xnnehang.top/MrXnneHang/blog_img/refs/heads/main/BlogHosting/img/25/11/202512291044412.png)

![系统信息面板](https://cdn.xnnehang.top/MrXnneHang/blog_img/refs/heads/main/BlogHosting/img/25/11/202512291055872.png)

![终端](https://cdn.xnnehang.top/MrXnneHang/blog_img/refs/heads/main/BlogHosting/img/25/11/202512291055842.png)

![sftp](https://cdn.xnnehang.top/MrXnneHang/blog_img/refs/heads/main/BlogHosting/img/25/11/202512291057168.png)

值得一玩 =-=//

这个 UI 我也很喜欢，颜控在此。

下次见。