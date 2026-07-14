import { useState } from "react";
import { FiFilm } from "react-icons/fi";
import "./App.css";

const API = "http://47.236.205.58:5000";

function App() {
  const [topic, setTopic] = useState("");
  const [genre, setGenre] = useState("drama");
  const [loading, setLoading] = useState(false);
  const [loadingMsg, setLoadingMsg] = useState("");
  const [error, setError] = useState(null);
  const [demoMode, setDemoMode] = useState(false);

  // preview = free text output (enriched + script) before spending video quota
  const [preview, setPreview] = useState(null);
  const [editedScript, setEditedScript] = useState("");

  // parts = each produced video (Part 1, Part 2, ...)
  const [parts, setParts] = useState([]);

  // continuation input
  const [continuing, setContinuing] = useState(false);
  const [continueText, setContinueText] = useState("");

  // STEP 1 — free: enrich + script + storyboard, no video
  const handleGenerateScript = async () => {
    if (!topic.trim()) return;
    setLoading(true);
    setLoadingMsg("Writing your script...");
    setError(null);
    setPreview(null);
    try {
      const res = await fetch(`${API}/generate/preview`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic, genre }),
      });
      const data = await res.json();
      if (data.success) {
        setPreview(data);
        setEditedScript(data.script);
      } else {
        setError(data.error || "Something went wrong");
      }
    } catch {
      setError("Could not connect to backend. Make sure Flask is running.");
    } finally {
      setLoading(false);
    }
  };

  // STEP 2 — produce video from the (possibly edited) script
  const handleProduce = async () => {
    setLoading(true);
    setLoadingMsg("Producing your film. This takes a few minutes...");
    setError(null);

    const isContinuation = preview?.isContinuation;
    const endpoint = isContinuation
      ? `${API}/generate/from-script-video`
      : `${API}/generate`;
    const body = isContinuation
      ? { script: editedScript, bible: preview.bible }
      : { topic, genre, script: editedScript };

    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await res.json();
      if (data.success) {
        setParts((prev) => [
          ...prev,
          {
            label: `Part ${prev.length + 1}`,
            video_url: data.video_url,
            script: editedScript,
            enriched: data.enriched_prompt || preview?.enriched_prompt,
            vibe: data.vibe || preview?.vibe,
            bible: data.bible || preview?.bible,
            topic: preview?.topic || topic,
            storyboard: data.storyboard,
          },
        ]);
        setPreview(null);
        setContinuing(false);
        setContinueText("");
      } else {
        setError(data.error || "Video generation failed");
      }
    } catch {
      setError("Could not reach backend during video production.");
    } finally {
      setLoading(false);
    }
  };

  // CONTINUATION — build next part's script from user's added text, reuse bible
  const handleContinueScript = async () => {
    if (!continueText.trim()) return;
    const lastPart = parts[parts.length - 1];
    setLoading(true);
    setLoadingMsg("Writing the next part...");
    setError(null);
    try {
      const res = await fetch(`${API}/generate/from-script`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ script: continueText, bible: lastPart.bible }),
      });
      const data = await res.json();
      if (data.success) {
        setPreview({ ...data, isContinuation: true, bible: lastPart.bible });
        setEditedScript(continueText);
      } else {
        setError(data.error || "Could not build continuation");
      }
    } catch {
      setError("Could not reach backend.");
    } finally {
      setLoading(false);
    }
  };

  const handleNewStory = () => {
    setTopic("");
    setPreview(null);
    setParts([]);
    setError(null);
    setContinuing(false);
    setContinueText("");
    setEditedScript("");
  };

  const showInput = parts.length === 0 && !preview && !loading;

  return (
    <div className="app">
      <header className="header">
        <div className="header-inner">
          <div className="logo">
            <span className="logo-icon"><FiFilm /></span>
            <span className="logo-text">ReelCraft</span>
          </div>
          <div className="header-right">
            <label className="demo-switch">
              <input
                type="checkbox"
                checked={demoMode}
                onChange={(e) => setDemoMode(e.target.checked)}
              />
              <span>Demo mode</span>
            </label>
            <span className="logo-tag">AI Showrunner</span>
          </div>
        </div>
      </header>

      <main className="main">
        {/* Hero + input */}
        {showInput && (
          <>
            <div className="hero">
              <h1 className="hero-title">
                Type a few words.
                <br />
                <span className="hero-accent">Get a directed film.</span>
              </h1>
              <p className="hero-sub">
                ReelCraft rewrites your idea into cinematic direction, then
                produces it with Qwen + Wan AI on Alibaba Cloud.
              </p>
            </div>

            <div className="input-card">
              <div className="input-group">
                <label className="input-label">What do you want to see?</label>
                <textarea
                  className="input-textarea"
                  placeholder="e.g. a girl walking down the aisle"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  rows={3}
                />
              </div>

              <div className="input-group">
                <label className="input-label">Genre hint (optional)</label>
                <select
                  className="input-select"
                  value={genre}
                  onChange={(e) => setGenre(e.target.value)}
                >
                  <option value="drama">Drama</option>
                  <option value="romance">Romance</option>
                  <option value="thriller">Thriller</option>
                  <option value="comedy">Comedy</option>
                </select>
              </div>

              <button
                className="btn-generate"
                onClick={handleGenerateScript}
                disabled={!topic.trim()}
              >
                Generate script
              </button>
            </div>
          </>
        )}

        {/* Loading */}
        {loading && (
          <div className="loading-card">
            <div className="loading-spinner" />
            <p className="loading-text">{loadingMsg}</p>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="error-card">
            <p className="error-text">⚠ {error}</p>
          </div>
        )}

        {/* Script preview — editable, before spending video quota */}
        {preview && !loading && (
          <div className="result-section">
            <div className="result-header">
              <h2 className="result-title">
                {preview.isContinuation ? "Next part — review the script" : "Review your script"}
              </h2>
              {preview.vibe && <span className="vibe-badge">{preview.vibe}</span>}
            </div>

            {demoMode && preview.enriched_prompt && (
              <div className="transform-card">
                <span className="transform-label">Cinematic prompt (enriched)</span>
                <p className="transform-rich">{preview.enriched_prompt}</p>
              </div>
            )}

            <div className="script-card">
              <label className="input-label">Script — edit freely before producing</label>
              <textarea
                className="script-editor"
                value={editedScript}
                onChange={(e) => setEditedScript(e.target.value)}
                rows={14}
              />
            </div>

            <div className="preview-actions">
              <button className="btn-generate" onClick={handleProduce}>
                Produce video
              </button>
              <button className="btn-reset" onClick={handleNewStory}>
                Cancel
              </button>
            </div>
          </div>
        )}

        {/* Produced parts */}
        {parts.length > 0 && !preview && !loading && (
          <div className="result-section">
            <div className="result-header">
              <h2 className="result-title">Your film</h2>
              <button className="btn-reset" onClick={handleNewStory}>
                Create another story
              </button>
            </div>

            {parts.map((part, i) => (
              <div key={i} className="part-block">
                <div className="part-label">{part.label}</div>
                <div className="video-card">
                  <video className="video-player" controls src={`${API}${part.video_url}`} />
                </div>
                <a className="btn-download" href={`${API}${part.video_url}`} download>
                  Download {part.label}
                </a>

                {demoMode && (
                  <div className="demo-section">
                    {part.enriched && (
                      <div className="transform-card">
                        <span className="transform-label">Enriched prompt</span>
                        <p className="transform-rich">{part.enriched}</p>
                      </div>
                    )}
                    <div className="script-card">
                      <h3 className="section-title">Script</h3>
                      <pre className="script-text">{part.script}</pre>
                    </div>
                  </div>
                )}
              </div>
            ))}

            {/* Continue the story */}
            {!continuing && (
              <button className="btn-continue" onClick={() => setContinuing(true)}>
                + Continue the story
              </button>
            )}

            {continuing && (
              <div className="input-card">
                <label className="input-label">
                  What happens next? (same character continues)
                </label>
                <textarea
                  className="input-textarea"
                  placeholder="e.g. she reaches the altar and turns to face the crowd"
                  value={continueText}
                  onChange={(e) => setContinueText(e.target.value)}
                  rows={3}
                />
                <div className="preview-actions">
                  <button
                    className="btn-generate"
                    onClick={handleContinueScript}
                    disabled={!continueText.trim()}
                  >
                    Write next part
                  </button>
                  <button className="btn-reset" onClick={() => setContinuing(false)}>
                    Cancel
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </main>

      <footer className="footer">
        <p>Built on Alibaba Cloud · Qwen + Wan AI · Track 2: AI Showrunner</p>
      </footer>
    </div>
  );
}

export default App;