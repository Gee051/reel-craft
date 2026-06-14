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
WAN_MODEL = "wanx2.1-t2v-plus"

# Video settings
VIDEO_SIZE = "1280*720"
VIDEO_DURATION = 4  # seconds per scene clip

# Flask settings
DEBUG = True
PORT = 5000