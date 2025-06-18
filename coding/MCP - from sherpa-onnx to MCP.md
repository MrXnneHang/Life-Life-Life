> 今天正好 PFCC 例会在讲 MCP, 我也过去旁听了一波. 当时后半段略微提及 PaddleOCR 搭建对 MCP Server 构建的设想和预期, 也是让我补全了一点印象. 以及看到了 MCP Server 本身更多的可能性.

首先, 目前大部分人把 Agent 的工作和 MCP 混为一谈, 会议里第一个人上来就这么强调,  把原本 Agent 的工作归于 MCP, 于是乎让 MCP 变得超级恐怖, 似乎想要掌握它必须掌握一系列框架, 需要明白复杂的工作流, 而且工作流是多变且不固定的, 这让 MCP 似乎也变得复杂难解起来了.

> 我最初就是这么想的 (>\_<)

但实际上那个通常包含 `Agent - MCP Server - Tools`.

甚至可以这样 `Agent - XXX Server(当然这里可能不是 MCP 了哈, 只是类似这样的通信协议) - Agent - MCP Server - tools`, 参考 Google 的 Agent2Agent.

MCP 存在的初衷应该是为了统一, 以语音模型来说,  不同的 ASR 模型直接或者间接支持不一样的输入格式(wav, mp3, opus, m4a), 有的只支持 wav , 另外在采样率上, 有的是 16000Hz, 有的 44100Hz 或者 48000Hz. 返回的格式, 每个模型开发方似乎也都表现的不拘小节, 各不相同. 甚至在模型调用上, 有的也各不相同, 有的是 `.onnx` ,有的给出了 `.pth` ,有的是 `.pt`. 有的是 `.bin` -\_-.

而对于应用开发方来说, 那就有点惨了, 比如, [Open-LLM-VTuber](https://github.com/Open-LLM-VTuber/Open-LLM-VTuber) 中, 用到了很多 ASR 模型, 如果正常开发, 那么需要为输入预处理和输出信息规格化写很多不必要的代码, 而调用的模型越多, 重复的工作也越多. 但那个作者比较聪明, [用了 sherpa_onnx 来作为中间层](https://github.com/Open-LLM-VTuber/Open-LLM-VTuber/blob/main/src/open_llm_vtuber/asr/sherpa_onnx_asr.py), 这样子初始化后调用起来就不必考虑很多, 因为所有工作都被 `sherpa_onnx` 的逆天(非贬义)作者给包揽了. 那个作者所做的工作和 MCP Server 实际上是异曲同工, 只不过 MCP 还考虑了更多, 包括 Client 连接, 搜索功能, 执行功能, 终止连接, 整套链接和计算机网络课程上的通信协议复杂度不遑多让, 很多概念也是共通的.

但是, 所做 `sherpa_onnx` 和 MCP Server 的都是在做类似于统一协议的工作, 但两者完成方式完全不同:

`sherpa_onnx` 收录了常用的  `vad`, `asr`, `tts`, `punc` 这样大量模型的流式和非流式调用, 并且一个一个地用抽象层包裹, 类似于集中式, 但它的工作有些吃力不讨好, 模型越多, 更新的版本越多, 兼容性就越差, 工作量就越庞大, 到后面根本不是正常人可以维护的. (而作者大部分时间似乎只是一个人在维护, 这也是我觉得逆天的一点.) 但是 `sherpa_onnx` 的 API 变动纯看作者心情, API Docs 也没写好, typing 我看了都摇头(怨气!).【这点还需要扩展，但是我目前的了解不够深入，等我自己训练完 sherpa-kws-onnx 后， 我或许会更加了解, 需要等我去进修 onnx-runtime】

> 但两者似乎并不冲突， `sherpa_onnx` 和 `MCP Server` 的关注点不一样， 比如， `sherpa_onnx` 更加关心如何 `让更多的设备能够同时运行和处理多种不同模型的推理`（它兼容的设备确实相当广泛）， 而 `MCP Server` 则更关心如何如何处理请求和提供更多服务。 但我最近发现似乎在搭建 MCP Server 的时候， 用 sherpa_onnx 做个中间层处理就还不错。因为如果直接对接其他模型的正常调用的话会让事情变得相当复杂， 它们需要复杂的运行环境（通常还冲突和存在大量的 API Breaking），比如有的用 torch, 有的用 paddle, 有的用 tensorflow, 【这只是简单比喻】反观 sherpa_onnx 似乎把所有模型的运行调用放到了相同的环境下(还是得等先进修 onnx-runtime) ，这样反而可以把sherpa-onnx 理解为 MCP Server 的前置步骤， 这样反而非常利于 MCP Server 的搭建。
> 我也许可以通过学 sherpa-onnx 然后搭建出自己的 MCP Server。


## 如何定义 tools

[MCP Server 这样定义 tools](https://modelcontextprotocol.io/docs/concepts/tools):

```shell
{
  name: string;          // Unique identifier for the tool
  description?: string;  // Human-readable description
  inputSchema: {         // JSON Schema for the tool's parameters
    type: "object",
    properties: { ... }  // Tool-specific parameters
  },
  annotations: {        // Optional hints about tool behavior
    title?: string;      // Human-readable title for the tool
    readOnlyHint?: boolean;    // If true, the tool does not modify its environment
    destructiveHint?: boolean; // If true, the tool may perform destructive updates
    idempotentHint?: boolean;  // If true, repeated calls with same args have no additional effect
    openWorldHint?: boolean;   // If true, tool interacts with external entities
  }
}
```


它看上去相当像 [OpenAI 的 Function Calling 的格式](https://platform.openai.com/docs/guides/function-calling?api-mode=chat) :

```python
from openai import OpenAI

client = OpenAI()

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Bogotá, Colombia"
                }
            },
            "required": [
                "location"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
}]

completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": "What is the weather like in Paris today?"}],
    tools=tools
)

print(completion.choices[0].message.tool_calls)
```

> 至于它们为什么都选择以 json 的格式, 这还是比较有意思的点, 简单来说就是, LLM 经常答非所问, 不管你如何地调整 system promot 的权重, 它回答的时候也总是有意识或者无意识地偷工减料, 或者格式对不上, 而 Function Calling 就是解决这种问题的, 它直接约束了输出的格式. 类似于填空.(**需要确认下**)

但思考一个更哲学的问题， 那就是我们在创建模型服务的时候应该尽量地以统一的，最小化的环境搭建， 为此甚至可以放弃一些功能， 之保留基础的功能。 或者说我们更应该思考作为一个 tool 我们具体应该提供的功能是什么， 最小化的算力需求是多少。（这个我更喜欢用显存来衡量）， 我们既可以用一个多模态的大模型进行视觉工作， 也可以用一个最小化的视觉模型完成它。（以这种情况来说，它可以被很简单的像是卸下一个螺丝换个新的那样替换）， 但如果提供了一个综合性 tools 的化，那会让 Client 产生惰性， 或者说产生非它不可的感觉， 或者说一种参数量依赖（这种依赖通常让显存爆炸）， 所以有时候即使大模型的工作更好， 在 tool 的设计上，我依然会考虑最小化计i。 【这块有点抽象， 简单来说就是小功能可以被更简单地衡量，修改和替换，但如果是一个多模态大模型，你想要单独做特化是很困难的，通常也是破坏性的。而我可以随时毫无心里负担地更换一个小模型，并且，还是快速地，时间就是一切=-=】

关于统一的，最小化的工作环境，似乎可以考虑 onnx-runtime, 重新训练模型， 或者简单的转换模型， 以及像我前面提到的， 剪切模型， 去掉多余的部分， 让每个 tool 的 description 可以简单地被一句话概括， 并且它单一。

所以似乎总是要在等为先看 onnx-runtime 然后事情才会更有进展。 不然现在多讲只是纸上谈兵。

至少先从一个 kws 模型开始！

---

先睡觉了 (> ω <), tnnd, 感觉写的太条条框框了, 还是下面的写法爽. 明天再写写.

先我当时感受最深的点

MCP Server 的中介, 它让遵循协议的各大厂商之间的模型可以互通, 比如可以很容易地用 Genmi 调用 PaddleOCR 以及更多的 tools 进行配合, 不需要关心太多兼容性或者其他问题, 只需要关专注 tools 本身的功能(本质能干什么)即可. 这样既大大地缩减了开发时浪费的时间, 也让应用开发者有更多的精力去优化体验, 以及把精力放在想象力上, 思考我能做什么的时间大于把时间花在制作上. Server 构建方也有了更多的精力在考虑和实验 Agent 需要接受的信息到底是什么, 什么样的任务需要什么层的信息.

比如当时提到了,  PaddleOCR 在返回时, 可以让大模型选择性接受三个输出层, 第一层是识别到的文字, 第二层是坐标, 第三层是 tensor 和 log, 这相当于间接让大模型思考, 而且是递进式思考. 这样的形式似乎要比我们自己和它对话要更好, 这点也让我很兴奋.

而且, 它也可以原本一个 tool 的难题困境比如 PaddleOCR 的技术难题转移到全世界 OCR 面临的技术难题上, 人们更容易地看到问题的本质, 被迫从闭门造车到直接投入市场.  问题会暴露在更多人的视野中, 可能原本的问题就已经不再是问题了. 这点让人相当期待, 不过说起来 Paddle OCR 的 MCP Server 似乎也只是起草和定下来, 应该还没到这地步. 但这个发展方向确实有`开源让世界更美好`的意思.(虽然它本身可能并不开源)