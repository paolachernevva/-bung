# 3. Animation & Visual Effects

## Block Falling Animation
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

## Line Clear Animation
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

## Rotation Animation
```
Rotation Effect:
- Block rotates 90° clockwise instantly (no animation needed)
- Quick visual feedback (highlight the block briefly)
- If wall-kick occurs: block "bounces" 1-2 pixels left/right

Ghost Piece Update:
- Ghost updates instantly with rotation
- Helps player see where rotated piece will land
```

## Game Over Animation
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

## Visual Feedback for User Actions
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
