# Tetris Game - GitHub Instructions

## Project Overview


**Timeline**: Complete today

---
applyTo: "**"
---

## Table of Contents

1. [Architecture](#architecture)
2. [Technology Stack](#technology-stack)
3. [Setup Instructions](#setup-instructions)
4. [Development Workflow](#development-workflow)
5. [Code Organization](#code-organization)
6. [Game Features](#game-features)
7. [Testing &amp; Deployment](#testing--deployment)

---

## Architecture

### Recommended Stack

- **Backend**: Python 3.12 + FastAPI (lightweight, fast WebSocket support)
- **Frontend**: Vanilla JavaScript + HTML5 Canvas (no build step needed)
- **Communication**: WebSockets for real-time multiplayer
- **Storage**: SQLite database (easiest setup)

### System Design

```
┌─────────────────┐
│   Web Browser   │
│  (JavaScript)   │
│  - Render Game  │
│  - Handle Input │
└────────┬────────┘
         │ WebSocket
         │
┌────────▼────────┐
│  FastAPI Server │
│  (Python 3.12)  │
│  - Game Logic   │
│  - Multiplayer  │
│  - Scoring      │
└────────┬────────┘
         │
┌────────▼────────┐
│  SQLite DB      │
│  - Leaderboard  │
│  - Player Data  │
└─────────────────┘
```

---

## Technology Stack

### Backend (Python)

- **FastAPI**: Modern web framework with WebSocket support
- **Pydantic**: Data validation
- **SQLAlchemy**: ORM for database
- **SQLite**: Embedded database (no separate server needed)

### Frontend (JavaScript)

- **HTML5 Canvas**: Game rendering
- **Vanilla JavaScript**: Game mechanics, input handling
- **WebSocket API**: Real-time communication
- **LocalStorage**: Browser-side score caching

### Dependencies

```
# Python requirements.txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
websockets==12.0
python-multipart==0.0.6
```

---

## Setup Instructions

### Prerequisites

- Python 3.12 installed
- Node.js or npm (optional, not required)
- Git

### Step 1: Clone & Initialize

```bash
git clone <repository-url>
cd tetris-game
```

### Step 2: Python Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Database Initialization

```bash
# Create database schema
python scripts/init_db.py
```

### Step 4: Start Backend Server

```bash
# Run FastAPI server (auto-reload enabled)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 5: Open Frontend

```
Open browser to: http://localhost:8000
(HTML served by FastAPI)
```

---

## Development Workflow

### Folder Structure

```
tetris-game/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry
│   ├── game/
│   │   ├── __init__.py
│   │   ├── logic.py            # Tetris game mechanics
│   │   ├── models.py           # Game state models
│   │   └── multiplayer.py      # Multiplayer logic
│   ├── db/
│   │   ├── __init__.py
│   │   ├── models.py           # SQLAlchemy models
│   │   └── crud.py             # Database operations
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py           # API endpoints
│   │   └── websockets.py       # WebSocket handlers
│   └── static/
│       ├── index.html          # Main game page
│       ├── css/
│       │   └── style.css       # Game styling
│       └── js/
│           ├── game.js         # Game logic
│           ├── renderer.js     # Canvas rendering
│           ├── input.js        # Keyboard/touch input
│           ├── audio.js        # Sound effects
│           └── multiplayer.js  # Multiplayer client
├── scripts/
│   ├── init_db.py              # Database initialization
│   └── seed_data.py            # Populate test data
├── tests/
│   ├── test_game_logic.py
│   ├── test_api.py
│   └── test_multiplayer.py
├── requirements.txt            # Python dependencies
├── .gitignore
├── README.md
└── github-instructions.md      # This file
```

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/game-mechanics

# Make changes and commit
git add .
git commit -m "Implement piece rotation and collision detection"

# Push and create PR
git push origin feature/game-mechanics
```

---

## Game Features

### 1. Core Mechanics

- [X] 7 Tetromino pieces (I, O, T, S, Z, J, L)
- [X] Grid-based movement (left, right, down, rotate)
- [X] Collision detection
- [X] Line clearing with animation
- [X] Game over detection

### 2. Scoring System

- Points for line clears (100 points per line)
- Bonus for multiple lines (Tetris = 400 points)
- Difficulty increases with score

### 3. Game Modes

- **Classic**: Single player, increasing difficulty
- **Multiplayer**: Real-time vs other players
- **Time Attack**: Clear as many lines as possible in 2 minutes

### 4. Visual Features

- Smooth animations
- Next piece preview
- Hold piece (store one piece)
- Ghost piece (shows where piece will land)

### 5. Audio

- Background music (looped, volume control)
- Line clear sound effect
- Game over sound

### 6. Leaderboard

- Top 10 high scores (stored in database)
- Player name, score, date
- Display on game over screen

---

## Code Guidelines

### Python Code Style

- Use PEP 8 (checked with `flake8`)
- Type hints for all functions
- Docstrings for classes and complex methods
- Maximum line length: 100 characters

### JavaScript Code Style

- Use ES6+ syntax
- Descriptive variable names (avoid single letters)
- Comments for complex logic
- Use `const` by default, `let` for mutations, avoid `var`

### Example: Game Logic Structure

```python
# app/game/logic.py
from typing import List, Tuple
from app.game.models import GameState, Piece

class TetrisGame:
    """Manages Tetris game state and logic"""
  
    def __init__(self):
        self.grid = [[0 for _ in range(10)] for _ in range(20)]
        self.current_piece = None
        self.score = 0
  
    def move_piece(self, direction: str) -> bool:
        """Move current piece left/right/down"""
        pass
  
    def rotate_piece(self) -> bool:
        """Rotate current piece 90 degrees"""
        pass
  
    def check_collision(self, piece: Piece) -> bool:
        """Check if piece collides with walls/grid"""
        pass
  
    def clear_lines(self) -> int:
        """Clear completed lines, return count"""
        pass
```

---

## API Endpoints

### REST Endpoints

```
GET  /                      # Serve game page
GET  /api/leaderboard       # Get top 10 scores
POST /api/scores            # Submit new score
GET  /api/game-state        # Get current game state
```

### WebSocket Endpoints

```
WS /ws/game/{player_id}     # Single player game
WS /ws/multiplayer/{room_id} # Multiplayer game
```

---

## Testing & Validation

### Run Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_game_logic.py

# With coverage
pytest --cov=app tests/
```

### Manual Testing Checklist

- [ ] Pieces spawn and fall correctly
- [ ] Left/right movement works
- [ ] Rotation works without clipping
- [ ] Collision detection works (walls, floor, other pieces)
- [ ] Lines clear when filled
- [ ] Score updates correctly
- [ ] Game over triggers at right time
- [ ] Multiplayer sync is smooth
- [ ] Leaderboard displays correctly
- [ ] Sound plays without lag
- [ ] Mobile/touch input works (if applicable)

### Browser Compatibility

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)

---

## Deployment

### Local Development

```bash
# Terminal 1: Start backend
uvicorn app.main:app --reload

# Terminal 2: Open browser
# http://localhost:8000
```

### Production (Render, Heroku, etc.)

1. Add `Procfile`:

   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
2. Deploy:

   ```bash
   git push heroku main
   ```

---

## Contributing Guidelines

### Before Submitting Code

1. Follow code style guidelines (PEP 8 for Python, ES6 for JS)
2. Write tests for new features
3. Run all tests: `pytest`
4. Update README if needed
5. Ensure no console errors in browser DevTools

### Commit Message Format

```
[Feature/Fix/Refactor] Brief description

- Detailed explanation of changes
- Any breaking changes
- Related issue/feature number
```

---

## Troubleshooting

### Backend Won't Start

```bash
# Check Python version
python --version  # Should be 3.12.x

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check port 8000 isn't in use
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows
```

### Game Doesn't Render

```bash
# Check browser console for errors (F12)
# Verify WebSocket connection in Network tab
# Check server logs for errors
```

### Database Errors

```bash
# Reset database
rm database.db
python scripts/init_db.py
```

---

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [HTML5 Canvas](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)

---

## Questions or Issues?

Open a GitHub issue or check the troubleshooting section above.

**Let's build Tetris! 🎮**
