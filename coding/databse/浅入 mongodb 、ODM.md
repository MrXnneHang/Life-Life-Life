## 开始

https://github.com/mongodb/mongo

mongo 是一个相当活跃的社区。

而且我见过的不少优秀的博客系统似乎都是以 mongodb 作为数据库的。

它有自己独立的数据库编辑和查看工具 mongodb compass

https://github.com/mongodb-js/compass

当然最重要的是，它不同于 MySQL 的数据存储方式让我觉得很对胃口。它是非关系型数据库，它可以不断地"中途变卦",虽然这不是好习惯，但是，在开发一些特殊场景时，比如某天我希望给 Agent 增加一个功能，或者突然地想要新增一个功能且这个功能需要用到数据库。我并没有很早地为它规划出位置（我这人真的不善规划），那么我希望可以临时加入而不是再花费大量时间重新开始。

如果说 MySQL 就像一个严谨的一丝不苟但是不懂变通的老学究，那么 MongoDB 则更像是一个充满活力和创造力且包容力极强的导师。

如果你觉得我讲得过于抽象，那么请移步

[# MySQL vs MongoDB | 说起来我上次看 langchain and langraph 也是这个老头，真的是博而不精](https://www.youtube.com/watch?v=OdgZ0jr4jpM)

如果你希望更加专业和具体的:

https://www.geeksforgeeks.org/mongodb-vs-mysql/

> MongoDB 和 MySQL 都是流行的数据库管理系统（DBMS），但它们的用途不同，功能也各不相同。MongoDB 是一种 NoSQL 数据库，专为处理具有高扩展性的非结构化数据而设计，而 MySQL 则是一种传统的关系数据库管理系统（RDBMS），非常适合处理具有复杂关系的结构化数据。<br>
> 在本文中，我们将探讨 MongoDB 和 MySQL 之间的主要区别、它们的功能、用例以及如何决定哪一个最适合您的项目需求。我们还将深入探讨两者的优势和局限性，以便根据您的具体应用需求做出更明智的选择。<br>
## 安装和启动

我选择了 docker 。

```shell
docker pull mongo
docker run -d -p 27017:27017 mongon
```


然后查看状态:

```shell
➜  Downloads docker ps
CONTAINER ID   IMAGE     COMMAND                   CREATED       STATUS       PORTS                                           NAMES
5dfa55496560   mongo     "docker-entrypoint.s…"   4 hours ago   Up 4 hours   0.0.0.0:27017->27017/tcp, :::27017->27017/tcp   adoring_perlman
```

## MongoDB Compress

https://www.mongodb.com/products/tools/compass

下载用于可视化数据库的工具。当然不反对 `mongosh`。 但这里不教 0.0。


## What is ODM

> **ODM (Object Document Mapper)**，中文通常译作“对象文档映射器”，是一种用于在面向对象编程语言和文档型数据库之间进行数据转换的工具。简单来说，它允许开发者使用熟悉的面向对象语法（如类、对象、属性等）来操作文档型数据库中的数据，而无需直接编写数据库的查询语言（例如 MongoDB 的 BSON 查询语法）。<br>

简单说, 大多数时候面向数据库编程，包括之前在用 MySQL 的时候，大多代码量实际上浪费在了把 Python 数据结构存储到表中。比如说 str -> char(256) 一大堆的。以及有时候一个 TypedDict 可能要拆分到不同的表里面进行保存，而且有时候多个表用到的时候需要保存多次或者非常高深莫测的创建一个图映射。这块内容实际上很不友好。

更多时候实际上开发者更愿意把精力投入在要做的内容上，而不是数据库的管理上，而不严谨的设计还可能导致后续得推倒重来。比如发现 char 的长度不够用了，当然这是最简单的情况。

而 ODM 则让我们可以不必关心那么多。它让我们可以把一个 Python 的类直接地转换为可以存储到数据库中的类，有时候还简化了 CRUD 的操作。或者更加简单来说它减少了我们花费在数据库管理上的精力，让我们可以更加专注地开发我们想要的东西，而这正是我想要的。

https://www.mongodb.com/zh-cn/docs/drivers/

Mongo 有一个非常有活力的 ODM 社区。对于 Python , 我选用了 Beanie。


> - **Beanie：** Beanie 是一个异步的 MongoDB ODM，它基于 `Motor` (MongoDB 的异步驱动) 和 `Pydantic`。Beanie 的设计目标是提供一个现代、高效且易于使用的异步接口来操作 MongoDB。<br>

## 构建我们的 MongonDB 应用

### 架构

先说一下架构。我们实际上不希望直接操作数据库，或者说，大部分时候，我们希望看不见数据库里那些弯弯绕绕的。

所以这里我们大概用这样的架构:

![MongoDB_FastAPI.png](../../dist/img/MongoDB_FastAPI.png)

我们大部分写应用的时候只关心我们的应用。对于 DB 的操作全部用 FastAPI 代理，这样也方便远程操作。

### 代码

https://juejin.cn/post/7112748113860755469

有的抄为何不抄

> 如果你发现它挂了也欢迎查看我的这个 PR ，它包含了这个用例。<br>
> https://github.com/XnneHangLab/XnneHangLab/pull/39 <br>

中间碰到了这样的问题

`422 Unprocessable Entity`

具体解法参见: 

https://stackoverflow.com/questions/77262447/getting-error-422-unprocessable-entity-in-my-fastapi-python-demo-api

问题在于 ruff 建议我使用 `name: str | None` 来替代 `Optional[str]`. 而这两个在高版本(>=3.11)的 Python 中似乎和低版本中有出入。

具体表现为:

It's a bit unintuitive, but `Optional` in python only meanst that the value can also be `None`. It doesn't actually make `id` optional, to achieve that, you must provide a default value:  

这有点不直观，但在 python 中， `Optional` 只表示该值也可以是 `None` 。 实际上，它并没有使 `id` 成为可选值，要做到这一点，必须提供一个默认值：

```python
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: str
```

意思是说，如果我没有给它指定 `= None` , 那么即使我的选项中存在 None `str | None`,  Pydantic 依然会把它当作是 `str required`。

那么我在 put 的时候传入不完整的内容就会被阻止: 

`{"detail":[{"type":"missing","loc":["body","date"],"msg":"Field required","input":{"name":"Abdulazeez Abdulazeez","product":"TestDriaven TDD Course","rating":5.0,"review":"hello"}}]}`

少什么就会报什么，并且，全量修改（传入所有的参数）不会引起这个错误。

解法就是在 `str | None` 这样后面显式赋值 None.
