一直以来除了基本的 `cd`, `mkdir`, `cat`, `ls`, `chmod` 等几乎天天用到的指令外，其余的我几乎都是要用的时候问大模型，这也间接导致了，我实际上不会写 shell 脚本。还是应该放一个在这里作为查询。

### 文件系统

#### df

```shell
➜  ~ df -h
文件系统        大小  已用  可用 已用% 挂载点
udev            7.6G     0  7.6G    0% /dev
tmpfs           1.6G  5.8M  1.6G    1% /run
/dev/nvme1n1p5   73G   42G   27G   62% /
tmpfs           7.7G  826M  6.9G   11% /dev/shm
tmpfs           5.0M   12K  5.0M    1% /run/lock
efivarfs        256K  119K  133K   48% /sys/firmware/efi/efivars
/dev/nvme1n1p7  104G   90G  8.9G   92% /home
/dev/nvme1n1p3  281G  276G  5.4G   99% /media/xnne/系统
/dev/nvme0n1p1  932G  731G  201G   79% /media/xnne/Data
tmpfs           1.6G  224K  1.6G    1% /run/user/1000
```

查看挂载点（分区）的空间大小和所占空间占比。但是看不了文件夹的。

#### ls 

查看文件大小，不包含文件夹，这里看不到文件夹的大小，而且都是 4k， 大概是一个指针？

```shell
➜  test git:(dev) ls -lah 
总计 224K
drwxrwxr-x  8 xnne xnne 4.0K  4月 2日 19:35 .
drwxrwxr-x 48 xnne xnne 4.0K  6月18日 20:31 ..
drwxrwxr-x  2 xnne xnne 4.0K  4月 2日 19:35 config
-rw-rw-r--  1 xnne xnne 1.2K  4月 2日 19:35 CONTRIBUTING.md
drwxrwxr-x  8 xnne xnne 4.0K  4月15日 14:23 .git
-rw-rw-r--  1 xnne xnne  435  4月 2日 19:35 .gitignore
-rw-rw-r--  1 xnne xnne  214  4月 2日 19:35 .gitmodules
-rw-rw-r--  1 xnne xnne   77  4月 2日 19:35 hot_words.txt
-rw-rw-r--  1 xnne xnne 1.1K  4月 2日 19:35 justfile
-rw-rw-r--  1 xnne xnne 1.1K  4月 2日 19:35 LICENCE
drwxrwxr-x  2 xnne xnne 4.0K  4月 2日 19:35 models
drwxrwxr-x  3 xnne xnne 4.0K  4月 2日 19:35 packages
-rw-rw-r--  1 xnne xnne   58  4月 2日 19:35 .prettierignore
-rw-rw-r--  1 xnne xnne 3.4K  4月 2日 19:35 pyproject.toml
-rw-rw-r--  1 xnne xnne  11K  4月 2日 19:35 README.md
drwxrwxr-x  3 xnne xnne 4.0K  4月 2日 19:35 src
drwxrwxr-x  2 xnne xnne 4.0K  4月 2日 19:35 tests
-rw-rw-r--  1 xnne xnne 4.3K  4月 2日 19:35 UPDATELOG.md
-rw-rw-r--  1 xnne xnne 139K  4月 2日 19:35 uv.lock
```

#### du

查看文件夹大小。

```shell
➜  test git:(dev) du -h --max-depth=0
992K    .
```

```shell
➜  test git:(dev) du -h --max-depth=1 | sort -nr
992K    .
564K    ./.git
192K    ./src
20K     ./config
8.0K    ./packages
8.0K    ./models
4.0K    ./tests
```


#### tree

```shell
➜  chatbot git:(fix-audio-fix-chat) ✗ tree -P "*.py|pyproject.toml|uv.lock" -I "__pycache__"
.
├── cache
│   ├── asr
│   ├── tts
│   └── vad_monitor
├── config
├── dist
│   └── assets
│       ├── image
│       ├── live2d_core
│       └── live2d_model
│           ├── hiyori_free_t08
│           │   ├── hiyori_free_t08.2048
│           │   └── motion
│           └── paimeng
│               ├── motions
│               ├── paimeng.4096
│               └── sounds
├── docs
├── examples
├── models
│   ├── keywords_spotting
│   └── sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01
│       └── test_wavs
├── prompts
├── pyproject.toml
├── src
│   └── chatbot
│       ├── api
│       │   ├── async_api.py
│       │   └── sync_api.py
│       ├── chatter
│       │   ├── audio_processing_workflow.py
│       │   ├── __init__.py
│       │   ├── _typing.py
│       │   ├── util.py
│       │   ├── voice_activity_monitor.py
│       │   ├── voice_recorder.py
│       │   └── wake_word_detector.py
│       ├── config_manager
│       │   ├── abs_root.py
│       │   ├── config.py
│       │   ├── __init__.py
│       │   ├── service.py
│       │   └── _typing.py
│       ├── console
│       │   ├── attribute.py
│       │   ├── colorful.py
│       │   ├── formatter.py
│       │   ├── __init__.py
│       │   ├── logger.py
│       │   └── status_bar.py
│       ├── _dictionary.py
│       ├── __init__.py
│       ├── list_model_name.py
│       ├── live2d.py
│       ├── __main__.py
│       ├── pages
│       │   ├── home.py
│       │   └── setting.py
│       ├── styles
│       │   ├── global_style.py
│       │   └── __init__.py
│       ├── tests
│       │   ├── test_async_openai.py
│       │   ├── test_async_openai_workflow.py
│       │   ├── test_async_vad.py
│       │   ├── test_gpio.py
│       │   ├── test_light.py
│       │   ├── test_openai.py
│       │   ├── test_openai_workflow.py
│       │   ├── test_play_audio.py
│       │   ├── test_porcupine_kws.py
│       │   └── test_spotter_keyword.py
│       ├── tools
│       │   ├── audio.py
│       │   ├── __init__.py
│       │   ├── live2d_mouth.py
│       │   └── timed_helper.py
│       ├── _typing.py
│       └── webui.py
└── uv.lock

34 directories, 47 files
```

我终于知道别人 Contribute.md 中的 file_tree 是咋来的了。



