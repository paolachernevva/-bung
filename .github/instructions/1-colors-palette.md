# 1. Color Scheme & Tetrominoes Palette

**applyTo:** `app/colors/**`

---

## Standard Tetromino Colors
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

## UI Color Palette
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

## Implementation Rules
- ✅ Always use these exact colors for block types (for consistency across versions)
- ✅ Blocks should be slightly smaller than their cell to show grid lines
- ✅ Add dark shadow beneath blocks for 3D effect
- ✅ Highlight currently falling piece with brighter outline
- ✅ Use semi-transparent ghost piece (opacity 0.3) to show drop location

## Code Example
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
