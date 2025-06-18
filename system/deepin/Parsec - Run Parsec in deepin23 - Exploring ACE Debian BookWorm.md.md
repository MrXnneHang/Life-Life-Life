今天正在打算改用 parsec 作为我的远程桌面工具。它很好的满足了我的需求，我家里的电脑是 windows, 作为 Server , 而我的 Client 是 deepin. Parsec 正好不支持 linux 作为 Server, 在这点上它完美满足了我的需求。


## 碰到的问题

但是我正在使用的 deepinv23 似乎并不兼容 parsec.

```shell
➜  Downloads neofetch
             ............                xnne@xnne-PC 
         .';;;;;.       .,;,.            ------------ 
      .,;;;;;;;.       ';;;;;;;.         OS: Deepin 23 x86_64 
    .;::::::::'     .,::;;,''''',.       Host: OMEN by HP Laptop 16-b1xxx 
   ,'.::::::::    .;;'.          ';      Kernel: 6.6.59-amd64-desktop-hwe 
  ;'  'cccccc,   ,' :: '..        .:     Uptime: 1 hour, 52 mins 
 ,,    :ccccc.  ;: .c, '' :.       ,;    Packages: 2361 (dpkg) 
.l.     cllll' ., .lc  :; .l'       l.   Shell: zsh 5.9 
.c       :lllc  ;cl:  .l' .ll.      :'   Resolution: 1920x1080, 1920x1080 
.l        'looc. .   ,o:  'oo'      c,   DE: DDE 
.o.         .:ool::coc'  .ooo'      o.   WM: KWin 
 ::            .....   .;dddo      ;c    Theme: deepin-dark [GTK2], Adwaita [GTK3] 
  l:...            .';lddddo.     ,o     Icons: flow [GTK2], Adwaita [GTK3] 
   lxxxxxdoolllodxxxxxxxxxc      :l      Terminal: deepin-terminal 
    ,dxxxxxxxxxxxxxxxxxxl.     'o,       CPU: 12th Gen Intel i7-12700H (20) @ 4.600GHz 
      ,dkkkkkkkkkkkkko;.    .;o;         GPU: NVIDIA GeForce RTX 3060 Mobile / Max-Q 
        .;okkkkkdl;.    .,cl:.           GPU: Intel Alder Lake-P GT2 [Iris Xe Graphics] 
            .,:cccccccc:,.               Memory: 8214MiB / 15650MiB 

                                                                 
                                                                 

➜  Downloads sudo dpkg -i parsec-linux.deb 
请输入密码:
验证成功
正在选中未选择的软件包 parsec。
(正在读取数据库 ... 系统当前共安装有 399458 个文件和目录。)
准备解压 parsec-linux.deb  ...
正在解压 parsec (150-97c) ...
dpkg: 依赖关系问题使得 parsec 的配置工作不能继续：
 parsec 依赖于 libjpeg8；然而：
  未安装软件包 libjpeg8。

dpkg: 处理软件包 parsec (--install)时出错：
 依赖关系问题 - 仍未被配置
正在处理用于 bamfdaemon (0.5.6+repack-1) 的触发器 ...
Rebuilding /usr/share/applications/bamf-2.index...
正在处理用于 desktop-file-utils (0.26-deepin) 的触发器 ...
正在处理用于 hicolor-icon-theme (0.17-2) 的触发器 ...
在处理时有错误发生：
 parsec

➜  Downloads sudo apt install libjpeg8   
正在读取软件包列表... 完成
正在分析软件包的依赖关系树... 完成
正在读取状态信息... 完成                 
您也许需要运行“apt --fix-broken install”来修正上面的错误。
下列软件包有未满足的依赖关系：
 libjpeg8 : 预依赖: multiarch-support 但无法安装它
E: 有未能满足的依赖关系。请尝试不指明软件包的名字来运行“apt --fix-broken install”(也可以指定一个解决办法)。
```

原因是 libjpeg8 似乎已经被弃用了。

参见这里:

[问题求助 deepin v23 beta3何时才能支持parsec？](https://bbs.deepin.org/zh/post/271236)

> 如果你比较急， 那么建议直接跳到最终我是如何解决的。因为我发现，尽管最开始我从 ACE Debian Bookworm 出发，但是最终 parsec 我是成功安装到我的宿主机里的 0.0 , 我这样算不算标题党呢。 总而言之，你可以直接在 deepin23 中安装和运行 parsec 的。下面一大坨就当是我探索一下 ACE Debian Bookworm 好了。但是，我的 deepinv23 并不是 beta3 版本的，我的 deepin 仅仅出现了 libjpeg8 的依赖缺失。<br>
> 在使用 ACE Debian BookWorm 我成功解决了所有依赖问题并且成功开启，但是似乎因为驱动问题并不能看见实际内容，只开起来了一个黑框框。

### 为什么使用 ACE Debian BookWorm

然后我又顺着一个版主的指路找到了这里：

[经验分享 使用ACE兼容环境运行应用的教程](https://bbs.deepin.org.cn/post/261794?_gl=1*1g7lmn*_ga*NDI3NjQxNTc2LjE3MzAwNzk5Njk.*_ga_QHZ7DPPD2D*czE3NDk5OTcxNzgkbzI1JGcxJHQxNzQ5OTk3Nzk5JGo2MCRsMCRoMA..)

原理类似于新开了一个 debian12 的容器， 并且它的容器还和主机共享一个文件系统。有点像开了一个 user 组然后单独放，使用体验上更像 Windows 的 WSL2, 直接使得 debian12 可以与宿主系统兼容，并且启动超级快。 
### 安装 ACE Debian Bookworm

又顺藤摸瓜找到了这里:

[ACE Debian Bookworm](https://gitee.com/amber-ce/amber-ce-bookworm/blob/master/README.zh.md)

```shell
git clone https://gitee.com/amber-ce/amber-ce-bookworm.git --recurse-submodules
```

先克隆后，我直接运行了:(具体可以参考它的 README，记得加 root 权限运行)

```shel
sudo apt build-dep .
sudo dpkg-buildpackage -us -uc -b 
```

之后进行了长达一个小时的构建后～

我发现作者已经提供了对 deepin23 的构建包.

`https://mirrors.sdu.edu.cn/spark-store/amber-ce/`

当然为了防止像上次那样作者炸了我也跟着炸了，所以部分重要内容我会直接跟着存档和转载。

如果你你也可以使用我的备份:

```shell
链接: https://pan.baidu.com/s/1sKnsGLa4l1lRb8n_JuVkUw?pwd=xnne
提取码: xnne 
```

主要是给自己留一手防备 0.0 .

我也不太晓得这俩 `cn.flamescion.bookworm-compatibility-mode_12.8.0_amd64.deb`,  `amber-ce-deepin23_23.7.0-fix1_amd64.deb` 是什么关系，不过能放在一起，我索性就一起装了。

另外，那个作者的温馨提醒: **首次安装后请注销或重启以展示启动器入口**

我是照做了， 如果你出现了什么奇奇怪怪的问题也可以尝试照做。

启动! 并且运行 `sudo apt update`

```shell
➜  ~ sudo bookworm-run 
请输入密码:
验证成功
root@Amber-CE-Bookworm:/home/xnne# 
```

之后我们尝试在 bookworm-run 中安装 neofetch 并且运行:

```shell
root@Amber-CE-Bookworm:/home/xnne/Downloads# neofetch
       _,met$$$$$gg.          root@Amber-CE-Bookworm 
    ,g$$$$$$$$$$$$$$$P.       ---------------------- 
  ,g$$P"     """Y$$.".        OS: Debian GNU/Linux 12 (bookworm) x86_64 
 ,$$P'              `$$$.     Host: OMEN by HP Laptop 16-b1xxx 
',$$P       ,ggs.     `$$b:   Kernel: 6.6.59-amd64-desktop-hwe 
`d$$'     ,$P"'   .    $$$    Uptime: 5 mins 
 $$P      d$'     ,    $$P    Packages: 346 (dpkg) 
 $$:      $$.   -    ,d$$'    Shell: bash 5.2.15 
 $$;      Y$b._   _,d$P'      Resolution: 2560x1440 
 Y$$.    `.`"Y$$$$P"'         DE: DDE 
 `$$b      "-.__              Terminal: bwrap 
  `Y$$                        CPU: 12th Gen Intel i7-12700H (20) @ 4.600GHz                                                                    
   `Y$$.                      GPU: Intel Alder Lake-P 
     `$$b.                    GPU: NVIDIA GeForce RTX 3060 Mobile / Max-Q 
       `Y$$b.                 Memory: 4087MiB / 15650MiB 
          `"Y$b._
              `"""                                    
                                                      
```


可以看到成功变身 debian12.

### 添加 debian 的 sourcelist

但是在尝试安装 parsec 的时候却出现了问题:

```shell
root@Amber-CE-Bookworm:/home/xnne/Downloads# dpkg -i parsec-linux.deb 
正在选中未选择的软件包 parsec。
(正在读取数据库 ... 系统当前共安装有 16895 个文件和目录。)
准备解压 parsec-linux.deb  ...
正在解压 parsec (150-97c) ...
dpkg: 依赖关系问题使得 parsec 的配置工作不能继续：
 parsec 依赖于 libxcursor1；然而：
  未安装软件包 libxcursor1。
 parsec 依赖于 libxi6；然而：
  未安装软件包 libxi6。
 parsec 依赖于 libgl1-mesa-glx | libgl1；然而：
  未安装软件包 libgl1-mesa-glx。
  未安装软件包 libgl1。
 parsec 依赖于 libasound2；然而：
  未安装软件包 libasound2。
 parsec 依赖于 libjpeg8；然而：
  未安装软件包 libjpeg8。
 parsec 依赖于 libavcodec57 | libavcodec58 | libavcodec59 | libavcodec60 | libavcodec61；然而：
  未安装软件包 libavcodec57。
  未安装软件包 libavcodec58。
  未安装软件包 libavcodec59。
  未安装软件包 libavcodec60。
  未安装软件包 libavcodec61。

root@Amber-CE-Bookworm:/home/xnne/Downloads# sudo apt install libavcodec61
正在读取软件包列表... 完成
正在分析软件包的依赖关系树... 完成
正在读取状态信息... 完成                 
没有可用的软件包 libavcodec61，但是它被其它的软件包引用了。
这可能意味着这个缺失的软件包可能已被废弃，
或者只能在其他发布源中找到

E: 软件包 libavcodec61 没有可安装候选
root@Amber-CE-Bookworm:/home/xnne/Downloads# sudo apt install libavcodec57
正在读取软件包列表... 完成
正在分析软件包的依赖关系树... 完成
正在读取状态信息... 完成                 
没有可用的软件包 libavcodec57，但是它被其它的软件包引用了。
这可能意味着这个缺失的软件包可能已被废弃，
或者只能在其他发布源中找到

E: 软件包 libavcodec57 没有可安装候选
```


初步推断是 deepin 的 source.list 有问题， 因为可以看到我们即使我们运行着容器，依然是在宿主机器的环境目录下的，那么可以推断目前用的是宿主机的 source.list。

于是乎我又找到了一个赛博菩萨:

[Debian 12 (Bookworm) -- Full sources.list and debian.sources](https://gist.github.com/ishad0w/e1ba0843edc9eb3084a1a0750861d073)

似乎是完全针对于 Bookworm 环境的。

于是乎:

```shell
root@Amber-CE-Bookworm:~# cd /etc/apt/
root@Amber-CE-Bookworm:/etc/apt# ls
apt.conf.d  auth.conf.d  keyrings  preferences.d  sources.list  sources.list.d  trusted.gpg.d
root@Amber-CE-Bookworm:/etc/apt# cat sources.list
deb https://mirrors.ustc.edu.cn/debian bookworm main contrib non-free-firmware non-free
root@Amber-CE-Bookworm:/etc/apt# ls sources.list.d/
root@Amber-CE-Bookworm:/etc/apt# 
```

我又对 `sources.list` 和 `sources.list.d` 感到好奇, 略微查询得到的结论是这样的:

>目录"/etc/apt/sources.list.d"和[文件](https://so.csdn.net/so/search?q=%E6%96%87%E4%BB%B6&spm=1001.2101.3001.7020)/etc/apt/sources.list的不同和相同点如下：
>- [相同点：它们都是用来保存Ubuntu软件更新的源服务器的地址的文件，它们的格式都是一样的，都是以deb或deb-src开头，后面跟着源的URL，发行版的代号，以及软件包的分类](https://www.cnblogs.com/kelamoyujuzhen/p/9728260.html "相同点：它们都是用来保存Ubuntu软件更新的源服务器的地址的文件，它们的格式都是一样的，都是以deb或deb-src开头，后面跟着源的URL，发行版的代号，以及软件包的分类")[1](https://www.cnblogs.com/kelamoyujuzhen/p/9728260.html "1")[2](https://blog.csdn.net/a772304419/article/details/120533938 "2")。
>- [不同点：/etc/apt/sources.list是一个单独的文件，而/etc/apt/sources.list.d是一个目录，可以在这个目录下创建多个以.list为扩展名的文件，每个文件可以写入不同的源的地址，通常用来安装第三方的软件](https://www.cnblogs.com/kelamoyujuzhen/p/9728260.html "不同点：/etc/apt/sources.list是一个单独的文件，而/etc/apt/sources.list.d是一个目录，可以在这个目录下创建多个以.list为扩展名的文件，每个文件可以写入不同的源的地址，通常用来安装第三方的软件")[1](https://www.cnblogs.com/kelamoyujuzhen/p/9728260.html "1")[2](https://blog.csdn.net/a772304419/article/details/120533938 "2")[。APT会自动读取这个目录下的所有文件，合并到sources.list中，所以不需要手动修改sources.list文件](https://qastack.cn/ubuntu/190149/how-do-you-tell-apt-to-use-files-in-etc-apt-sources-list-d "。APT会自动读取这个目录下的所有文件，合并到sources.list中，所以不需要手动修改sources.list文件")[3](https://qastack.cn/ubuntu/190149/how-do-you-tell-apt-to-use-files-in-etc-apt-sources-list-d "3")。
>copyfrom:https://blog.csdn.net/u010087338/article/details/134286449

也就是说我只要创建 `debian12.list` 然后放到 `sources.list.d/` 中即可:

```shell
root@Amber-CE-Bookworm:/etc/apt# cat sources.list.d/debian12.list 
deb http://deb.debian.org/debian/ bookworm main contrib non-free non-free-firmware
deb-src http://deb.debian.org/debian/ bookworm main contrib non-free non-free-firmware

deb http://deb.debian.org/debian/ bookworm-updates main contrib non-free non-free-firmware
deb-src http://deb.debian.org/debian/ bookworm-updates main contrib non-free non-free-firmware

deb http://deb.debian.org/debian/ bookworm-backports main contrib non-free non-free-firmware
deb-src http://deb.debian.org/debian/ bookworm-backports main contrib non-free non-free-firmware

deb http://security.debian.org/debian-security/ bookworm-security main contrib non-free non-free-firmware
deb-src http://security.debian.org/debian-security/ bookworm-security main contrib non-free non-free-firmware
```

然后更新软件源确实可以看到 debian.org 进入了我们的获取列表:

```shell
root@Amber-CE-Bookworm:/etc/apt# sudo apt update
命中:1 https://mirrors.ustc.edu.cn/debian bookworm InRelease
获取:2 http://security.debian.org/debian-security bookworm-security InRelease [48.0 kB]
获取:3 http://deb.debian.org/debian bookworm InRelease [151 kB]
获取:4 http://deb.debian.org/debian bookworm-updates InRelease [55.4 kB]
获取:5 http://security.debian.org/debian-security bookworm-security/main amd64 Packages [263 kB]
获取:6 http://deb.debian.org/debian bookworm-backports InRelease [59.4 kB]
获取:7 http://deb.debian.org/debian bookworm/main amd64 Packages [8,793 kB]
获取:8 http://security.debian.org/debian-security bookworm-security/main Translation-en [158 kB]
获取:9 http://security.debian.org/debian-security bookworm-security/contrib amd64 Packages [896 B]
获取:10 http://security.debian.org/debian-security bookworm-security/contrib Translation-en [652 B]
获取:11 http://security.debian.org/debian-security bookworm-security/non-free-firmware amd64 Packages [688 B]
获取:12 http://security.debian.org/debian-security bookworm-security/non-free-firmware Translation-en [472 B]
获取:13 http://deb.debian.org/debian bookworm/main Translation-zh_CN [125 kB]                                                                 
获取:14 http://deb.debian.org/debian bookworm/main Translation-en [6,109 kB]                                                                  
获取:15 http://deb.debian.org/debian bookworm/main Translation-zh [1,215 B]                                                                   
获取:16 http://deb.debian.org/debian bookworm/contrib amd64 Packages [53.5 kB]                                                                
获取:17 http://deb.debian.org/debian bookworm/contrib Translation-en [48.4 kB]                                                                
获取:18 http://deb.debian.org/debian bookworm/non-free amd64 Packages [102 kB]                                                                
获取:19 http://deb.debian.org/debian bookworm/non-free Translation-en [68.1 kB]                                                               
获取:20 http://deb.debian.org/debian bookworm/non-free-firmware amd64 Packages [6,372 B]                                                      
获取:21 http://deb.debian.org/debian bookworm/non-free-firmware Translation-en [20.9 kB]                                                      
获取:22 http://deb.debian.org/debian bookworm-updates/main amd64 Packages [756 B]                                                             
获取:23 http://deb.debian.org/debian bookworm-updates/main Translation-en [664 B]                                                             
获取:24 http://deb.debian.org/debian bookworm-backports/main amd64 Packages [289 kB]                                                          
获取:25 http://deb.debian.org/debian bookworm-backports/main Translation-en [246 kB]                                                          
获取:26 http://deb.debian.org/debian bookworm-backports/contrib amd64 Packages [5,852 B]                                                      
获取:27 http://deb.debian.org/debian bookworm-backports/contrib Translation-en [5,864 B]                                                      
获取:28 http://deb.debian.org/debian bookworm-backports/non-free amd64 Packages [13.3 kB]                                                     
获取:29 http://deb.debian.org/debian bookworm-backports/non-free Translation-en [8,460 B]                                                     
获取:30 http://deb.debian.org/debian bookworm-backports/non-free-firmware amd64 Packages [3,828 B]                                            
获取:31 http://deb.debian.org/debian bookworm-backports/non-free-firmware Translation-en [2,860 B]                                            
已下载 16.6 MB，耗时 8秒 (2,173 kB/s)                                                                                                         
正在读取软件包列表... 完成
正在分析软件包的依赖关系树... 完成
正在读取状态信息... 完成                 
有 8 个软件包可以升级。请执行 ‘apt list --upgradable’ 来查看它们。
```

但是即使这样也找不到那个逆天的 libavcodec57~61:

```shell
root@Amber-CE-Bookworm:/etc/apt/sources.list.d# sudo apt install libavcodec57
正在读取软件包列表... 完成
正在分析软件包的依赖关系树... 完成
正在读取状态信息... 完成                 
没有可用的软件包 libavcodec57，但是它被其它的软件包引用了。
这可能意味着这个缺失的软件包可能已被废弃，
或者只能在其他发布源中找到
```

### dive into libavcodec57~61

- https://discourse.panda3d.org/t/problems-with-libavcodec57/25270
- https://forums.linuxmint.com/viewtopic.php?t=370870

从上面两个来看，每个系统大概最多只支持一个版本的 libavcodec.

比如对于我  Bookworm-run 的 debian12 来说. 59 是可用的.

```shell
root@Amber-CE-Bookworm:/etc/apt/sources.list.d# sudo apt install libavcodec59
正在读取软件包列表... 完成
正在分析软件包的依赖关系树... 完成
正在读取状态信息... 完成                 
将会同时安装下列软件：
  i965-va-driver intel-media-va-driver libavutil57 libcodec2-1.0 libdrm-intel1 libdrm-nouveau2 libdrm-radeon1 libgl1 libgl1-mesa-dri
  libglx-mesa0 libglx0 libgsm1 libigdgmm12 libmfx1 libmp3lame0 libogg0 libopus0 libpciaccess0 librav1e0 libsensors-config libsensors5
  libshine3 libsnappy1v5 libsoxr0 libspeex1 libsvtav1enc1 libswresample4 libtheora0 libtwolame0 libva-drm2 libva-x11-2 libva2 libvdpau-va-gl1
  libvdpau1 libvorbis0a libvorbisenc2 libvpx7 libx264-164 libxcb-glx0 libxfixes3 libxvidcore4 libxxf86vm1 libzvbi-common libzvbi0
  mesa-va-drivers mesa-vdpau-drivers ocl-icd-libopencl1 va-driver-all vdpau-driver-all
建议安装：
  i965-va-driver-shaders libcuda1 libnvcuvid1 libnvidia-encode1 opus-tools lm-sensors speex opencl-icd nvidia-vdpau-driver
  nvidia-tesla-440-vdpau-driver nvidia-tesla-418-vdpau-driver nvidia-legacy-390xx-vdpau-driver nvidia-legacy-340xx-vdpau-driver
下列【新】软件包将被安装：
  i965-va-driver intel-media-va-driver libavcodec59 libavutil57 libcodec2-1.0 libdrm-intel1 libdrm-nouveau2 libdrm-radeon1 libgl1
  libgl1-mesa-dri libglx-mesa0 libglx0 libgsm1 libigdgmm12 libmfx1 libmp3lame0 libogg0 libopus0 libpciaccess0 librav1e0 libsensors-config
  libsensors5 libshine3 libsnappy1v5 libsoxr0 libspeex1 libsvtav1enc1 libswresample4 libtheora0 libtwolame0 libva-drm2 libva-x11-2 libva2
  libvdpau-va-gl1 libvdpau1 libvorbis0a libvorbisenc2 libvpx7 libx264-164 libxcb-glx0 libxfixes3 libxvidcore4 libxxf86vm1 libzvbi-common
  libzvbi0 mesa-va-drivers mesa-vdpau-drivers ocl-icd-libopencl1 va-driver-all vdpau-driver-all
升级了 0 个软件包，新安装了 50 个软件包，要卸载 0 个软件包，有 8 个软件包未被升级。
需要下载 41.2 MB 的归档。
解压缩后会消耗 152 MB 的额外空间。
您希望继续执行吗？ [Y/n] 
```

如果之前因为执行过 `dpkg -i parsec_linux.deb` 那么可能需要先 `apt --fix-broken install`:

```shell
root@Amber-CE-Bookworm:/home/xnne/Downloads# apt --fix-broken install
正在读取软件包列表... 完成
正在分析软件包的依赖关系树... 完成
正在读取状态信息... 完成                 
正在修复依赖关系... 完成
下列软件包将被【卸载】：
  parsec
升级了 0 个软件包，新安装了 0 个软件包，要卸载 1 个软件包，有 8 个软件包未被升级。
有 1 个软件包没有被完全安装或卸载。
解压缩后会消耗 0 B 的额外空间。
您希望继续执行吗？ [Y/n] y
```

解决了 libavcodec59 那么之后就是继续解决剩下的依赖包。

### 解决剩下的一系列依赖:

```shell
 parsec 依赖于 libxcursor1；然而：
  未安装软件包 libxcursor1。
 parsec 依赖于 libxi6；然而：
  未安装软件包 libxi6。
 parsec 依赖于 libasound2；然而：
  未安装软件包 libasound2。
 parsec 依赖于 libjpeg8；然而：
  未安装软件包 libjpeg8。
```

#### 对于 libjpeg8:

[# A linux app I'm using requires -libjpeg8, where and how do I get it?](https://www.reddit.com/r/chromeos/comments/15twk76/a_linux_app_im_using_requires_libjpeg8_where_and/)

>Libjpeg8 hasn't been in Debian since 2017. What you need to do (as root) is:  
Libjpeg8 自 2017 年起就不在 Debian 中了。您需要（以 root 用户身份）做的是<br>
>`apt-get install libjpeg62-turbo`<br>
> `ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so.62 /usr/lib/x86_64-linux-gnu/libjpeg.so.8`<br>

但即使这么做，在安装时 apt 依然会喋喋不休地提醒你，`libjpeg8` 未安装。

可以这么解决:

[# Debian 12 – Fix libjpeg8 missing dependency error for Parsec]()

>ou can always choose to run Parsec through [Flatpak](https://flathub.org/apps/com.parsecgaming.parsec)[1] or [AppImage](https://appimage.github.io/parsec-linux-appimage/)[2]. I should look into containerizing Parsec and running it through Docker, which is becoming my favorite choice for running various pieces of software, as it avoids all the clutter and potential dependency issues, exactly like the one we’re dealing with here.  <br>
>你可以选择通过 Flatpak[1] 或 AppImage[2] 运行 Parsec。我应该考虑将 Parsec 容器化，并通过 Docker 运行它。Docker 正在成为我运行各种软件时最喜欢的选择，因为它可以避免所有杂乱和潜在的依赖性问题，就像我们在这里遇到的问题一样。<br>
>Of course, the easy solution would be to just install libjpeg8 .deb package directly and skip all the symlink stuff, like this: <br>
>当然，简单的解决办法是直接安装 libjpeg8 .deb 包，跳过所有符号链接，就像这样：<br>
>`wget https://archive.debian.org/debian/pool/main/libj/libjpeg8/libjpeg8_8b-1_amd64.deb`<br>
>`sudo dpkg -i libjpeg8_8b-1_amd64.deb`<br>

#### 对于 libasound2&&libxcursor1

```shell
root@Amber-CE-Bookworm:/home/xnne/Downloads# sudo apt install libasound2
正在读取软件包列表... 完成
正在分析软件包的依赖关系树... 完成
正在读取状态信息... 完成                 
您也许需要运行“apt --fix-broken install”来修正上面的错误。
下列软件包有未满足的依赖关系：
 libasound2 : 依赖: libasound2-data (>= 1.2.8-1) 但是它将不会被安装
 parsec : 依赖: libxcursor1 但是它将不会被安装
          依赖: libxi6 但是它将不会被安装
E: 有未能满足的依赖关系。请尝试不指明软件包的名字来运行“apt --fix-broken install”(也可以指定一个解决办法)。

root@Amber-CE-Bookworm:/home/xnne/Downloads# apt --fix-broken install
正在读取软件包列表... 完成
正在分析软件包的依赖关系树... 完成
正在读取状态信息... 完成                 
正在修复依赖关系... 完成
将会同时安装下列软件：
  alsa-topology-conf alsa-ucm-conf libasound2 libasound2-data libxcursor1 libxi6
建议安装：
  libasound2-plugins alsa-utils
下列【新】软件包将被安装：
  alsa-topology-conf alsa-ucm-conf libasound2 libasound2-data libxcursor1 libxi6
升级了 0 个软件包，新安装了 6 个软件包，要卸载 0 个软件包，有 8 个软件包未被升级。
有 1 个软件包没有被完全安装或卸载。
需要下载 574 kB 的归档。
解压缩后会消耗 2,767 kB 的额外空间。
您希望继续执行吗？ [Y/n] y
```

似乎两个一起装了哈。所以这个反而很容易解决。

再次运行:

```shell
root@Amber-CE-Bookworm:/home/xnne/Downloads# dpkg -i parsec-linux.deb 
(正在读取数据库 ... 系统当前共安装有 17958 个文件和目录。)
准备解压 parsec-linux.deb  ...
正在解压 parsec (150-97c) 并覆盖 (150-97c) ...
正在设置 parsec (150-97c) ...
正在处理用于 ace-host-integration (1.2.2) 的触发器 ...
[WARN] No /opt/apps directory. Skip...
/usr/share/applications/parsecd.desktop is detected. Processing host system integration...
正在处理用于 hicolor-icon-theme (0.17-2) 的触发器 ...
```

已经没有缺少依赖了。

### 在容器内运行 parsec

```shell
root@Amber-CE-Bookworm:/home/xnne/Downloads# parsecd
[D 2025-06-16 05:21:23] log: Parsec release-ui[release] (150-97c, Service: -1, Loader: 12)
[D 2025-06-16 05:21:24] log: Parsec release-ui[release] (150-99, Service: -1, Loader: 12)
[2 2025-06-16 05:21:24] Force Relay Mode: Off
[2 2025-06-16 05:21:24] Force Relay Mode: Off
[2 2025-06-16 05:21:24] UPNP: upnp_create
Authorization required, but no authorization protocol specified

sh: 1: zenity: not found
段错误
```

卧槽不是你怎么问题那么多啊。

```shell
root@Amber-CE-Bookworm:/home/xnne/Downloads# zenity --version
bash: zenity: 未找到命令
```

确实是我的错 - [# {resize, zenity} command not found #35](https://github.com/r00t-3xp10it/venom/issues/35)

>**zenity**: command not found <-- **zenity allows me to use GUI's in sh scripts.** <br>  
>zenity: command not found < -- zenity 允许我在 sh 脚本中使用图形用户界面。<br>
>Install zenity `sudo apt-get install zenity`

可以知道， zenity 的作用和安装方式。

然后就有了灭世的一幕:

```shell
root@Amber-CE-Bookworm:/home/xnne/Downloads# sudo apt install zenity
正在读取软件包列表... 完成
正在分析软件包的依赖关系树... 完成
正在读取状态信息... 完成                 
将会同时安装下列软件：
  adwaita-icon-theme aspell aspell-en at-spi2-common at-spi2-core bubblewrap dbus-user-session dconf-gsettings-backend dconf-service
  dictionaries-common emacsen-common enchant-2 fuse3 glib-networking glib-networking-common glib-networking-services
  gsettings-desktop-schemas gstreamer1.0-gl gstreamer1.0-libav gstreamer1.0-plugins-bad gstreamer1.0-plugins-base gstreamer1.0-plugins-good
  gstreamer1.0-x gtk-update-icon-cache hunspell-en-us iso-codes libaa1 libaacs0 libabsl20220623 libaspell15 libass9 libasyncns0
  libatk-bridge2.0-0 libatk1.0-0 libatomic1 libatspi2.0-0 libavc1394-0 libavfilter8 libavformat59 libavif15 libbdplus0 libblas3 libbluray2
  libbs2b0 libcdparanoia0 libchromaprint1 libcjson1 libcolord2 libdc1394-25 libdca0 libdconf1 libdecor-0-0 libdecor-0-plugin-1-cairo
  libdirectfb-1.7-7 libdv4 libdvdnav4 libdvdread8 libdw1 libenchant-2-2 libepoxy0 libevdev2 libfaad2 libflac12 libflite1 libfluidsynth3
  libfreeaptx0 libfuse3-3 libgav1-1 libgfortran5 libgles2 libgme0 libgraphene-1.0-0 libgssdp-1.6-0 libgstreamer-gl1.0-0
  libgstreamer-plugins-bad1.0-0 libgstreamer-plugins-base1.0-0 libgstreamer1.0-0 libgtk-3-0 libgtk-3-bin libgtk-3-common libgudev-1.0-0
  libgupnp-1.6-0 libgupnp-igd-1.0-4 libharfbuzz-icu0 libhunspell-1.7-0 libhyphen0 libiec61883-0 libinstpatch-1.0-2 libjack-jackd2-0
  libjavascriptcoregtk-4.1-0 libjson-glib-1.0-0 libjson-glib-1.0-common libkate1 liblapack3 libldacbt-enc2 liblilv-0-0 liblrdf0 libltc11
  libmanette-0.2-0 libmbedcrypto7 libmjpegutils-2.1-0 libmodplug1 libmpcdec6 libmpeg2encpp-2.1-0 libmpg123-0 libmplex2-2.1-0 libmysofa1
  libncurses6 libneon27 libnice10 libnorm1 libnspr4 libnss-myhostname libnss3 libopenal-data libopenal1 libopenh264-7 libopenmpt0
  libopenni2-0 liborc-0.4-0 libpam-systemd libpgm-5.3-0 libpipewire-0.3-0 libpipewire-0.3-common libplacebo208 libpocketsphinx3 libpostproc56
  libproxy1v5 libpulse0 libqrencode4 libquadmath0 librabbitmq4 libraptor2-0 libraw1394-11 librist4 librubberband2 libsamplerate0 libsbc1
  libsdl2-2.0-0 libsecret-1-0 libsecret-common libserd-0-0 libshout3 libsndfile1 libsndio7.0 libsodium23 libsord-0-0 libsoundtouch1
  libsoup-3.0-0 libsoup-3.0-common libsoup2.4-1 libsoup2.4-common libspa-0.2-modules libspandsp2 libsphinxbase3 libsratom-0-0
  libsrt1.5-gnutls libsrtp2-1 libssh-gcrypt-4 libswscale6 libsystemd-shared libsystemd0 libtag1v5 libtag1v5-vanilla libudev1 libudfread0
  libunwind8 libusb-1.0-0 libv4l-0 libv4lconvert0 libvidstab1.1 libvisual-0.4-0 libvo-aacenc0 libvo-amrwbenc0 libvorbisfile3 libwavpack1
  libwayland-cursor0 libwayland-egl1 libwebkit2gtk-4.1-0 libwebrtc-audio-processing1 libwildmidi2 libwoff1 libxcb-xkb1 libxcomposite1
  libxdamage1 libxinerama1 libxkbcommon-x11-0 libxkbcommon0 libxrandr2 libxslt1.1 libxss1 libxtst6 libxv1 libyajl2 libyuv0 libzbar0 libzimg2
  libzmq5 libzxing2 pocketsphinx-en-us systemd systemd-sysv timgm6mb-soundfont udev xdg-dbus-proxy xdg-desktop-portal xdg-desktop-portal-gtk
  xkb-data zenity-common
建议安装：
  aspell-doc spellutils wordlist frei0r-plugins gvfs hunspell openoffice.org-hunspell | openoffice.org-core isoquery libbluray-bdj colord
  libdirectfb-extra libdv-bin oss-compat libdvdcss2 libenchant-2-voikko libvisual-0.4-plugins gstreamer1.0-tools jackd2 liblrdf0-dev
  libportaudio2 pipewire pulseaudio raptor2-utils libraw1394-doc xdg-utils serdi sndiod sordi gstreamer1.0-alsa libwildmidi-config
  systemd-container systemd-homed systemd-userdbd systemd-boot systemd-resolved libfido2-1 libtss2-esys-3.0.2-0 libtss2-mu0 libtss2-rc0
  polkitd | policykit-1 fluid-soundfont-gm accountsservice evince xdg-desktop-portal-gnome
推荐安装：
  systemd-timesyncd | time-daemon libnss-systemd
下列【新】软件包将被安装：
  adwaita-icon-theme aspell aspell-en at-spi2-common at-spi2-core bubblewrap dbus-user-session dconf-gsettings-backend dconf-service
  dictionaries-common emacsen-common enchant-2 fuse3 glib-networking glib-networking-common glib-networking-services
  gsettings-desktop-schemas gstreamer1.0-gl gstreamer1.0-libav gstreamer1.0-plugins-bad gstreamer1.0-plugins-base gstreamer1.0-plugins-good
  gstreamer1.0-x gtk-update-icon-cache hunspell-en-us iso-codes libaa1 libaacs0 libabsl20220623 libaspell15 libass9 libasyncns0
  libatk-bridge2.0-0 libatk1.0-0 libatomic1 libatspi2.0-0 libavc1394-0 libavfilter8 libavformat59 libavif15 libbdplus0 libblas3 libbluray2
  libbs2b0 libcdparanoia0 libchromaprint1 libcjson1 libcolord2 libdc1394-25 libdca0 libdconf1 libdecor-0-0 libdecor-0-plugin-1-cairo
  libdirectfb-1.7-7 libdv4 libdvdnav4 libdvdread8 libdw1 libenchant-2-2 libepoxy0 libevdev2 libfaad2 libflac12 libflite1 libfluidsynth3
  libfreeaptx0 libfuse3-3 libgav1-1 libgfortran5 libgles2 libgme0 libgraphene-1.0-0 libgssdp-1.6-0 libgstreamer-gl1.0-0
  libgstreamer-plugins-bad1.0-0 libgstreamer-plugins-base1.0-0 libgstreamer1.0-0 libgtk-3-0 libgtk-3-bin libgtk-3-common libgudev-1.0-0
  libgupnp-1.6-0 libgupnp-igd-1.0-4 libharfbuzz-icu0 libhunspell-1.7-0 libhyphen0 libiec61883-0 libinstpatch-1.0-2 libjack-jackd2-0
  libjavascriptcoregtk-4.1-0 libjson-glib-1.0-0 libjson-glib-1.0-common libkate1 liblapack3 libldacbt-enc2 liblilv-0-0 liblrdf0 libltc11
  libmanette-0.2-0 libmbedcrypto7 libmjpegutils-2.1-0 libmodplug1 libmpcdec6 libmpeg2encpp-2.1-0 libmpg123-0 libmplex2-2.1-0 libmysofa1
  libncurses6 libneon27 libnice10 libnorm1 libnspr4 libnss3 libopenal-data libopenal1 libopenh264-7 libopenmpt0 libopenni2-0 liborc-0.4-0
  libpam-systemd libpgm-5.3-0 libpipewire-0.3-0 libpipewire-0.3-common libplacebo208 libpocketsphinx3 libpostproc56 libproxy1v5 libpulse0
  libqrencode4 libquadmath0 librabbitmq4 libraptor2-0 libraw1394-11 librist4 librubberband2 libsamplerate0 libsbc1 libsdl2-2.0-0
  libsecret-1-0 libsecret-common libserd-0-0 libshout3 libsndfile1 libsndio7.0 libsodium23 libsord-0-0 libsoundtouch1 libsoup-3.0-0
  libsoup-3.0-common libsoup2.4-1 libsoup2.4-common libspa-0.2-modules libspandsp2 libsphinxbase3 libsratom-0-0 libsrt1.5-gnutls libsrtp2-1
  libssh-gcrypt-4 libswscale6 libtag1v5 libtag1v5-vanilla libudfread0 libunwind8 libusb-1.0-0 libv4l-0 libv4lconvert0 libvidstab1.1
  libvisual-0.4-0 libvo-aacenc0 libvo-amrwbenc0 libvorbisfile3 libwavpack1 libwayland-cursor0 libwayland-egl1 libwebkit2gtk-4.1-0
  libwebrtc-audio-processing1 libwildmidi2 libwoff1 libxcb-xkb1 libxcomposite1 libxdamage1 libxinerama1 libxkbcommon-x11-0 libxkbcommon0
  libxrandr2 libxslt1.1 libxss1 libxtst6 libxv1 libyajl2 libyuv0 libzbar0 libzimg2 libzmq5 libzxing2 pocketsphinx-en-us timgm6mb-soundfont
  xdg-dbus-proxy xdg-desktop-portal xdg-desktop-portal-gtk xkb-data zenity zenity-common
下列软件包将被升级：
  libnss-myhostname libsystemd-shared libsystemd0 libudev1 systemd systemd-sysv udev
升级了 7 个软件包，新安装了 203 个软件包，要卸载 0 个软件包，有 1 个软件包未被升级。
需要下载 144 MB 的归档。
解压缩后会消耗 450 MB 的额外空间。
您希望继续执行吗？ [Y/n] y
```

这 tm 这么多的吗？不过安装过程还算顺利。

再次尝试启动:

```shell
root@Amber-CE-Bookworm:/home/xnne/Downloads# parsecd
[D 2025-06-16 05:28:42] log: Parsec release-ui[release] (150-99, Service: -1, Loader: 12)
[2 2025-06-16 05:28:43] Force Relay Mode: Off
[2 2025-06-16 05:28:43] Force Relay Mode: Off
[2 2025-06-16 05:28:43] UPNP: upnp_create
Authorization required, but no authorization protocol specified

Authorization required, but no authorization protocol specified


(zenity:62856): Gtk-WARNING **: 05:28:43.201: cannot open display: :0
```

我的心快死了。

中途我尝试了那个作者提供的用法在 ACE 容器内安装了一下 VLC, 就像 WSL2 一样和宿机无缝对接。

```shell
sudo apt install vlc -y
```

以及重新安装了一次 parsec:

```shell
xnne@Amber-CE-Bookworm:~/Downloads$ sudo dpkg -i parsec-linux.deb
请输入密码:
验证成功
(正在读取数据库 ... 系统当前共安装有 35571 个文件和目录。)
准备解压 parsec-linux.deb  ...
正在解压 parsec (150-97c) 并覆盖 (150-97c) ...
正在设置 parsec (150-97c) ...
正在处理用于 ace-host-integration (1.2.2) 的触发器 ...
[WARN] No /opt/apps directory. Skip...
/usr/share/applications/parsecd.desktop is detected. Processing host system integration...
/usr/share/applications/vlc.desktop is detected. Processing host system integration...
/usr/share/applications/xdg-desktop-portal-gtk.desktop is detected. Processing host system integration...
/usr/share/applications/zutty.desktop is detected. Processing host system integration...
正在处理用于 hicolor-icon-theme (0.17-2) 的触发器 ...
```

然后成功以用户组启动了 parsecd: (也许用户组才是决定因素？)

```shell
xnne@Amber-CE-Bookworm:~/Downloads$ parsecd 
[D 2025-06-16 05:32:38] log: Parsec release-ui[release] (150-97c, Service: -1, Loader: 12)
[D 2025-06-16 05:32:38] log: Parsec release-ui[release] (150-99, Service: -1, Loader: 12)
[2 2025-06-16 05:32:38] Force Relay Mode: Off
[2 2025-06-16 05:32:38] Force Relay Mode: Off
[2 2025-06-16 05:32:38] UPNP: upnp_create
[I 2025-06-16 05:32:38] unprivileged_user=1 webview_available=0 enable_webview=0
ALSA lib pcm_dmix.c:999:(snd_pcm_dmix_open) unable to open slave
[D 2025-06-16 05:32:39] MTY_AudioCreate: 'snd_pcm_open' failed with error -2
[D 2025-06-16 05:32:39] Client status changed to: -3
[AVHWDeviceContext @ 0x7fe62c2fef40] Cannot load libcuda.so.1
[AVHWDeviceContext @ 0x7fe62c2fef40] Could not dynamically load CUDA                                                                           
[AVHWDeviceContext @ 0x7fe62c2ff5c0] Cannot load libcuda.so.1                                                                                  
[AVHWDeviceContext @ 0x7fe62c2ff5c0] Could not dynamically load CUDA                                                                           
libva info: VA-API version 1.17.0                                                                                                              
libva info: Trying to open /usr/lib/x86_64-linux-gnu/dri/iHD_drv_video.so
libva info: Found init function __vaDriverInit_1_17
libva info: va_openDriver() returns 0
libva info: VA-API version 1.17.0
libva info: Trying to open /usr/lib/x86_64-linux-gnu/dri/iHD_drv_video.so
libva info: Found init function __vaDriverInit_1_17
libva info: va_openDriver() returns 0
[D 2025-06-16 05:32:39] MTY_DeleteFile: 'remove' failed with errno 2
[D 2025-06-16 05:32:46] UPNP: No devlist
```


但是可以看到是存在警告的:

```shell
[AVHWDeviceContext @ 0x7fe62c2fef40] Cannot load libcuda.so.1
[AVHWDeviceContext @ 0x7fe62c2fef40] Could not dynamically load CUDA                                                                           
[AVHWDeviceContext @ 0x7fe62c2ff5c0] Cannot load libcuda.so.1                                                                                  
[AVHWDeviceContext @ 0x7fe62c2ff5c0] Could not dynamically load CUDA  
```

这大概率是我没有在 linux 中安装 nvidia 驱动? 

**大概率是没有无头模式造成的，以及容器内无法正确找到一些驱动。**

## 最终我是如何解决的:

最终我是在容器外也就是 deepin 里装上的 parsec 0.0

```shell
xnne@xnne-PC:~/Downloads$ sudo apt-get install libjpeg62-turbo
正在读取软件包列表... 完成
正在分析软件包的依赖关系树... 完成
正在读取状态信息... 完成                 
libjpeg62-turbo 已经是最新版 (1:2.1.5-2)。
libjpeg62-turbo 已设置为手动安装。
升级了 0 个软件包，新安装了 0 个软件包，要卸载 0 个软件包，有 576 个软件包未被升级。
xnne@xnne-PC:~/Downloads$ ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so.62 /usr/lib/x86_64-linux-gnu/libjpeg.so.8
ln: 无法创建符号链接 '/usr/lib/x86_64-linux-gnu/libjpeg.so.8': 权限不够
xnne@xnne-PC:~/Downloads$ sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so.62 /usr/lib/x86_64-linux-gnu/libjpeg.so.8
xnne@xnne-PC:~/Downloads$ wget https://archive.debian.org/debian/pool/main/libj/libjpeg8/libjpeg8_8b-1_amd64.deb
--2025-06-16 13:49:21--  https://archive.debian.org/debian/pool/main/libj/libjpeg8/libjpeg8_8b-1_amd64.deb
正在解析主机 archive.debian.org (archive.debian.org)... 172.29.0.150
正在连接 archive.debian.org (archive.debian.org)|172.29.0.150|:443... 已连接。
已发出 HTTP 请求，正在等待回应... 200 OK
长度：133524 (130K) [application/vnd.debian.binary-package]
正在保存至: “libjpeg8_8b-1_amd64.deb.1”

libjpeg8_8b-1_amd64.deb.1           100%[==================================================================>] 130.39K   298KB/s  用时 0.4s    

2025-06-16 13:49:27 (298 KB/s) - 已保存 “libjpeg8_8b-1_amd64.deb.1” [133524/133524])

xnne@xnne-PC:~/Downloads$ sudo dpkg -i libjpeg8_8b-1_amd64.deb 
正在选中未选择的软件包 libjpeg8。
(正在读取数据库 ... 系统当前共安装有 400753 个文件和目录。)
准备解压 libjpeg8_8b-1_amd64.deb  ...
正在解压 libjpeg8 (8b-1) ...
正在设置 libjpeg8 (8b-1) ...
xnne@xnne-PC:~/Downloads$ sudo dpkg -i parsec-linux.deb 
正在选中未选择的软件包 parsec。
(正在读取数据库 ... 系统当前共安装有 400760 个文件和目录。)
准备解压 parsec-linux.deb  ...
正在解压 parsec (150-97c) ...
正在设置 parsec (150-97c) ...
正在处理用于 bamfdaemon (0.5.6+repack-1) 的触发器 ...
Rebuilding /usr/share/applications/bamf-2.index...
正在处理用于 desktop-file-utils (0.26-deepin) 的触发器 ...
正在处理用于 hicolor-icon-theme (0.17-2) 的触发器 ...
```


我回到了我的 deepin23, 并且再次安装 parsec, 我发现似乎只有 `libjpeg8` 的问题。

而这个我们在前面容器内解决过，于是乎我按照前面那个先安装 `libjpeg62` 然后创建软连接。

之后再直接安装 `libjpeg8` 来防止它报错。

以及，我这么成功了。但是，我并没有用到 ACE 容器 =-=。

也许下次会用到。 
