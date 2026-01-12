"""
Instagram Webhook Handler - Real-time notifications
"""
from flask import Flask, request, jsonify
import hashlib
import hmac
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.config import Config
from src.utils.logger import api_logger

app = Flask(__name__)


@app.route('/webhook/instagram', methods=['GET', 'POST'])
def instagram_webhook():
    """
    Instagram Webhook Endpoint

    GET: Verification challenge (Meta sends this during setup)
    POST: Webhook notification (when someone tags @amitydrinks.cz)
    """

    if request.method == 'GET':
        # Webhook verification
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        verify_token = os.getenv('WEBHOOK_VERIFY_TOKEN', 'amity_webhook_2024')

        if mode == 'subscribe' and token == verify_token:
            api_logger.info("✅ Webhook verified successfully")
            return challenge, 200
        else:
            api_logger.warning("❌ Webhook verification failed")
            return 'Forbidden', 403

    if request.method == 'POST':
        # Verify signature
        signature = request.headers.get('X-Hub-Signature-256', '')
        body = request.get_data()

        if not verify_signature(body, signature):
            api_logger.error("❌ Invalid webhook signature")
            return jsonify({'error': 'Invalid signature'}), 403

        # Process webhook payload
        try:
            data = request.json
            api_logger.info(f"📨 Webhook received: {data}")

            for entry in data.get('entry', []):
                for change in entry.get('changes', []):
                    field = change.get('field')
                    value = change.get('value')

                    if field == 'mentions':
                        # Someone mentioned/tagged @amitydrinks.cz
                        process_mention(value)
                    elif field == 'media':
                        # New media posted (if subscribed)
                        process_media(value)

            return jsonify({'status': 'ok'}), 200

        except Exception as e:
            api_logger.error(f"❌ Webhook processing error: {str(e)}")
            return jsonify({'error': str(e)}), 500


def verify_signature(payload: bytes, signature: str) -> bool:
    """
    Verify webhook signature using HMAC SHA256

    Args:
        payload: Request body bytes
        signature: X-Hub-Signature-256 header value

    Returns:
        True if signature is valid
    """
    if not signature:
        return False

    try:
        # Remove 'sha256=' prefix if present
        if signature.startswith('sha256='):
            signature = signature[7:]

        # Compute expected signature
        secret = Config.META_APP_SECRET.encode()
        expected = hmac.new(secret, payload, hashlib.sha256).hexdigest()

        # Constant-time comparison
        return hmac.compare_digest(expected, signature)

    except Exception as e:
        api_logger.error(f"Signature verification error: {str(e)}")
        return False


def process_mention(mention_data: dict):
    """
    Process mention webhook (someone tagged @amitydrinks.cz)

    mention_data = {
        'media_id': '...',
        'comment_id': '...',  # nebo null pro tag
        'username': 'dustyfeet_23'  # KDO označil
    }
    """
    media_id = mention_data.get('media_id')
    username = mention_data.get('username')

    if not media_id or not username:
        api_logger.warning(f"Incomplete mention data: {mention_data}")
        return

    api_logger.info(f"🏷️  Tagged by @{username} in media {media_id}")

    # Import here to avoid circular dependency
    try:
        from src.monitoring.sync_instagram import InstagramSync

        sync = InstagramSync()
        sync.process_tagged_mention({
            'media_id': media_id,
            'username': username
        })

        api_logger.info(f"✅ Mention processed: @{username} → media {media_id}")

    except Exception as e:
        api_logger.error(f"❌ Failed to process mention: {str(e)}")


def process_media(media_data: dict):
    """
    Process media webhook (new post/story published)

    media_data = {
        'id': '...',
        'media_type': 'IMAGE/VIDEO/CAROUSEL_ALBUM',
        ...
    }
    """
    media_id = media_data.get('id')
    media_type = media_data.get('media_type')

    api_logger.info(f"📸 New media: {media_type} ({media_id})")

    # Optional: Process new media from @amitydrinks.cz account
    # (not critical for influencer tracking)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({
        'status': 'healthy',
        'service': 'webhook_handler',
        'version': '1.0.0'
    }), 200


@app.route('/', methods=['GET'])
def root():
    """Root endpoint - show webhook status"""
    return jsonify({
        'service': 'Amity Drinks Webhook Handler',
        'status': 'running',
        'endpoints': {
            '/webhook/instagram': 'Instagram webhook endpoint',
            '/health': 'Health check'
        }
    }), 200


if __name__ == '__main__':
    # Development mode
    port = int(os.getenv('WEBHOOK_PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
