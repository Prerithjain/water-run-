from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from pymongo import MongoClient
import os
from datetime import datetime, timedelta
from typing import List, Optional
import json
import csv
import io
from dotenv import load_dotenv
import requests
import traceback
from bson import ObjectId

# Load environment variables
load_dotenv()

app = FastAPI()

# Telegram Bot Configuration
ENABLE_TELEGRAM_ALERTS = os.getenv('ENABLE_TELEGRAM_ALERTS', 'true').lower() == 'true'
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = 'water_tracker'

def get_db():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]

def send_telegram_alert(who_went: List[str], who_is_next: str, is_manual: bool = False) -> dict:
    """Send Telegram alert using Telegram Bot API"""
    if not ENABLE_TELEGRAM_ALERTS:
        return {"success": False, "error": "Telegram alerts disabled"}
    
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return {"success": False, "error": "Telegram not configured"}
   
    try:
        if is_manual:
            message_text = f"🚰 <b>Reminder!</b>\n\n{who_is_next} - it's your turn for the water run! 💧"
        else:
            if len(who_went) == 1:
                went_text = f"{who_went[0]} just went"
            else:
                went_text = f"{', '.join(who_went)} just went together"
            
            message_text = f"🚰 <b>Water Run Update!</b> 💧\n\n✅ {went_text}\n\n👉 <b>{who_is_next}</b> - you're up next!\n\nThanks team! 🙌"
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message_text,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print(f"✓ Telegram message sent")
            return {"success": True, "to": "telegram"}
        else:
            error_msg = f"Failed: {response.text}"
            print(f"✗ Telegram error: {error_msg}")
            return {"success": False, "error": error_msg}
    
    except Exception as e:
        error_msg = f"Failed to send Telegram message: {str(e)}"
        print(f"✗ {error_msg}")
        traceback.print_exc()
        return {"success": False, "error": error_msg}

def get_state_data():
    """Helper to calculate state without API overhead"""
    db = get_db()
    people_cursor = db.people.find()
    people_map = {str(p['_id']): p for p in people_cursor}
    
    # Initialize scores
    scores = {pid: 0 for pid in people_map}
    last_visit = {pid: None for pid in people_map}
    
    # Aggregate runs
    runs = db.runs.find().sort('timestamp', 1) # Process in order
    run_count = 0
    
    for r in runs:
        run_count += 1
        try:
            actor_ids = r['actors'] # List of strings (ObjectIds as strings)
            points = r['points_each']
            ts = r['timestamp']
            
            for aid in actor_ids:
                if aid in scores:
                    scores[aid] += points
                    # Update last visit if this run is newer
                    if last_visit[aid] is None or ts > last_visit[aid]:
                        last_visit[aid] = ts
        except Exception as e:
            print(f"Error processing run {r.get('_id')}: {e}")
            continue
            
    people_list = []
    for pid, p in people_map.items():
        lv = last_visit[pid]
        # Format date for frontend if exists
        lv_str = lv.isoformat() + "Z" if lv else None
        
        people_list.append({
            "id": pid,
            "name": p['name'],
            "score": scores.get(pid, 0),
            "last_visit": lv_str,
            "phone": p.get('phone')
        })
        
    return people_list, run_count

def notify_after_run(actor_names: List[str]):
    """Automatically notify after someone completes a water run"""
    try:
        people_list, _ = get_state_data()
        
        if not people_list:
            return {"success": False, "error": "No people found"}
        
        # Sort by score asc, then last_visit asc
        def sort_key(p):
            lv = p['last_visit'] or "0000-01-01"
            return (p['score'], lv)
        
        sorted_people = sorted(people_list, key=sort_key)
        next_person = sorted_people[0]
        
        return send_telegram_alert(
            who_went=actor_names,
            who_is_next=next_person['name'],
            is_manual=False
        )
    except Exception as e:
        print(f"Error notifying: {e}")
        return {"success": False, "error": str(e)}

def notify_next_person():
    """Manually notify about whose turn it is"""
    try:
        people_list, _ = get_state_data()
        
        if not people_list:
            return {"success": False, "error": "No people found"}
        
        def sort_key(p):
            lv = p['last_visit'] or "0000-01-01"
            return (p['score'], lv)
        
        sorted_people = sorted(people_list, key=sort_key)
        next_person = sorted_people[0]
        
        return send_telegram_alert(
            who_went=[],
            who_is_next=next_person['name'],
            is_manual=True
        )
    except Exception as e:
        return {"success": False, "error": str(e)}

def init_db():
    try:
        db = get_db()
        if db.people.count_documents({}) == 0:
            print("Initializing MongoDB with default data...")
            
            # Define initial state
            # Prerith: 7, 23-11-2025 00:43
            # Prashanth: 6, 20-11-2025
            # Bhuvan Gumma: 6, 20-11-2025
            # Vishwas: 7, 19-11-2025
            # Vikas Reddy: 3, 19-11-2025
            
            target_people = [
                {"name": "Vishwas", "score": 7, "date": datetime(2025, 11, 19), "phone": "+919876543210"},
                {"name": "Prerith", "score": 7, "date": datetime(2025, 11, 23, 0, 43), "phone": "+919876543211"},
                {"name": "Prashanth", "score": 6, "date": datetime(2025, 11, 20), "phone": "+919876543212"},
                {"name": "Bhuvan Gumma", "score": 6, "date": datetime(2025, 11, 20), "phone": "+919876543213"},
                {"name": "Vikas Reddy", "score": 3, "date": datetime(2025, 11, 19), "phone": "+919876543214"}
            ]
            
            for p in target_people:
                # Insert person
                res = db.people.insert_one({"name": p['name'], "phone": p['phone']})
                pid = str(res.inserted_id)
                
                # Insert legacy run to establish score and date
                if p['score'] > 0:
                    db.runs.insert_one({
                        "timestamp": p['date'],
                        "mode": "legacy_import",
                        "actors": [pid],
                        "points_each": p['score']
                    })
            
            print("DB Initialization Complete")
            
    except Exception as e:
        print(f"DB Init Error: {e}")
        traceback.print_exc()

# Initialize on startup
init_db()

class RecordRunRequest(BaseModel):
    actors: List[str] # List of IDs
    mode: str

@app.get("/api/state")
def get_state():
    people_list, run_count = get_state_data()
    return {"people": people_list, "total_runs": run_count}

@app.post("/api/record")
def record_run(req: RecordRunRequest):
    if req.mode == 'alone':
        if len(req.actors) != 1:
            raise HTTPException(400, "Alone mode requires exactly 1 actor")
        points = 2
    elif req.mode == 'group':
        if len(req.actors) < 2:
            raise HTTPException(400, "Group mode requires at least 2 actors")
        points = 1
    else:
        raise HTTPException(400, "Invalid mode")
        
    db = get_db()
    
    # Get actor names
    actor_names = []
    for aid in req.actors:
        p = db.people.find_one({"_id": ObjectId(aid)})
        if p:
            actor_names.append(p['name'])
        else:
            actor_names.append("Unknown")
    
    timestamp = datetime.utcnow() # MongoDB stores datetime objects
    
    db.runs.insert_one({
        "timestamp": timestamp,
        "mode": req.mode,
        "actors": req.actors,
        "points_each": points
    })
    
    # Notify
    telegram_result = notify_after_run(actor_names)
    
    return {"success": True, "new_state": get_state(), "telegram_sent": telegram_result}

@app.get("/api/history")
def get_history(limit: int = 50, page: int = 1):
    db = get_db()
    offset = (page - 1) * limit
    
    runs_cursor = db.runs.find().sort('timestamp', -1).skip(offset).limit(limit)
    
    # Cache people names
    people_cursor = db.people.find()
    people_map = {str(p['_id']): p['name'] for p in people_cursor}
    
    history = []
    for r in runs_cursor:
        actor_ids = r['actors']
        actor_names = [people_map.get(aid, "Unknown") for aid in actor_ids]
        
        history.append({
            "id": str(r['_id']),
            "timestamp": r['timestamp'].isoformat() + "Z",
            "mode": r['mode'],
            "actors": actor_ids,
            "actor_names": actor_names,
            "points_each": r['points_each']
        })
        
    return history

@app.get("/api/suggest")
def suggest_pair():
    people_list, _ = get_state_data()
    
    if not people_list:
        return {"error": "No people found"}
    
    def sort_key(p):
        lv = p['last_visit'] or "0000-01-01"
        return (p['score'], lv)
        
    sorted_people = sorted(people_list, key=sort_key)
    
    if len(sorted_people) < 2:
        return {"suggested": [], "reason": "Not enough people"}
        
    suggestion = [sorted_people[0], sorted_people[1]]
    reason = "Lowest scores & longest time since last visit"
    
    # Check last run to avoid repeat
    db = get_db()
    last_run = db.runs.find_one(sort=[('timestamp', -1)])
    
    if last_run:
        last_actors = set(last_run['actors'])
        suggested_ids = {suggestion[0]['id'], suggestion[1]['id']}
        
        if last_actors == suggested_ids and len(people_list) > 2:
            suggestion = [sorted_people[0], sorted_people[2]]
            reason += " (rotated to avoid repeat)"
            
    return {
        "suggested": suggestion,
        "reason": reason
    }

@app.get("/api/export/csv")
def export_csv_endpoint():
    db = get_db()
    runs = db.runs.find().sort('timestamp', -1)
    
    people_cursor = db.people.find()
    people_map = {str(p['_id']): p['name'] for p in people_cursor}
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['id', 'timestamp', 'mode', 'actors', 'points_each'])
    
    for r in runs:
        actor_ids = r['actors']
        actor_names = ", ".join([people_map.get(aid, "Unknown") for aid in actor_ids])
        writer.writerow([str(r['_id']), r['timestamp'].isoformat(), r['mode'], actor_names, r['points_each']])
            
    return Response(content=output.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=water_runs.csv"})

@app.post("/api/send-alert")
def send_alert_manually():
    result = notify_next_person()
    if result.get('success'):
        return {"success": True, "message": f"Telegram alert sent to {result.get('to')}"}
    else:
        raise HTTPException(500, result.get('error', 'Failed to send alert'))

@app.get("/api/telegram-status")
def telegram_status():
    return {
        "enabled": ENABLE_TELEGRAM_ALERTS,
        "service": "Telegram Bot API"
    }
