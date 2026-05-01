# ---------- 1. Imports ----------
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import text

# ---------- 2. App setup ----------
app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///college_basketball.db"

# SERIALIZABLE
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "isolation_level": "AUTOCOMMIT"
}
db = SQLAlchemy(app)

# ---------- 3. Database models ----------
class Conference(db.Model):
    conf_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
class Team(db.Model):
    team_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    conf_id = db.Column(db.Integer, db.ForeignKey("conference.conf_id"))
    logo_url = db.Column(db.String(255), unique=True)
class Player(db.Model):
    player_id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("team.team_id"))
    name = db.Column(db.String(100))
    year = db.Column(db.String(100))
    pts = db.Column(db.Float)
    reb = db.Column(db.Float)
    ast = db.Column(db.Float)
class Fan(db.Model):
    fan_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    team_id = db.Column(db.Integer, db.ForeignKey("team.team_id"))
    fav_player_id = db.Column(db.Integer, db.ForeignKey("player.player_id"))
    year = db.Column(db.String(100))

# ---------- 4. Seed initial data ----------
def seed_data():
    db.create_all()
    if not Conference.query.first():
        acc = Conference(name="ACC")
        big_ten = Conference(name="Big Ten")
        sec = Conference(name = "SEC")
        big_east = Conference(name="Big East")
        big_twelve = Conference(name="Big Twelve")

        db.session.add_all([acc, big_ten, sec, big_east, big_twelve])
        db.session.flush()

        teams = [
            #ACC Teams
            Team(name="Duke", conf_id=acc.conf_id, wins = 33, losses = 3, logo_url="/static/images/duke.png"),
            Team(name="North Carolina", conf_id=acc.conf_id, wins = 33, losses = 3, logo_url="/static/images/north_carolina.png"),

            #SEC Teams
            Team(name="Florida", conf_id=sec.conf_id, wins=27, losses=8, logo_url="/static/images/florida.png"),
            Team(name="Alabama", conf_id=sec.conf_id, wins=25, losses=9, logo_url="/static/images/alabama.png"),
            Team(name="Arkansas", conf_id=sec.conf_id, wins=28, losses=8, logo_url="/static/images/arkansas.png"),
            Team(name="Vanderbilt", conf_id=sec.conf_id, wins=27, losses=9, logo_url="/static/images/vanderbilt.png"),
            Team(name="Tennessee", conf_id=sec.conf_id, wins=24, losses=11, logo_url="/static/images/tennessee.png"),
            Team(name="Texas A&M", conf_id=sec.conf_id, wins=22, losses=12, logo_url="/static/images/texasA&M.png"),
            Team(name="Georgia", conf_id=sec.conf_id, wins=22, losses=11, logo_url="/static/images/georgia.png"),
            Team(name="Kentucky", conf_id=sec.conf_id, wins=22, losses=14, logo_url="/static/images/kentucky.png"),
            Team(name="Missoursi", conf_id=sec.conf_id, wins=20, losses=13, logo_url="/static/images/missouri.png"),
            Team(name="Texas", conf_id=sec.conf_id, wins=21, losses=14, logo_url="/static/images/texas.png"),
            Team(name="Oklahoma", conf_id=sec.conf_id, wins=19, losses=15, logo_url="/static/images/oklahoma.png"),
            Team(name="Auburn", conf_id=sec.conf_id, wins=20, losses=16, logo_url="/static/images/auburn.png"),
            Team(name="Mississippi State", conf_id=sec.conf_id, wins=13, losses=19, logo_url="/static/images/mississippi.png"),
            Team(name="South Carolina", conf_id=sec.conf_id, wins=13, losses=19, logo_url="/static/images/south_carolina.png"),
            Team(name="Ole Miss", conf_id=sec.conf_id, wins=15, losses=20, logo_url="/static/images/ole_miss.png"),
            Team(name="LSU", conf_id=sec.conf_id, wins=15, losses=17, logo_url="/static/images/lsu.png"),
            

            #Big Ten Teams
            Team(name="Michigan", conf_id=big_ten.conf_id, wins = 33, losses = 3, logo_url="/static/images/michigan.png"),
            Team(name="Ohio State", conf_id=big_ten.conf_id, wins = 21, losses = 12, logo_url="/static/images/ohio_state.png"),
            Team(name="Purdue", conf_id=big_ten.conf_id, wins = 27, losses = 8, logo_url="/static/images/purdue.png"),
            Team(name="Wisconsin", conf_id=big_ten.conf_id, wins = 24, losses = 10, logo_url="/static/images/wisconsin.png"),
            Team(name="Indiana University", conf_id=big_ten.conf_id, wins = 18, losses = 14, logo_url="/static/images/indiana_university.png"),
            Team(name="Northwestern", conf_id=big_ten.conf_id, wins = 15, losses = 19, logo_url="/static/images/northwestern.png"),
            Team(name="Nebraska", conf_id=big_ten.conf_id, wins = 28, losses = 6, logo_url="/static/images/nebraska.png"),
            Team(name="Michigan State", conf_id=big_ten.conf_id, wins = 27, losses = 7, logo_url="/static/images/michigan_state.png"),
            Team(name="Illinois", conf_id=big_ten.conf_id, wins = 26, losses = 8, logo_url="/static/images/uic.png"),
            Team(name="UCLA", conf_id=big_ten.conf_id, wins = 24, losses = 12, logo_url="/static/images/ucla.png"),
            Team(name="USC", conf_id=big_ten.conf_id, wins = 18, losses = 14, logo_url="/static/images/usc.png"),
            Team(name="Iowa", conf_id=big_ten.conf_id, wins = 23, losses = 12, logo_url="/static/images/iowa.png"),
            Team(name="Minnesota", conf_id=big_ten.conf_id, wins = 15, losses = 17, logo_url="/static/images/minnesota.png"),
            Team(name="Washington", conf_id=big_ten.conf_id, wins = 16, losses = 17, logo_url="/static/images/washington.png"),
            Team(name="Rutgers", conf_id=big_ten.conf_id, wins = 14, losses = 19, logo_url="/static/images/rutgers.png"),
            Team(name="Oregon", conf_id=big_ten.conf_id, wins = 12, losses = 20, logo_url="/static/images/oregon.png"),
            Team(name="Maryland", conf_id=big_ten.conf_id, wins = 12, losses = 21, logo_url="/static/images/maryland.png"),
            Team(name="Penn St.", conf_id=big_ten.conf_id, wins = 12, losses = 20, logo_url="/static/images/penn_st.png"),

            
        ]
        db.session.add_all(teams)
        db.session.flush()

        purdue = next(t for t in teams if t.name == "Purdue")
        db.session.add_all([

            #Purdue Players

            Player(name = "Braden Smith", team_id = purdue.team_id, year = "Senior", pts = 14.3, reb = 3.0, ast = 9.0),
            Player(name = "CJ Cox", team_id = purdue.team_id, year = "Sophomore", pts = 8.5, reb = 2.6, ast = 1.3),
            Player(name = "Trey Kaufman-Renn", team_id = purdue.team_id, year = "Senior", pts = 14.1, reb = 8.5, ast = 2.6),
            Player(name = "Fletcher Loyer", team_id = purdue.team_id, year = "Senior", pts = 14.1, reb = 2.3, ast = 2.0),
            Player(name = "Oscar Cluff", team_id = purdue.team_id, year = "Senior", pts = 10.5, reb = 7.5, ast = 1.8),
            Player(name = "Daniel Jacobsen", team_id = purdue.team_id, year = "Sophomore", pts = 5.8, reb = 3.2, ast = 0.4),
            Player(name = "Omer Mayer", team_id = purdue.team_id, year = "Freshman", pts = 5.6, reb = 1.1, ast = 1.2),
            Player(name = "Jack Benter", team_id = purdue.team_id, year = "Freshman", pts = 4.6, reb = 2.7, ast = 0.9),
            Player(name = "Gicarri Harris", team_id = purdue.team_id, year = "Sophomore", pts = 4.5, reb = 1.6, ast = 0.9)

        ])
        db.session.commit()
    db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_conference_name ON conference(name)"))
    db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_team_conf_id ON team(conf_id)"))
# call it once on startup
with app.app_context():
    seed_data()
# ---------- 5. Routes ----------


@app.route("/")
def index():
    return "<h3>College Basketball API is running.<br>Try /api/conferences</h3>"


# GET CONFERENCES
@app.route("/api/conferences")
def get_conferences():
    sql = text("SELECT conf_id AS id, name FROM Conference")
    result = db.session.execute(sql)
    conferences = [dict(row._mapping) for row in result]  # convert rows to dicts
    return jsonify(conferences)

# GET TEAMS FROM CONFERENCE
@app.route("/api/teams")
def get_teams():
    conf_name = request.args.get("conference")

    query = text(
        "SELECT t.team_id, t.name, t.logo_url, t.wins, t.losses "
        "FROM Team t "
        "JOIN Conference c ON t.conf_id = c.conf_id "
        "WHERE c.name = :conf_name "
        "ORDER BY t.wins DESC")

    result = db.session.execute(query, {"conf_name": conf_name})

    teams = [
        {
            "id": row.team_id,
            "name": row.name,
            "logo_path": row.logo_url,
            "wins": row.wins,
            "losses": row.losses
        }
        for row in result
    ]

    return jsonify(teams)

# GET PLAYERS FROM TEAM, OPTIONAL YEAR PARAMETER
@app.route("/api/players")
def get_players():
    team_id = request.args.get("team_id")
    year = request.args.get("year")  # optional filter

    query = """
        SELECT player_id, name, year, pts, reb, ast
        FROM Player
        WHERE team_id = :team_id
    """

    params = {"team_id": team_id}

    if year:
        query += " AND year = :year"

    query += " ORDER BY pts DESC"

    result = db.session.execute(text(query), params)

    players = [
        {
            "id": row.player_id,
            "name": row.name,
            "year": row.year,
            "PTS" : row.pts,
            "REB" : row.reb,
            "AST" : row.ast
        }
        for row in result
    ]

    return jsonify(players)

# GET INFORMATION ABOUT A TEAM
@app.route("/api/stats")
def get_team_stats():
    team_name = request.args.get("team")
    if not team_name:
        return jsonify({"error": "Team name is required"}), 400
    team = Team.query.filter_by(name=team_name).first()
    if not team:
        return jsonify({"error": "Team not found"}), 404
    return jsonify({
        "team": team.name,
        "wins": team.wins,
        "losses": team.losses
    })

# ADD A FAN
@app.route("/api/fans", methods=["POST"])
def add_fan():
    data = request.json

    first = data.get("first_name")
    last = data.get("last_name")
    team_id = data.get("team_id")
    year = data.get("year")
    fav_player_id = data.get("fav_player_id")

    if not first or not last:
        return jsonify({"error": "First and last name are required"}), 400
    if not team_id:
        return jsonify({"error": "Team ID is required"}), 400

    # Check if fan exists on a different team
    existing = db.session.execute(text("""
        SELECT team_id FROM fan
        WHERE first_name = :first AND last_name = :last
    """), {"first": first, "last": last}).fetchone()

    if existing and existing.team_id != team_id:
        return jsonify({"error": "Fan already belongs to another team"}), 400

    # Insert fan
    db.session.execute(text("""
        INSERT INTO fan (first_name, last_name, team_id, year, fav_player_id)
        VALUES (:first, :last, :team_id, :year, :fav_player_id)
    """), {
        "first": first,
        "last": last,
        "team_id": team_id,
        "year": year,
        "fav_player_id": fav_player_id
    })

    db.session.commit()  # commit after the insert

    # Retrieve the last inserted fan_id (SQLite uses last_insert_rowid)
    fan_id = db.session.execute(text("SELECT last_insert_rowid()")).scalar()

    # Return response
    return jsonify({
        "fan_id": fan_id,
        "first_name": first,
        "last_name": last,
        "team_id": team_id,
        "year": year,
        "fav_player_id": fav_player_id
    }), 201

# DELETE FAN
@app.route("/api/fans/<int:fan_id>", methods=["DELETE"])
def delete_fan(fan_id):
    result = db.session.execute(text("""
        DELETE FROM Fan WHERE fan_id = :id
    """), {"id": fan_id})

    db.session.commit()

    if result.rowcount == 0:
        return jsonify({"error": "Fan not found"}), 404

    return jsonify({"message": "Fan deleted"})

# UPDATE FAN
@app.route("/api/fans/<int:fan_id>", methods=["PUT"])
def update_fan(fan_id):
    data = request.json

    first = data.get("first_name")
    last = data.get("last_name")
    team_id = data.get("team_id")
    year = data.get("year")
    fav_player_id = data.get("fav_player_id")

    existing = db.session.execute(text("""
        SELECT fan_id, team_id FROM Fan
        WHERE first_name = :first AND last_name = :last
    """), {"first": first, "last": last}).fetchone()
    # prevent only if there's another fan (different id) with same name but on another team
    if existing and existing.fan_id != fan_id and existing.team_id != team_id:
        return jsonify({"error": "Fan already belongs to another team"}), 400

    # Update Querey
    result = db.session.execute(text("""
        UPDATE Fan
        SET first_name = :first,
            last_name = :last,
            team_id = :team_id,
            year = :year,
            fav_player_id = :fav_player_id
        WHERE fan_id = :id
    """), {
        "first": first,
        "last": last,
        "team_id": team_id,
        "year": year,
        "fav_player_id": fav_player_id,
        "id": fan_id
    })

    db.session.commit()

    if result.rowcount == 0:
        return jsonify({"error": "Fan not found"}), 404

    return jsonify({
        "fan_id": fan_id,
        "first_name": first,
        "last_name": last,
        "team_id": team_id,
        "year": year,
        "fav_player_id": fav_player_id
    })

# GET FANS BASED ON TEAM
@app.route("/api/fans", methods=["GET"])
def get_fans():
    team_id = request.args.get("team_id")

    if team_id:
        result = db.session.execute(text("""
            SELECT * FROM Fan WHERE team_id = :team_id
        """), {"team_id": team_id})
    else:
        result = db.session.execute(text("SELECT * FROM Fan"))

    fans = []
    for row in result:
        fans.append({
            "fan_id": row.fan_id,
            "first_name": row.first_name,
            "last_name": row.last_name,
            "team_id": row.team_id,
            "year": row.year,
            "fav_player_id": row.fav_player_id
        })

    return jsonify(fans)


@app.route("/api/sqltest")
def sql_test():
    sql = text("SELECT c.name AS conference, COUNT(t.team_id) AS team_count "
               "FROM conference c LEFT JOIN team t ON c.conf_id = t.conf_id "
               "GROUP BY c.name")
    result = db.session.execute(sql)
    data = [dict(row._mapping) for row in result]  # convert to dict
    return jsonify(data)
# ---------- 6. Run app ----------
if __name__ == "__main__":
    app.run(debug=True)