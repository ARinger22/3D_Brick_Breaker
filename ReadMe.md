# 3D Brick Breaker Style Ball Game with Paddle

## Description
This is a 3D version of a classic brick breaker game implemented using PyOpenGL. The player controls a paddle at the bottom of a cube to bounce a ball, trying to keep it in play as long as possible. The game features physics-based ball movement, collision detection, and a scoring system.

## Features

3D environment with perspective camera 
Realistic ball physics with bouncing mechanics 
Player-controlled paddle to keep the ball in play 
Score tracking system (1 point per wall hit) 
Game over detection when ball misses the paddle 
Visual feedback on collisions 
Restart functionality 
Mouse-controlled view rotation 

## Controls

W: Move paddle left 
S: Move paddle right 
A: Move paddle forward 
D: Move paddle backward 
R: Restart game (after game over) 
Left-click + drag: Rotate view 

## Requirements

Python 3.x 
PyOpenGL 
PyOpenGL_accelerate 
GLUT (freeglut on Windows) 

pip install PyOpenGL PyOpenGL_accelerate 

## How to Play

Run the script: 
python 3d_brick_breaker.py 
Use the controls to move the paddle and keep the ball in play 

Try to score as many points as possible by bouncing the ball off the walls 
The game ends when the ball hits the bottom surface without hitting your paddle 
Press 'R' to restart after game over 

## Scoring

+1 point for each wall hit (top, sides, front, back) 
No points for bouncing off the paddle 
The game ends when you miss the ball with the paddle 
