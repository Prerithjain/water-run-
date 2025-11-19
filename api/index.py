from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import sqlite3
import os
from datetime import datetime
from typing import List, Optional
import json
import csv
import io

app = FastAPI()

# Determine DB path
# For Vercel, we might need to use /tmp if we want write access (but it's ephemeral)
# The prompt says "sqlite DB file (data/waterrun.db) persists on Vercel ephemeral storage... Include alternative"
# We will stick to data/waterrun.db for now, assuming the user understands the limitation or is running locally.
# To make it work on Vercel (read-only root), we might HAVE to use /tmp.
# But let's try to use the project root 'data' folder first. If it fails, we catch it.
# Actually, on Vercel, only /tmp is writable. So we MUST use /tmp for the DB if we want to write to it.
# But for local dev, we want 'data/waterrun.db'.
# We can check an env var or just catch the error.

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

def init_db():
    try:
        conn = get_db()
        c = conn.cursor()
        
        # Check if we need to migrate to the new people list
        # We check if 'Vishwas' exists. If not, we assume we need to reset (or it's a fresh DB).
        # This is a simple way to switch from the default "Alice..." list to the user's list.
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
            name TEXT UNIQUE NOT NULL
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY,
            timestamp TEXT NOT NULL,
            mode TEXT NOT NULL,
            actors TEXT NOT NULL,
            points_each INTEGER NOT NULL
        )''')
        
        # Insert specific people and scores
        # Names: Vishwas, Prerith, Prashanth, Bhuvan Gumma, Vikas Reddy
        # Scores: Vishwas-7, Bhuvan Gumma-5, Prashanth-5, Prerith-5, Vikas Reddy-3
        
        target_people = [
            {"name": "Vishwas", "score": 7},
            {"name": "Prerith", "score": 5},
            {"name": "Prashanth", "score": 5},
            {"name": "Bhuvan Gumma", "score": 5},
            {"name": "Vikas Reddy", "score": 3}
        ]
        
        for p in target_people:
            try:
                c.execute("INSERT INTO people (name) VALUES (?)", (p['name'],))
                # Get the ID
                c.execute("SELECT id FROM people WHERE name = ?", (p['name'],))
                pid = c.fetchone()[0]
                
                # Insert initial score if needed
                # We check if they have any runs. If not, add a legacy run.
                # We assume if we just inserted them, they have 0 runs.
                if p['score'] > 0:
                    # Check if they already have points (in case we re-run this)
                    # Actually, since we dropped tables if Vishwas wasn't there, this runs once.
                    # But if we restart server, table exists, so we skip the DROP.
                    # So we need to check if they have points.
                    pass 
                    
            except sqlite3.IntegrityError:
                pass

        # Now ensure scores match target (idempotent check)
        # This handles the case where we just created them, OR if they exist but we want to ensure initial scores.
        # However, we only want to add "Initial Score" ONCE.
        # So we check if there is a run with mode='legacy_import' for this user.
        
        for p in target_people:
            c.execute("SELECT id FROM people WHERE name = ?", (p['name'],))
            row = c.fetchone()
            if not row: continue
            pid = row[0]
            
            # Calculate current score
            # This is a bit complex to do in pure SQL with the JSON actors, so we'll just do a quick check
            # simpler: just insert a legacy run if NO runs exist for this user?
            # But the user might have added runs since then.
            # Let's just do it on the "Reset" path.
            pass

        if not table_exists:
            # We just reset the DB, so we can safely insert the initial scores
            timestamp = datetime.utcnow().isoformat() + "Z"
            for p in target_people:
                if p['score'] > 0:
                    c.execute("SELECT id FROM people WHERE name = ?", (p['name'],))
                    pid = c.fetchone()[0]
                    actors_json = json.dumps([pid])
                    c.execute("INSERT INTO runs (timestamp, mode, actors, points_each) VALUES (?, ?, ?, ?)",
                              (timestamp, 'legacy_import', actors_json, p['score']))

        # Force update scores for Prerith and Vikas if needed
        # This is a bit hacky but ensures the user's request is met even if DB exists
        updates = [
            ("Prerith", 5),
            ("Vikas Reddy", 3)
        ]
        
        for name, score in updates:
            try:
                c.execute("SELECT id FROM people WHERE name = ?", (name,))
                row = c.fetchone()
                if row:
                    pid = row[0]
                    # Calculate current score
                    # We can't easily "set" the score because it's derived from runs.
                    # So we need to see what the current score is, and add a correction run.
                    
                    # Get current score
                    current_score = 0
                    c.execute("SELECT * FROM runs")
                    all_runs = c.fetchall()
                    for r in all_runs:
                        try:
                            if pid in json.loads(r['actors']):
                                current_score += r['points_each']
                        except:
                            pass
                            
                    diff = score - current_score
                    if diff != 0:
                        print(f"Correcting score for {name}: current {current_score}, target {score}, diff {diff}")
                        timestamp = datetime.utcnow().isoformat() + "Z"
                        actors_json = json.dumps([pid])
                        c.execute("INSERT INTO runs (timestamp, mode, actors, points_each) VALUES (?, ?, ?, ?)",
                                  (timestamp, 'correction', actors_json, diff))
            except Exception as e:
                print(f"Error updating score for {name}: {e}")

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
            "last_visit": last_visit.get(p['id'])
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
    
    timestamp = datetime.utcnow().isoformat() + "Z"
    actors_json = json.dumps(req.actors)
    
    c.execute("INSERT INTO runs (timestamp, mode, actors, points_each) VALUES (?, ?, ?, ?)",
              (timestamp, req.mode, actors_json, points))
    conn.commit()
    conn.close()
    
    return {"success": True, "new_state": get_state()}

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
