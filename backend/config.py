import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Qwen / DashScope API Key
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

# API Base URL - International region
DASHSCOPE_BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

# Qwen text model for script + storyboard
QWEN_MODEL = "qwen-plus"

# Wan video generation model
WAN_MODEL = "wan2.2-t2v-plus"

# Video settings
VIDEO_SIZE = "1080*1920"
VIDEO_DURATION = 4  # seconds per scene clip

# Flask settings
DEBUG = True
PORT = 5000