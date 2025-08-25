import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Discord Webhook Configuration
    DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL', '')
    
    # Application Configuration
    HOST = "0.0.0.0"
    PORT = 26435
    DEBUG = False
    
    # File Storage Configuration
    MAX_FILE_SIZE = int(9.99 * 1024 * 1024)     # ~9.99MB in bytes (Discord limit per chunk)
    CHUNK_SIZE = int(9.99 * 1024 * 1024)        # ~9.99MB chunks (Discord limit)
    MAX_TOTAL_FILE_SIZE = int(1024 * 1024 * 1024 * 512)  # 512GB total file size limit
    DATA_FILE = 'files.json'
    
    # Security
    WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
    
    @classmethod
    def validate_config(cls):
        """Validate the configuration"""
        if not cls.DISCORD_WEBHOOK_URL:
            print("Warning: DISCORD_WEBHOOK_URL not set!")
            print("Files will be stored locally only.")
            print("Set the environment variable to enable Discord uploads.")
            return False
        return True
    
    @classmethod
    def _format_size(cls, size_bytes: int) -> str:
        """Format bytes into a human-readable string"""
        units = ["B", "KB", "MB", "GB", "TB"]
        size = float(size_bytes)
        for unit in units:
            if size < 1024:
                return f"{size:.2f}{unit}"
            size /= 1024
        return f"{size:.2f}PB"
    
    @classmethod
    def print_config(cls):
        """Print current configuration"""
        print("> DisStored Configuration:")
        print(f"   Host: {cls.HOST}")
        print(f"   Port: {cls.PORT}")
        print(f"   Max File Size (per chunk): {cls._format_size(cls.MAX_FILE_SIZE)}")
        print(f"   Chunk Size: {cls._format_size(cls.CHUNK_SIZE)}")
        print(f"   Max Total File Size: {cls._format_size(cls.MAX_TOTAL_FILE_SIZE)}")
        print(f"   Discord Webhook: {'Set and connected' if cls.DISCORD_WEBHOOK_URL else 'Not set'}")
        print(f"   Data File: {cls.DATA_FILE}")
