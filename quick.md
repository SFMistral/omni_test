VAD 模式（Voice Activity Detection，自动检测语音起止）

服务端自动判断用户何时开始与停止说话并作出回应。


运行vad_dash.py，通过麦克风即可与 Qwen-Omni-Realtime 模型实时对话，系统会检测您的音频起始位置并自动发送到服务器，无需您手动发送。



交互流程
VAD 模式

将session.update事件的session.turn_detection 设为"server_vad"以启用 VAD 模式。此模式下，服务端自动检测语音起止并进行响应。适用于语音通话场景。

交互流程如下：

    1.服务端检测到语音开始，发送input_audio_buffer.speech_started 事件。

    2.客户端随时发送 input_audio_buffer.append与input_image_buffer.append事件追加音频与图片至缓冲区。

        发送 input_image_buffer.append 事件前，至少发送过一次 input_audio_buffer.append 事件。

    3.服务端检测到语音结束，发送input_audio_buffer.speech_stopped事件。

    4.服务端发送input_audio_buffer.committed 事件提交音频缓冲区。

    5.服务端发送 conversation.item.created事件，包含从缓冲区创建的用户消息项。



1. 建立连接

Qwen-Omni-Realtime 模型通过 WebSocket 协议接入，可通过 omni_example.py 示例代码建立连接。


2. 配置会话

发送客户端事件session.update。参考模板session.update.example


3. 输入音频与图片

客户端通过input_audio_buffer.append和 input_image_buffer.append 事件发送 Base64 编码的音频和图片数据到服务端缓冲区。音频输入是必需的；图片输入是可选的。

    图片可以来自本地文件，或从视频流中实时采集。

    启用服务端VAD时，服务端会在检测到语音结束时自动提交数据并触发响应。禁用VAD时（手动模式），客户端必须在发送完数据后，主动调用input_audio_buffer.commit事件来提交。

4. 接收模型响应

模型的响应格式取决于配置的输出模态。

    仅输出文本

    通过response.text.delta事件接收流式文本，response.text.done事件获取完整文本。

    输出文本+音频

        文本：通过response.audio_transcript.delta事件接收流式文本，response.audio_transcript.done事件获取完整文本。

        音频：通过response.audio.delta事件获取 Base64 编码的流式输出音频数据。response.audio.done事件标志音频数据生成完成。