from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Optional

app = FastAPI(
    title="Sports Stats API",
    description="A containerized REST API for computing cricket and basketball player performance metrics. Built for MLOps Docker Lab 1.",
    version="1.0.0",
)

# ── CRICKET MODELS ────────────────────────────────────────────────

class CricketBatterInput(BaseModel):
    player_name: str = Field(..., example="Virat Kohli")
    runs_scored: int = Field(..., ge=0, example=82)
    balls_faced: int = Field(..., ge=1, example=70)
    innings_played: int = Field(..., ge=1, example=5)
    times_not_out: int = Field(..., ge=0, example=1)
    fours: int = Field(..., ge=0, example=8)
    sixes: int = Field(..., ge=0, example=3)

    @field_validator("times_not_out")
    @classmethod
    def not_out_less_than_innings(cls, v, info):
        if "innings_played" in info.data and v >= info.data["innings_played"]:
            raise ValueError("times_not_out must be less than innings_played")
        return v

class CricketBatterOutput(BaseModel):
    player_name: str
    batting_average: float
    strike_rate: float
    boundary_percentage: float
    impact_score: float
    performance_tier: str

class CricketBowlerInput(BaseModel):
    player_name: str = Field(..., example="Jasprit Bumrah")
    overs_bowled: float = Field(..., gt=0, example=8.3)
    runs_conceded: int = Field(..., ge=0, example=42)
    wickets_taken: int = Field(..., ge=0, example=3)
    maidens: int = Field(..., ge=0, example=1)

class CricketBowlerOutput(BaseModel):
    player_name: str
    economy_rate: float
    bowling_average: Optional[float]
    bowling_strike_rate: Optional[float]
    wicket_impact: str

# ── BASKETBALL MODELS ─────────────────────────────────────────────

class BasketballPlayerInput(BaseModel):
    player_name: str = Field(..., example="Jayson Tatum")
    points: float = Field(..., ge=0, example=26.5)
    rebounds: float = Field(..., ge=0, example=8.1)
    assists: float = Field(..., ge=0, example=4.9)
    steals: float = Field(..., ge=0, example=1.1)
    blocks: float = Field(..., ge=0, example=0.8)
    turnovers: float = Field(..., ge=0, example=2.3)
    minutes_played: float = Field(..., gt=0, example=35.2)
    field_goals_made: float = Field(..., ge=0, example=9.2)
    field_goals_attempted: float = Field(..., gt=0, example=20.1)
    free_throws_made: float = Field(..., ge=0, example=5.8)
    free_throws_attempted: float = Field(..., ge=0, example=6.9)
    three_pointers_made: float = Field(..., ge=0, example=2.3)

class BasketballPlayerOutput(BaseModel):
    player_name: str
    points_per_36: float
    true_shooting_percentage: float
    player_efficiency_rating: float
    usage_proxy: float
    role_classification: str

# ── HELPERS ───────────────────────────────────────────────────────

def get_performance_tier(average: float, strike_rate: float) -> str:
    score = (average * 0.6) + (strike_rate * 0.4 / 10)
    if score >= 50:
        return "Elite"
    elif score >= 35:
        return "Quality"
    elif score >= 20:
        return "Developing"
    else:
        return "Struggling"

def classify_basketball_role(pts: float, reb: float, ast: float) -> str:
    if pts >= 20 and (reb >= 8 or ast >= 7):
        return "Star / All-Around"
    elif pts >= 20:
        return "Primary Scorer"
    elif ast >= 7:
        return "Playmaker"
    elif reb >= 9:
        return "Rebounder / Anchor"
    elif pts >= 12:
        return "Rotation Contributor"
    else:
        return "Role Player"

# ── ROUTES ────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {"service": "Sports Stats API", "status": "running", "docs": "/docs", "version": "1.0.0"}

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}

@app.post("/cricket/batter", response_model=CricketBatterOutput, tags=["Cricket"])
def analyze_batter(data: CricketBatterInput):
    dismissals = data.innings_played - data.times_not_out
    if dismissals == 0:
        raise HTTPException(status_code=400, detail="Dismissals cannot be zero.")
    batting_avg = round(data.runs_scored / dismissals, 2)
    strike_rate = round((data.runs_scored / data.balls_faced) * 100, 2)
    boundary_runs = (data.fours * 4) + (data.sixes * 6)
    boundary_pct = round((boundary_runs / data.runs_scored) * 100, 2) if data.runs_scored > 0 else 0.0
    impact = round((batting_avg * 0.40) + (strike_rate * 0.35 / 10) + (boundary_pct * 0.25 / 10), 2)
    tier = get_performance_tier(batting_avg, strike_rate)
    return CricketBatterOutput(
        player_name=data.player_name,
        batting_average=batting_avg,
        strike_rate=strike_rate,
        boundary_percentage=boundary_pct,
        impact_score=impact,
        performance_tier=tier,
    )

@app.post("/cricket/bowler", response_model=CricketBowlerOutput, tags=["Cricket"])
def analyze_bowler(data: CricketBowlerInput):
    full_overs = int(data.overs_bowled)
    extra_balls = round((data.overs_bowled - full_overs) * 10)
    total_balls = (full_overs * 6) + extra_balls
    total_overs_decimal = total_balls / 6
    economy = round(data.runs_conceded / total_overs_decimal, 2)
    bowling_avg = round(data.runs_conceded / data.wickets_taken, 2) if data.wickets_taken > 0 else None
    bowling_sr = round(total_balls / data.wickets_taken, 2) if data.wickets_taken > 0 else None
    if data.wickets_taken >= 3:
        impact = "Match-winner"
    elif data.wickets_taken >= 1:
        impact = "Useful contributor"
    else:
        impact = "Wicketless"
    return CricketBowlerOutput(
        player_name=data.player_name,
        economy_rate=economy,
        bowling_average=bowling_avg,
        bowling_strike_rate=bowling_sr,
        wicket_impact=impact,
    )

@app.post("/basketball/player", response_model=BasketballPlayerOutput, tags=["Basketball"])
def analyze_basketball_player(data: BasketballPlayerInput):
    pts_per_36 = round((data.points / data.minutes_played) * 36, 2)
    ts_denominator = 2 * (data.field_goals_attempted + 0.44 * data.free_throws_attempted)
    ts_pct = round((data.points / ts_denominator) * 100, 2) if ts_denominator > 0 else 0.0
    positive = (data.points + data.rebounds * 1.2 + data.assists * 1.5 + data.steals * 2.0 + data.blocks * 2.0)
    negative = data.turnovers * 1.5
    per = round(((positive - negative) / data.minutes_played) * 36, 2)
    usage = round(((data.field_goals_attempted + 0.44 * data.free_throws_attempted + data.turnovers) / data.minutes_played) * 36, 2)
    role = classify_basketball_role(data.points, data.rebounds, data.assists)
    return BasketballPlayerOutput(
        player_name=data.player_name,
        points_per_36=pts_per_36,
        true_shooting_percentage=ts_pct,
        player_efficiency_rating=per,
        usage_proxy=usage,
        role_classification=role,
    )

@app.get("/basketball/compare", tags=["Basketball"])
def compare_players(
    player1_pts: float, player1_reb: float, player1_ast: float,
    player2_pts: float, player2_reb: float, player2_ast: float,
    player1_name: str = "Player 1", player2_name: str = "Player 2"
):
    score1 = round(player1_pts * 1.0 + player1_reb * 0.8 + player1_ast * 0.7, 2)
    score2 = round(player2_pts * 1.0 + player2_reb * 0.8 + player2_ast * 0.7, 2)
    winner = player1_name if score1 >= score2 else player2_name
    return {player1_name: {"composite_score": score1}, player2_name: {"composite_score": score2}, "edge": winner}