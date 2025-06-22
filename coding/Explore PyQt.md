# 劝退

看到很久以前自己探索 PyQt 的过程，它分了很多天，我看它很不爽。于是乎在这里把它整理一下。

但是在开始之前，我就得先说一下， PyQt 实际上使用范围已经很窄了。只有这些场景可能会用到： 我是一个个人开发者，我正在写一个纯 Python 后端的东西，我希望可以把写的东西简单地打包成 exe 让用户可以零基础地打开并且使用它。这个软件不是很大，并且对性能要求也不是那么高。

举个栗子：

https://github.com/AliceNavigator/Navigator-Audio-Toolkit

如果工程项目依然在用 PyQt 那么赶紧跑，这个项目不正常。

即使是现在，如果像上面那样的个人使用的项目我更建议使用一些 WebUI 框架比如 Gradio 或者 Streamlit。具体原因在下面

首先来举一下 PyQt 的主要弊端：

- 它的效率是真的低。首先是启动慢，但是最重要的是它相比于成熟的 WebUI 框架并没有自己成熟的多线程保护体系。所有异步和并行都需要用户手动处理。如果你是一坨，那它更是一坨。
- 它在多平台兼容上是灾难性的。虽然它打着多平台兼容的旗号，但是兼容的意思是你需要主动调整一些东西，比如系统依赖。而并不是直接运行。所以有时候，你在你的 deepin 上打包可以用，但是对方的 ubuntu 不能用，这可能就是依赖库存在差异造成的，你不可能为每个系统都打包一份。也许你想，用 docker 吧。但是 pyqt 的依赖库似乎和 docker 的无头模式有点冲突。至少我在 windows 上打包时， wsl2 的 ubuntu 可以运行，而打包镜像后就不行，报错是 X-Server 什么的，显示驱动找不到什么东西的，我不熟悉，就没继续往下搞。更别说一开始刚刚接触 PyQt 的人压根不会这么多东西。
- 前后端不分离的项目通常很难一个后端供多个前端使用。比如你希望既可以使用软件程序，又可以使用 Web 程序，甚至在 Unity 中使用。那么前后端分离才是最好的做法。前后端混合只会让一切乱的像混沌初开。
- PyQt 似乎和 PySide 似乎还有各种扯不清道不明的关系，PyQt 似乎不让商用所以别人项目总用 PySide, 你还得做代码转换。虽然大部分 API 结构都一致，但是只要有一点不一样那都是浪费时间。
- PyQt 的社区活跃度根本不行。如果你问一个问题，不管是在他社区里问还是问其他人都得不到好的解法。另外，很多多年前的 bug 你搜到了，但是依然显示 unsolved。

吐槽到此结束。实际上如果真的要写好一个前端， 最好去学 React, Vue 之类的。这样才能最好的前后端分离，而前后端分离才能专注地优化两个部分。但是我这个菜鸡实际上目前也只会 WebUI，React 也只是会跑跑而已。

ok 接下来记录下之前的东西，实际上这无关紧要，但如果你固执己见依然要学 PyQt , 下面的东西或许对你会有一点点帮助。但是实际上， Qt 还是 CPP Qt 更好使。


# 介绍

我之前用了两种方式开发，第一种是不依赖 PyQt Designer 的，第二种是以来 Designer 的。实际上第一种对于正常来说完全够用 =-=， 没必要增加开发成本。代码可读性第一的话我依然建议第一种。就是直接用 config.yml 控制 window 布局。

与其专注布局不如专注代码结构。这是我一直以来的理念。如果一定要好看的布局，不如花点时间学学设计和绘画。

# PyQt yaml 文件管理界面布局的使用总结


>入门，练手，可以。项目小，快速开发，可以。
>但是如果你要做大的项目的话，建议使用QT Designer来管理布局和控件。
>但这篇绝对值得你看。关于怎么安全地开多线程和绘制贴图，动画。


有了之前[期末设计-人脸识别系统](http://xnnehang.top/blog/55)的经验，其实只要改改内容就可以用了。

但是毕竟那不是我写的，我也得熟悉一下窗口初始化的一个流程。所以这边就用之前做的没有UI的番茄钟来练练手。最后也顺便学一下python的可执行文件打包。（我终于要有自己的release啦）。

但其实说是自己写，其实都是参考。严格地说就是缝，使劲缝。

## #窗口、控件关系和Pos的管理：

这里我用的是yaml。我存了一个yasumi_config.yml。

### yaml 列表的写法。

```yaml
# ❌
main_window_size: (600,600)
main_window_size: [600,600]

# ✔
main_window_size:
- 600
- 600
- pretty good
# 第一种写法默认解析成字符串。第二种才会被当作一个list。可以混合int和str，和列表差不多。
```

### yaml 写字典：

```yaml
yasumi_clock:
  main_window:
    window_pos:
    - 100
    - 100
    - 700
    - 450
    start_draw:
    - 277
    - 194
    - 166
    - 49
    start_fanqie:
    - 281
    - 333
    - 167
    - 50
```

之后我们window之间的关系都会反映在这里面。所以缩进很重要，也让自己看得清晰。上一次全都是写在源码里面实在是难以忍受。



## #窗口的响应和界面代码分离。

有点模拟前后端分离的写法。因为如果控件多的话，真的混在一起会乱。

做法就是，**响应的class继承界面的class。**python的继承很好写，简单理解就是子类拥有父类所有的变量和函数。

这里主要是为了增加代码易读性和易改性，不时兴套娃，各种库里面的类嵌套看得我是很头疼的。

这里举个例子,

### 分离前:

```python
class Main_Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.config = load_config("./yasumi_config.yml")
        self.main_window = self.config["yasumi_clock"]["main_window"]
        self.main_window_pos = self.main_window["window_pos"]
        self.draw_button_pos = self.main_window["start_draw"]
        self.start_fanqie_pos = self.main_window["start_fanqie"]
        self.initUI()
    def initUI(self):
        self.setGeometry(self.main_window_pos[0],
                         self.main_window_pos[1],
                         self.main_window_pos[2],
                         self.main_window_pos[3],)
        self.setWindowTitle('Main Window')  

        self.startdrawButton = PrimaryPushButton('draw_main_window', self)
        self.startdrawButton.setGeometry(self.draw_button_pos[0],
                                         self.draw_button_pos[1],
                                         self.draw_button_pos[2],
                                         self.draw_button_pos[3])
        self.startFanqieButton = PrimaryPushButton('Start', self)
        self.startFanqieButton.setGeometry(self.start_fanqie_pos[0],
                                           self.start_fanqie_pos[1],
                                           self.start_fanqie_pos[2],
                                           self.start_fanqie_pos[3])


        self.startdrawButton.clicked.connect(self.showDrawMainWindow)

    def showDrawMainWindow(self):
        child_window_pos = self.list_all_button_pos()
        self.selectionWindow = ManualSelectionWindow(self.main_window_pos,child_window_pos)
        self.selectionWindow.show()
    def list_all_button_pos(self):
        return [self.draw_button_pos,self.start_fanqie_pos]
```

可以看到Button初始化，设置位置和click是混合在一起的。

### 我们对它进行分离:

```python
# 没有响应的界面
class Main_Window_UI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.config = load_config("./yasumi_config.yml")
        self.main_window = self.config["yasumi_clock"]["main_window"]
        self.main_window_pos = self.main_window["window_pos"]
        self.draw_button_pos = self.main_window["start_draw"]
        self.start_fanqie_pos = self.main_window["start_fanqie"]
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Main Window')
        self.setGeometry(self.main_window_pos[0],
                         self.main_window_pos[1],
                         self.main_window_pos[2],
                         self.main_window_pos[3],)
        
        self.startdrawButton = PrimaryPushButton('draw_main_window', self)
        self.startdrawButton.setGeometry(self.draw_button_pos[0],
                                         self.draw_button_pos[1],
                                         self.draw_button_pos[2],
                                         self.draw_button_pos[3])
        self.startFanqieButton = PrimaryPushButton('Start', self)
        self.startFanqieButton.setGeometry(self.start_fanqie_pos[0],
                                           self.start_fanqie_pos[1],
                                           self.start_fanqie_pos[2],
                                           self.start_fanqie_pos[3])

# 单纯的响应        
class Main_Window_Response(Main_Window_UI):
    def __init__(self):
        super().__init__()
        self.startdrawButton.clicked.connect(self.showDrawMainWindow)

    def showDrawMainWindow(self):
        child_window_pos = self.list_all_button_pos()
        self.selectionWindow = ManualSelectionWindow(self.main_window_pos,child_window_pos)
        self.selectionWindow.show()
    def list_all_button_pos(self):
        return [self.draw_button_pos,self.start_fanqie_pos]
    
# 调用时选择response
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Main_Window_Response()
    mainWindow.show()
    sys.exit(app.exec_())

```

相信我，在你的button超过十个之后，你会觉得，这是个好主意。



## #自己写draw_window的class。

在确定button的位置和大小的时候，如果直接更改x,y,w,h相当麻烦，需要反复确认。而当项目大一些运行一次PyQt启动就要四五秒。这能忍？于是手动写了一个可以画方框然后返回坐标的类，可以适用于主窗口和任意的子窗口。

### 为什么不用插件

PyQt是有插件的，支持手动画控件，然后最后直接生成一份UI的代码。这样很不好，因为不方便调试，我习惯写一部分，确认没有bug了再写下一部分。最终几乎不需要调试，那么生成最终调试的时间估计不会比我写代码短。

但是我看过我室友生成的那份代码，只能说相当炸裂，能自己写的还是不要自动生成了。而且插件很臃肿，安装是第一个关卡，摸索功能又是第二个关卡。有时间折腾，都自己实现出来了。

而我只需要，一个画框，然后返回x,y,w,h。

### 代码：

```python
from PyQt5 import QtCore, QtGui, QtWidgets
from qfluentwidgets import PrimaryPushButton
class ManualSelectionWindow(QtWidgets.QWidget):
    def __init__(self, select_window_pos,child_button_pos):
        super().__init__()
        
        self.pos = select_window_pos
        self.button_pos = child_button_pos
        self.isSelecting = False
        self.startPos = None
        self.initUI()
        
        
    
    def initUI(self):
        self.setGeometry(self.pos[0]+600,
                         self.pos[1]+150,
                         self.pos[2],
                         self.pos[3])
        self.setWindowTitle('Manual Selection Tool')
        self.setStyleSheet("background-color: white;")

        self.selectionLabel = QtWidgets.QLabel(self)
        self.selectionLabel.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.selectionLabel.setStyleSheet("border: 2px dashed red;")
        for pos in self.button_pos:
            self.selectButton = PrimaryPushButton(self)
            self.selectButton.setGeometry(pos[0],pos[1],pos[2],pos[3])


        self.setMouseTracking(True)
    

    def mousePressEvent(self, event):
        self.isSelecting = True
        self.startPos = event.pos()
        self.selectionLabel.setGeometry(QtCore.QRect(self.startPos, QtCore.QSize()))

    def mouseMoveEvent(self, event):
        if self.isSelecting:
            rect = QtCore.QRect(self.startPos, event.pos()).normalized()
            self.selectionLabel.setGeometry(rect)

    def mouseReleaseEvent(self, event):
        if self.isSelecting:
            self.isSelecting = False
            endPos = event.pos()
            rect = QtCore.QRect(self.startPos, endPos).normalized()
            self.selectionLabel.setGeometry(rect)
            print(f"Selected Rectangle: {rect.x()}, {rect.y()}, {rect.width()}, {rect.height()}")

```

这份代码我就没有手动去分离UI和response。

因为UI是根据传入的Pos自动生成的。

### 效果：

main window 中，单击draw_main_window就可以。

![main_window](https://image.baidu.com/search/down?url=https://img1.doubanio.com/view/photo/l/public/p2910589160.webp)

之后会跳出一个和main_window布局一样，但是支持手动画方框的窗口。

![draw_rec](https://image.baidu.com/search/down?url=https://img3.doubanio.com/view/photo/l/public/p2910589162.webp)

画出的方框会显示x,y,w,h在下方。

### 关于调用：

```python
# 连接到button
self.startdrawButton.clicked.connect(self.showDrawMainWindow)


def showDrawMainWindow(self):
    child_window_pos = self.list_main_button_pos()
    self.selectionWindow = ManualSelectionWindow(self.main_window_pos,child_window_pos)
    self.selectionWindow.show()
def list_main_button_pos(self):
    return [self.draw_button_pos,self.start_fanqie_pos]

```

布局会显示多少取决于传入的child_window_pos。



## #控件



### 0.Window 初始化和调用

```python
class Main_Window_UI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        ...
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Main_Window_Response()
    mainWindow.show()
    sys.exit(app.exec_())
```



### 1.设置Window Pos&Size&Tittle

```python
self.setWindowTitle('Main Window')
self.setGeometry(self.main_window_pos[0],
                 self.main_window_pos[1],
                 self.main_window_pos[2],
                 self.main_window_pos[3],)
```

### 2.Button(触发器,按钮)

```python
from PyQt5.QtWidgets import QPushButton
from qfluentwidgets import PrimaryPushButton

# QtWidgets自带的
self.startdrawButton = QPushButton('Draw Main Window', self)
self.startdrawButton.setGeometry(50, 50, 200, 50)

# qfluentwidgets提供的
self.startFanqieButton = PrimaryPushButton('Start', self)
self.startFanqieButton.setGeometry(self.start_fanqie_pos[0],
                                   self.start_fanqie_pos[1],
                                   self.start_fanqie_pos[2],
                                   self.start_fanqie_pos[3])

# 连接触发函数，注意不要传入()，只是传入地址:
self.startdrawButton.clicked.connect(self.showDrawMainWindow)
```

![有美化和无美化](https://image.baidu.com/search/down?url=https://img3.doubanio.com/view/photo/l/public/p2910589163.webp)

白色的是自带的，青色的是引入的。

主要是字体也变了。原本的字体似乎是windows自带的字体。我也忍不住跟着吐槽一句，比尔盖茨什么都好，就是没审美=-=。那个字体用来做代码看得是不错，但是用来当button，真的看不清，而且毛刺感很强，很扎眼睛，在纯白的背景下。放一组近距离对比：

![soft](https://image.baidu.com/search/down?url=https://img3.doubanio.com/view/photo/l/public/p2910589167.webp)![hard](https://image.baidu.com/search/down?url=https://img9.doubanio.com/view/photo/l/public/p2910589165.webp)

UI这东西，感官体验上区别就是这么一点点积累起来的。

### 3.创建窗口并且用按钮打开。

其实PyQt中没有父子关系。可以理解为，就是另一个窗口被当前主窗口触发了。因此你也会发现关掉主窗口并不会让子窗口自动关闭，而是需要关掉所有窗口才会退出程序。

可能也存在真正的父子窗口，但这里我没用到。

```python
self.startdrawButton.clicked.connect(self.showDrawMainWindow)

def showDrawMainWindow(self):
    child_window_pos = self.list_main_button_pos()
    self.selectionWindow = ManualSelectionWindow(self.main_window_pos,child_window_pos)
    self.selectionWindow.show()
```

以这个为例，我的ManualSelectionWindow也是继承于QtWidgets.QWidget。

也同样就是初始化类，然后调用show()就可以了。

>
>
>我目前发现的一个父子关系，在于Button和Label创建时传入的self,这个会将该Button和self建立父子关系绑定在一起。
>
>如果传入其他Window的实例，则会和其他Window绑定在一起。一般用self。

### 4.Draw Picture in Window。

我先调了一下布局，让出了一些空间给贴图。如果config.yml用得好，那么改布局只需要改config就行了，很方便。

![调了一下布局](https://image.baidu.com/search/down?url=https://img1.doubanio.com/view/photo/l/public/p2910589168.webp)

确定了一下贴图的Pos和Size:

![确定要贴图的区域](https://image.baidu.com/search/down?url=https://img1.doubanio.com/view/photo/l/public/p2910589169.webp)

大概7:6，那我就截一张7:6的图：

![选一张差不多比例的图.](https://image.baidu.com/search/down?url=https://img2.doubanio.com/view/photo/l/public/p2910589171.webp)

这里我创了一个src.yml。

```yaml
example: "./src/img/example.jpeg"
```

Init UI中创建Label Object(和按钮们排在一起):

```python
self.animation_label = QtWidgets.QLabel(self)
self.animation_label.setGeometry(QtCore.QRect(self.animation_pos[0],
                                              self.animation_pos[1],
                                              self.animation_pos[2],
                                              self.animation_pos[3]))
self.animation_label.setText("")
self.animation_label.setObjectName("Animation")

# 在Init_UI中调用贴图函数
self.Draw_Image(Label=self.Animation_Label,
                path=self.example_img_path,
                Pos=self.animation_pos)
```

然后单独写一个贴图函数:

```python
def Draw_Image(self,Label,Pos,path=None,frame=None):

    img = Image.open(path)
    img = img.resize((Pos[2],Pos[3]),Image.BILINEAR)
    img = np.array(img)
    rgb_image = img

    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(q_img)
    Label.setPixmap(pixmap)
```

这样就有了：

![这样就有了](https://image.baidu.com/search/down?url=https://img3.doubanio.com/view/photo/l/public/p2910589172.webp)

#### 进阶用法：

但其实它可以用来画动画，画摄像头的帧等等。

这里演示画动画。

但在这之前，我们插入一个Qt多线程工作的部分。当一个按钮耗时很长时，如果没有独立线程，就会出现这个按钮按下去后，窗口就无响应了，不接受任何消息，拖动，关闭，都不接受。而且要画动画的话是一个持续的过程，如果不独立线程就会把主线程塞住，while true里面出不来。

如果你用过Python自带的thread.Threading，你可能可以实现你想要的功能。但相信我它只会坑你，是个大坑。自带的Threading线程是进程级的，和你开的main window一个级别，当你关掉main window,你会发现你的程序依然没有退出。因为仍然卡在threading中，这会埋下很大隐患。

#### 安全地添加多线程：

这里介绍一种比较安全的Threading方法。

```python
import sys
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from time import sleep

# 继承自QThread的自定义线程类
class MainWindowWorkerThread(QThread):
    # 自定义信号，用于向主线程发送信息
    update_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        # 模拟耗时操作
        for i in range(1, 11):
            sleep(1)  # 模拟耗时操作
            self.update_signal.emit(f"Task Progress: {i * 10}%")
        self.update_signal.emit("Task Complete")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QThread Example')
        self.setGeometry(100, 100, 400, 200)

        self.label = QLabel("Task Progress: 0%", self)
        self.label.setGeometry(50, 50, 300, 30)

        self.startButton = QPushButton("Start Task", self)
        self.startButton.setGeometry(50, 100, 100, 30)
        self.startButton.clicked.connect(self.start_task)

        self.thread = None

    def start_task(self):
        if not self.thread or not self.thread.isRunning():
            self.thread = MainWindowWorkerThread()
            self.thread.update_signal.connect(self.update_progress)
            self.thread.start()

    def update_progress(self, msg):
        self.label.setText(msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
```



我模拟了一个耗时十秒的工作，如果不用多线程，你将在按下按钮后十秒内无法对窗口执行任何操作。

而上面是安全地添加线程的方法。我上次改Qt的时候，很大的一个不稳定因素就是来源于python自带的thread,它甚至会和一些button争抢资源，导致一个窗口刚刚打开就闪退。我之前一直不知道是这个原因。

#### 用多线程更新帧

那么我们学着做，开一个线程给Animation画图。

加入这些:

class Main_Window_UI(QtWidgets.QWidget):

```python
def __init__(self):
        super().__init__()
        self.animation_thread = None
        ...
        self.initUI()
def initUI():
    ...
    self.start_drawgif_task()
    
def start_drawgif_task(self):
    if not self.animation_thread or not self.animation_thread.isRunning():
        self.animation_thread = DrawAnimationThread()
        self.animation_thread.setup(path=self.example_gif_path,
                                          label=self.animation_label,
                                          pos=self.animation_pos,
                                          frame_speed=12)
        self.animation_thread.start()
```

Thread class:

```python
import sys
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap, QImage,QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from time import sleep
import numpy as np
from util import split_gif_to_frames
from PIL import Image

# 继承自QThread的自定义线程类
class DrawAnimationThread(QThread):
    update_signal = pyqtSignal(np.ndarray)
    def __init__(self):
        super().__init__()
    
    def setup(self,path, label, pos, frame_speed=24):
        self.path = path
        self.label = label
        self.pos = pos
        self.frame_speed = frame_speed
    def run(self):
        self.running = True
        frames = split_gif_to_frames(self.path)
        while self.running:
            for frame in frames:
                if not self.running:
                    return
                rgb_image = frame.resize((self.pos[2],self.pos[3]),Image.BILINEAR)
                rgb_image = np.array(rgb_image)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_img)
                self.label.setPixmap(pixmap)
                sleep(1 / self.frame_speed)

```

这样子可以复用多次，如果有多个地方需要动画的话，就初始化多个类实例即可。

最终会像这样，因为我这里不支持gif，我截了两帧:

![animation](https://image.baidu.com/search/down?url=https://img3.doubanio.com/view/photo/l/public/p2910589173.webp)

![animation2](https://image.baidu.com/search/down?url=https://img9.doubanio.com/view/photo/l/public/p2910589176.webp)

好家伙，找不同。其实PyQt可以解析gif的图像，但是，学会多线程是有必要的，建议为所有耗时较久的控件都加上独立线程，而这个是一个很好的例子。另外，请避免使用thread.Threading。用Qthread中的run方法替代。

因为小问题可能会在某个瞬间爆发然后杀了你，与其到时候再修修补补，不如现在就规范地使用。



### 5.设置icon图标。

```python
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Main_Window_Response()
    mainWindow.setWindowIcon(QIcon(mainWindow.src_config["icon"]))
    mainWindow.show()
    sys.exit(app.exec_())
```

只需要在类示例那边加一个设置icon的方法即可，传入的是路径。一般只要是图片都支持。

![icon](https://image.baidu.com/search/down?url=https://img3.doubanio.com/view/photo/l/public/p2910589177.webp)

### 6.Set text:

之前那个太丑了，之后用到了找一个美化过的。

## #一个想法：

之前在开启项目的时候要挺久，需要四五秒到五六秒，比如3dsmax开启很久，就会被人喷说它打开项目的时间都够blender做个模型了。

我对加载也是很没有耐心的。

但是我们如果开大的开不起来，可以先开小的。

就是，在打开我们主程序窗口之前，先开一个加载窗口，里面放上一些有意思的动画，或者加载动画。让人觉得时间没那么久。

我们现在就来试一下。

![加载动画](https://image.baidu.com/search/down?url=https://img1.doubanio.com/view/photo/l/public/p2910589178.webp)

### LoadingWindow:

```python
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QMainWindow

from PyQt5.QtCore import Qt
from util import load_config
from MainWindowThread import DrawAnimationThread
# 定义加载窗口类
class LoadingWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.windowconfig = load_config("./yasumi_config.yml")
        self.src_conifg = load_config("./src.yml")
        self.LoadingWindow = self.windowconfig["yasumi_clock"]["LoadingWindow"]

        self.animation_thread = None
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Loading...")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setFixedSize(self.LoadingWindow["window_pos"][0],
                          self.LoadingWindow["window_pos"][1])  # 固定窗口大小
        self.setStyleSheet("background-color: white;")  # 设置背景色为白色
        
        # 隐藏最小化，关闭等按键
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMinimizeButtonHint)  # 设置窗口标志位
        self.animation_label = QLabel(self)
        self.animation_label.setGeometry(QtCore.QRect(self.LoadingWindow["animation"][0],
                                                      self.LoadingWindow["animation"][1],
                                                      self.LoadingWindow["animation"][2],
                                                      self.LoadingWindow["animation"][3]))
        self.start_drawgif_task()


    def start_drawgif_task(self):
        if not self.animation_thread or not self.animation_thread.isRunning():
            self.animation_thread = DrawAnimationThread()
            self.animation_thread.setup(path=self.src_conifg["loading"],
                                              label=self.animation_label,
                                              pos=self.LoadingWindow["animation"],
                                              frame_speed=24)
            self.animation_thread.start()

```



### 重写Show，在打开主窗口后关闭Loading窗口

```python
class Main_Window_Response(Main_Window_UI):
    def __init__(self,loading_window):
        super().__init__()
        self.startdrawButton.clicked.connect(self.showDrawMainWindow)
        self.loadingwindow = loading_window
        

    def showDrawMainWindow(self):
        child_window_pos = self.list_main_button_pos()
        self.selectionWindow = ManualSelectionWindow(self.main_window_pos,child_window_pos)
        self.selectionWindow.show()
    def Show(self):
        self.show()
        self.loadingwindow.close()

    def list_main_button_pos(self):
        return [self.draw_button_pos,self.start_fanqie_pos]
```

### 加入延时，因为目前主窗口打开得太快了。

```python
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    
    loading_window = LoadingWindow()
    loading_window.show()

    mainWindow = Main_Window_Response(loading_window)
    mainWindow.setWindowIcon(QIcon(mainWindow.src_config["icon"]))

    timer = QtCore.QTimer()
    timer.singleShot(3000, mainWindow.Show)  # Delay mainWindow's show by 1 second
    

    sys.exit(app.exec_())
```





所有代码已经传到github:

[MrXnneHang/Yasumi-Clock](https://github.com/MrXnneHang/Yasumi-Clock)

这一次算是总结了上次用到的所有PyQt的功能，并且更正了不安全的地方。明天可能会探索一下我要写番茄钟需要的功能，比如按时间缩减的沙漏。但其实根据今天的经验，只需要先做个动画，然后再多线程画上去就可以了。不过得探索一下怎么设置alpha通道透明背景。不然颜色不一样太扎眼了。


## #多线程的bug和解法
### QThread: Destroyed while thread is still running



```python
class Main_Window_Response(Main_Window_UI):
    def __init__(self,loading_window):
        super().__init__()
        self.startdrawButton.clicked.connect(self.showDrawMainWindow)
        self.startFanqieButton.clicked.connect(self.startFanqie)
        self.loadingwindow = loading_window
        
    def startFanqie(self):
        loadingwindow = LoadingWindow()
        loadingwindow.show()
```

发生再startFanqie这边，因为我用的是局部变量。当函数执行完了就直接退出了。变量被销毁，类实例没了，所以就会报错，线程在运行时被销毁。

将loadingwindow 改成 self.loadingwindow即可，这样除非主窗口被销毁，否则就不会被销毁。


# Explore PyQt Designer

## sipPyTypeDict() is deprecated      

Solve:

[https://github.com/MrXnneHang/QT-Designer-Explore/blob/master/issuses.md](https://github.com/MrXnneHang/QT-Designer-Explore/blob/master/issuses.md)

Issue[1]

## clicked.connect  误触发函数。

```python
# ✔
self.startdrawButton.clicked.connect(self.showDrawMainWindow)

# ❌
self.path_selector_1.clicked.connect(self.open_file_dialog(self.path_line_1))
```

正常传入函数地址，不会触发函数，只有点击时才会触发。

但是在传参进去后，会在执行绑定时触发。需要用lambda:

```python
self.path_selector_1.clicked.connect(lambda:self.open_file_dialog(self.path_line_1))
```



##  Path Select

### File:

```python
def open_file_dialog(self,line_edit):
    # 弹出文件对话框
    path = QFileDialog.getOpenFileName(self, "选择文件位置", "")
    # path-like:
    # ('D:/program/Designer/README.md', 'All Files (*)')
    if path:
        # 将选择的路径设置到LineEdit中
        line_edit.setText(path[0])  
```

Use

```python
line_edit.text()
```

来获取text。

### Directory:

Use:

```python
QFileDialog.getExistingDirectory
```



经过测试，都是只能单选，不能多选。



## 隐藏Layout下的所有项目。



```python
from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout

def hidden_layout(layout):
    """隐藏布局及其子控件

    layout: QVBoxLayout/QHBoxLayout ,可以传入列表

    hidden_layout(Layout1)
    hidden_layout([Layout1,Layout2])
    """
    if isinstance(layout, list):
        for i in range(layout):
            hidden_layout(i)
    for i in range(layout.count()):  # 遍历子控件
        item = layout.itemAt(i)
        if isinstance(item, QVBoxLayout) or isinstance(item, QHBoxLayout):  # 检查是否为QLayoutItem
            hidden_layout(item)
        else:
            widget = item.widget()  # 获取子控件
            widget.setVisible(False)  # 递归调用隐藏子布局
```



依然存在瑕疵，就是当我隐藏部分布局，和它同级的布局会因此而改变，我希望它保持不变。



## Check Box



```python
class RSP_ChartSelector(QMainWindow,Ui_ChartSelector):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Connect the CheckBox signal to a slot
        self.line_chart.stateChanged.connect(self.on_checkbox_state_changed)  
        self.bar_chart.stateChanged.connect(self.on_checkbox_state_changed)
        self.pie_chart.stateChanged.connect(self.on_checkbox_state_changed)
        # Set initial state of CheckBox
        self.bar_chart.setChecked(True)


    def on_checkbox_state_changed(self, state):
        if state == 0:
            print("CheckBox is unchecked")
        elif state == 2:
            print("CheckBox is checked")
```

上面适用于立即触发，我们到时候也有用，当勾选后立刻更新图片而非再次手动点击生成图片。

另外也可以通过这个方式来获取是否被选中:

```python
if self.line_chart.isChecked():
    print("Line Chart CheckBox is checked")
```


## Tab:

![Snipaste_2024-07-21_20-30-36](https://image.baidu.com/search/down?url=https://img2.doubanio.com/view/photo/l/public/p2910896221.webp)

不打开新窗口，但切换不同页面。

QT Designer自带Tab，拖进去即可。

这里贡献一份美化。

```css
QTabWidget::pane {
    border-top: 2px solid rgba(0, 0, 0, 1); /* 黑色 */
}

QTabBar::tab {
    font-family: "Microsoft YaHei";
    font-size: 12px;
    font-weight: 500;
    padding: 10px 25px; /* 增加内边距 */
    border-bottom: none;
	min-width: 45px;
   
}

QTabBar::tab:selected {
    color: rgba(123,190,254, 1); /* 淡蓝色 */
    border-bottom: 2px solid rgba(123,190,254, 1); /* 淡蓝色 */
}

QTabBar::tab:!selected {
    margin-bottom: 2px;
}

```

关于qss的写法。

现在看来和C++的类很像。每个对象的qss只能编辑自己，但之所以会有多个不同的{}，是因为一个对象有不同的子对象::，和不同的状态:。

常见状态,hover,selected。

### 还需要补充:

* 如果创建三个以上的Tab，默认只有两个。

## 用 Button 链接Tab。

RSP:

```python
class RSP_Tab(QMainWindow,Ui_Tab):
    def __init__(self)->None:
        super().__init__()
        self.setupUi(self)
        self.t1_switch_t2_button.clicked.connect(self.switch_to_tab2)
        self.t2_swicth_t1_button.clicked.connect(self.switch_to_tab1)
    
    def switch_to_tab1(self):
        util.switch_tab_index(self.TabWidget,1)
    def switch_to_tab2(self):
        util.switch_tab_index(self.TabWidget,2)
```

util:

```python
def switch_tab_index(TabWidget,index):
    TabWidget.setCurrentIndex(index-1)
```



### 值得注意的是，tab的index是从0开始的。

## 可以被触发的Label。

因为Label可以直接贴上贴图，甚至可以播放动画,gif。所以我当时死磕要把Label当成Button用。因为开始界面我想做点动态的。

ClickQLabel:

```python
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal, QPropertyAnimation, QRect, Qt



class ClickQLabel(QLabel):
    """可以被触发的Label
    
    @func:
    animate_geometry:缩放Label。
    
    """
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initial_geometry = None  # 记录初始几何位置
        self.setAlignment(Qt.AlignCenter)  # 设置文本居中
        self.init_animation()



    def init_animation(self):
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(30)  # 动画持续时间30毫秒

    def enterEvent(self, event):
        if self.initial_geometry is None:
            self.initial_geometry = self.geometry()  # 记录初始几何位置
        self.animate_geometry(scale=1.12)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animate_geometry(scale=(1))  # 恢复到原始大小
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def animate_geometry(self, scale):
        if self.initial_geometry is None:
            return

        width = self.initial_geometry.width()
        height = self.initial_geometry.height()
        new_width = width * scale
        new_height = height * scale
        new_x = self.initial_geometry.x() - (new_width - width) / 2
        new_y = self.initial_geometry.y() - (new_height - height) / 2
        new_geometry = QRect(new_x, new_y, new_width, new_height)
        
        self.anim.stop()
        self.anim.setStartValue(self.geometry())
        self.anim.setEndValue(new_geometry)
        self.anim.start()


```

目前把代码缩减了，只剩下缩放动画，以及我依然屈服地使用了hover。可恶，因为qss读不进来。QT Designer生成QLabel，我将QLabel替换成ClickLabel。按理说它有SetStyleSheet，但是我读不到。

以及hover的一个毛病，它不是渐变色，看上去变色变得挺着急的。

但没事，逼急了，我直接做个动画，然后把动画拿去播放。关于那个阴影问题。

动画:
把图片饱和度调高一丢丢

把图片亮度调低一丢丢

把边框由黑色调成白色

变化时长0.1s.

### 有待解决:

* 每次缩放动画的时候字体都会抖一下，但增大缩放倍率，也不会抖得更厉害，幅度永远是一丢丢，但这一丢丢我看得很难受。

* 制作渐变色
* 制作动画



## 纸飞机，快速回到定位的某一个段。

```python
def scroll_to_last_self_message(self):
if self.self_message_indices:
    last_self_index = self.self_message_indices[-1]
    self.message_list_lswdg.scrollToItem(self.message_list_lswdg.item(last_self_index), QAbstractItemView.PositionAtTop)
    self.current_message_index = last_self_index

def locate_previous_message(self):
if self.self_message_indices:
    current_pos = self.self_message_indices.index(self.current_message_index) if self.current_message_index in self.self_message_indices else -1
    if current_pos > 0:
        previous_index = self.self_message_indices[current_pos - 1]
        self.message_list_lswdg.scrollToItem(self.message_list_lswdg.item(previous_index), QAbstractItemView.PositionAtTop)
        self.current_message_index = previous_index

def locate_next_message(self):
if self.self_message_indices:
    current_pos = self.self_message_indices.index(self.current_message_index) if self.current_message_index in self.self_message_indices else -1
    if current_pos < len(self.self_message_indices) - 1:
        next_index = self.self_message_indices[current_pos + 1]
        self.message_list_lswdg.scrollToItem(self.message_list_lswdg.item(next_index), QAbstractItemView.PositionAtTop)
        self.current_message_index = next_index
```

化身无情调试机器和gpt对话一个小时最终解决。  

效果还是相当惊艳的。

如果消息够长，它总是能够把自己的消息定位到最上层。

![Snipaste_2024-07-21_20-54-11](https://image.baidu.com/search/down?url=https://img3.doubanio.com/view/photo/l/public/p2910896222.webp)

如果间隔不够长，也会把两条都定位出来，并且不会再重复点击两次才切换。

![Snipaste_2024-07-21_20-54-24](https://image.baidu.com/search/down?url=https://img1.doubanio.com/view/photo/l/public/p2910896220.webp)

我可能那时候真有点累，午睡就睡了一小会儿。

不得不说，早上刚刚起床的时候，是觉得，20分钟太短了，经常偷偷不计时然后干个四五十分钟。

但下午的时候，特别是到了六点，差不多只要十分钟左右就感觉有点昏了。

所以说专注也是个体力活。跑步还是得跑的。又偷懒了两天。

## 编辑资源。

在QT Designer中特别贴心地把它放在很显眼的位置。

右下角资源浏览器->resource root -> 添加。

而且似乎这么做的话最终引用的图片都会生成一个.py文件里面会有png什么hard编码。

![Snipaste_2024-07-21_21-01-56](https://image.baidu.com/search/down?url=https://img1.doubanio.com/view/photo/l/public/p2910896219.webp)



之后会整理一个QT Designer Explore,所有的待补充和待完善都会集中在那里。

以及这里又是一次忠告。当我们一个实现行不通的时候，一定记得换一个实现。不要徒增bug，徒耗时间。

## 高dpi导致窗口看起来异常。

表现，在1080p上面表现和QTDesigner中一样。

但是放在4k屏幕上面就挤成一坨。

Issue:

[https://linux.do/t/topic/156959](https://linux.do/t/topic/156959)

>QT Designer中预览窗口正常，控件也会自适应缩放，有用spacer和layout。
>最终在4k屏幕和1080p上面表现差异巨大。
>在1080p下和预览的一致。
>而4k下屏幕和控件缩成一团。
>用resize把main窗口缩放两倍后，控件排版正常了，但是所有字体都很小。大概也只有预览的一半大小。
>
>应该如何解决？字体几乎都是写在stylesheet里面的。

Solve:

[https://doc.qt.io/qt-6/highdpi.html](https://doc.qt.io/qt-6/highdpi.html)

具体解法:

创建app之前设置高dpi自适应，以及pixmap高Dpi自适应。

```python
QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
app = QtWidgets.QApplication(sys.argv)
```

我的env:

```cmd
PyQt5==5.15.4 
PyQt5-Qt5==5.15.2 
PyQt5-sip==12.12.1
pyqt5-tools==5.15.4.3.0.3
```



## 学会了弹性窗口和自定义布局。

### Layout

之前我一创建空项目（只有一个MainLayout）就会开始往里面拖Layout。

其实并不建议直接拖动Layout。

我现在是把Widget当作Layout用。因为Widget可以在Layout中自动填充，自适应缩放。并且Widget可以内置Layout。可以实现Widget嵌套Widget。

以前手动拖动Layout真的不是人干的事情。

具体操作可以参考:

[https://www.bilibili.com/video/BV1gT4y1e7Pj/?spm_id_from=333.1007.top_right_bar_window_history.content.click](https://www.bilibili.com/video/BV1gT4y1e7Pj/?spm_id_from=333.1007.top_right_bar_window_history.content.click)

大概看个三四分钟，就能明白，其他操作都是一样的。



### Spacer

Spacer

建议使用max和min。

我没弄明白expanding的意义是什么。

经常可以一个max一个min。

然后ctrl+r看看window顺便再缩放一下。能达到预期效果就行。

**碰到问题。**

QT Designer自动生成.py的时候,spacer的命名会被格式化，而并不是用我的命名，不清楚为什么。其他的Object基本上都能够正常。

这样子就存在一个问题。

比如我之前碰到在写聊天气泡的时候，

实现左边发送和右边发送，就是靠删掉一个spacer。但是由于spacer不存在，命名不同，就很难用生成的代码进行交互。

这里的解决依然是，用widget当spacer就好。



## 并不是所有的窗体都是指定死的。

比如说聊天气泡。随着发送得越多，每次发送会自动产生一个内容。

这种程序性生成也是很重要的。

而且很巧，只要留一个widget给它。

它可以自己在里面写layout。然后比如这次的气泡。就是一列下来。


## QT Designer中的样式表并不是只针对该对象。

我最初以为样式表是针对该对象的。
但是样式表针对这些：该对象的不同状态（:hover,:selected）,该对象的不同子组件(::tab), **以及，该对象的所有对象(实例)。(#background)【#对象名】** 又由于Qwidget可以支持一个套一个。

如果我在最外层的Qwidget写上

```css
background-image:url(:/bg/resource/draw/bg.jpg);
background-repeat:no-repeat;
background-position:center;
background-size: contain;
```

就会碰上下面所有对象都会是以这个背景图片为背景的现象。

正确的写法:

```css
QWidget#background{
background-image:url(:/bg/resource/draw/bg.jpg);
background-repeat:no-repeat;
background-position:center;
background-size: contain;}

/*实测你也可以用#background来指定，这个是变量名。*/
```

用类#示例名称来指定你要赋予的对象。

当然你也可以在这里赋予子对象属性。

当我这么写:

```css
QWidget#background{
background-image:url(:/bg/resource/draw/bg.jpg);
background-repeat:no-repeat;
background-position:center;
background-size: contain;}

#tab_1{
background-image:url(:/bg/resource/draw/bg.jpg);
background-repeat:no-repeat;
background-position:center;
background-size: contain;}

```

就会让tab_1和background具有相同属性。

但是要想让他生效，需要该类具有相同的属性，或者说它们是相同类，那么这种qss是可以继承的。

更多参考:
[https://blog.csdn.net/qq_56720262/article/details/131733284](https://blog.csdn.net/qq_56720262/article/details/131733284)



## 给窗口制作圆角。

有了上面那个Background的Widget作为背景，我们其实只需要把background image给做个圆角，然后隐藏窗口上面QMainWindow自带的最小化关闭那一栏隐藏了就行。

qss做倒角:

```css
QWidget#background{
background-image:url(:/bg/resource/draw/bg.jpg);
background-repeat:no-repeat;
background-position:center;
border-radius: 6px;}
```

是radius那一行，如果你喜欢圆润一点，可以设的更大，比如20px。

然后Python代码隐藏菜单栏。

```python
from PyQt5.QtCore import Qt

# 隐藏菜单栏
self.setWindowFlags(Qt.FramelessWindowHint)
self.setAttribute(Qt.WA_TranslucentBackground)

# self是QMainWindow对象。
```





## 给窗口制作阴影（投影）。

```python
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

# 创建阴影效果
shadow = QGraphicsDropShadowEffect()
shadow.setBlurRadius(20)  # 模糊半径
shadow.setXOffset(0)  # X方向的偏移
shadow.setYOffset(0)  # Y方向的偏移
shadow.setColor(QColor(0, 0, 0, 160))  # 阴影颜色 (黑色，160透明度)
# 将阴影效果应用到窗口(实际上是应用到背景图像的widget上)。
self.background.setGraphicsEffect(shadow)
```

这里的self.background是窗口最外层包含background的widget。qss等见#1.





## 写在最后。



似乎就算我一天看两部电影，几乎没怎么去想那个项目，最后解决的问题和做的进度和我一整天盯着也没差多少。

甚至可能更多一些。

我觉得更多是钻牛角尖。

比如这个窗口阴影的问题，我最初跟着别人做，他用ps制作了投影效果。我也跟着做，但是他做的是非弹性窗口，就是不会缩放的，不用管布局，只要使劲叠就行。但我要做窗口可以接受缩放就得考虑布局。

他用QLabel来做，我这里QLabel放下去整个布局就填满了，不存在叠加性。至少我没学会。布局里面一般我常用水平和垂直，不存在叠加。我先是考虑了半天叠加，无果，又试着用qwidget的stylesheet。但是有个问题。图片加载进来，只加载到了有rgb值的位置，投影部分实际是透明的，也就没能加载进来。结果加载进来的图片没有阴影。我大概在这里钻牛角尖钻了一个中午。

在我去看了一部电影后我打算换实现。

就是我不用画好的图片，而是用一张没有阴影没有圆角的纯背景，然后用qss做倒角，用QGraphicsDropShadowEffect来做阴影。可以说倒角和阴影合起来才花了我二十分钟的时间，还顺便学会了#1,我想不明白我为什么要花那么久时间掉在一个实现里面。换实现呗。 

以及一些问题想是想不明白的，适当的时候应该去问，比如:  

[开源字体网站（字体用于需要交付的软件嵌入）](https://linux.do/t/topic/157878/1)  

很感谢那个解了我燃眉之急的大佬。  

我觉得自己前几天也很多次陷入这种坑里面。这个时候换个事情做或许会比较好。

到这里我的QT即使不算专精，也是能够自由自定义了。

但我依然在想，难道不能像psd里面叠加图层那样叠加渲染吗？布局还是有点死板的。

