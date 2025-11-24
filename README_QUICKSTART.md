# 🚀 快速开始指南

这是一个 Qwen-Omni-Realtime 实时语音对话的快速入门示例。

## 📋 前置要求

1. Python 3.10+（推荐 3.11）
2. 获取 API Key：访问 [阿里云 DashScope](https://dashscope.aliyun.com/) 获取你的 API Key

## 🔧 环境安装

### 方法一：使用 Conda（推荐）

```bash
# 创建并激活环境
conda env create -f environment.yml
conda activate omni-realtime
```

### 方法二：使用 pip

```bash
# 创建虚拟环境（可选）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

## ⚡ 配置 API Key

### 方法一：使用环境变量文件（推荐）

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的 API Key
# DASHSCOPE_API_KEY=sk-your-api-key-here
```

### 方法二：使用环境变量

```bash
export DASHSCOPE_API_KEY="sk-your-api-key-here"
```

### 方法三：直接修改代码

打开 `quickstart_demo.py`，找到配置区域，修改：
```python
dashscope.api_key = "sk-your-api-key-here"
```

## 🎬 运行 Demo

```bash
# 确保已激活环境
conda activate omni-realtime

# 运行快速开始 demo
python quickstart_demo.py
```

## 🎯 使用说明

1. 运行程序后，等待提示 "✓ 连接成功！"
2. 对着麦克风说话，AI 会自动检测你的语音并回复
3. 按 `Ctrl+C` 退出程序

## 🔧 自定义配置

在 `quickstart_demo.py` 的配置区域，你可以修改：

- **REGION**: 选择地域
  - `'cn'` - 中国大陆（北京）
  - `'intl'` - 国际（新加坡）

- **VOICE**: 选择音色
  - `'Cherry'` - 甜美女声
  - `'Stella'` - 温柔女声
  - `'Bella'` - 活泼女声

- **INSTRUCTIONS**: 设置 AI 角色
  - 例如："你是一个幽默风趣的助手"
  - 例如："你是一个专业的技术顾问"

## 📝 示例对话

```
🎤 开始对话！请对着麦克风说话...

👤 你说: 你好，今天天气怎么样？
🤖 AI: 你好！很抱歉，我无法获取实时天气信息。你可以查看天气预报应用或网站来了解今天的天气情况。

👤 你说: 给我讲个笑话
🤖 AI: 好的！为什么程序员总是分不清万圣节和圣诞节？因为 Oct 31 == Dec 25！
```

## 🐛 常见问题

### 1. 麦克风无法使用
- 检查系统麦克风权限
- 确认麦克风设备正常工作

### 2. API Key 错误
- 确认 API Key 正确无误
- 检查环境变量是否设置成功

### 3. 连接失败
- 检查网络连接
- 确认选择了正确的地域（cn 或 intl）

## 📚 更多示例

- `omni_example.py` - 基础连接示例
- `vad_dash.py` - 完整的 VAD 模式示例
- `quick.md` - 详细的技术文档

## 💡 提示

- 在安静的环境中使用效果更好
- 说话清晰，语速适中
- 等待 AI 回复完成后再继续说话

---

祝你使用愉快！🎉
