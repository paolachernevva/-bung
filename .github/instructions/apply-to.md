# Apply To - Implementation Mapping

This document maps each instruction file to the implementation files where they should be applied during development.

---

## 1. Colors Palette → Apply To
**File**: `.github/instructions/1-colors-palette.md`

### Implementation Files:
- **`app/static/js/renderer.js`** ← Use block colors when drawing pieces
  ```javascript
  const BLOCK_COLORS = {
      'I': '#00F0F0',  // From 1-colors-palette.md
      'O': '#F0F000',
      // etc...
  };
  ```

- **`app/static/css/style.css`** ← Use UI colors for backgrounds and text
  ```css
  body {
      background-color: #1a1a1a;  /* From 1-colors-palette.md */
      color: #FFFFFF;
  }
  ```

- **`app/static/index.html`** ← Apply color scheme to HTML elements
  ```html
  <div id="gameContainer" style="background: #1a1a1a;">
      <!-- Game grid here -->
  </div>
  ```

- **`app/game/models.py`** ← Define color constants in backend (Python)
  ```python
  BLOCK_COLORS = {
      'I': '#00F0F0',  # From 1-colors-palette.md
      'O': '#F0F000',
      # etc...
  }
  ```

---

## 2. Visual Layout & Grid Dimensions → Apply To
**File**: `.github/instructions/2-visual-layout.md`

### Implementation Files:
- **`app/static/index.html`** ← Set up canvas and container sizes
  ```html
  <canvas id="gameCanvas" width="300" height="600"></canvas>
  <!-- 300×600px from 2-visual-layout.md -->
  ```

- **`app/static/css/style.css`** ← Apply spacing, padding, responsive breakpoints
  ```css
  #gameCanvas {
      width: 300px;      /* From 2-visual-layout.md */
      height: 600px;
      margin: 20px;      /* Grid margin from instructions */
  }

  @media (max-width: 500px) {
      /* Mobile layout from 2-visual-layout.md */
      #gameContainer { ... }
  }
  ```

- **`app/static/js/renderer.js`** ← Use cell size for drawing
  ```javascript
  const CELL_SIZE = 30;  // From 2-visual-layout.md
  const GRID_WIDTH = 10;
  const GRID_HEIGHT = 20;
  ```

- **`app/static/js/game.js`** ← Use grid dimensions in game logic
  ```javascript
  const GRID = {
      width: 10,    // From 2-visual-layout.md
      height: 20,
      cellSize: 30
  };
  ```

---

## 3. Animations & Visual Effects → Apply To
**File**: `.github/instructions/3-animations-effects.md`

### Implementation Files:
- **`app/static/js/renderer.js`** ← Implement falling, rotation, game-over animations
  ```javascript
  // Block falling animation (50ms per row from 3-animations-effects.md)
  animateFall() {
      // duration = 50ms per row
  }

  // Ghost piece (30% opacity from 3-animations-effects.md)
  drawGhostPiece(piece) {
      ctx.globalAlpha = 0.3;
  }
  ```

- **`app/static/css/style.css`** ← CSS animations and transitions
  ```css
  @keyframes lineClear {
      0% { opacity: 1; background: white; }
      50% { opacity: 0.5; background: black; }
      100% { opacity: 0; }
  }

  .line-clearing {
      animation: lineClear 900ms;  /* From 3-animations-effects.md */
  }
  ```

- **`app/static/js/game.js`** ← Manage animation timings
  ```javascript
  // Fall speed from 3-animations-effects.md
  const FALL_SPEEDS = {
      0: 500,   // Level 0: 500ms
      1: 450,   // Level 1: 450ms
      2: 400,   // Level 2: 400ms
  };
  ```

- **`app/static/js/audio.js`** ← Play sounds for animations
  ```javascript
  // Line clear animation + sound (from 3-animations-effects.md)
  clearLines() {
      playSound('line_clear.mp3');
      showAnimation('lineClear', 900);  // 900ms duration
  }
  ```

---

## 4. Typography & UI Text Styling → Apply To
**File**: `.github/instructions/4-typography-ui.md`

### Implementation Files:
- **`app/static/css/style.css`** ← All font and text styling
  ```css
  h1 {
      font-size: 48px;        /* From 4-typography-ui.md */
      font-weight: bold;
      color: #FFFFFF;
      text-shadow: 2px 2px 4px #000000;
  }

  .score {
      font-size: 24px;        /* From 4-typography-ui.md */
      font-weight: bold;
      color: #FFFFFF;
  }

  button {
      background: #333333;    /* From 4-typography-ui.md */
      color: #FFFFFF;
      border: 2px solid #CCCCCC;
      padding: 10px 20px;
      border-radius: 5px;
  }

  button:hover {
      background: #555555;
      border-color: #FFD700;
      box-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
  }
  ```

- **`app/static/index.html`** ← Apply text styling to HTML
  ```html
  <h1>TETRIS GAME</h1>  <!-- 48px bold white from 4-typography-ui.md -->
  <div class="score">Score: <span id="scoreValue">1250</span></div>  <!-- 24px -->
  <button id="playAgain">Play Again</button>
  ```

- **`app/static/js/renderer.js`** ← Draw text on canvas with correct styling
  ```javascript
  drawScore(score) {
      ctx.font = 'bold 24px Arial';  // From 4-typography-ui.md
      ctx.fillStyle = '#FFFFFF';
      ctx.fillText(`SCORE: ${score}`, 20, 50);
  }
  ```

---

## 5. Sound Design & Audio Guidelines → Apply To
**File**: `.github/instructions/5-sound-design.md`

### Implementation Files:
- **`app/static/js/audio.js`** ← Load and manage all audio files
  ```javascript
  // From 5-sound-design.md
  const AUDIO = {
      backgroundMusic: new Audio('sounds/game_music.mp3'),
      lineClear: new Audio('sounds/line_clear.mp3'),
      gameOver: new Audio('sounds/game_over.mp3'),
      rotate: new Audio('sounds/rotate.mp3'),
      move: new Audio('sounds/move.mp3')
  };

  // Set volumes from 5-sound-design.md
  AUDIO.backgroundMusic.volume = 0.6;   // 60% default
  AUDIO.lineClear.volume = 0.7;         // 70% default
  AUDIO.gameOver.volume = 0.75;         // 75% default
  ```

- **`app/static/js/game.js`** ← Call audio functions at right times
  ```javascript
  // Play line clear sound when rows cleared
  if (linesCleared > 0) {
      playLineSound();  // From 5-sound-design.md
  }

  // Play game over sound when game ends
  gameOver() {
      playGameOverSound();  // From 5-sound-design.md
  }

  // Play movement sound when moving
  moveLeft() {
      playMoveSound();  // From 5-sound-design.md (optional)
  }
  ```

- **`app/static/index.html`** ← Add volume control UI
  ```html
  <div id="audioControls">
      <label>Volume: <input type="range" id="volumeControl" min="0" max="100" value="60"></label>
      <button id="muteButton">Mute</button>
  </div>
  ```

- **`app/static/css/style.css`** ← Style audio controls
  ```css
  #audioControls {
      margin-top: 20px;
      display: flex;
      gap: 10px;
  }

  input[type="range"] {
      width: 150px;
  }
  ```

- **`app/static/js/renderer.js`** ← Optional: Show audio indicator
  ```javascript
  // Show speaker icon or mute indicator on canvas
  drawAudioStatus(isMuted) {
      if (isMuted) {
          ctx.fillText('🔇 MUTED', 10, 20);
      }
  }
  ```

---

## Implementation Timeline

### Phase 5 (Frontend - Rendering):
- Apply **1-colors-palette.md** to: `renderer.js`, `style.css`, `index.html`
- Apply **2-visual-layout.md** to: `index.html`, `style.css`, `renderer.js`, `game.js`
- Apply **3-animations-effects.md** to: `renderer.js`, `style.css`, `game.js`
- Apply **4-typography-ui.md** to: `style.css`, `index.html`, `renderer.js`

### Phase 7 (Sound & Polish):
- Apply **5-sound-design.md** to: `audio.js`, `game.js`, `index.html`, `style.css`, `renderer.js`

---

## Quick Reference Checklist

When implementing each file, check which instructions apply:

### `app/static/index.html`
- [ ] Apply colors from **1-colors-palette.md**
- [ ] Apply layout from **2-visual-layout.md**
- [ ] Apply typography from **4-typography-ui.md**
- [ ] Add audio controls from **5-sound-design.md**

### `app/static/css/style.css`
- [ ] Apply colors from **1-colors-palette.md**
- [ ] Apply layout/spacing from **2-visual-layout.md**
- [ ] Apply animations from **3-animations-effects.md**
- [ ] Apply typography from **4-typography-ui.md**
- [ ] Apply audio control styling from **5-sound-design.md**

### `app/static/js/renderer.js`
- [ ] Apply colors from **1-colors-palette.md**
- [ ] Apply grid dimensions from **2-visual-layout.md**
- [ ] Apply animations from **3-animations-effects.md**
- [ ] Apply typography from **4-typography-ui.md**

### `app/static/js/game.js`
- [ ] Apply grid dimensions from **2-visual-layout.md**
- [ ] Apply fall speeds from **3-animations-effects.md**
- [ ] Call audio functions from **5-sound-design.md**

### `app/static/js/audio.js`
- [ ] Load all audio files from **5-sound-design.md**
- [ ] Set volumes from **5-sound-design.md**
- [ ] Implement mute/volume control from **5-sound-design.md**

---

## Notes
- Each instruction file is independent but interconnected
- Some files apply to multiple implementation files
- Always refer to the specific instruction file when implementing
- Keep the instruction values consistent across all files
