#!/usr/bin/env python3
"""
Webhook Server - Entry point for Instagram webhooks

Runs alongside Streamlit dashboard on Railway
"""
import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.api.webhook_handler import app
from src.utils.logger import api_logger

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))

    api_logger.info(f"🚀 Starting webhook server on port {port}")
    api_logger.info(f"📍 Webhook endpoint: http://0.0.0.0:{port}/webhook/instagram")

    # Production mode
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )
