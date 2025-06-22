## Reference:

- [# CentOS 7如何安装Neofetch _](https://www.cnblogs.com/gcstsz/p/16213646.html)

本文参考了上面链接里佬的做法，说起来，博客园也可以做的好漂亮，而且还是静态渲染。

[https://github.com/dylanaraps/neofetch/wiki/Installation](https://github.com/dylanaraps/neofetch/wiki/Installation) 里记录了不同系统的安装方式。

## 开始


```shell
sudo yum install epel-release
curl -o /etc/yum.repos.d/konimex-neofetch-epel-7.repo https://copr.fedorainfracloud.org/coprs/konimex/neofetch/repo/epel-7/konimex-neofetch-epel-7.repo
sudo yum install neofetch
```


>EPEL (Extra Packages for Enterprise Linux)是基于Fedora的一个项目，为“红帽系”的操作系统提供额外的软件包，适用于RHEL、CentOS和Scientific Linux.<br>
>我们在Centos下使用yum安装时往往找不到rpm的情况，官方的rpm repository提供的rpm包也不够丰富，很多时候需要自己编译很痛苦，而EPEL恰恰可以解决这两方面的问题。EPEL的全称叫 Extra Packages for Enterprise Linux 。EPEL是由 Fedora 社区打造，为 RHEL 及衍生发行版如 CentOS、Scientific Linux 等提供高质量软件包的项目。装上了 EPEL之后，就相当于添加了一个第三方源。

## 测试

```shell
[root@113-29-232-47 ~]# neofetch
        #####           root@113-29-232-47.rev.aptransit.com 
       #######          ------------------------------------ 
       ##O#O##          OS: AlmaLinux 9.6 (Sage Margay) x86_64 
       #######          Host: KVM RHEL 7.6.0 PC (i440FX + PIIX, 1996) 
     ###########        Kernel: 5.14.0-427.13.1.el9_4.x86_64 
    #############       Uptime: 18 days, 19 hours, 33 mins 
   ###############      Packages: 688 (rpm) 
   ################     Shell: bash 5.1.8 
  #################     Resolution: 1024x768 
#####################   Terminal: /dev/pts/0 
#####################   CPU: AMD EPYC 7713P (1) @ 1.999GHz 
  #################     GPU: 00:02.0 Vendor 1234 Device 1111 
                        Memory: 316MiB / 3659MiB 

                                                
                                                
```
