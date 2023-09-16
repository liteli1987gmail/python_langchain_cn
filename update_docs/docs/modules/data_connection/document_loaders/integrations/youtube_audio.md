# 从 YouTube url 加载文档

在 YouTube 视频上构建聊天或问答应用程序是一个非常有趣的话题。

下面我们将展示如何从 YouTube url 轻松地转换为文本以进行聊天！

我们将使用 `OpenAIWhisperParser`，它将使用 OpenAI Whisper API 将音频转录为文本。

注意：您需要提供 `OPENAI_API_KEY`。

```python
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
```

我们将使用 `yt_dlp` 下载 YouTube url 的音频。

我们将使用 `pydub` 来拆分已下载的音频文件（以符合 Whisper API 的 25MB 文件大小限制）。


```python
! pip install yt_dlp
! pip install pydub
```

### YouTube url 转为文本

使用 `YoutubeAudioLoader` 来获取/下载音频文件。

然后，使用 `OpenAIWhisperParser()` 将它们转录为文本。

让我们以 Andrej Karpathy 的 YouTube 课程的第一节为例！


```python
# 两个 Karpathy 讲座视频
urls = ["https://youtu.be/kCc8FmEb1nY", "https://youtu.be/VMj-3S1tku0"]

# 保存音频文件的目录
save_dir = "~/Downloads/YouTube"

# 将视频转录为文本
loader = GenericLoader(YoutubeAudioLoader(urls, save_dir), OpenAIWhisperParser())
docs = loader.load()
```


    [youtube] Extracting URL: https://youtu.be/kCc8FmEb1nY
    [youtube] kCc8FmEb1nY: Downloading webpage
    [youtube] kCc8FmEb1nY: Downloading android player API JSON
    [info] kCc8FmEb1nY: Downloading 1 format(s): 140
    [dashsegments] Total fragments: 11
    [download] Destination: /Users/31treehaus/Desktop/AI/langchain-fork/docs/modules/indexes/document_loaders/examples/Let's build GPT: from scratch, in code, spelled out..m4a
    [download] 100% of  107.73MiB in 00:00:18 at 5.92MiB/s                   
    [FixupM4a] Correcting container of "/Users/31treehaus/Desktop/AI/langchain-fork/docs/modules/indexes/document_loaders/examples/Let's build GPT: from scratch, in code, spelled out..m4a"
    [ExtractAudio] Not converting audio /Users/31treehaus/Desktop/AI/langchain-fork/docs/modules/indexes/document_loaders/examples/Let's build GPT: from scratch, in code, spelled out..m4a; file is already in target format m4a
    [youtube] Extracting URL: https://youtu.be/VMj-3S1tku0
    [youtube] VMj-3S1tku0: Downloading webpage
    [youtube] VMj-3S1tku0: Downloading android player API JSON
    [info] VMj-3S1tku0: Downloading 1 format(s): 140
    [download] /Users/31treehaus/Desktop/AI/langchain-fork/docs/modules/indexes/document_loaders/examples/The spelled-out intro to neural networks and backpropagation: building micrograd.m4a has already been downloaded
    [download] 100% of  134.98MiB
    [ExtractAudio] Not converting audio /Users/31treehaus/Desktop/AI/langchain-fork/docs/modules/indexes/document_loaders/examples/The spelled-out intro to neural networks and backpropagation: building micrograd.m4a; file is already in target format m4a



```python
# 返回一个 Document 列表，可以很容易地查看或解析



docs[0].page_content[0:500]
```