- [ ] <a href="https://xnnehang.top/">

  <div align="center">
      <img src="https://fastly.jsdelivr.net/gh/MrXnneHang/blog_img/BlogHosting/img/25/02/202505101919055.png" alt="yutto-uiya" width="180" height="172">
  </div>
  <h1 align="center">yutto-uiya</h1>

  </a>
  <br/>

  <div align="center">
  <a href="https://github.com/astral-sh/uv"><img alt="uv" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json&style=flat-square"></a>
  <a href="https://github.com/astral-sh/ruff"><img alt="ruff" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=flat-square"></a>
  <a href="https://gitmoji.dev"><img alt="Gitmoji" src="https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67?style=flat-square"></a>
  <a href="https://github.com/casey/just"><img alt="just" src="https://img.shields.io/badge/just-🤖-yellow?style=flat-square&logoWidth=20"></a>
  <a href="https://streamlit.io/"><img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white&style=flat-square"></a>
  <br/>
  </div>

  <p align="center">
   这里是为 yutto 开发的 WebUI!<br>
  </p>

  <p align="center">
  <a href='https://xnnehang.top/posts/default/yutto_uiya_v1_1_2_guide' style='font-size: 20px;'><strong>文档</strong></a> ·
  <a href='https://www.bilibili.com/video/BV1vzEtzNEAx/'><strong>演示视频</strong></a>
  </p>
  <p align="center">
    <a href="#预览"><strong>预览</strong></a> ·
    <a href="#本地部署"><strong>本地部署</strong></a> ·
    <a href="#如何使用"><strong>如何使用</strong></a>
  </p>

  ## 为什么开发 ?

  我先前用过 downkyi,JJdown.共同的问题就是,我自己没能力改源代码。downkyi 是`C#`开发的，而 JJdown 似乎是闭源的。每次 b 站上的朋友问我说"为啥子突然不行了"，我也只能说我去向作者反馈一下，然后去提一个 Issue。<br>

  但对于 yutto, 我可以尝试自己修复和维护, 也从中学到了很多。<br>

  # 支持项:

  -  [x] [用户投稿单个视频](https://www.bilibili.com/video/BV1mUBXYeE1h/?spm_id_from=333.1387.homepage.video_card.click&vd_source=d7601f0fc447d708fff71aa75186ea10)
  -  [x] [用户投稿视频列表](https://www.bilibili.com/video/BV1Hp4y1M7gq/?spm_id_from=333.1387.top_right_bar_window_custom_collection.content.click)
  -  [x] [收藏夹](https://space.bilibili.com/100969474/favlist?fid=1306978874&ftype=create)
  -  [x] [合集](https://space.bilibili.com/100969474/lists/1947439?type=series)
  -  [x] [up 空间](https://space.bilibili.com/100969474)
  -  [x] [番剧](https://www.bilibili.com/bangumi/play/ss48029?from_spmid=666.4.mylist.2)
  -  [x] [课程](https://www.bilibili.com/cheese/play/ss63429?csource=common_myclass_purchasedlecture_null&spm_id_from=333.874.selfDef.mine_paid_list)

  但有个前提, 所有支持项最终能否被获取到都取决于用户本身是否具有对该资源的访问权限, 比如是否是大会员, 是否是购买了课程.

  ## 预览：

  ![](https://cdn.xnnehang.top/MrXnneHang/blog_img/refs/heads/main/BlogHosting/img/25/02/202505091128956.png)
  ![](https://cdn.xnnehang.top/MrXnneHang/blog_img/refs/heads/main/BlogHosting/img/25/02/202505131622249.png)
  ![](https://cdn.xnnehang.top/MrXnneHang/blog_img/refs/heads/main/BlogHosting/img/25/02/202505191248006.png)
  ![](https://cdn.xnnehang.top/MrXnneHang/blog_img/refs/heads/main/BlogHosting/img/25/02/202505191249700.png)

  ## 本地部署:

  ### 1.安装前置:

  > 如果你是 windows 用户, 那么可以考虑先安装 [scoop](https://scoop.sh/) ,它可以让你更方便的安装下面的工具.<br>
  > 仅需在 powershell 中运行:<br>
  >
  > ```
  > Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  > Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expressionb
  > ```

  <details closed>
  <summary><b>ffmpeg #</b><br>

  在合并音视频为视频, 以及转换音视频格式的时候, 均使用到了 `ffmpeg`。你可以选择全局安装或者在设置中配置 `ffmpeg` 的所在路径.<br>

  </summary>

  对于`mac/linux`用户:<br>

  ```shell
  brew install ffmpeg # mac
  sudo apt install ffmpeg # linux
  scoop install ffmpeg # windows
  ```

  或者你也可以直接把 `ffmpeg` 可执行文件路径写到设置的 `ffmpeg_path` 中, 并且保存设置。<br>

  </details>

  <details closed>
  <summary><b>uv #</b><br>

  本项目完全使用 `uv` 管理, 所以需要安装 `uv`.<br>

  </summary>

  请参考它的[**安装文档**](https://docs.astral.sh/uv/getting-started/installation/).

  ```shell
  scoop install uv # windows
  curl -LsSf https://astral.sh/uv/install.sh | sh # linux / mac
  ```

  只需要保证全局环境下 uv 可访问即可: <br>

  ```shell
  xnne@xnne-PC:~$ uv -V
  uv 0.7.0
  ```

  </details>

  <details closed>
  <summary> <b>just(可选) #</b> <br>
  just 是一款用 rust 编写的简单易用的命令执行工具，通过它可以方便地执行一些开发时常用的命令。<br>
  </summary>

  对于 `mac/linux` 用户:<br>

  ```shell
  brew install just # mac
  sudo apt install just # linux
  
  scoop install git # 先利用 git 获取 sh 的特性
  scoop install just # windows
  ```

  对于 windows 用户来说, 也可以考虑写入 `.bat` 文件来替代.

  </details>

  ### 2.克隆仓库

  ```shell
  git clone https://github.com/XnneHangLab/yutto-uiya.git
  cd yutto-uiya
  ```

  ### 3.使用镜像源(可选)

  默认使用的 python 下载源是从 github, packages index 是 pypi.

  如果你的机器在国内, 你可以通过修改 `pyproject.toml` 来使用国内的源.

  修改这几行:

  ```toml
  [tool.uv]
  # 下载 Python 的镜像
  python-install-mirror = "https://github.com/astral-sh/python-build-standalone/releases/download" # 使用官方的镜像, 直接从 github 安装, 需要连接外网, 官方默认配置
  # python-install-mirror = "https://mirror.nju.edu.cn/github-release/indygreg/python-build-standalone/" # 使用南京大学的镜像, 可能需要更新 uv 到新版本.
  
  
  # 默认使用 pypi 源
  [[tool.uv.index]]
  # 清华源
  # name = "tsinghua"
  # url = "https://pypi.tuna.tsinghua.edu.cn/simple"
  # default = true
  
  # pypi 源, 官方默认实际上就是这个配置
  name = "pypi"
  url = "https://pypi.org/simple"
  default= true
  ```

  改为这样即可:

  ```toml
  [tool.uv]
  # python-install-mirror = "https://github.com/astral-sh/python-build-standalone/releases/download" # 使用官方的镜像, 直接从 github 安装, 需要连接外网, 官方默认配置
  python-install-mirror = "https://mirror.nju.edu.cn/github-release/indygreg/python-build-standalone/" # 使用南京大学的镜像, 可能需要更新 uv 到新版本.
  
  # 默认使用 pypi 源
  [[tool.uv.index]]
  # 清华源
  name = "tsinghua"
  url = "https://pypi.tuna.tsinghua.edu.cn/simple"
  default = true
  
  # pypi 源, 官方默认实际上就是这个配置
  # name = "pypi"
  # url = "https://pypi.org/simple"
  # default= true
  ```

  ### 4.启动程序:<br>

  ```shell
  just start # 如果你安装了 just
  
  # 如果没有安装 just
  uv lock
  uv sync
  uv run streamlit run src/uiya/yutto_uiya.py
  ```

  该过程会自动安装依赖, 第一次启动可能较久, 你只需要耐心等待即可. 有安装问题欢迎反馈~

  ## 如何使用:

  参考[使用手册](docs/guide.md)

  ## 待开发:

  -  [x] 提供单独下载音频、视频、弹幕、封面的勾选项。放在 webui 中。
  -  [x] 结合 nfo 显示部分视频信息。
  -  [x] 提供手动选集。
  -  [ ] 提供不同的保存格式。
  -  [x] 加入覆盖下载。（目前当下载已下载的视频不同清晰度，会跳过。无法下载不同清晰度。）
  -  [x] 首次运行自动创建配置文件
  -  [x] Typing, 优化代码结构, 让代码变得优雅.
  -  [ ] release as a python lib
  -  [ ] 提高解析速度.
  -  [x] 简化安装步骤.
  -  [ ] 可增添的任务列表 / 按任务列表启动下载