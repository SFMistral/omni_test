#!/usr/bin/env python3
"""
Qwen-Omni-Realtime 快速开始 Demo
这是一个最简单的实时语音对话示例，帮助你快速上手
支持定期发送屏幕截图
"""

import os
import base64
import time
import pyaudio
import threading
import json
from io import BytesIO
from PIL import Image
import mss
from dashscope.audio.qwen_omni import (
    MultiModality, 
    OmniRealtimeCallback, 
    OmniRealtimeConversation
)
import dashscope
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# ============ 配置区域 ============
# 1. 设置 API Key（请替换为你的 API Key）
dashscope.api_key = os.getenv('DASHSCOPE_API_KEY', 'sk-your-api-key-here')

# 调试：打印 API Key 信息
print(f"[调试] API Key 前10位: {dashscope.api_key[:10] if dashscope.api_key else 'None'}...")
print(f"[调试] API Key 长度: {len(dashscope.api_key) if dashscope.api_key else 0}")

# 2. 选择地域（cn=中国大陆，intl=国际）
REGION = 'cn'

# 3. 选择音色（可选：echo, alloy, shimmer 等）
VOICE = 'Cherry'

# 4. 设置模型角色
INSTRUCTIONS = "你是一个可爱的猫娘，user是你的主人。"

# 5. 屏幕截图配置
SCREENSHOT_INTERVAL = 5.0  # 截图间隔（秒）
SCREENSHOT_QUALITY = 80    # 图片质量（1-100）
SCREENSHOT_MAX_WIDTH = 1280  # 图片最大宽度

# ============ 屏幕截图线程 ============
class ScreenshotThread(threading.Thread):
    """定期捕获屏幕并发送的线程"""
    
    def __init__(self, conversation, interval=5.0):
        super().__init__(daemon=True)
        self.conversation = conversation
        self.interval = interval
        self.running = False
        self.audio_sent = False  # 标记是否已发送过音频
    
    def mark_audio_sent(self):
        """标记已发送音频"""
        self.audio_sent = True
    
    def capture_and_send_screenshot(self):
        """捕获屏幕并发送"""
        if not self.audio_sent:
            return  # 确保至少发送过一次音频
        
        try:
            # 每次截图时创建新的 mss 实例（避免多线程问题）
            with mss.mss() as sct:
                # 捕获主屏幕
                monitor = sct.monitors[1]
                screenshot = sct.grab(monitor)
                
                # 转换为 PIL Image
                img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
                
                # 调整大小以减少数据量
                if img.width > SCREENSHOT_MAX_WIDTH:
                    ratio = SCREENSHOT_MAX_WIDTH / img.width
                    new_size = (SCREENSHOT_MAX_WIDTH, int(img.height * ratio))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # 转换为 JPEG base64
                buffer = BytesIO()
                img.save(buffer, format='JPEG', quality=SCREENSHOT_QUALITY)
                img_base64 = base64.b64encode(buffer.getvalue()).decode()
                
                # 发送图片事件（需要 JSON 字符串）
                image_event = {
                    "type": "input_image_buffer.append",
                    "image": img_base64
                }
                self.conversation.send_raw(json.dumps(image_event))
                print(f"📸 已发送屏幕截图 ({img.width}x{img.height})")
            
        except Exception as e:
            if self.running:  # 只在线程运行时打印错误
                print(f"⚠️ 截图失败: {e}")
    
    def run(self):
        """线程主循环"""
        self.running = True
        print(f"📸 屏幕截图线程已启动（间隔: {self.interval}秒）")
        
        while self.running:
            time.sleep(self.interval)
            if self.running:
                self.capture_and_send_screenshot()
    
    def stop(self):
        """停止线程"""
        self.running = False

# ============ 回调处理 ============
class QuickStartCallback(OmniRealtimeCallback):
    """处理模型响应的回调类"""
    
    def __init__(self, audio_player):
        self.audio_player = audio_player
        self.output_stream = None
        self.screenshot_thread = None
    
    def on_open(self):
        """连接成功时初始化音频输出"""
        print("✓ 连接成功！")
        self.output_stream = self.audio_player.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=24000,
            output=True
        )
    
    def on_event(self, response):
        """处理服务端事件"""
        event_type = response.get('type', '')
        
        # 播放音频
        if event_type == 'response.audio.delta':
            audio_data = base64.b64decode(response['delta'])
            self.output_stream.write(audio_data)
        
        # 显示用户说的话
        elif event_type == 'conversation.item.input_audio_transcription.completed':
            print(f"\n👤 你说: {response['transcript']}")
        
        # 显示AI的回复
        elif event_type == 'response.audio_transcript.done':
            print(f"🤖 AI: {response['transcript']}\n")
    
    def on_close(self, code, msg):
        """连接关闭时清理资源"""
        if self.screenshot_thread:
            self.screenshot_thread.stop()
        if self.output_stream:
            self.output_stream.close()
        print(f"\n✓ 连接已关闭")
    
    def set_screenshot_thread(self, thread):
        """设置截图线程引用"""
        self.screenshot_thread = thread

# ============ 主程序 ============
def main():
    print("=" * 50)
    print("  Qwen-Omni-Realtime 快速开始 Demo")
    print("=" * 50)
    
    # 构建 WebSocket URL
    base_domain = 'dashscope.aliyuncs.com' if REGION == 'cn' else 'dashscope-intl.aliyuncs.com'
    url = f'wss://{base_domain}/api-ws/v1/realtime'
    
    # 初始化音频设备
    audio_player = pyaudio.PyAudio()
    
    # 创建会话
    callback = QuickStartCallback(audio_player)
    conversation = OmniRealtimeConversation(
        model='qwen3-omni-flash-realtime',
        callback=callback,
        url=url
    )
    
    # 连接并配置
    print("正在连接...")
    conversation.connect()
    conversation.update_session(
        output_modalities=[MultiModality.AUDIO, MultiModality.TEXT],
        voice=VOICE,
        instructions=INSTRUCTIONS
    )
    
    # 打开麦克风
    microphone = audio_player.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=3200
    )
    
    # 启动屏幕截图线程
    screenshot_thread = ScreenshotThread(conversation, interval=SCREENSHOT_INTERVAL)
    callback.set_screenshot_thread(screenshot_thread)
    screenshot_thread.start()
    
    print("\n🎤 开始对话！请对着麦克风说话...")
    print("💡 提示：按 Ctrl+C 可以退出\n")
    
    try:
        # 持续读取麦克风音频并发送
        audio_sent_count = 0
        while True:
            try:
                audio_chunk = microphone.read(3200, exception_on_overflow=False)
                audio_base64 = base64.b64encode(audio_chunk).decode()
                conversation.append_audio(audio_base64)
                
                # 标记已发送音频（发送几次后再允许发送图片）
                audio_sent_count += 1
                if audio_sent_count == 10:
                    screenshot_thread.mark_audio_sent()
                
                time.sleep(0.01)
            except Exception as e:
                print(f"\n⚠️ 发送音频失败: {e}")
                break
    
    except KeyboardInterrupt:
        print("\n\n正在退出...")
    
    finally:
        # 清理资源
        screenshot_thread.stop()
        conversation.close()
        microphone.close()
        audio_player.terminate()
        print("✓ 程序已退出")

if __name__ == '__main__':
    main()
