# Tetris Game - Step-by-Step Implementation Plan

## 1. Goal and Instruction Sources

Build a browser-based Tetris game with a Python 3.12/FastAPI backend,
vanilla JavaScript, HTML5 Canvas, WebSockets, and a SQLite leaderboard.
This document is a plan only. No gameplay has been implemented yet.

Follow these project guides:

- [Technical instructions](../.github/instructions/infrastructure-instructions.md): architecture,
  game modes, endpoints, code style, storage, and deployment.
- [Colors](../.github/instructions/1-colors-palette.md): exact piece and UI colors.
- [Layout](../.github/instructions/2-visual-layout.md): grid, spacing, and responsive layout.
- [Animations](../.github/instructions/3-animations-effects.md): movement, line clears,
  pause, and game-over effects.
- [Typography](../.github/instructions/4-typography-ui.md): fonts, labels, and buttons.
- [Sound](../.github/instructions/5-sound-design.md): audio assets, triggers, and volume.

The five design guides currently declare `applyTo` paths such as `app/colors/**`,
but the technical guide places the frontend under `app/static/`. Treat all five
as requirements for the corresponding frontend work. Before implementation,
align their targeting metadata with the actual files and the instruction loader's
supported format; do not create unused folders just to match those patterns.

### Resolved Rules - Latest Instructions Take Precedence

Use the current infrastructure and design guides instead of superseded rules
from the original plan. Where the guides do not specify a value, retain the
existing plan's rule and identify it below. These decisions are final for this
plan; no further confirmation is required for these five topics.

| Topic | Final rule | Source and interpretation |
| --- | --- | --- |
| Scoring | Award 100/200/300/400 points for clearing 1/2/3/4 rows. No additional bonus or level multiplier. | Current infrastructure guide: 100 points per line and 400 total for a Tetris; replaces the old 100/300/500/800 table. |
| Starting level | Start at level 0 with score 0 and zero cleared lines. | Current animation guide explicitly starts its speed reference at level 0. |
| Speed progression | Set `level = score // 500`. Gravity intervals are 500 ms at level 0, 450 ms at level 1, 400 ms at level 2, and 350 ms at every level from 3 onward. | Use the animation guide's literal level 3+ rule, not the previously proposed extrapolation. The 500-point level threshold is retained from the original plan because newer guides do not replace it. The guide's 100 ms minimum is a safety floor, not a requirement to accelerate beyond level 3. |
| Movement distance | Move exactly one grid cell: 30 px normally and 20 px below 500 px viewport width. Animation must end on that cell. | Preserve the layout guide's grid geometry. Interpret the animation guide's 20 px slide as the mobile-cell case, not a second board coordinate system. |
| Score font | Use a 24 px bold score value with a 12 px label; level and lines remain 18 px. | The newer typography guide replaces the layout guide's general 18 px score suggestion. |

Store scoring, level progression, and gravity intervals in shared game constants.
The speed formula is `max(100, 500 - 50 * min(level, 3))` ms per row;
it deliberately stays at 350 ms after level 3.

Do not treat examples or checked boxes in the technical guide as proof that a
feature already exists. Replace the old fixed four-week schedule with
verification gates; finish a working Classic mode before adding other modes.

## 2. Planned Files

All paths below are relative to the repository root. Create files only when
their phase needs them; add package `__init__.py` files where required.

| Files to create or change | Purpose |
| --- | --- |
| `requirements.txt`, `requirements-dev.txt`, `.gitignore` | Runtime/test dependencies; ignore environments, caches, and local database files. |
| `app/main.py` | FastAPI entry point, static page/assets, database and game-task lifecycle. |
| `app/game/constants.py` | Grid size, resolved scoring, level progression, and timing. |
| `app/game/pieces.py` | Seven tetrominoes, rotation states, and piece generation. |
| `app/game/models.py` | Typed piece, game state, action, and event models. |
| `app/game/logic.py` | Collision, movement, rotation, falling, hold, ghost, line clearing, and scoring. |
| `app/game/multiplayer.py` | Room membership, independent boards, synchronized starts, and match results. |
| `app/api/routes.py`, `app/api/websockets.py` | REST endpoints, socket validation, player sessions, and game loops. |
| `app/db/models.py`, `app/db/crud.py` | SQLAlchemy score records and top-ten queries. |
| `scripts/init_db.py` | Explicit, non-destructive schema initialization. |
| `app/static/index.html`, `app/static/css/style.css` | Canvas, responsive layout, controls, typography, and overlays. |
| `app/static/js/game.js`, `renderer.js`, `input.js` | State synchronization, drawing, keyboard, and touch controls. |
| `app/static/js/animations.js`, `audio.js`, `multiplayer.js` | Visual transitions, audio management, and room UI. |
| `app/static/sounds/` | Original or appropriately licensed music and effects. |
| `tests/test_game_logic.py`, `tests/test_api.py`, `tests/test_multiplayer.py` | Focused engine, persistence, API, and multiplayer tests. |
| `README.md` | Setup, controls, resolved game rules, validation, and deployment. |
| `.github/instructions/` | Align instruction targeting with actual frontend files before implementation. |

Use Python type hints, PEP 8, and a 100-character line limit. Use ES6 modules,
descriptive names, and `const` by default in JavaScript. Reuse shared logic
instead of implementing separate game rules in the browser.

## 3. Phase 1 - Setup, State, and Piece Definitions

**Files:** dependency manifests, package initializers, `main.py`, `constants.py`,
`pieces.py`, `models.py`, and `tests/test_game_logic.py`.

1. Prepare Python 3.12 and the FastAPI/Pydantic/SQLAlchemy/WebSocket stack.
   Verify dependency compatibility before adopting the guide's example pins.
   Include pytest, FastAPI test-client support, and flake8 as development tools.
2. Define a 10-column by 20-row board containing locked cells only.
3. Keep the active piece separate: type, rotation, column, and row.
4. Track score, level, cleared lines, next piece, held piece, mode, pause state,
   revision, and status: ready, falling, clearing, or finished.
5. Define all seven pieces as four occupied cells, with consistent rotation
   origins. The O piece remains unchanged on rotation.
6. Generate pieces using a shuffled seven-piece bag and an injectable random
   source for reproducible tests.

**Verification gate:** Each piece has four cells in every rotation; four
rotations restore the original shape; each bag contains all seven pieces.
New games have independent boards, score 0, level 0, and zero cleared lines.

## 4. Phase 2 - Falling, Movement, Rotation, and Collision

**Files:** `logic.py`, `pieces.py`, and `tests/test_game_logic.py`.

1. Implement one placement check used by movement, rotation, spawning, and drops.
   For every occupied cell, check horizontal bounds, floor, and locked cells.
   Handle cells above the visible board explicitly without negative indexing.
2. Spawn each piece centered at the top. A blocked spawn ends the game.
   If a piece locks with occupied cells above the board, end the game without
   writing outside the board.
3. On each gravity tick, try moving down one row. If blocked, lock the piece
   once, resolve completed rows, then spawn the next piece.
4. Move left/right by one column only when the destination is valid.
5. Rotate clockwise. Try the rotated shape in place, then horizontal offsets
   `-1`, `+1`, `-2`, `+2` in that order. Reject the rotation if all fail.
   This is a simple wall-kick rule, not a claim of full official SRS support.
6. Down arrow performs a one-row soft drop; Space performs a hard drop to the
   last valid row and locks immediately. Neither awards unrequested drop points.
7. Hold with C: swap with the held piece, or store the current piece and consume
   the next piece. Allow one hold per locked piece; validate the replacement spawn.
8. Calculate the ghost landing position with the same placement check.
   Computing a ghost must not mutate the actual game state.
9. Ignore gameplay actions while paused, clearing rows, or finished.

**Verification gate:** Test walls, floor, stacked blocks, blocked spawn,
top-out, successful and rejected wall kicks, soft/hard drops, and repeated
hold attempts. Rejected actions leave the board unchanged. Ghost and hard-drop
landing positions match.

## 5. Phase 3 - Line Clearing, Scoring, and Modes

**Files:** `logic.py`, `constants.py`, `models.py`, and `tests/test_game_logic.py`.

1. After locking, identify all full rows together.
2. Emit a line-clear event carrying the affected rows and their pre-clear cells.
   Keep the game in a clearing state during the visual transition.
3. After the 900 ms clearing interval, remove those rows together, preserve the
   order of surviving rows, and insert the same number of empty rows at the top.
4. Award 100 points per cleared row once, update total lines, set
   `level = score // 500`, and apply the resolved gravity interval before
   spawning the next piece. Four rows award 400 points total.
5. Classic ends on top-out. Time Attack ends after 120 seconds of active play
   or earlier top-out; pausing stops its timer and gravity.
6. Restart creates a fresh game without stale timers, pending events, or scores.

**Verification gate:** Test one through four simultaneous clears, nonadjacent
full rows, preserved row order, unchanged board dimensions, and exact
100/200/300/400 point totals. Check level boundaries at 499/500, 999/1000,
and 1499/1500 points; verify 500/450/400/350 ms intervals and that levels
above 3 remain at 350 ms without dropping below the 100 ms safety floor.
Test the 900 ms transition,
pause/resume, and the exact 120-second Time Attack boundary with an injected
clock rather than real sleeps.

## 6. Phase 4 - Server Gameplay and Persistent Leaderboard

**Files:** API modules, `main.py`, database modules, `scripts/init_db.py`,
`game.js`, and `tests/test_api.py`.

JavaScript can perform game calculations, but this architecture intentionally
keeps authoritative game rules and scores on the Python server.

### Communication Contract

- `GET /`: serve the game page.
- `WS /ws/game/{player_id}`: start/restart a game, send actions, pause/resume,
  and receive snapshots/events.
- `GET /api/game-state`: return the requesting session's state, never a global
  player's board; reject a missing or invalid session explicitly.
- `GET /api/leaderboard`: return the top ten persisted scores.
- `POST /api/scores`: attach a validated player name to a finished,
  server-owned result; do not trust a client-supplied score.

1. Associate each connection and REST request with a server-issued session
   credential. A player ID in a URL alone is not authorization.
2. Validate message types and allowed actions with Pydantic. Return explicit
   errors for malformed messages, unknown games, and invalid state transitions.
3. Run gravity on a server-owned monotonic clock, not browser timers.
   Serialize each game's actions and ticks to avoid double locks or lost moves.
4. Send complete snapshots containing the locked grid, active/next/held pieces,
   ghost position, score, level, lines, status, remaining time, and revision.
   Number events so the browser does not replay sounds or effects.
5. On disconnect, stop the game task and show a visible disconnected state.
   Initially require an explicit new game rather than silently pretending to
   resume an authoritative session.
6. Store player name, server-calculated score, mode, completion time, and a
   unique result ID. Make submissions idempotent and order ties deterministically.
7. Keep Classic and Time Attack leaderboard results distinguishable.
   LocalStorage may cache display values/settings, never authoritative scores.
8. Log server errors and show actionable connection/save failures in the UI;
   failed saves must not display as successful.

**Verification gate:** Use FastAPI's test client and a temporary SQLite database
to test endpoints, two isolated sessions, invalid actions, ordered revisions,
disconnect cleanup, and task shutdown. Verify exact top-ten ordering, rejected
score tampering, duplicate submissions, and persistence after reopening the DB.

## 7. Phase 5 - Canvas, Layout, Colors, Typography, and Input

**Files:** `index.html`, `style.css`, `renderer.js`, `input.js`, and `game.js`.

1. Draw locked cells, ghost, then active piece on the Canvas. Render previews
   separately so they do not change the main board.
2. Use these exact piece colors:

   | I | O | T | S | Z | J | L |
   | --- | --- | --- | --- | --- | --- | --- |
   | `#00F0F0` | `#F0F000` | `#A000F0` | `#00F000` | `#F00000` | `#0000F0` | `#F0A000` |

3. Use background `#1a1a1a`, grid `#333333`, empty cells `#0a0a0a`,
   primary text `#FFFFFF`, secondary text `#CCCCCC`, and gold `#FFD700`.
   Add block shadows, a brighter active outline, and a ghost at 0.3 opacity.
4. At normal size, use 30 px cells, a 300 by 600 px board, 28 px block faces,
   1 px grid lines, and 2 px block borders. Center each face with a 1 px inset
   per side; the 2 px gap is total, not a 2 px inset on each side.
5. Use 20 px outer spacing, 15 px sidebar spacing, and an approximately 200 px
   sidebar. Treat the suggested overall window size as approximate so padding
   does not clip the board.
6. Below 500 px viewport width, use 20 px cells, a single column, stats beneath
   the board, and touch buttons. From 500 to 1200 px, put the sidebar right;
   above 1200 px, center the full layout with extra information.
7. Use Arial/Helvetica/sans-serif and 1.5 line height. Apply the typography guide:
   title 48 px bold; score 24 px bold with 12 px label; level/lines 18 px;
   next label 14 px bold; controls 10 px; game-over title 64 px gold and
   final score 32 px. Keep overlays responsive instead of clipping small screens.
8. Style buttons with the specified gray background, white text, 2 px border,
   5 px radius, gold hover border/glow, and 0.95 pressed scale.
9. Show next/hold previews, score, level, lines, high score, mode/time,
   pause/quit, restart, leaderboard, mute, and volume controls.
10. Map Left/Right, Up, Down, Space, C, and P to movement, rotation, soft drop,
    hard drop, hold, and pause. Route keyboard and touch through one action sender.
    Prevent page scrolling only for handled gameplay keys while the game is
    focused; do not intercept typing in player-name fields.

**Verification gate:** Inspect Canvas backing dimensions and cell placement,
not only appearance. Check exact colors, ghost opacity, fonts, button states,
previews, and live stats. Test 375 px, 768 px, and 1440 px viewports for overflow,
keyboard focus, all controls, and touch behavior.

## 8. Phase 6 - Animations and Sound

**Files:** `animations.js`, `renderer.js`, `audio.js`, `game.js`, `style.css`,
and `app/static/sounds/`.

1. Use `requestAnimationFrame` for presentation. Interpolate each gravity step
   over 50 ms, independently of the server's 500/450/400/350 ms gravity cadence.
   Animation must never change collision rules or drift from the latest state.
2. Rotate instantly with a brief highlight; add a small wall-kick bounce and
   update the ghost immediately. Movement always ends on an exact cell.
3. On a clear event: blink for 200 ms, fade for 300 ms, and slide surviving
   rows for 400 ms. Spawn the next piece after the server's clearing interval;
   do not make server progress depend on a browser animation callback.
4. Pause dims the board to 0.5 opacity and displays the menu. Game over stops
   input immediately, flashes gold three times over 1 second, settles visually
   for 500 ms, then reveals the score over 500 ms. Settling is visual only.
5. Honor reduced-motion preferences by skipping flashes and shortening visual
   transitions without changing authoritative gameplay timing.
6. Prepare original/licensed MP3 or WAV assets at 44.1/48 kHz; use 16-bit source
   audio, mono effects, stereo music, and approximately 128 kbps MP3 encoding:

   | Asset | Duration | Default volume | Trigger |
   | --- | --- | --- | --- |
   | `game_music.mp3` | 1-2 minute loop | 60% | Start/resume; 2 s fade-in, 1 s pause/end fade-out |
   | `line_clear.mp3` | 500 ms | 70% | One confirmed clear event; higher pitch for more rows |
   | `game_over.mp3` | 800 ms | 75% | One finished-game event |
   | `rotate.mp3` (optional) | 50 ms | 40% | Successful rotation |
   | `move.mp3` (optional) | 30 ms | 30% | Successful horizontal movement |

7. Use non-intrusive retro sounds. Initialize playback after user interaction
   to respect browser autoplay restrictions. Handle blocked playback or missing
   assets visibly without breaking gameplay.
8. Apply `effective volume = asset default * master volume`, with master
   initially 100%. Provide mute and persist preferences in LocalStorage.
   Prevent duplicate listeners, overlapping music loops, and replayed events.

**Verification gate:** Measure animation stages against their specified timing.
Test reduced motion, pause/restart during transitions, duplicate snapshots,
music fades, exact default volumes, master scaling, mute, autoplay rejection,
and missing assets. Audio failure must not stop play.

## 9. Phase 7 - Real-Time Multiplayer

**Files:** `multiplayer.py`, `websockets.py`, `multiplayer.js`,
`index.html`, and `tests/test_multiplayer.py`.

1. Implement `WS /ws/multiplayer/{room_id}` with validated room membership,
   player-ready status, a synchronized start, and separate authoritative boards.
2. Reuse the engine, renderer, protocol validation, and session ownership rules.
   Show opponent progress without allowing either player to modify the other.
3. Confirm match rules before coding this phase: room capacity, winner/tie
   conditions, whether garbage attacks exist, and disconnect outcomes.
   Do not silently add competitive mechanics absent from the source guides.
4. Define room cleanup and stop all game tasks when the match ends.

**Verification gate:** Test two clients joining and starting, isolated inputs,
invalid membership/actions, full rooms, agreed match results, disconnects,
and room/task cleanup. Play in two browser windows and verify synchronized UI.

## 10. Phase 8 - Final Validation, Documentation, and Deployment

**Files:** tests, `README.md`, and only the chosen host's deployment configuration.

Run the smallest relevant test selection during each phase. Planned commands,
once implementation and dependencies exist:

```powershell
python -m pytest tests\test_game_logic.py
python -m pytest tests\test_api.py
python -m pytest tests\test_multiplayer.py
python -m flake8 app tests scripts --max-line-length=100
python -m pytest
```

Do not promise a fixed number of passing tests before tests exist. Add focused
behavior tests for the gates above, using deterministic pieces and clocks.
Automate browser interactions/timing where practical; manually inspect visual
and audio quality in addition to functional checks.

Final release checklist:

- [ ] Classic mechanics, hold, ghost, next piece, pause, and restart work.
- [ ] Scoring, initial level, gravity, movement distance, and score typography
      match the resolved rules in Section 1.
- [ ] Time Attack ends at 120 seconds of active play.
- [ ] Multiplayer passes its agreed rules and two-client tests.
- [ ] All five design guides are checked, including responsive/touch behavior.
- [ ] Leaderboard saves survive server restart and show the correct top ten.
- [ ] Network, audio, and database failures are visible and recoverable.
- [ ] Latest two Chrome/Edge, Firefox, and Safari versions are checked.
- [ ] No uncaught browser errors, leaked tasks, or duplicate audio/event handlers.
- [ ] README explains Windows setup, controls, rules, tests, and known limitations.

For local use, serve the frontend through FastAPI at `http://localhost:8000`.
For deployment, select a WebSocket-capable host, use HTTPS/WSS, and put SQLite
on persistent storage. Start with one server worker while active games and rooms
live in memory; multiple workers require shared session/room coordination.
Verify page loading, a complete game, two-client multiplayer, and score
persistence after a deployment restart before declaring the game ready.
