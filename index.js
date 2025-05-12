import { useState } from 'react';

export default function Home() {
  const [token, setToken] = useState("");
  const [spends, setSpends] = useState({ dining: "", travel: "", groceries: "" });
  const [result, setResult] = useState("");
  const [loginCreds, setLoginCreds] = useState({ username: "", password: "" });

  const handleLogin = async () => {
    const res = await fetch("https://localhost:8000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(loginCreds),
    });
    const data = await res.json();
    if (data.access_token) {
      setToken(data.access_token);
    } else {
      alert("Invalid login");
    }
  };

  const handleRecommend = async () => {
    const res = await fetch("https://localhost:8000/recommend", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        spends: {
          dining: parseFloat(spends.dining),
          travel: parseFloat(spends.travel),
          groceries: parseFloat(spends.groceries),
        },
      }),
    });
    const data = await res.json();
    setResult(data.best_card);
  };

  const handleParseGmail = async () => {
    await fetch("https://localhost:8000/parse_gmail", {
      method: "POST",
    });
    alert("Gmail parsed!");
  };

  return (
    <div style={{ padding: 20, fontFamily: 'sans-serif' }}>
      <h1>Maxx Mai Card Assignment</h1>

      {!token ? (
        <>
          <h2>Login</h2>
          <label>Username: </label>
          <input
            type="text"
            value={loginCreds.username}
            onChange={(e) => setLoginCreds({ ...loginCreds, username: e.target.value })}
            style={{ margin: '5px' }}
          />
          <br />
          <label>Password: </label>
          <input
            type="password"
            value={loginCreds.password}
            onChange={(e) => setLoginCreds({ ...loginCreds, password: e.target.value })}
            style={{ margin: '5px' }}
          />
          <br />
          <button onClick={handleLogin}>Login</button>
        </>
      ) : (
        <>
          <h2>Spends Form</h2>
          <label>Dining: </label>
          <input
            type="number"
            value={spends.dining}
            onChange={(e) => setSpends({ ...spends, dining: e.target.value })}
            style={{ margin: '5px' }}
          />
          <br />
          <label>Travel: </label>
          <input
            type="number"
            value={spends.travel}
            onChange={(e) => setSpends({ ...spends, travel: e.target.value })}
            style={{ margin: '5px' }}
          />
          <br />
          <label>Groceries: </label>
          <input
            type="number"
            value={spends.groceries}
            onChange={(e) => setSpends({ ...spends, groceries: e.target.value })}
            style={{ margin: '5px' }}
          />
          <br />
          <button onClick={handleRecommend}>Get Best Card</button>
          <div style={{ marginTop: '10px' }}>
            <strong>Best Card:</strong> {result}
          </div>

          <h2 style={{ marginTop: '30px' }}>Gmail Parse</h2>
          <button onClick={handleParseGmail}>Parse Gmail</button>
        </>
      )}
    </div>
  );
}
