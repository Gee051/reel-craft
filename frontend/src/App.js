import { useState } from "react";
import "./App.css";

function App() {
  const [topic, setTopic] = useState("");
  const [genre, setGenre] = useState("drama");
  const [loading, setLoading] = useState(false);
  const [stage, setStage] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showPipeline, setShowPipeline] = useState(false);
  const [completedStages, setCompletedStages] = useState([]);

  const stages = [
    { id: 1, name: "Script Generation", desc: "Writing your drama script..." },
    { id: 2, name: "Storyboard", desc: "Breaking script into visual scenes..." },
    { id: 3, name: "Video Generation", desc: "Generating clips via Wan AI..." },
    { id: 4, name: "Assembly", desc: "Assembling final video..." },
  ];

  const handleGenerate = async () => {
    if (!topic.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);
    setCompletedStages([]);
    setStage("Script Generation");

    try {
      // Simulate stage progression for UI
      // Real pipeline runs on backend
      const stageDelay = (stageName, delay) =>
        new Promise((resolve) =>
          setTimeout(() => {
            setStage(stageName);
            resolve();
          }, delay)
        );

      // Start the actual API call
      const fetchPromise = fetch("http://localhost:5000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic, genre }),
      });

      // Update UI stages while backend works
      await stageDelay("Script Generation", 0);
      await stageDelay("Storyboard", 8000);
      setCompletedStages([1]);
      await stageDelay("Video Generation", 5000);
      setCompletedStages([1, 2]);
      await stageDelay("Assembly", 60000);
      setCompletedStages([1, 2, 3]);

      // Wait for actual response
      const response = await fetchPromise;
      const data = await response.json();

      if (data.success) {
        setCompletedStages([1, 2, 3, 4]);
        setResult(data);
        setStage("Complete");
      } else {
        setError(data.error || "Something went wrong");
      }
    } catch (err) {
      setError("Could not connect to backend. Make sure Flask is running.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setTopic("");
    setResult(null);
    setError(null);
    setStage("");
    setCompletedStages([]);
    setShowPipeline(false);
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-inner">
          <div className="logo">
            <span className="logo-icon">🎬</span>
            <span className="logo-text">ReelCraft</span>
          </div>
          <span className="logo-tag">AI Showrunner</span>
        </div>
      </header>

      <main className="main">
        {/* Hero */}
        {!result && (
          <div className="hero">
            <h1 className="hero-title">
              From idea to short drama
              <br />
              <span className="hero-accent">in minutes.</span>
            </h1>
            <p className="hero-sub">
              Powered by Qwen + Wan AI on Alibaba Cloud.
              Type a topic, get a fully produced short drama.
            </p>
          </div>
        )}

        {/* Input Section */}
        {!result && (
          <div className="input-card">
            <div className="input-group">
              <label className="input-label">What's your drama about?</label>
              <textarea
                className="input-textarea"
                placeholder="e.g. A girl discovers her boyfriend has a secret family..."
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                disabled={loading}
                rows={3}
              />
            </div>

            <div className="input-group">
              <label className="input-label">Genre</label>
              <select
                className="input-select"
                value={genre}
                onChange={(e) => setGenre(e.target.value)}
                disabled={loading}
              >
                <option value="drama">Drama</option>
                <option value="romance">Romance</option>
                <option value="thriller">Thriller</option>
                <option value="comedy">Comedy</option>
              </select>
            </div>

            <button
              className="btn-generate"
              onClick={handleGenerate}
              disabled={loading || !topic.trim()}
            >
              {loading ? "Generating..." : "Generate Drama"}
            </button>

            {/* Pipeline Toggle */}
            <button
              className="btn-pipeline-toggle"
              onClick={() => setShowPipeline(!showPipeline)}
            >
              {showPipeline ? "Hide" : "Show"} pipeline view
            </button>
          </div>
        )}

        {/* Pipeline View */}
        {showPipeline && loading && (
          <div className="pipeline-card">
            <h3 className="pipeline-title">Agent Pipeline</h3>
            <div className="pipeline-stages">
              {stages.map((s) => {
                const isComplete = completedStages.includes(s.id);
                const isActive = stage === s.name;
                return (
                  <div
                    key={s.id}
                    className={`pipeline-stage ${
                      isComplete
                        ? "stage-complete"
                        : isActive
                        ? "stage-active"
                        : "stage-pending"
                    }`}
                  >
                    <div className="stage-indicator">
                      {isComplete ? "✓" : isActive ? "⟳" : s.id}
                    </div>
                    <div className="stage-info">
                      <div className="stage-name">{s.name}</div>
                      <div className="stage-desc">
                        {isActive ? s.desc : isComplete ? "Done" : "Waiting"}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="error-card">
            <p className="error-text">⚠ {error}</p>
          </div>
        )}

        {/* Result */}
        {result && (
          <div className="result-section">
            <div className="result-header">
              <h2 className="result-title">Your Drama is Ready</h2>
              <button className="btn-reset" onClick={handleReset}>
                Create Another
              </button>
            </div>

            {/* Video Player */}
            <div className="video-card">
              <video
                className="video-player"
                controls
                src={`http://localhost:5000${result.video_url}`}
              />
            </div>

            {/* Script */}
            <div className="script-card">
              <h3 className="script-title">Generated Script</h3>
              <pre className="script-text">{result.script}</pre>
            </div>

            {/* Storyboard */}
            <div className="storyboard-card">
              <h3 className="storyboard-title">
                Storyboard — {result.scenes_count} Scenes
              </h3>
              {result.storyboard.map((scene, i) => (
                <div key={i} className="storyboard-scene">
                  <span className="scene-number">Scene {i + 1}</span>
                  <p className="scene-prompt">{scene}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="footer">
        <p>Built on Alibaba Cloud · Qwen + Wan AI · Track 2: AI Showrunner</p>
      </footer>
    </div>
  );
}

export default App;