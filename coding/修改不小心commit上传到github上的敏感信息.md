## 修改不小心commit上传到github上的敏感信息

![image-20240913083346382](https://cdn.xnnehang.top/MrXnneHang/blog_img/refs/heads/main/BlogHosting/img/24/09/202409130834760.png)

昨天在上传的时候，把我的api-key也给commit上去了，差点一个晚上睡不着。





## bfg

[下载地址](https://rtyley.github.io/bfg-repo-cleaner/)

![image-20240913083529143](https://cdn.xnnehang.top/MrXnneHang/blog_img/refs/heads/main/BlogHosting/img/24/09/202409130838417.png)

之后:

```cmd
git clone --mirror https://github.com/your-username/your-repo.git
java -jar bfg-1.14.0.jar --replace-text replacements.txt your-repo 
```

your-repo成为你的本地仓库目录名。

不过这个似乎得要java才能运行，如果有玩mc的话会有，我是上次部署博客后端的时候顺手安装的。

[java下载地址](https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html)

选择jdk,然后添加系统环境变量或者直接怼着用就行。如果是安装的话安装完后重启即可。

最后强制推送:

```cmd
cd your-repo
git push origin master -f
```



