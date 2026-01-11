# Web interface for Music Generator Company.

import logging
from flask import Flask, render_template, request, jsonify
from datetime import datetime

try:
    from knowledge import KnowledgeBase
except ImportError:
    from knowledge_simple import KnowledgeBase

try:
    from llm_service import LLMService
except ImportError:
    from llm_service_simple import LLMService

from orchestrator import MusicCompany
from twitter_service import TwitterService
from scheduler import Scheduler

logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize services
kb = KnowledgeBase()
llm_service = LLMService()
company = MusicCompany(kb, llm_service)
twitter = TwitterService()
scheduler = Scheduler()


@app.route('/')
def index():
    # Flask route
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def generate_music():
    # Flask route
    try:
        track = company.music_agent.generate_track()
        return jsonify({"success": True, "track": track})
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/ollama/prompt', methods=['POST'])
def ollama_prompt():
    # Flask route
    data = request.json
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({"success": False, "error": "Prompt is required"}), 400
    
    if not llm_service.is_available():
        return jsonify({
            "success": False,
            "error": "Ollama not available. Please install and start Ollama.",
            "response": None
        })
    
    try:
        # Direct Ollama call
        response = llm_service.llm.invoke(prompt)
        return jsonify({
            "success": True,
            "prompt": prompt,
            "response": response
        })
    except Exception as e:
        logger.error(f"Ollama prompt failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/marketing/create', methods=['POST'])
def create_marketing():
    # Flask route
    data = request.json
    track_id = data.get('track_id')
    
    try:
        # Get recent track or use provided data
        recent_tracks = kb.get('recent_tracks', [])
        if recent_tracks:
            track = recent_tracks[-1]
        else:
            return jsonify({"success": False, "error": "No tracks available"}), 404
        
        post = company.marketing_agent.create_post(track)
        return jsonify({"success": True, "post": post})
    except Exception as e:
        logger.error(f"Marketing creation failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/twitter/schedule', methods=['POST'])
def schedule_twitter_post():
    # Flask route
    data = request.json
    content = data.get('content', '')
    scheduled_time = data.get('scheduled_time', '')
    
    if not content:
        return jsonify({"success": False, "error": "Content is required"}), 400
    
    try:
        post = twitter.schedule_post(content, scheduled_time)
        return jsonify({"success": True, "post": post})
    except Exception as e:
        logger.error(f"Twitter scheduling failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/twitter/post-now', methods=['POST'])
def post_now():
    # Flask route
    data = request.json
    content = data.get('content', '')
    
    if not content:
        return jsonify({"success": False, "error": "Content is required"}), 400
    
    try:
        result = twitter.post_now(content)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        logger.error(f"Twitter posting failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/twitter/pending')
def get_pending_posts():
    # Flask route
    try:
        posts = twitter.get_pending_posts()
        return jsonify({"success": True, "posts": posts})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/twitter/posted')
def get_posted():
    # Flask route
    try:
        posts = twitter.get_posted()
        return jsonify({"success": True, "posts": posts})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/operations/run', methods=['POST'])
def run_operations():
    # Flask route
    try:
        results = company.run_daily_operations()
        return jsonify({"success": True, "results": results})
    except Exception as e:
        logger.error(f"Operations failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/status')
def get_status():
    # Flask route
    return jsonify({
        "success": True,
        "status": {
            "ollama_available": llm_service.is_available(),
            "twitter_api": twitter.api_available,
            "pending_posts": len(twitter.get_pending_posts()),
            "recent_tracks": len(kb.get('recent_tracks', [])),
            "timestamp": datetime.now().isoformat()
        }
    })


def start_scheduler():
    # Check for scheduled posts every minute
    scheduler.add_task(
        func=lambda: twitter.process_scheduled_posts(),
        interval_seconds=60,
        name="process_twitter_schedule"
    )
    
    scheduler.start()
    logger.info("Background scheduler started")


def run_server(host='0.0.0.0', port=5000, debug=False):
    # Run the web server
    start_scheduler()
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run_server(debug=True)




