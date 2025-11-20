from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import sqlite3
import os
from datetime import datetime, timedelta
from typing import List, Optional
import json
import csv
import io
from dotenv import load_dotenv
import requests
import traceback

# Load environment variables
load_dotenv()

app = FastAPI()

# Telegram Bot Configuration (FREE & RELIABLE!)
# Get bot token from @BotFather on Telegram
ENABLE_TELEGRAM_ALERTS = os.getenv('ENABLE_TELEGRAM_ALERTS', 'true').lower() == 'true'
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')  # Bot token from @BotFather
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')  # Group chat ID or personal chat ID

# Determine DB path
IS_VERCEL = os.environ.get('VERCEL') == '1'
DB_DIR = '/tmp' if IS_VERCEL else os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
DB_PATH = os.path.join(DB_DIR, 'waterrun.db')

# Ensure data dir exists (locally)
if not os.path.exists(DB_DIR):
    try:
        os.makedirs(DB_DIR)
    except:
        pass

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def send_telegram_alert(who_went: List[str], who_is_next: str, is_manual: bool = False) -> dict:
    """Send Telegram alert using Telegram Bot API (100% FREE & RELIABLE!)"""
    if not ENABLE_TELEGRAM_ALERTS:
        return {"success": False, "error": "Telegram alerts disabled"}
    
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return {"success": False, "error": "Telegram not configured. Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env"}
   
    try:
        # Create message
        if is_manual:
            message_text = f"🚰 <b>Reminder!</b>\n\n{who_is_next} - it's your turn for the water run! 💧"
        else:
            # Format who went
            if len(who_went) == 1:
                went_text = f"{who_went[0]} just went"
            else:
                went_text = f"{', '.join(who_went)} just went together"
            
            message_text = f"🚰 <b>Water Run Update!</b> 💧\n\n✅ {went_text}\n\n👉 <b>{who_is_next}</b> - you're up next!\n\nThanks team! 🙌"
        
        # Telegram Bot API - 100% FREE and RELIABLE!
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

def notify_after_run(actor_names: List[str]):
    """Automatically notify after someone completes a water run"""
    try:
        # Get suggestion (next person)
        state = get_state()
        people = state['people']
        
        if not people:
            return {"success": False, "error": "No people found"}
        
        # Sort by score asc, then last_visit asc (same logic as /api/suggest)
        def sort_key(p):
            lv = p['last_visit'] or "0000-01-01"
            return (p['score'], lv)
        
        sorted_people = sorted(people, key=sort_key)
        next_person = sorted_people[0]  # Person with lowest score & oldest visit
        
        # Send Telegram alert
        return send_telegram_alert(
            who_went=actor_names,
            who_is_next=next_person['name'],
            is_manual=False
        )
    
    except Exception as e:
        error_msg = f"Error notifying: {str(e)}"
        print(f"✗ {error_msg}")
        traceback.print_exc()
        return {"success": False, "error": error_msg}

def notify_next_person():
    """Manually notify about whose turn it is (for manual trigger button)"""
    try:
        # Get suggestion (next person)
        state = get_state()
        people = state['people']
        
        if not people:
            return {"success": False, "error": "No people found"}
        
        # Sort by score asc, then last_visit asc
        def sort_key(p):
            lv = p['last_visit'] or "0000-01-01"
            return (p['score'], lv)
        
        sorted_people = sorted(people, key=sort_key)
        next_person = sorted_people[0]
        
        # Send manual reminder
        return send_telegram_alert(
            who_went=[],
            who_is_next=next_person['name'],
            is_manual=True
        )
    
    except Exception as e:
        error_msg = f"Error notifying next person: {str(e)}"
        print(f"✗ {error_msg}")
        traceback.print_exc()
        return {"success": False, "error": error_msg}

def init_db():
    try:
        conn = get_db()
        c = conn.cursor()
        
        # Check if we need to migrate to the new people list
        table_exists = False
        try:
            c.execute("SELECT count(*) FROM people WHERE name = 'Vishwas'")
            if c.fetchone()[0] > 0:
                table_exists = True
        except:
            pass

        if not table_exists:
            print("Resetting DB for new user list...")
            c.execute("DROP TABLE IF EXISTS runs")
            c.execute("DROP TABLE IF EXISTS people")
            
        c.execute('''CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            phone TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY,
            timestamp TEXT NOT NULL,
            mode TEXT NOT NULL,
            actors TEXT NOT NULL,
            points_each INTEGER NOT NULL
        )''')
        
        # Insert specific people and scores
        target_people = [
            {"name": "Vishwas", "score": 7, "phone": "+919876543210"},
            {"name": "Prerith", "score": 5, "phone": "+919876543211"},
            {"name": "Prashanth", "score": 5, "phone": "+919876543212"},
            {"name": "Bhuvan Gumma", "score": 5, "phone": "+919876543213"},
            {"name": "Vikas Reddy", "score": 3, "phone": "+919876543214"}
        ]
        
        for p in target_people:
            try:
                c.execute("INSERT INTO people (name, phone) VALUES (?, ?)", (p['name'], p.get('phone')))
                c.execute("SELECT id FROM people WHERE name = ?", (p['name'],))
                pid = c.fetchone()[0]
                    
            except sqlite3.IntegrityError:
                # Person already exists, update phone if needed
                c.execute("UPDATE people SET phone = ? WHERE name = ?", (p.get('phone'), p['name']))
                pass

        if not table_exists:
            # We just reset the DB, so we can safely insert the initial scores
            # Set timestamp to Nov 19, 2024 as requested
            # Using datetime(2024, 11, 19) for Nov 19, 2024
            initial_date = datetime(2024, 11, 19, 0, 0, 0)
            old_timestamp = initial_date.isoformat() + "Z"
            
            for p in target_people:
                if p['score'] > 0:
                    c.execute("SELECT id FROM people WHERE name = ?", (p['name'],))
                    pid = c.fetchone()[0]
                    actors_json = json.dumps([pid])
                    c.execute("INSERT INTO runs (timestamp, mode, actors, points_each) VALUES (?, ?, ?, ?)",
                              (old_timestamp, 'legacy_import', actors_json, p['score']))


        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB Init Error: {e}")

# Initialize on startup
init_db()

class RecordRunRequest(BaseModel):
    actors: List[int]
    mode: str

@app.get("/api/state")
def get_state():
    init_db() # Ensure DB is ready (in case of cold start on Vercel resetting /tmp)
    conn = get_db()
    c = conn.cursor()
    
    c.execute("SELECT * FROM people")
    people_rows = c.fetchall()
    
    c.execute("SELECT * FROM runs")
    runs = c.fetchall()
    
    scores = {p['id']: 0 for p in people_rows}
    last_visit = {p['id']: None for p in people_rows}
    
    for r in runs:
        try:
            actor_ids = json.loads(r['actors'])
            for aid in actor_ids:
                if aid in scores:
                    scores[aid] += r['points_each']
                    ts = r['timestamp']
                    if last_visit[aid] is None or ts > last_visit[aid]:
                        last_visit[aid] = ts
        except:
            continue
                    
    people_list = []
    for p in people_rows:
        people_list.append({
            "id": p['id'],
            "name": p['name'],
            "score": scores.get(p['id'], 0),
            "last_visit": last_visit.get(p['id']),
            "phone": p['phone'] if 'phone' in p.keys() else None
        })
        
    conn.close()
    return {"people": people_list, "total_runs": len(runs)}

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
        
    conn = get_db()
    c = conn.cursor()
    
    # Get actor names for Telegram notification
    c.execute("SELECT * FROM people")
    people = {p['id']: p['name'] for p in c.fetchall()}
    actor_names = [people.get(aid, "Unknown") for aid in req.actors]
    
    timestamp = datetime.utcnow().isoformat() + "Z"
    actors_json = json.dumps(req.actors)
    
    c.execute("INSERT INTO runs (timestamp, mode, actors, points_each) VALUES (?, ?, ?, ?)",
              (timestamp, req.mode, actors_json, points))
    conn.commit()
    conn.close()
    
    # Automatically notify via Telegram (with who went and who's next)
    telegram_result = notify_after_run(actor_names)
    
    
    return {"success": True, "new_state": get_state(), "telegram_sent": telegram_result}

@app.get("/api/history")
def get_history(limit: int = 50, page: int = 1):
    conn = get_db()
    c = conn.cursor()
    offset = (page - 1) * limit
    c.execute("SELECT * FROM runs ORDER BY timestamp DESC LIMIT ? OFFSET ?", (limit, offset))
    rows = c.fetchall()
    
    c.execute("SELECT * FROM people")
    people = {p['id']: p['name'] for p in c.fetchall()}
    
    history = []
    for r in rows:
        try:
            actor_ids = json.loads(r['actors'])
            actor_names = [people.get(aid, "Unknown") for aid in actor_ids]
            history.append({
                "id": r['id'],
                "timestamp": r['timestamp'],
               "mode": r['mode'],
                "actors": actor_ids,
                "actor_names": actor_names,
                "points_each": r['points_each']
            })
        except:
            continue
        
    conn.close()
    return history

@app.get("/api/suggest")
def suggest_pair():
    state = get_state()
    people = state['people']
    
    if not people:
        return {"error": "No people found"}
    
    # Sort by score asc, then last_visit asc (None is oldest)
    def sort_key(p):
        lv = p['last_visit'] or "0000-01-01"
        return (p['score'], lv)
        
    sorted_people = sorted(people, key=sort_key)
    
    if len(sorted_people) < 2:
        return {"suggested": [], "reason": "Not enough people"}
        
    suggestion = [sorted_people[0], sorted_people[1]]
    reason = "Lowest scores & longest time since last visit"
    
    # Check last run
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT actors FROM runs ORDER BY timestamp DESC LIMIT 1")
    last_run = c.fetchone()
    conn.close()
    
    if last_run:
        try:
            last_actors = set(json.loads(last_run['actors']))
            suggested_ids = {suggestion[0]['id'], suggestion[1]['id']}
            
            if last_actors == suggested_ids and len(people) > 2:
                suggestion = [sorted_people[0], sorted_people[2]]
                reason += " (rotated to avoid repeat)"
        except:
            pass
            
    return {
        "suggested": suggestion,
        "reason": reason
    }

@app.get("/api/export/csv")
def export_csv_endpoint():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM runs ORDER BY timestamp DESC")
    rows = c.fetchall()
    
    c.execute("SELECT * FROM people")
    people = {p['id']: p['name'] for p in c.fetchall()}
    conn.close()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['id', 'timestamp', 'mode', 'actors', 'points_each'])
    
    for r in rows:
        try:
            actor_ids = json.loads(r['actors'])
            actor_names = ", ".join([people.get(aid, "Unknown") for aid in actor_ids])
            writer.writerow([r['id'], r['timestamp'], r['mode'], actor_names, r['points_each']])
        except:
            continue
            
    return Response(content=output.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=water_runs.csv"})

@app.post("/api/send-alert")
def send_alert_manually():
    """Manually trigger Telegram alert to next person (admin only)"""
    result = notify_next_person()
    if result.get('success'):
        return {"success": True, "message": f"Telegram alert sent to {result.get('to')}"}
    else:
        raise HTTPException(500, result.get('error', 'Failed to send alert'))

@app.get("/api/telegram-status")
def telegram_status():
    """Check if Telegram alerts are enabled"""
    return {
        "enabled": ENABLE_TELEGRAM_ALERTS,
        "service": "Telegram Bot API (FREE)"
    }
