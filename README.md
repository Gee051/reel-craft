## 🎬 ReelCraft — AI Showrunner

> Autonomously transforms a topic into a fully produced short drama —
> from scriptwriting to video generation — powered by Qwen + Wan AI
> on Alibaba Cloud.

---

## 🏆 Hackathon

**Global AI Hackathon Series with Qwen Cloud**
**Track 2: AI Showrunner**
Built with Qwen Cloud · Alibaba Cloud · Wan AI

---

## 🎯 What It Does

ReelCraft is an end-to-end AI Showrunner agent that takes a single
topic from a user and autonomously runs a four-stage pipeline to
produce a finished short drama video.

**User types a topic → ReelCraft produces a short drama video.**

No manual steps. No editing required. Fully autonomous.

---

## 🔄 Pipeline
User Input (topic + genre)

↓

[Stage 1] Script Agent — Qwen

Generates a full short drama script

using professional craft rules

↓

[Stage 2] Storyboard Agent — Qwen

Converts each scene into precise

visual descriptions optimized for Wan

↓

[Stage 3] Video Agent — Wan AI

Generates one video clip per scene

via Alibaba Cloud DashScope API

↓

[Stage 4] Assembly Agent — MoviePy

Stitches all clips into one

finished short drama video

↓

Final Video Output

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Text Model | Qwen (via Alibaba Cloud DashScope) |
| AI Video Model | Wan / wanx2.1-t2v-plus |
| Backend | Python + Flask |
| Frontend | React.js |
| Video Assembly | MoviePy |
| Cloud | Alibaba Cloud |
| API Protocol | OpenAI-compatible + DashScope SDK |

---

## 📁 Project Structure
reel-craft/

├── backend/

│   ├── agents/

│   │   ├── script_agent.py       # Qwen script generation

│   │   ├── storyboard_agent.py   # Scene visual descriptions

│   │   ├── video_agent.py        # Wan video generation

│   │   └── assembly_agent.py     # MoviePy clip assembly

│   ├── app.py                    # Flask API server

│   ├── config.py                 # Configuration + API settings

│   └── requirements.txt          # Python dependencies

├── frontend/

│   └── src/

│       ├── App.js                # Main React UI

│       └── App.css               # Styling

├── architecture.png              # System architecture diagram

├── LICENSE                       # MIT License

└── README.md

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Alibaba Cloud account with DashScope API key

### 1. Clone the repository
```bash
git clone https://github.com/Gee051/reel-craft.git
cd reel-craft
```

### 2. Set up the backend
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

cd backend
pip install -r requirements.txt
```

### 3. Add your API key
Create a `.env` file inside the `backend` folder:
DASHSCOPE_API_KEY=your_api_key_here

Get your API key from:
**https://home.qwencloud.com**

### 4. Run the backend
```bash
cd backend
python app.py
```
Backend runs at: `http://localhost:5000`

### 5. Run the frontend
```bash
cd frontend
npm install
npm start
```
Frontend runs at: `http://localhost:3000`

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check — confirms Alibaba Cloud backend |
| POST | `/generate` | Full pipeline — script → storyboard → video → assembly |
| POST | `/generate/script` | Script generation only |
| POST | `/generate/storyboard` | Script + storyboard only |

### Example Request
```json
POST /generate
{
  "topic": "a girl discovers her boyfriend has a secret family",
  "genre": "drama"
}
```

### Example Response
```json
{
  "success": true,
  "topic": "a girl discovers her boyfriend has a secret family",
  "genre": "drama",
  "script": "SCENE 1:\n...",
  "storyboard": ["Close up shot of...", "Wide shot of..."],
  "video_url": "/output/final_video.mp4",
  "scenes_count": 4
}
```

---

## ☁️ Alibaba Cloud Deployment

Backend is deployed on Alibaba Cloud ECS.
API calls are made to Alibaba Cloud DashScope:
- Text generation: `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
- Video generation: `https://dashscope-intl.aliyuncs.com/api/v1`

---

## 🏗 Architecture

See `architecture.png` for the full system diagram.

---

## 📝 License

MIT License — see LICENSE file for details.

---

## 👤 Author

Built for the Global AI Hackathon Series with Qwen Cloud
Track 2: AI Showrunner
Save the file then push:
bashgit add .
git commit -m "docs: add full README documentation"
git push origin main
Tell me when pushed and we move to building the architecture diagram — which is the last thing we can complete before the API key arrives.You said: drop everything in one file so i can just copy and paste it in readme file so it will be oncedrop everything in one file so i can just copy and paste it in readme file so it will be once8:39 PMClaude responded: Here's the complete README — copy everything between the lines:Here's the complete README — copy everything between the lines:

markdown# 🎬 ReelCraft — AI Showrunner

> Autonomously transforms a topic into a fully produced short drama — from scriptwriting to video generation — powered by Qwen + Wan AI on Alibaba Cloud.

---

## 🏆 Hackathon

**Global AI Hackathon Series with Qwen Cloud**  
**Track 2: AI Showrunner**  
Built with Qwen Cloud · Alibaba Cloud · Wan AI

---

## 🎯 What It Does

ReelCraft is an end-to-end AI Showrunner agent that takes a single topic from a user and autonomously runs a four-stage pipeline to produce a finished short drama video.

**User types a topic → ReelCraft produces a short drama video.**

No manual steps. No editing required. Fully autonomous.

---

## 🔄 Pipeline
User Input (topic + genre)

↓

[Stage 1] Script Agent — Qwen

Generates a full short drama script

using professional craft rules

↓

[Stage 2] Storyboard Agent — Qwen

Converts each scene into precise

visual descriptions optimized for Wan

↓

[Stage 3] Video Agent — Wan AI

Generates one video clip per scene

via Alibaba Cloud DashScope API

↓

[Stage 4] Assembly Agent — MoviePy

Stitches all clips into one

finished short drama video

↓

Final Video Output

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Text Model | Qwen (via Alibaba Cloud DashScope) |
| AI Video Model | Wan / wanx2.1-t2v-plus |
| Backend | Python + Flask |
| Frontend | React.js |
| Video Assembly | MoviePy |
| Cloud | Alibaba Cloud |
| API Protocol | OpenAI-compatible + DashScope SDK |

---

## 📁 Project Structure
reel-craft/

├── backend/

│   ├── agents/

│   │   ├── script_agent.py       # Qwen script generation

│   │   ├── storyboard_agent.py   # Scene visual descriptions

│   │   ├── video_agent.py        # Wan video generation

│   │   └── assembly_agent.py     # MoviePy clip assembly

│   ├── app.py                    # Flask API server

│   ├── config.py                 # Configuration + API settings

│   └── requirements.txt          # Python dependencies

├── frontend/

│   └── src/

│       ├── App.js                # Main React UI

│       └── App.css               # Styling

├── architecture.png              # System architecture diagram

├── LICENSE                       # MIT License

└── README.md

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Alibaba Cloud account with DashScope API key

### 1. Clone the repository
```bash
git clone https://github.com/Gee051/reel-craft.git
cd reel-craft
```

### 2. Set up the backend
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

cd backend
pip install -r requirements.txt
```

### 3. Add your API key
Create a `.env` file inside the `backend` folder:
DASHSCOPE_API_KEY=your_api_key_here

Get your API key from: **https://home.qwencloud.com**

### 4. Run the backend
```bash
cd backend
python app.py
```
Backend runs at: `http://localhost:5000`

### 5. Run the frontend
```bash
cd frontend
npm install
npm start
```
Frontend runs at: `http://localhost:3000`

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check — confirms Alibaba Cloud backend |
| POST | `/generate` | Full pipeline — script → storyboard → video → assembly |
| POST | `/generate/script` | Script generation only |
| POST | `/generate/storyboard` | Script + storyboard only |

### Example Request
```json
POST /generate
{
  "topic": "a girl discovers her boyfriend has a secret family",
  "genre": "drama"
}
```

### Example Response
```json
{
  "success": true,
  "topic": "a girl discovers her boyfriend has a secret family",
  "genre": "drama",
  "script": "SCENE 1:\n...",
  "storyboard": ["Close up shot of...", "Wide shot of..."],
  "video_url": "/output/final_video.mp4",
  "scenes_count": 4
}
```

---

## ☁️ Alibaba Cloud Deployment

Backend is deployed on Alibaba Cloud ECS.  
API calls are made to Alibaba Cloud DashScope:
- Text generation: `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
- Video generation: `https://dashscope-intl.aliyuncs.com/api/v1`

---

## 🏗 Architecture

See `realcraft_architecture.png` for the full system diagram.

---

## 📝 License

MIT License — see LICENSE file for details.

---

## 👤 Author
Name : OG

Built for the Global AI Hackathon Series with Qwen Cloud  

Track 2: AI Showrunner
