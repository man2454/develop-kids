# 3 Lane Wave System (Prototype)

Play here:
- Fire: https://man2454.github.io/develop-kids/
- OX: https://man2454.github.io/develop-kids/ox.html

## Why I made this
I keep seeing a lot of ads that show “fun looking” lane / wave defense gameplay — but many of them don’t actually have a real playable game behind the ad.  
So I made a simple playable version for myself. The graphics are intentionally super basic (just rectangles), because the goal was to get the core gameplay working first.

If you want to fork this and make it prettier, add sound effects, polish the UI, or improve the visuals — I’d really appreciate it.

## What this game is about (based on the code)
This is a **wave-based lane defense shooter**:

- You control a **player unit** stationed on a **defense line** near the bottom of the screen.
- **Enemies** spawn from the top and move downward toward your defense line.
- The player **auto-shoots** upward. Your firepower is based on how many **Soldiers** you have.
- If enemies reach the defense line, they **reduce your Soldiers** by their remaining HP.  
  If your Soldiers drop to **0**, the game ends.

### Core mechanics
- **Waves**
  - Each wave lasts **45 seconds**.
  - Enemy count increases dramatically each wave (exponential growth).
  - A performance cap limits enemies per wave, and the “extra” enemies are converted into **HP boost** so difficulty still scales.

- **Shooting / Power bullets**
  - The player auto-fires every ~0.166s.
  - Total damage per shot is basically your **Soldiers** value, split across multiple bullets.
  - More Soldiers = more bullets / more total damage.

- **Mid-bosses**
  - A mid-boss spawns at **13s** and another at **40s** in every wave.
  - They have much higher HP and are slower, with visible HP bars.

- **Big boss**
  - Every **3 waves**, a big boss can spawn after ~20s.
  - Very high HP, very slow, and dangerous if it reaches the defense line.

- **Pickups (Signs)**
  - Green “+N” signs drop regularly.
  - If you touch them, you gain **Soldiers** (your main resource).

- **Rare target (Gold block)**
  - A special “rare” block sits on the left lane area with its own HP.
  - Destroying it increases the **sign value** (so future pickups give more Soldiers).
  - After it dies, it respawns with higher HP each time.

## Controls
- Move: **Mouse / Touch** (move pointer left-right to position the player)
- Start: **Start**
- Pause / Resume: **Pause**
- Restart: **Restart**

## Notes
- This is a prototype focused on gameplay logic and wave stability.
- Visuals are minimal by design. PRs for art, SFX, UI polish, and balancing are welcome.

## License
No formal license yet — feel free to fork and experiment. If you publish improvements, a link back is appreciated.
