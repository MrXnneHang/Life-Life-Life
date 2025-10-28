## 问题：

在 wsl2 的 Ubuntu-24.04 中，我尝试运行:

```shell
sudo apt update && sudo apt install curl software-properties-common
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# 确保这一行是针对 JAZZY 和 Noble (24.04)
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu noble main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

但是它仅仅只是在第一步 `sudo apt update` 的时候就经常卡在 `[0%] waiting for headers`。

而几乎每个 Get 都会停顿十秒以上，导致一个 update 持续了十几分钟依然没有结束。

期间更换了香港，日本，美国的代理，没有改善。

![waiting_for_headers](../dist/img/waiting_for_headers.png)

## 原因和解决

https://www.reddit.com/r/Ubuntu/comments/oqqyek/waiting_for_headers_0/

`Changing mirror from http to https worked for me :)`

似乎是 source 源的 URL 都是 http 而非 https 造成的。

我将这两个文件内修改为 https 后得到了解决:

```shell
xnne@DESKTOP-3I1GRP0:/mnt/c/Users/Zhouyuan$ sudo vim /etc/apt/sources.list.d/
ros2.list       ubuntu.sources
xnne@DESKTOP-3I1GRP0:/mnt/c/Users/Zhouyuan$ sudo vim /etc/apt/sources.list
```

最后在半分钟内完成了 update。