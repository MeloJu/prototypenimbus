# Quick tests for Music Generator Company.

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"


def test_status():
        print("Testing /api/status...")
    response = requests.get(f"{BASE_URL}/api/status")
    data = response.json()
    
    print(f"✓ Status: {response.status_code}")
    print(f"  Ollama: {'✓' if data['status']['ollama_available'] else '✗'}")
    print(f"  Twitter: {'✓' if data['status']['twitter_api'] else '✗'}")
    print()


def test_generate_music():
        print("Testing music generation...")
    response = requests.post(f"{BASE_URL}/api/generate")
    data = response.json()
    
    if data['success']:
        track = data['track']
        print(f"✓ Generated: {track['title']}")
        print(f"  Genre: {track['genre']}")
        print(f"  Mood: {track['mood']}")
        print(f"  Method: {track.get('generation_method', 'unknown')}")
    else:
        print(f"✗ Failed: {data.get('error')}")
    print()


def test_ollama_prompt():
        print("Testing Ollama prompt...")
    response = requests.post(
        f"{BASE_URL}/api/ollama/prompt",
        json={"prompt": "Say hello in a creative way"}
    )
    data = response.json()
    
    if data['success']:
        print(f"✓ Response: {data['response'][:100]}...")
    else:
        print(f"✗ Ollama not available (expected without Ollama running)")
    print()


def test_twitter_post():
        print("Testing Twitter post now...")
    response = requests.post(
        f"{BASE_URL}/api/twitter/post-now",
        json={"content": "Test post from Music Generator Company 🎵"}
    )
    data = response.json()
    
    if data['success']:
        print(f"✓ Posted successfully")
        print(f"  Post ID: {data['result']['post_id']}")
        if data['result'].get('simulated'):
            print("  (Simulated - no API credentials)")
    else:
        print(f"✗ Failed: {data.get('error')}")
    print()


def test_twitter_schedule():
        print("Testing Twitter scheduling...")
    
    # Schedule for 2 minutes from now
    scheduled_time = (datetime.now() + timedelta(minutes=2)).isoformat()
    
    response = requests.post(
        f"{BASE_URL}/api/twitter/schedule",
        json={
            "content": "Scheduled test post 🚀",
            "scheduled_time": scheduled_time
        }
    )
    data = response.json()
    
    if data['success']:
        print(f"✓ Scheduled successfully")
        print(f"  Time: {scheduled_time}")
        print(f"  Post ID: {data['post']['id']}")
    else:
        print(f"✗ Failed: {data.get('error')}")
    print()


def test_pending_posts():
        print("Testing pending posts...")
    response = requests.get(f"{BASE_URL}/api/twitter/pending")
    data = response.json()
    
    if data['success']:
        print(f"✓ Found {len(data['posts'])} pending posts")
        for post in data['posts'][:3]:
            print(f"  - {post['content'][:50]}...")
    else:
        print(f"✗ Failed: {data.get('error')}")
    print()


def test_operations():
        print("Testing full operations...")
    response = requests.post(f"{BASE_URL}/api/operations/run")
    data = response.json()
    
    if data['success']:
        print(f"✓ Operations completed")
        results = data['results']
        
        if 'track' in results:
            print(f"  Music: {results['track']['title']}")
        
        if 'billing' in results:
            print(f"  Billing: ${results['billing']['revenue']:.2f}")
        
        if 'marketing' in results:
            print(f"  Marketing: Created post")
    else:
        print(f"✗ Failed: {data.get('error')}")
    print()


def run_all_tests():
        print("=" * 60)
    print("Music Generator Company - API Tests")
    print("=" * 60)
    print()
    
    try:
        test_status()
        test_generate_music()
        test_ollama_prompt()
        test_twitter_post()
        test_twitter_schedule()
        test_pending_posts()
        test_operations()
        
        print("=" * 60)
        print("✓ All tests completed")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to server")
        print("  Make sure the server is running: python web_app.py")
    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    run_all_tests()



