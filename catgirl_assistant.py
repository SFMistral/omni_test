#!/usr/bin/env python3
"""
猫娘屏幕助手 - 基于 YAML 配置
Catgirl Screen Assistant with YAML Configuration
"""

import os
import yaml
import base64
import time
import pyaudio
import threading
from io import BytesIO
from PIL import ImageGrab, Image
import pyautogui
from dashscope.audio.qwen_omni import (
    MultiModality, 
    OmniRealtimeCallback, 
    OmniRealtimeConversation
)
import dashscope
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class ConfigLoader:
    """配置加载器"""
    
    @staticmethod
    def load_config(config_path='catgirl_prompt.yaml'):
        """加载 YAML 配置文件"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

class ScreenMouseTracker:
    """屏幕内容和鼠标位置追踪器"""
    
    def __init__(self, config):
        self.config = config
        self.current_screen = None
        self.mouse_position = (0, 0)
        self.screen_size = pyautogui.size()
        self.running = False
        
        # 从配置读取参数
        self.capture_interval = config['screen_capture']['interval']
        self.mouse_interval = config['mouse_tracking']['interval']
        self.image_size = (
            config['screen_capture']['image_max_width'],
            config['screen_capture']['image_max_height']
        )
        self.image_quality = config['screen_capture']['image_quality']
