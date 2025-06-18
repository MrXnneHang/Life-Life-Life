## parsec connect error:  - 6023 - 6024 

### 原因

首先明确原因，其实就是被连接的 host 方没有公网 ip 或者双方均没有公网 ip.
### 解决方法

使用贝锐蒲公英组网。或者其他的组网方式。因为蒲公英可以不必自己有一个公网服务器。并且它对 deepin 支持很不错，个人用户支持三台设备授权。

### 步骤

下载并且安装:

```shell
wget https://pgy.oray.com/softwares/153/download/2549/PgyVisitor-6.9.0-amd64.deb
sudo dpkg -i PgyVisitor-6.9.0-amd64.deb
```

login - autologin - getmbrs

```shell
➜  Downloads pgyvisitor
Copyright © 2002-2024 Oray. All Rights Reserved.

-h --help 使用帮助
-v --version 获取版本

以下是常见的 pgyvisitor 命令

login         登录
logout        退出
logininfo     显示历史登录设备信息
autologin     设置自动登录
certcheck     启用或禁用证书检验
bypass        显示旁路信息
getmbrs       显示组网成员信息
setdefaultmac 设置默认mac
showsets      显示设置
```

在此之前，你可能需要先到蒲公英控制台那里添加设备。

`https://console.sdwan.oray.com/zh/sdwan/softwareMember`

对于 windows 端的蒲公英， 登录后会自动添加设备。 如果设备超限可以在这里移除。

对于 linux 我们需要手动添加设备， `软件成员` -> `成员列表` -> `添加成员` , 名称密码随便填，可以记住就行，手机号选填。只要注意网络选择和目标计算机(我们的 host )处于同一个网络下即可。添加的成员默认就是该设备。

之后在成员列表里把 UID/SID 点开并且复制。

之后就可以进入终端:

```shell
➜  Downloads pgyvisitor login
请输入贝锐账号/UID：
XXXXXXXX:002
请输入密码：
登录成功
```

如果你忘记了密码也可以点击成员重设。

autologin

```shell
➜  Downloads pgyvisitor autologin -y
自动登录开启
```

这样处理后，再次使用 parsec 就能成功连上了。