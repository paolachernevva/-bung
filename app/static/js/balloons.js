/**
 * Balloon popping celebration animation for game win screen
 */

class BalloonManager {
  constructor(canvas, colors) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.colors = colors;
    this.balloons = [];
    this.particles = [];
    this.isActive = false;
    this.animationFrameId = null;
  }

  /**
   * Create and display balloons on the canvas
   * @param {number} count - Number of balloons to create
   */
  createBalloons(count = 15) {
    this.balloons = [];
    this.particles = [];

    for (let i = 0; i < count; i++) {
      const balloon = {
        x: Math.random() * this.canvas.width,
        y: this.canvas.height + 50,
        radius: 15 + Math.random() * 10,
        color: this.colors[Math.floor(Math.random() * this.colors.length)],
        velocityY: -1 - Math.random() * 1.5,
        velocityX: (Math.random() - 0.5) * 2,
        floatDuration: 2000 + Math.random() * 1500,
        startTime: Date.now() + i * 100,
        isPopped: false,
        stringLength: 50 + Math.random() * 50
      };
      this.balloons.push(balloon);
    }

    this.isActive = true;
    this.animate();
  }

  /**
   * Check if a point (like mouse click) hits any balloon
   * @param {number} x - Click x coordinate
   * @param {number} y - Click y coordinate
   * @returns {boolean} - True if a balloon was popped
   */
  checkBalloonClick(x, y) {
    for (let balloon of this.balloons) {
      if (balloon.isPopped) continue;

      const dist = Math.hypot(x - balloon.x, y - balloon.y);
      if (dist < balloon.radius) {
        this.popBalloon(balloon);
        return true;
      }
    }
    return false;
  }

  /**
   * Pop a balloon and create particle effects
   * @param {Object} balloon - The balloon to pop
   */
  popBalloon(balloon) {
    balloon.isPopped = true;

    // Create pop particles
    const particleCount = 8 + Math.floor(Math.random() * 4);
    for (let i = 0; i < particleCount; i++) {
      const angle = (i / particleCount) * Math.PI * 2;
      const speed = 2 + Math.random() * 3;

      this.particles.push({
        x: balloon.x,
        y: balloon.y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        life: 500 + Math.random() * 300,
        startTime: Date.now(),
        radius: 2 + Math.random() * 3,
        color: balloon.color
      });
    }

    // Play pop sound if available
    if (window.audioManager && window.audioManager.playPopSound) {
      window.audioManager.playPopSound();
    }
  }

  /**
   * Main animation loop
   */
  animate = () => {
    if (!this.isActive) return;

    // Clear canvas (semi-transparent for trail effect)
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    const now = Date.now();

    // Update and draw balloons
    for (let balloon of this.balloons) {
      if (balloon.isPopped) continue;

      const elapsed = now - balloon.startTime;
      if (elapsed < 0) continue;

      const progress = Math.min(elapsed / balloon.floatDuration, 1);

      // Floating animation
      balloon.y += balloon.velocityY;
      balloon.x += balloon.velocityX + Math.sin(elapsed / 300) * 0.5;

      // Draw string
      this.ctx.strokeStyle = 'rgba(200, 200, 200, 0.4)';
      this.ctx.lineWidth = 1;
      this.ctx.beginPath();
      this.ctx.moveTo(balloon.x, balloon.y + balloon.radius);
      this.ctx.lineTo(balloon.x, balloon.y + balloon.radius + balloon.stringLength);
      this.ctx.stroke();

      // Draw balloon
      this.ctx.fillStyle = balloon.color;
      this.ctx.beginPath();
      this.ctx.arc(balloon.x, balloon.y, balloon.radius, 0, Math.PI * 2);
      this.ctx.fill();

      // Balloon highlight
      this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
      this.ctx.lineWidth = 2;
      this.ctx.beginPath();
      this.ctx.arc(
        balloon.x - balloon.radius * 0.3,
        balloon.y - balloon.radius * 0.3,
        balloon.radius * 0.4,
        0,
        Math.PI * 2
      );
      this.ctx.stroke();

      // Auto-pop after float duration (if not already popped)
      if (progress >= 1) {
        this.popBalloon(balloon);
      }
    }

    // Update and draw particles
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const particle = this.particles[i];
      const elapsed = now - particle.startTime;
      const life = particle.life - elapsed;

      if (life <= 0) {
        this.particles.splice(i, 1);
        continue;
      }

      particle.x += particle.vx;
      particle.y += particle.vy;
      particle.vy += 0.1; // gravity

      const opacity = life / particle.life;
      this.ctx.fillStyle = this.hexToRgba(particle.color, opacity);
      this.ctx.beginPath();
      this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
      this.ctx.fill();
    }

    // Check if animation is done
    const allPopped = this.balloons.every(b => b.isPopped);
    const noParticles = this.particles.length === 0;

    if (allPopped && noParticles) {
      this.isActive = false;
      return;
    }

    this.animationFrameId = requestAnimationFrame(this.animate);
  };

  /**
   * Stop the balloon animation
   */
  stop() {
    this.isActive = false;
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
    }
    this.balloons = [];
    this.particles = [];
  }

  /**
   * Convert hex color to rgba string
   * @param {string} hex - Hex color code
   * @param {number} alpha - Opacity (0-1)
   * @returns {string} - RGBA color string
   */
  hexToRgba(hex, alpha = 1) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  }
}

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = BalloonManager;
}
