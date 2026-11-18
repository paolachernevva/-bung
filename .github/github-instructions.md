# Tetris Game - GitHub Instructions

## Overview
This document contains 5 sets of visual and design instructions for the Tetris game project.

---

## 1. Color Scheme & Tetrominoes Palette

### Standard Tetromino Colors
Each block type has a specific color (matches official Tetris color scheme):

```
I-Piece (Cyan/Light Blue)
  Color: #00F0F0
  RGB: (0, 240, 240)
  Usage: 4 blocks in a line

O-Piece (Yellow)
  Color: #F0F000
  RGB: (240, 240, 0)
  Usage: 2×2 square

T-Piece (Purple/Magenta)
  Color: #A000F0
  RGB: (160, 0, 240)
  Usage: T-shape

S-Piece (Green)
  Color: #00F000
  RGB: (0, 240, 0)
  Usage: S-shape

Z-Piece (Red)
  Color: #F00000
  RGB: (240, 0, 0)
  Usage: Z-shape

J-Piece (Blue)
  Color: #0000F0
  RGB: (0, 0, 240)
  Usage: J-shape

L-Piece (Orange)
  Color: #F0A000
  RGB: (240, 160, 0)
  Usage: L-shape
```

### UI Color Palette
```
Background:        #1a1a1a (Dark gray - game background)
Grid Lines:        #333333 (Medium gray - borders between cells)
Filled Cell:       Block color (from above)
Empty Cell:        #0a0a0a (Very dark gray - empty space)
Text (Primary):    #FFFFFF (White - main text, scores)
Text (Secondary):  #CCCCCC (Light gray - labels)
Highlight:         #FFD700 (Gold - for game over, high score)
Shadow:            #000000 (Black - for depth/contrast)
```

### Implementation Rules
- ✅ Always use these exact colors for block types (for consistency across versions)
- ✅ Blocks should be slightly smaller than their cell to show grid lines
- ✅ Add dark shadow beneath blocks for 3D effect
- ✅ Highlight currently falling piece with brighter outline
- ✅ Use semi-transparent ghost piece (opacity 0.3) to show drop location

### Code Example
```javascript
// In renderer.js
const BLOCK_COLORS = {
    'I': '#00F0F0',
    'O': '#F0F000',
    'T': '#A000F0',
    'S': '#00F000',
    'Z': '#F00000',
    'J': '#0000F0',
    'L': '#F0A000'
};

const UI_COLORS = {
    background: '#1a1a1a',
    gridLines: '#333333',
    emptyCell: '#0a0a0a',
    text: '#FFFFFF',
    highlight: '#FFD700'
};
```

---

## 2. Visual Layout & Grid Dimensions

### Game Grid Layout
```
┌─────────────────────────────────────────┐
│          TETRIS GAME                    │
├─────────────────────────────────────────┤
│                                         │
│         MAIN GAME GRID                  │
│         (10 cells wide)                 │
│         (20 cells tall)                 │
│                                         │
│         Currently Falling Block          │
│         [with rotation preview]          │
│                                         │
├──────────────┬──────────────────────────┤
│ NEXT PIECE   │  SCORE: 1,250            │
│ PREVIEW      │  LEVEL: 2                │
│              │  LINES: 5                │
│              │                          │
│              │  [HIGH SCORE: 5,420]     │
│              │                          │
├──────────────┴──────────────────────────┤
│  Controls: ← → ↑ SPACE  |  PAUSE/QUIT   │
└─────────────────────────────────────────┘
```

### Canvas Specifications
```
Grid Cell Size:        30 × 30 pixels
Grid Width:            10 cells = 300 pixels
Grid Height:           20 cells = 600 pixels
Total Canvas:          300 × 600 pixels (minimum)

Block Size:            28 × 28 pixels (2px margin)
Grid Line Width:       1 pixel
Block Border:          2 pixels

UI Sidebar Width:      200 pixels (optional, for next piece + stats)
Total Game Window:     500 × 650 pixels (recommended)
```

### Spacing & Padding
```
Grid Margin (from edge):   20 pixels
Sidebar Margin:            15 pixels
Text Line Height:          1.5
Score Display Font:        18px
Label Font:                12px
Control Text:              10px
```

### Responsive Design
```
Mobile (< 500px width):
  - Single column layout
  - Grid smaller (20 × 20px cells)
  - Sidebar below game grid
  - Touch controls (buttons instead of keyboard)

Tablet (500px - 1200px):
  - Two column layout
  - Grid normal size (30 × 30px)
  - Sidebar to the right

Desktop (> 1200px):
  - Centered layout
  - Grid normal size
  - Sidebar to the right with extra info
```

---

## 3. Animation & Visual Effects

### Block Falling Animation
```
Block Movement:
- Smooth drop (each row takes 50ms to animate)
- No jerky movement
- Constant speed during fall

Falling Block Effect:
- Shadow beneath block (5px darker)
- Slight glow on current piece (outline 1px brighter)
- Ghost piece always visible (semi-transparent, 30% opacity)

Speed Reference:
- Level 0: Block falls 1 row every 500ms
- Level 1: Block falls 1 row every 450ms
- Level 2: Block falls 1 row every 400ms
- Level 3+: Block falls 1 row every 350ms (minimum 100ms)
```

### Line Clear Animation
```
Step 1: Highlight (200ms)
  - Selected row blinks (alternates between color and black)
  - Play line-clear sound

Step 2: Clear (300ms)
  - Row fades out
  - Particle effect (optional): small blocks scatter

Step 3: Drop (400ms)
  - Rows above slide down smoothly
  - Blocks accelerate slightly for realism

Total Duration: ~900ms before next piece spawns
```

### Rotation Animation
```
Rotation Effect:
- Block rotates 90° clockwise instantly (no animation needed)
- Quick visual feedback (highlight the block briefly)
- If wall-kick occurs: block "bounces" 1-2 pixels left/right

Ghost Piece Update:
- Ghost updates instantly with rotation
- Helps player see where rotated piece will land
```

### Game Over Animation
```
Step 1: Stop (immediate)
  - Current piece locks
  - No new pieces spawn

Step 2: Flash (1 second)
  - Game grid flashes 3 times
  - Entire grid turns highlight color (#FFD700)

Step 3: Slide (500ms)
  - Stacked blocks "settle" down with gravity
  - Each block drops a bit further (visual effect)

Step 4: Display Score (500ms)
  - Final score slides up from bottom
  - "GAME OVER" text fades in
  - Option to play again or view leaderboard
```

### Visual Feedback for User Actions
```
Button Press Effects:
- Move Left/Right: Block slides smoothly 20px
- Rotate: Block rotates with highlight
- Drop: Piece accelerates falling
- Pause: Game dims (opacity 0.5), pause menu appears

Sound Effects:
- Move: Soft beep (100ms, low frequency)
- Rotate: Click sound (50ms)
- Line Clear: Ascending tone (500ms)
- Game Over: Descending tone (800ms)
- Background: Looping music (adjustable volume)
```

---

## 4. Typography & UI Text Styling

### Font Choices
```
Main Font (all text):  Arial, Helvetica, sans-serif
Monospace (for code):  Courier New, monospace

Fallback fonts: Arial → Helvetica → sans-serif
System Font Option:   -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
```

### Text Sizing & Styling

#### Game Title
```
Font Size:       48px
Font Weight:     Bold
Color:           #FFFFFF
Text Shadow:     2px 2px 4px #000000
Margin Bottom:   20px
Letter Spacing:  2px
```

#### Score Display
```
Font Size:       24px
Font Weight:     Bold
Color:           #FFFFFF
Prefix Label:    "SCORE:" (12px, gray)
Value:           "1,250" (24px, yellow highlight on match)
```

#### Level & Lines Cleared
```
Font Size:       18px
Font Weight:     Normal
Color:           #CCCCCC
Format:          "Level: 2" / "Lines: 5"
```

#### Next Piece Label
```
Font Size:       14px
Font Weight:     Bold
Color:           #FFFFFF
Uppercase:       "NEXT PIECE"
```

#### Control Instructions
```
Font Size:       10px
Font Weight:     Normal
Color:           #999999
Text:            "← → = Move  |  ↑ = Rotate  |  SPACE = Drop"
Opacity:         0.7 (less prominent)
```

#### Game Over Screen
```
"GAME OVER" Text:
  Font Size:     64px
  Font Weight:   Bold
  Color:         #FFD700 (gold)
  Text Shadow:   3px 3px 8px #000000

Final Score:
  Font Size:     32px
  Color:         #FFFFFF
  Margin Top:    20px
```

### Button Styling
```
Buttons (Play Again, Leaderboard, Quit):

Default State:
  - Background: #333333
  - Text Color: #FFFFFF
  - Border: 2px solid #CCCCCC
  - Padding: 10px 20px
  - Border Radius: 5px
  - Font Size: 14px

Hover State:
  - Background: #555555
  - Border: 2px solid #FFD700
  - Cursor: pointer
  - Box Shadow: 0 0 10px rgba(255, 215, 0, 0.5)

Active/Pressed State:
  - Background: #666666
  - Border: 2px solid #FFFFFF
  - Transform: scale(0.95)
```

---

## 5. Sound Design & Audio Guidelines

### Audio File Specifications
```
Format:        MP3 or WAV (MP3 recommended for web)
Sample Rate:   44.1 kHz or 48 kHz
Bit Depth:     16-bit
Channels:      Mono (most effects), Stereo (music)
Compression:   128 kbps (MP3) for web optimization
```

### Sound Effects Library

#### 1. Background Music (Looping)
```
File Name:     game_music.mp3
Duration:      1-2 minutes (loops)
Volume Level:  60% (default, adjustable)
Tone:          Upbeat, 8-bit retro Tetris style
Fade In:       2 seconds (when game starts)
Fade Out:      1 second (when game pauses/ends)
Frequency:     110-220 Hz range (keep it cheerful)
```

#### 2. Line Clear Sound
```
File Name:     line_clear.mp3
Duration:      500ms
Volume Level:  70%
Tone:          Ascending beep (C-D-E notes, 262-330 Hz)
Trigger:       When 1+ rows cleared
Multiple Lines: Play same sound, slightly higher pitch each time
```

#### 3. Game Over Sound
```
File Name:     game_over.mp3
Duration:      800ms
Volume Level:  75%
Tone:          Descending tone (E-C-G, minor key, sad)
Frequency:     100-200 Hz range
Trigger:       When game ends (block reaches top)
```

#### 4. Rotation Sound (Optional)
```
File Name:     rotate.mp3
Duration:      50ms
Volume Level:  40%
Tone:          Quick "click" or "pop"
Frequency:     500-800 Hz
Trigger:       When player rotates block
```

#### 5. Movement Sound (Optional)
```
File Name:     move.mp3
Duration:      30ms
Volume Level:  30%
Tone:          Soft beep
Frequency:     300-400 Hz
Trigger:       When player moves block left/right
```

### Audio Implementation Code
```javascript
// In audio.js
const AUDIO = {
    backgroundMusic: new Audio('sounds/game_music.mp3'),
    lineClear: new Audio('sounds/line_clear.mp3'),
    gameOver: new Audio('sounds/game_over.mp3'),
    rotate: new Audio('sounds/rotate.mp3'),
    move: new Audio('sounds/move.mp3')
};

// Background music loops
AUDIO.backgroundMusic.loop = true;
AUDIO.backgroundMusic.volume = 0.6;

// Sound effects play once
function playLineSound() {
    AUDIO.lineClear.currentTime = 0;
    AUDIO.lineClear.play();
}

// Volume control
function setVolume(percent) {
    Object.values(AUDIO).forEach(audio => {
        audio.volume = (percent / 100) * 0.7; // Max 70%
    });
}

// Mute button
function toggleMute() {
    Object.values(AUDIO).forEach(audio => {
        audio.muted = !audio.muted;
    });
}
```

### Audio Guidelines
- ✅ All sounds should be non-intrusive (players can focus on game)
- ✅ Background music volume should be 60% (can be adjusted)
- ✅ Sound effects should be clear but not overpowering
- ✅ Provide mute button for accessibility
- ✅ Test on different devices (some have different speaker quality)
- ✅ Avoid loud sudden noises (startled players = bad experience)
- ✅ Use retro 8-bit style sounds (matches classic Tetris feel)

### Volume Levels (Recommended)
```
Background Music:    60% default
Line Clear Sound:    70% default
Game Over Sound:     75% default
Rotation Sound:      40% default
Movement Sound:      30% default
Master Volume:       100% default (player adjustable)
```

---

## Summary of All 5 Instruction Sets

| Set | Purpose | Key Content |
|-----|---------|------------|
| 1. Colors & Palette | Define block colors and UI colors | 7 tetromino colors, background, text colors |
| 2. Layout & Dimensions | Game grid and UI layout | Canvas size, spacing, responsive design |
| 3. Animations & Effects | Visual feedback and animations | Falling, line clear, rotation, game over effects |
| 4. Typography & UI | Text styling and buttons | Font sizes, colors, button states |
| 5. Sound Design | Audio guidelines | Sound files, volumes, frequencies, implementation |

---

## Implementation Checklist

When building the Tetris game, refer to these instructions:

**Phase 1-2 (Backend):**
- Use colors from Set 1 when defining block types
- Reference dimensions from Set 2

**Phase 5 (Frontend - Rendering):**
- Apply all colors from Set 1
- Use grid dimensions from Set 2
- Implement animations from Set 3
- Apply typography from Set 4

**Phase 7 (Sound & Polish):**
- Implement audio from Set 5
- Refine all animations from Set 3
- Polish UI text from Set 4

---

## Questions?
Refer to these 5 instruction sets when designing and building the visual/audio aspects of the Tetris game!
