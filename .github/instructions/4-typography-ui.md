# 4. Typography & UI Text Styling

**applyTo:** `app/typography/**`

---

## Font Choices
```
Main Font (all text):  Arial, Helvetica, sans-serif
Monospace (for code):  Courier New, monospace

Fallback fonts: Arial → Helvetica → sans-serif
System Font Option:   -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
```

## Text Sizing & Styling

### Game Title
```
Font Size:       48px
Font Weight:     Bold
Color:           #FFFFFF
Text Shadow:     2px 2px 4px #000000
Margin Bottom:   20px
Letter Spacing:  2px
```

### Score Display
```
Font Size:       24px
Font Weight:     Bold
Color:           #FFFFFF
Prefix Label:    "SCORE:" (12px, gray)
Value:           "1,250" (24px, yellow highlight on match)
```

### Level & Lines Cleared
```
Font Size:       18px
Font Weight:     Normal
Color:           #CCCCCC
Format:          "Level: 2" / "Lines: 5"
```

### Next Piece Label
```
Font Size:       14px
Font Weight:     Bold
Color:           #FFFFFF
Uppercase:       "NEXT PIECE"
```

### Control Instructions
```
Font Size:       10px
Font Weight:     Normal
Color:           #999999
Text:            "← → = Move  |  ↑ = Rotate  |  SPACE = Drop"
Opacity:         0.7 (less prominent)
```

### Game Over Screen
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

## Button Styling
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
