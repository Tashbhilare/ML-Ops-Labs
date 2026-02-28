import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "running"

def test_health():
    r = client.get("/health")
    assert r.status_code == 200

def test_cricket_batter_basic():
    payload = {"player_name": "Virat Kohli", "runs_scored": 500, "balls_faced": 420,
               "innings_played": 10, "times_not_out": 2, "fours": 45, "sixes": 10}
    r = client.post("/cricket/batter", json=payload)
    assert r.status_code == 200
    assert r.json()["batting_average"] == round(500/8, 2)

def test_cricket_batter_invalid():
    payload = {"player_name": "Bad", "runs_scored": 100, "balls_faced": 90,
               "innings_played": 3, "times_not_out": 3, "fours": 10, "sixes": 2}
    r = client.post("/cricket/batter", json=payload)
    assert r.status_code == 422

def test_cricket_bowler_basic():
    payload = {"player_name": "Bumrah", "overs_bowled": 10.0,
               "runs_conceded": 32, "wickets_taken": 4, "maidens": 2}
    r = client.post("/cricket/bowler", json=payload)
    assert r.status_code == 200
    assert r.json()["wicket_impact"] == "Match-winner"

def test_cricket_bowler_no_wickets():
    payload = {"player_name": "Expensive", "overs_bowled": 5.0,
               "runs_conceded": 55, "wickets_taken": 0, "maidens": 0}
    r = client.post("/cricket/bowler", json=payload)
    assert r.json()["bowling_average"] is None

def test_basketball_player():
    payload = {"player_name": "Tatum", "points": 26.5, "rebounds": 8.1, "assists": 4.9,
               "steals": 1.1, "blocks": 0.8, "turnovers": 2.3, "minutes_played": 35.2,
               "field_goals_made": 9.2, "field_goals_attempted": 20.1,
               "free_throws_made": 5.8, "free_throws_attempted": 6.9, "three_pointers_made": 2.3}
    r = client.post("/basketball/player", json=payload)
    assert r.status_code == 200
    assert r.json()["role_classification"] != ""

def test_basketball_compare():
    r = client.get("/basketball/compare", params={
        "player1_pts": 25, "player1_reb": 5, "player1_ast": 10,
        "player2_pts": 30, "player2_reb": 3, "player2_ast": 4,
        "player1_name": "Point God", "player2_name": "Scorer"})
    assert r.json()["edge"] == "Point God"