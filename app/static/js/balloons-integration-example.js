/**
 * Integration example for balloon celebration feature in Tetris game
 * 
 * This file demonstrates how to integrate the BalloonManager into your
 * main game loop and event handling system.
 */

// ============================================================================
// STEP 1: Initialize Balloon Manager in your game setup
// ============================================================================

class TetrisGame {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    
    // Initialize balloon manager
    const balloonColors = [
      "#FF6B6B",  // Red
      "#4ECDC4",  // Cyan
      "#45B7D1",  // Blue
      "#FFA07A",  // Orange
      "#FFD93D",  // Yellow
      "#6BCB77",  // Green
      "#FF7FB3",  // Purple
    ];
    
    this.balloonManager = new BalloonManager(this.canvas, balloonColors);
    
    // Game state
    this.gameState = {
      status: "ready",  // ready, falling, clearing, finished
      score: 0,
      level: 0,
      clearedLines: 0,
    };
    
    this.setupEventListeners();
  }

  // ============================================================================
  // STEP 2: Setup event listeners for balloon interactions
  // ============================================================================

  setupEventListeners() {
    // Handle balloon clicks
    this.canvas.addEventListener('click', (event) => {
      // Only allow balloon clicking when game is won
      if (this.gameState.status !== "finished") return;
      
      const rect = this.canvas.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
      
      // Check if click hit a balloon
      const balloonPopped = this.balloonManager.checkBalloonClick(x, y);
      
      if (balloonPopped) {
        console.log("Balloon popped!");
        // Optional: play sound, track stat, etc.
      }
    });
    
    // Handle touch events for mobile
    this.canvas.addEventListener('touchstart', (event) => {
      if (this.gameState.status !== "finished") return;
      
      const touch = event.touches[0];
      const rect = this.canvas.getBoundingClientRect();
      const x = touch.clientX - rect.left;
      const y = touch.clientY - rect.top;
      
      this.balloonManager.checkBalloonClick(x, y);
    });
  }

  // ============================================================================
  // STEP 3: Trigger balloons when game is won
  // ============================================================================

  /**
   * Called when the player wins (completes a game, reaches target score, etc.)
   */
  triggerWinAnimation() {
    this.gameState.status = "finished";
    
    // Optionally add a confetti or celebration overlay
    this.showWinScreen();
    
    // Create and start balloon animation
    // Count: 15 balloons (as per your preference)
    this.balloonManager.createBalloons(15);
    
    console.log("Win animation triggered! Click balloons to pop them.");
  }

  /**
   * Optional: Display a win screen overlay
   */
  showWinScreen() {
    // Clear the main canvas or add a semi-transparent overlay
    this.ctx.fillStyle = "rgba(0, 0, 0, 0.3)";
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    
    // Draw "YOU WIN!" text
    this.ctx.fillStyle = "#FFD700";
    this.ctx.font = "bold 48px Arial";
    this.ctx.textAlign = "center";
    this.ctx.textBaseline = "middle";
    this.ctx.fillText(
      "YOU WIN!",
      this.canvas.width / 2,
      this.canvas.height / 2
    );
    
    // Draw score
    this.ctx.font = "24px Arial";
    this.ctx.fillStyle = "#FFFFFF";
    this.ctx.fillText(
      `Final Score: ${this.gameState.score}`,
      this.canvas.width / 2,
      this.canvas.height / 2 + 60
    );
  }

  // ============================================================================
  // STEP 4: Main game loop
  // ============================================================================

  /**
   * Main animation frame update
   */
  update() {
    // ... existing game logic ...
    
    // Balloons are handled by their own animation loop via requestAnimationFrame
    // so you don't need to explicitly update them in your game loop
    // unless you want custom behavior
  }

  /**
   * Render everything
   */
  render() {
    // Clear canvas
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    
    // Draw game board, pieces, etc.
    // ... your existing rendering code ...
    
    // Note: BalloonManager handles its own rendering via requestAnimationFrame
  }

  /**
   * Clean up when game ends
   */
  cleanup() {
    this.balloonManager.stop();
    // ... other cleanup ...
  }
}

// ============================================================================
// STEP 5: Integration with WebSocket (if using multiplayer)
// ============================================================================

/**
 * Example: Handle win messages from server
 */
class MultiplayerTetrisGame extends TetrisGame {
  constructor(canvasId, websocketUrl) {
    super(canvasId);
    this.ws = new WebSocket(websocketUrl);
    this.setupWebSocket();
  }

  setupWebSocket() {
    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      
      if (message.type === "game_finished") {
        // Player won!
        this.gameState.score = message.score;
        this.gameState.level = message.level;
        this.gameState.clearedLines = message.clearedLines;
        
        // Trigger celebration
        this.triggerWinAnimation();
      }
    };
  }
}

// ============================================================================
// STEP 6: Usage example
// ============================================================================

/*
// Initialize the game
const game = new TetrisGame('gameCanvas');

// When player wins (e.g., after line clear logic)
function onGameWon() {
  game.triggerWinAnimation();
}

// Optional: Share balloon state over network
function sendWinToServer() {
  const balloonState = game.balloonManager.balloons;
  fetch('/api/game/win', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      score: game.gameState.score,
      balloonCount: balloonState.length,
    })
  });
}

// Clean up when navigating away
window.addEventListener('beforeunload', () => {
  game.cleanup();
});
*/
