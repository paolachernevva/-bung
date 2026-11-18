# Balloon Feature - Quick Start Guide

## What was added?

Your Tetris game now has a celebration feature where **15 colorful balloons appear and pop** when the player wins! Players can click balloons to pop them with particle effects.

## Files Created

```
app/
├── game/
│   └── balloons.py                    # Backend balloon logic
└── static/js/
    ├── balloons.js                    # Frontend animation system
    ├── balloons-integration-example.js # Integration example
    └── (index.html, style.css updated when needed)

tests/
└── test_balloons.py                   # 21 unit tests (all passing ✓)

BALLOON_FEATURE.md                      # Complete feature documentation
BALLOON_QUICKSTART.md                   # This file
```

## How to Use

### 1. Add to Your Game (Backend)

In your game logic when the player wins:

```python
from app.game.balloons import BalloonManager, BalloonConfig

# In your game finish handler:
def on_game_won(game_state):
    # Create balloon manager with default settings
    # (15 balloons, colors from Tetris palette, click to pop)
    balloon_manager = BalloonManager()
    
    # Send to frontend
    balloon_data = balloon_manager.create_balloons(
        canvas_width=600,
        canvas_height=800
    )
    
    # Send state to client via WebSocket/API
    return balloon_manager.to_dict()
```

### 2. Add to Your Game (Frontend)

In your `game.js` or main game initialization:

```javascript
// 1. Create the balloon manager
const balloonManager = new BalloonManager(gameCanvas, colors);

// 2. When game is won, trigger balloons
function onGameWon() {
  balloonManager.createBalloons(15);
}

// 3. Handle balloon clicks
gameCanvas.addEventListener('click', (event) => {
  if (gameState === 'finished') {
    const rect = gameCanvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    balloonManager.checkBalloonClick(x, y);
  }
});

// 4. Clean up when game ends
window.addEventListener('beforeunload', () => {
  balloonManager.stop();
});
```

### 3. Customize Settings (Optional)

Change balloon behavior by passing a custom config:

```python
from app.game.balloons import BalloonConfig, PopSpeed, PopTrigger

config = BalloonConfig(
    count=20,                    # 20 balloons instead of 15
    pop_speed=PopSpeed.SLOW,     # Slower pop animation
    pop_trigger=PopTrigger.AUTO, # Auto-pop instead of click
    float_animation=True,        # Balloons float upward
)

manager = BalloonManager(config)
```

## Configuration Options

| Option | Values | Default | What it does |
|--------|--------|---------|--------------|
| `count` | 1-100 | 15 | Number of balloons |
| `pop_speed` | `FAST`, `MEDIUM`, `SLOW` | `MEDIUM` | Pop animation duration |
| `pop_trigger` | `CLICK`, `AUTO`, `BOTH` | `CLICK` | How balloons pop |
| `float_animation` | `True`, `False` | `True` | Balloons float up before popping |
| `colors` | Hex color list | Tetris palette | Balloon colors |

## Features

✅ **15 colorful balloons** - Uses standard Tetris piece colors  
✅ **Click to pop** - Players click balloons to pop them  
✅ **Particle effects** - Burst particles on pop  
✅ **Floating animation** - Balloons drift upward  
✅ **Sound integration** - Plays pop sound (if audio manager available)  
✅ **Touch support** - Works on mobile/touch devices  
✅ **Fully tested** - 21 unit tests, all passing  
✅ **Easy to integrate** - Simple 4-line setup in game.js  
✅ **Customizable** - Change count, colors, speed, trigger  

## Default Colors (Tetris Palette)

- 🔴 Red (#FF6B6B) - I-piece
- 🔵 Cyan (#4ECDC4) - T-piece  
- 🟦 Blue (#45B7D1) - J-piece
- 🟧 Orange (#FFA07A) - L-piece
- 🟨 Yellow (#FFD93D) - O-piece
- 🟩 Green (#6BCB77) - S-piece
- 🟪 Purple (#FF7FB3) - Z-piece

## Testing

All 21 tests pass:
```bash
pytest tests/test_balloons.py -v
```

Tests cover:
- Config creation and validation
- Balloon state management
- Multiple balloon creation
- Serialization to JSON
- Color distribution
- Velocity randomization

## Example: Full Win Screen Integration

See `app/static/js/balloons-integration-example.js` for a complete working example that shows:
- How to initialize BalloonManager
- How to handle clicks
- How to trigger on win
- How to show a win screen
- How to integrate with multiplayer

## Troubleshooting

**Q: Balloons not appearing?**
A: Make sure you're calling `balloonManager.createBalloons(15)` after the game is won.

**Q: No pop sound?**
A: Sound only plays if `window.audioManager.playPopSound` exists. It's optional.

**Q: Performance issues?**
A: Try reducing `count` to 10, or disable `float_animation` for instant popping.

**Q: How to run tests?**
A: `pytest tests/test_balloons.py -v`

## What's Next?

You can enhance the feature by:
1. Adding confetti particles in addition to balloons
2. Playing celebration sounds
3. Tracking stats (balloons popped, etc.)
4. Creating special effects for multiplayer wins
5. Adding difficulty-based celebration intensity

## Documentation

- **Full documentation**: See `BALLOON_FEATURE.md`
- **Integration example**: See `app/static/js/balloons-integration-example.js`
- **Backend API**: See docstrings in `app/game/balloons.py`
- **Frontend API**: See docstrings in `app/static/js/balloons.js`

---

**Status**: ✅ Ready to integrate into your game!

Questions? Check BALLOON_FEATURE.md for detailed documentation.
