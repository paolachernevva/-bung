# 2. Visual Layout & Grid Dimensions

**applyTo:** `app/layout/**`

---

## Game Grid Layout

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

## Canvas Specifications

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

## Spacing & Padding

```
Grid Margin (from edge):   20 pixels
Sidebar Margin:            15 pixels
Text Line Height:          1.5
Score Display Font:        18px
Label Font:                12px
Control Text:              10px
```

## Responsive Design

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
