# Pixel-based Procedural Fighter

A lightweight 2D pixel-based procedural fighting game built without any sprite files, featuring:

* Procedural character animation
* Soft-body style motion
* Physics-based jumping and kicking
* AI-controlled enemy fighter
* Hit stun and knockback system
* KO animation sequence
* Particle effects (dust and impact sparks)
* Health bar system

The project demonstrates how procedural animation, simple physics, and gameplay logic can be combined without relying on sprite sheets or pre-rendered animations.

---

## Features

### Pixel and Procedural Character Animation

The player character is generated entirely through code.

Animations are calculated in real-time using:

* Sinusoidal motion
* Weight blending
* Body sway
* Walking bounce
* Jump offsets
* Kick pose interpolation

No animation frames or sprite sheets are used.

---

### Soft-Body Inspired Motion

The fighter's body dynamically reacts to movement:

* Walking bounce
* Idle breathing motion
* Landing impact
* Knockback reactions
* KO collapse

These effects create a more organic appearance than traditional rigid animations.

---

### Combat System

The combat system includes:

* Kick attacks
* Attack timing windows
* Hit detection
* Knockback forces
* Hit stun
* Health reduction
* KO state

Successful attacks generate particle sparks and push opponents backward.

---

### Enemy AI

The enemy fighter:

* Tracks player position
* Approaches the player
* Performs attacks when in range
* Reacts to damage
* Supports independent health and animation states

---

### Particle Effects

Visual feedback is generated procedurally:

#### Dust Effects

Created when:

* Landing from a jump
* Fast movement transitions

#### Impact Sparks

Created when:

* Kicks successfully connect

---

### KO Animation

When player health reaches zero:

* Character enters KO state
* Body rotates backward
* Arc motion is applied
* Character collapses to the ground
* Motion settles into a defeated pose

---

## Project Structure

```text
project/
│
├── main.py              # Main game loop
├── actor.py             # Procedural player rendering
├── enemy.py             # Enemy AI and rendering
├── physics.py           # Movement and combat physics
├── particle.py          # Particle system
├── input.py             # Keyboard input handling
│
└── README.md
```

---

## Controls

| Key         | Action      |
| ----------- | ----------- |
| Left Arrow  | Move Left   |
| Right Arrow | Move Right  |
| UP          | Jump        |
| SPACE       | Kick Attack |

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Sungki/PixelFighting.git
```


Activate:

## Running the Game

```bash
python main.py
```

---

## Technical Highlights

### Procedural Animation

Character motion is generated using:

```python
math.sin()
```

for:

* Leg movement
* Body bounce
* Idle breathing
* Directional sway

---

### Real-Time Motion Blending

Walking and idle states are blended smoothly through:

```python
walk_weight
```

allowing transitions without animation snapping.

---

### Physics System

Handles:

* Gravity
* Jump arcs
* Knockback
* Hit stun
* Landing detection
* KO state transitions

---

### Modular Architecture

Each gameplay system is isolated:

| Module          | Responsibility    |
| --------------- | ----------------- |
| InputHandler    | User input        |
| PhysicsEngine   | Character physics |
| ProceduralActor | Player rendering  |
| ProceduralEnemy | Enemy AI          |
| ParticleSystem  | Visual effects    |

This makes it easy to extend the game with:

* Additional attacks
* New enemies
* Combo systems
* Ragdoll effects
* Multiplayer support

---

## Future Improvements

Planned enhancements:

* Punch attacks
* Combo chains
* Block system
* Special moves
* Better enemy AI
* Sound effects
* Multiple fighters
* Online multiplayer
* Full soft-body simulation using spring-mass systems

---

## Educational Purpose

This project was created as an exploration of:

* Procedural animation
* Character physics
* Game architecture
* Combat systems
* Soft-body inspired motion
* Real-time rendering techniques

It serves as a useful reference for developers interested in creating animation systems without traditional sprite-based workflows.

---

## Requirements

* Python 3.10+
* Pygame 2.5+

---