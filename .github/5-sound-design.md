# 5. Sound Design & Audio Guidelines

## Audio File Specifications
```
Format:        MP3 or WAV (MP3 recommended for web)
Sample Rate:   44.1 kHz or 48 kHz
Bit Depth:     16-bit
Channels:      Mono (most effects), Stereo (music)
Compression:   128 kbps (MP3) for web optimization
```

## Sound Effects Library

### 1. Background Music (Looping)
```
File Name:     game_music.mp3
Duration:      1-2 minutes (loops)
Volume Level:  60% (default, adjustable)
Tone:          Upbeat, 8-bit retro Tetris style
Fade In:       2 seconds (when game starts)
Fade Out:      1 second (when game pauses/ends)
Frequency:     110-220 Hz range (keep it cheerful)
```

### 2. Line Clear Sound
```
File Name:     line_clear.mp3
Duration:      500ms
Volume Level:  70%
Tone:          Ascending beep (C-D-E notes, 262-330 Hz)
Trigger:       When 1+ rows cleared
Multiple Lines: Play same sound, slightly higher pitch each time
```

### 3. Game Over Sound
```
File Name:     game_over.mp3
Duration:      800ms
Volume Level:  75%
Tone:          Descending tone (E-C-G, minor key, sad)
Frequency:     100-200 Hz range
Trigger:       When game ends (block reaches top)
```

### 4. Rotation Sound (Optional)
```
File Name:     rotate.mp3
Duration:      50ms
Volume Level:  40%
Tone:          Quick "click" or "pop"
Frequency:     500-800 Hz
Trigger:       When player rotates block
```

### 5. Movement Sound (Optional)
```
File Name:     move.mp3
Duration:      30ms
Volume Level:  30%
Tone:          Soft beep
Frequency:     300-400 Hz
Trigger:       When player moves block left/right
```

## Audio Implementation Code
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

## Audio Guidelines
- ✅ All sounds should be non-intrusive (players can focus on game)
- ✅ Background music volume should be 60% (can be adjusted)
- ✅ Sound effects should be clear but not overpowering
- ✅ Provide mute button for accessibility
- ✅ Test on different devices (some have different speaker quality)
- ✅ Avoid loud sudden noises (startled players = bad experience)
- ✅ Use retro 8-bit style sounds (matches classic Tetris feel)

## Volume Levels (Recommended)
```
Background Music:    60% default
Line Clear Sound:    70% default
Game Over Sound:     75% default
Rotation Sound:      40% default
Movement Sound:      30% default
Master Volume:       100% default (player adjustable)
```
