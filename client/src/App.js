import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

const API_BASE = "http://localhost:5000";

function App() {
  const [conferences, setConferences] = useState([]);
  const [teams, setTeams] = useState([]);
  const [selectedConference, setSelectedConference] = useState("");
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [teamStats, setTeamStats] = useState(null);
  const [players, setPlayers] = useState([]);
  const [selectedYear, setSelectedYear] = useState("");
  const [fans, setFans] = useState([]);
  const [newFan, setNewFan] = useState({
    first_name: "",
    last_name: "",
    year: "",
    fav_player_id: ""
  });
  const [editingFan, setEditingFan] = useState(null);

  // Load all conferences on mount
  useEffect(() => {
    axios.get(`${API_BASE}/api/conferences`).then(res => setConferences(res.data));
  }, []);

  // Load teams when a conference is chosen
  useEffect(() => {
    if (selectedConference) {
      axios
        .get(`${API_BASE}/api/teams?conference=${selectedConference}`)
        .then(res => setTeams(res.data));
    } else {
      setTeams([]);
    }
  }, [selectedConference]);

  // Fetch stats when a team is clicked
  const handleTeamClick = team => {
    setSelectedTeam(team);

    // fetch stats
    axios
      .get(`${API_BASE}/api/stats?team=${encodeURIComponent(team.name)}&conference=${encodeURIComponent(selectedConference)}`)
      .then(res => setTeamStats(res.data));

    // fetch players
    axios
      .get(`${API_BASE}/api/players?team_id=${team.id}`)
      .then(res => setPlayers(res.data));

    // fetch fans
    axios
      .get(`${API_BASE}/api/fans?team_id=${team.id}`)
      .then(res => setFans(res.data));
  };

  const handleAddFan = () => {
  axios
    .post(`${API_BASE}/api/fans`, {
      ...newFan,
      team_id: selectedTeam.id
    })
    .then(res => {
      setFans([...fans, res.data]);
      setNewFan({
        first_name: "",
        last_name: "",
        year: "",
        fav_player_id: ""
      });
    })
    .catch(err => {
        // Axios attaches the backend response under err.response
        if (err.response) {
          alert(`Error: ${err.response.data.error || 'Unable to add fan.'}`);
        } else {
          alert('Network error — could not connect to server.');
        }
    });
  };

  const handleDeleteFan = id => {
    axios.delete(`${API_BASE}/api/fans/${id}`).then(() => {
      setFans(fans.filter(f => f.fan_id !== id));
    });
  };

  const handleEditFan = fan => {
    setEditingFan(fan);
  };

  const handleUpdateFan = () => {
    axios
      .put(`${API_BASE}/api/fans/${editingFan.fan_id}`, editingFan)
      .then(res => {
        setFans(
          fans.map(f => (f.fan_id === editingFan.fan_id ? res.data : f))
        );
        setEditingFan(null);
      })
        .catch(err => {
        // Axios attaches the backend response under err.response
        if (err.response) {
          alert(`Error: ${err.response.data.error || 'Unable to add fan.'}`);
        } else {
          alert('Network error — could not connect to server.');
        }
    });
  };

  const filteredPlayers = selectedYear
  ? players.filter(p => p.year === selectedYear)
  : players;

  return (
    <div className="App">
      <h2>🏀 College Basketball Explorer</h2>

      {/* Conference Dropdown */}
      <label>Conference:</label>
      <select
        value={selectedConference}
        onChange={e => {
          setSelectedConference(e.target.value);
          setSelectedTeam(null);
          setTeamStats(null);
        }}
      >
        <option value="">-- Choose a Conference --</option>
        {conferences.map(c => (
          <option key={c.id} value={c.name}>
            {c.name}
          </option>
        ))}
      </select>

      {/* Team rows */}
      {teams.length > 0 && (
        <div className="team-list">
          {teams.map(team => (
            <div
              key={team.id}
              className="team-row"
              onClick={() => handleTeamClick(team)}
            >
              <img
                src={`${API_BASE}/${team.logo_path}`}
                alt={team.name}
                className="team-logo"
              />
              <div className="team-info">
                <span className="team-name">{team.name}</span>
                <span className="team-stat">Wins: {team.wins}</span>
                <span className="team-stat">Losses: {team.losses}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Stats when a team is selected */}
      {teamStats && (
        <div className="modal-overlay" onClick={() => setTeamStats(null)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            
            <button className="close-btn" onClick={() => setTeamStats(null)}>
              ✖
            </button>

            <h2>{selectedTeam.name}</h2>

            {/* TEAM STATS */}
            <p>Wins: {teamStats.wins}</p>
            <p>Losses: {teamStats.losses}</p>

            <label>Filter by Year:</label>
            <select
              value={selectedYear}
              onChange={e => setSelectedYear(e.target.value)}
            >
              <option value="">All</option>
              <option value="Freshman">Freshman</option>
              <option value="Sophomore">Sophomore</option>
              <option value="Junior">Junior</option>
              <option value="Senior">Senior</option>
            </select>


            {/* PLAYERS SECTION (your existing code) */}
            <h3>Players</h3>
            <table className="player-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Year</th>
                <th>PTS</th>
                <th>REB</th>
                <th>AST</th>
              </tr>
            </thead>
            <tbody>
              {players.length > 0 ? (
                filteredPlayers.map(player => (
                  <tr key={player.id}>
                    <td>{player.name}</td>
                    <td>{player.year}</td>
                    <td>{player.PTS}</td>
                    <td>{player.REB}</td>
                    <td>{player.AST}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="2">No players found</td>
                </tr>
              )}
            </tbody>
            </table>

            <h3>Fans</h3>

            {/* ADD FAN FORM */}
            <div className="fan-form">
              <input
                placeholder="First Name"
                value={newFan.first_name}
                onChange={e =>
                  setNewFan({ ...newFan, first_name: e.target.value })
                }
              />

              <input
                placeholder="Last Name"
                value={newFan.last_name}
                onChange={e =>
                  setNewFan({ ...newFan, last_name: e.target.value })
                }
              />

              <select
                value={newFan.year}
                onChange={e =>
                  setNewFan({ ...newFan, year: e.target.value })
                }
              >
                <option value="">Year</option>
                <option value="Freshman">Freshman</option>
                <option value="Sophomore">Sophomore</option>
                <option value="Junior">Junior</option>
                <option value="Senior">Senior</option>
              </select>

              <select
                value={newFan.fav_player_id}
                onChange={e =>
                  setNewFan({
                    ...newFan,
                    fav_player_id: Number(e.target.value)
                  })
                }
              >
                <option value="">Favorite Player</option>
                {filteredPlayers.map(p => (
                  <option key={p.id} value={p.id}>
                    {p.name}
                  </option>
                ))}
              </select>

              <button onClick={handleAddFan}>Add Fan</button>
            </div>

            {/* EDIT FAN */}
            {editingFan && (
              <div className="fan-edit">
                <h4>Edit Fan</h4>

                <input
                  value={editingFan.first_name}
                  onChange={e =>
                    setEditingFan({
                      ...editingFan,
                      first_name: e.target.value
                    })
                  }
                />

                <input
                  value={editingFan.last_name}
                  onChange={e =>
                    setEditingFan({
                      ...editingFan,
                      last_name: e.target.value
                    })
                  }
                />

                <select
                  value={editingFan.year}
                  onChange={e =>
                    setEditingFan({
                      ...editingFan,
                      year: e.target.value
                    })
                  }
                >
                  <option value="Freshman">Freshman</option>
                  <option value="Sophomore">Sophomore</option>
                  <option value="Junior">Junior</option>
                  <option value="Senior">Senior</option>
                </select>

                <select
                  value={editingFan.fav_player_id}
                  onChange={e =>
                    setEditingFan({
                      ...editingFan,
                      fav_player_id: Number(e.target.value)
                    })
                  }
                >
                  {filteredPlayers.map(p => (
                    <option key={p.id} value={p.id}>
                      {p.name}
                    </option>
                  ))}
                </select>

                <button onClick={handleUpdateFan}>Save</button>
                <button onClick={() => setEditingFan(null)}>Cancel</button>
              </div>
            )}

            {/* FAN TABLE */}
            <table className="fan-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Year</th>
                  <th>Favorite Player</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {fans.map(fan => (
                  <tr key={fan.fan_id}>
                    <td>
                      {fan.first_name} {fan.last_name}
                    </td>
                    <td>{fan.year}</td>
                    <td>
                      {
                        players.find(p => p.id === fan.fav_player_id)
                          ?.name || "None"
                      }
                    </td>
                    <td>
                      <button onClick={() => handleEditFan(fan)}>
                        Edit
                      </button>
                      <button onClick={() => handleDeleteFan(fan.fan_id)}>
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
