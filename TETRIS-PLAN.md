# Tetris Game - Simple & Detailed Implementation Plan

## What is Tetris? (For Beginners)

**Tetris is a game where:**
1. **Colored blocks fall** from the top of the screen one at a time
2. **You move and rotate** each block using keyboard arrow keys
3. **Goal**: Stack blocks to create complete horizontal rows
4. **Completed rows disappear** and you earn points
5. **Game ends** when stacked blocks reach the top

### Visual Example of Tetris:
```
GAME GRID (10 blocks wide, 20 blocks tall)

Top (Blocks spawn here)
│  ┌──────────────┐
│  │      ██      │  ← Current falling block (can move left/right/rotate)
│  │     ████     │  ← Previous blocks that have fallen
│  │   ██  ██     │
│  │   ██████████ │  ← FULL ROW! Will disappear and score +100 points
│  └──────────────┘
  Bottom

KEYBOARD CONTROLS:
← → = Move block left or right
↑   = Rotate block (spin it)
↓   = Make block fall faster
SPACE = Drop block all the way down
```

### The 7 Block Types (Tetrominoes):
Each made of 4 small squares, each has a different shape and color:
```
I-piece (Cyan)   O-piece (Yellow)   T-piece (Purple)   S-piece (Green)
  ████            ██                  ███                 ██
                  ██                   █                 ██

Z-piece (Red)    J-piece (Blue)     L-piece (Orange)
  ██               █                     █
  ██               ███                 ███
```

---

## How The Game Works (Step by Step)

### 1. Game Starts
- Empty 10×20 grid appears
- Score = 0, Level = 1
- Random block appears at top center

### 2. Block Falls
- Block automatically moves **down 1 row every 500 milliseconds** (adjusts with difficulty)
- Player can move it left/right with arrow keys
- Player can rotate it with up arrow

### 3. Block Hits Bottom or Other Blocks
- Block **stops moving** (gets "locked" to the grid)
- Next random block appears at top

### 4. Check for Completed Rows
- Game checks if any **complete rows** (all 10 blocks filled)
- If yes → rows **disappear**, blocks above fall down
- Points are awarded based on how many rows cleared

### 5. Game Over
- If a **new block can't fit** at the top (blocked by other blocks)
- Game stops, final score is saved

---

## File Structure (What We'll Create)

### Backend (Python) - Game Logic
```
app/
├── game/
│   ├── pieces.py          ← Define the 7 block types and their shapes
│   ├── logic.py           ← Main game mechanics (falling, moving, rotating, clearing)
│   ├── models.py          ← Data structures for game state
│   └── constants.py       ← Grid size, colors, scoring rules
├── api/
│   └── routes.py          ← Buttons players click (start game, send moves)
├── db/
│   └── models.py          ← Save high scores to database
└── main.py                ← Start the game server
```

### Frontend (JavaScript/HTML) - What Player Sees
```
app/static/
├── index.html             ← The game page
├── css/
│   └── style.css          ← Make it look nice (colors, layout)
└── js/
    ├── renderer.js        ← Draw blocks on screen
    ├── input.js           ← Listen for keyboard (arrow keys, space)
    └── game.js            ← Connect frontend to backend
```

### Tests (Verification)
```
tests/
├── test_game_logic.py     ← Test: does falling work?
├── test_collision.py      ← Test: does it stop at walls/bottom?
├── test_scoring.py        ← Test: are points calculated correctly?
└── test_api.py            ← Test: do game buttons work?
```

---

## 7 Phases - Build Step by Step

### Phase 1: Create Block Definitions (Files to create: pieces.py, constants.py)

**What to do**: Define what each block looks like

**Simple explanation**:
- Each block is made of 4 small squares arranged in a pattern
- Each block has a color
- Each block can rotate (turn) into 4 different positions
- We need to store all this information

**Code example**:
```python
# Define the I-block (cyan, four in a row)
I_BLOCK = {
    'shape_1': [[1,1,1,1]],           # Four blocks in a horizontal line
    'shape_2': [[1],[1],[1],[1]],    # Four blocks in a vertical line
    'color': '#00f0f0'               # Cyan color
}

# Define the O-block (yellow, 2×2 square)
O_BLOCK = {
    'shape': [[1,1],[1,1]],          # Always a square, doesn't rotate
    'color': '#f0f000'               # Yellow color
}

# Same for T, S, Z, J, L blocks...
```

**How to test it**:
```python
# Just check that blocks are defined correctly
test_i_block_exists()
test_i_block_has_color()
test_all_7_blocks_defined()
```

---

### Phase 2: Implement Falling & Collision (Files to edit: logic.py)

**What to do**: Make blocks fall down, detect when they hit walls/floor/other blocks

**Simple explanation**:
- **Falling**: Every 500ms, move block down 1 row
- **Collision**: Check if block would go outside the grid or hit another block
- **Lock**: When block can't fall anymore, freeze it in place

**How falling works**:
```
Tick 1: Block at row 0 → move to row 1
Tick 2: Block at row 1 → move to row 2
Tick 3: Block at row 2 → move to row 3
...
Tick 10: Block at row 9 → Check: Can it move to row 10?
         YES → move to row 10
Tick 11: Block at row 10 → Check: Can it move to row 11?
         NO (hits wall) → LOCK it here, spawn new block
```

**How collision works**:
```python
def can_move_down(block, grid):
    # Check: Would the block go outside the grid?
    if block.y + 1 >= 20:  # 20 is grid height
        return False  # Can't go down, hit floor
    
    # Check: Would the block overlap with locked blocks?
    for each_cell in block:
        if grid[block.y + 1][block.x] != empty:
            return False  # Can't go down, hit another block
    
    return True  # Safe to move down
```

**How to test it**:
```python
test_block_falls_every_tick()
test_block_stops_at_floor()
test_block_stops_at_other_blocks()
test_block_stops_at_walls()
```

---

### Phase 3: Implement Movement & Rotation (Files to edit: logic.py)

**What to do**: Let player move blocks left/right and rotate them

**Simple explanation - MOVEMENT**:
```
LEFT ARROW:  block.x -= 1  (move 1 space left)
RIGHT ARROW: block.x += 1  (move 1 space right)

BUT: Only if it doesn't hit a wall or another block
```

**Simple explanation - ROTATION**:
- Block rotates 90 degrees (turns clockwise)
- Block has 4 possible rotations (shape 1, 2, 3, 4)
- When you press UP ARROW: rotation = (rotation + 1) % 4

**Example of rotation**:
```
Original:        Rotate 1:        Rotate 2:        Rotate 3:
  ███              █                 ███              ██
   █               ███                 █               █
                                                        █
```

**Wall Kick (special feature)**:
- If rotation would cause block to hit a wall, **shift the block** 1-2 spaces away first
- Then try rotation again
- This makes the game feel smoother

**How to test it**:
```python
test_move_left_works()
test_move_right_works()
test_cant_move_through_walls()
test_cant_move_through_other_blocks()
test_rotation_works()
test_rotation_has_wall_kick()
```

---

### Phase 4: Implement Line Clearing & Scoring (Files to edit: logic.py)

**What to do**: Remove completed rows and award points

**Simple explanation - LINE CLEARING**:
```
BEFORE:                    AFTER:
██████████  ← Full row!    (deleted)
█        █
██       █
         
         (empty row)       (from above)
```

**Algorithm**:
```
1. After block locks, scan each row
2. If a row has all 10 blocks filled → mark it for deletion
3. Delete those rows
4. All rows above shift down
5. Add empty rows at the top
```

**Simple explanation - SCORING**:
```
Points earned:
- Clear 1 row:     100 points
- Clear 2 rows:    300 points
- Clear 3 rows:    500 points
- Clear 4 rows:    800 points (called "TETRIS!")

Level increases every 500 points:
- Level 0:  500 points   → Game speed = normal
- Level 1: 1000 points   → Game speed = faster
- Level 2: 1500 points   → Game speed = even faster
```

**How to test it**:
```python
test_full_row_is_detected()
test_full_row_is_deleted()
test_rows_above_shift_down()
test_points_for_1_line()
test_points_for_4_lines()
test_level_increases()
test_game_gets_faster()
```

---

### Phase 5: Display Game on Screen (Files to create: renderer.js, input.js, index.html)

**What to do**: Draw the game grid and blocks on the browser screen, listen for keyboard

**Simple explanation - RENDERING (drawing)**:
- Use HTML5 Canvas (a rectangular area where we can draw pixels)
- Draw 10×20 grid of squares
- For each block in the grid, fill its square with its color
- Draw the falling block on top

**Example HTML canvas code**:
```javascript
// Create a canvas: 300px wide, 600px tall
<canvas id="gameCanvas" width="300" height="600"></canvas>

// Draw it
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Draw the grid background
ctx.fillStyle = 'black';
ctx.fillRect(0, 0, 300, 600);

// Draw each block
for (each block in grid):
    ctx.fillStyle = block.color
    ctx.fillRect(block.x, block.y, block.width, block.height)
```

**Simple explanation - INPUT (keyboard)**:
```javascript
// Listen for arrow key presses
document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft') {
        game.moveLeft()
    }
    if (event.key === 'ArrowRight') {
        game.moveRight()
    }
    if (event.key === 'ArrowUp') {
        game.rotate()
    }
    if (event.key === ' ') {
        game.dropDown()
    }
});
```

**Display on screen**:
```
┌─────────────────────┐
│   TETRIS GAME       │
├─────────────────────┤
│                     │
│   [Game Grid]       │
│   with blocks       │
│                     │
├─────────────────────┤
│ Score: 1250         │
│ Level: 2            │
│ Lines: 5            │
└─────────────────────┘
```

**How to test it**:
```javascript
test_grid_draws_on_canvas()
test_blocks_appear_with_correct_colors()
test_arrow_left_moves_block()
test_arrow_right_moves_block()
test_arrow_up_rotates_block()
test_space_drops_block()
```

---

### Phase 6: Connect Frontend to Backend (Files to edit: routes.py, game.js)

**What to do**: Make browser talk to Python server

**Simple explanation**:
- Browser (JavaScript) can't do complex math, so it asks the **Python server**
- JavaScript sends: "Move block left, please!"
- Python server does the calculation: "OK, new grid is..."
- Python sends back: "Here's the new game state"
- JavaScript draws it on screen

**Network flow**:
```
Browser (JavaScript)              Server (Python)
     │                                  │
     │─── "Start Game" ────────────────>│
     │                                  │ Initializes game
     │<─── Grid, Score, Level ─────────│
     │                                  │
     │─── "Move Left" ───────────────────│
     │                                  │ Moves block
     │<─── New Grid ──────────────────│
     │                                  │
     │─── "Rotate" ───────────────────>│
     │                                  │ Rotates block
     │<─── New Grid ──────────────────│
```

**Simple REST API (Python)**:
```python
@app.post("/start")
def start_game():
    game = TetrisGame()
    return {"grid": game.grid, "score": 0, "level": 1}

@app.post("/move")
def move(direction):
    # direction = "left" or "right"
    game.move(direction)
    return {"grid": game.grid}

@app.post("/rotate")
def rotate():
    game.rotate()
    return {"grid": game.grid}

@app.get("/leaderboard")
def leaderboard():
    return top_10_scores()
```

**JavaScript connecting to it**:
```javascript
async function startGame() {
    const response = await fetch('/start', {method: 'POST'});
    const data = await response.json();
    renderGrid(data.grid);
    renderScore(data.score);
}

async function moveBlock(direction) {
    const response = await fetch('/move', {
        method: 'POST',
        body: JSON.stringify({direction: direction})
    });
    const data = await response.json();
    renderGrid(data.grid);
}
```

**How to test it**:
```python
test_start_game_endpoint()
test_move_endpoint()
test_rotate_endpoint()
test_leaderboard_endpoint()
```

---

### Phase 7: Testing & Sound (Files: tests/, audio.js)

**What to do**: Make sure everything works, add sound effects

**Testing checklist** (try these manually):
```
GAMEPLAY:
□ Block spawns at top center
□ Block falls smoothly
□ Left arrow moves block left
□ Right arrow moves block right
□ Up arrow rotates block
□ Space drops block to bottom
□ Block stops when hits floor
□ Block stops when hits other block
□ Row with 10 blocks disappears
□ Score increases when row clears
□ Game gets faster with each level
□ Game over when blocks reach top

VISUAL:
□ Grid background is visible
□ Blocks have correct colors
□ Next block preview shows
□ Score/Level display updates
□ No lag or stuttering

SOUND:
□ Background music plays
□ Line clear sound plays
□ Game over sound plays
□ Volume control works
```

**Add sound effects**:
```javascript
// When line clears
playSound('lineclear.mp3');

// When game over
playSound('gameover.mp3');

// Background music looping
playBackgroundMusic('music.mp3');
```

---

## Testing Each Phase (How to Verify)

### Testing Phase 1 (Blocks defined):
```bash
pytest tests/test_blocks.py
# Output should say: "7 passed"
```

### Testing Phase 2 (Falling & collision):
```bash
pytest tests/test_falling.py
pytest tests/test_collision.py
# Output should say: "15 passed"
```

### Testing Phase 3 (Movement & rotation):
```bash
pytest tests/test_movement.py
pytest tests/test_rotation.py
# Output should say: "20 passed"
```

### Testing Phase 4 (Clearing & scoring):
```bash
pytest tests/test_clearing.py
pytest tests/test_scoring.py
# Output should say: "15 passed"
```

### Testing Phase 5-6 (Display & API):
1. Open browser: http://localhost:8000
2. Manual testing (see checklist above)
3. Try all keyboard controls
4. Watch the game run

### Testing Phase 7 (Full game):
- Play several games
- Check if score saves
- Check leaderboard

---

## Summary: Implementation Order

**Week 1:**
1. ✓ Create block definitions (Phase 1)
2. ✓ Implement falling & collision (Phase 2)

**Week 2:**
3. ✓ Implement movement & rotation (Phase 3)
4. ✓ Line clearing & scoring (Phase 4)

**Week 3:**
5. ✓ Game display on screen (Phase 5)
6. ✓ Connect front & back (Phase 6)

**Week 4:**
7. ✓ Testing & sound (Phase 7)
8. ✓ Deploy to internet

---

## Key Concepts Explained Simply

### Falling
Blocks **automatically move down** at a fixed speed. The speed increases as your score goes up, making the game harder.

### Collision Detection
Before moving a block, we **check if it would hit a wall or another block**. If yes, we **don't allow the move**.

### Line Clearing
When a row is **completely filled**, we **delete it** and shift everything above down. The player gets points.

### Scoring
You get **more points** for clearing multiple rows at once. The **level increases** every 500 points, making blocks fall faster.

### Database
The **top 10 high scores** are saved in a simple SQLite database so they persist even after closing the browser.

---

## Common Questions Answered

**Q: Why Python for backend?**
A: Python is great for game logic and runs on servers. JavaScript is for displaying it.

**Q: What's the difference between frontend and backend?**
A: Frontend = what the player sees (browser). Backend = calculations (server).

**Q: Why SQLite for scores?**
A: It's simple, doesn't require a separate database server, and stores data in one file.

**Q: Can I add multiplayer later?**
A: Yes! We'll use WebSocket so two players can play at the same time.

**Q: How fast should blocks fall?**
A: Start at 500ms per row, then get faster. After 500 points, blocks fall every 450ms, then 400ms, etc.
