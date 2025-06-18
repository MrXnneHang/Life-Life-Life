
## 具体报错: 

```shell
The Docker Desktop WSL data distro drive is missing.

If this issue persists, run "wsl --unregister docker-desktop-data" before restarting Docker Desktop. Note that unregistering the data distro will delete any previously created containers.

bootstrapping in the main distro: WSL data distro drive is missing
```

唔， 英语终究不是我的母语，看上去终究不如直接看中文清晰。所以应该先尝试部署个 deeplx 服务先。

```shell
Docker Desktop WSL 数据发行版驱动器丢失。

如果此问题仍然存在，请在重启 Docker Desktop 之前运行“wsl --unregister docker-desktop-data”。请注意，取消注册数据发行版将删除所有先前创建的容器。

在主发行版中引导：WSL 数据发行版驱动器丢失
```

原因似乎是 WSL 服务没打开。

我在这里找到了原因: [# Docker Desktop - Unexpected WSL error](https://www.reddit.com/r/docker/comments/1ft6u6f/docker_desktop_unexpected_wsl_error/):

Found this via Google since I had the same problem. It happened after updating Docker. 
Running `wsl --list --verbose` resulted in

```shell 
NAME              STATE           VERSION
* Ubuntu            Stopped         2
* docker-desktop    Uninstalling    2
```
Seems that during the update the docker-desktop distribution got stuck.
Running `wsl --unregister docker-desktop` and restarting Docker solved it.

---


而解法似乎就在报错中，按照它提示的一番操作:

```shell
PS D:\tmp> wsl -l -v
  NAME                   STATE           VERSION
* docker-desktop-data    Stopped         2
  docker-desktop         Stopped         2
  Ubuntu-20.04           Stopped         2
PS D:\tmp> wsl --unregister docker-desktop-data
正在注销。
操作成功完成。
PS D:\tmp> wsl -l -v
  NAME              STATE           VERSION
* docker-desktop    Running         2
  Ubuntu-20.04      Stopped         2
```

然后重开就很容易地解决了。

emmmm, 其实我要记得不是这些。当然也许之后时间久了依然有用。

我只是在反思一件事情，最近长久以来我记录得文档稀碎，甚至觉得大部分内容实际上一点都不值得记录。

这的原因大概率是因为我越来越依赖 LLM ,以及 LLM 对于我的问题的解决率越来越高了。直到前段时间有一个下午，我被迫断了 claude , gemini, grok, gpt 的所有供应。那个下午我一直处于低迷状态，我明明很清楚自己想做什么， 但是到要写的时候我一个 commit 也写不出来。因为长久以来我都是先描绘需求，然后把模块让大模型写，之后再自己修一下 lint, 调整下结构。我更像是一个 Code Reviewer 而大模型是我的 Coder （这么说也许有点奇怪，但是我确实一直那么做），但没了大模型后我发现自己实际上就连一个 ffmpeg 的调用都写不好...

而从昨天开始暂时截断大模型，我再次恢复从视频，博客中获取内容，也许联网大模型可以有，因为它可以帮我更快地找到我想要的内容。

原本今天这个内容如果让大模型来看的话，大概率是会解决的。但我不依赖它，让我这么久以来又一次地恢复了对记录的热情。

