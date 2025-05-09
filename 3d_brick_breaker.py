import sys 
import math 
from OpenGL.GL import * 
from OpenGL.GLU import * 
from OpenGL.GLUT import * 
import random 
import pygame

pygame.mixer.init()
hit_sound = pygame.mixer.Sound('hit.mp3')
game_over_sound = pygame.mixer.Sound('gameover.mp3')

SCRW, SCRH = 1740, 980  # Screen dimensions
FPS, BOX_W, SPHERE_R = 60, 20, 0.5  # Game settings
scr_w, scr_h = SCRW, SCRH  # Current window size (adjustable)
ang, ang_d = 0.0, 0.0  # Angle variables (for animations)
bx, by, bz = 0.0, 0.0, 0.0  # Ball position
dx, dy, dz = 0.0, 0.0, 0.0  # Ball velocity
cx, cy, cz = 0.0, 0.0, 0.0  # Collision point (for hit effects)
hit, hit_dir = 0.0, 0  # Hit animation control
game_over = False  # Game state
score = 0  # Player score

# Mouse rotation controls
mouse_x, mouse_y = 0, 0  # Current mouse position
rotate_x, rotate_y = 0, 0  # Camera rotation angles
is_rotating = False  # Is mouse dragging active?
last_x, last_y = 0, 0  # Previous mouse position

# Paddle (plane) settings
plane_x, plane_z = 0.0, 0.0  # Paddle position
plane_w, plane_h = 4.0, 2.0  # Paddle width & height
plane_y = -BOX_W / 2  # Paddle sits at the bottom

def init_work(): 
    global ang_d, dx, dy, dz, game_over, score, rotate_x, rotate_y
    game_over = False
    score = 0
    rotate_x, rotate_y = 0, 0  # Reset view rotation
    ang_d = 360.0 / (FPS * 30) 
    base_speed = (float(BOX_W) / float(FPS)) * 0.5 
    angle_xy = random.uniform(0, 2 * math.pi) 
    angle_z = random.uniform(-math.pi/4, math.pi/4) 
 
    dx = base_speed * math.cos(angle_xy) * math.cos(angle_z) 
    dy = base_speed * math.sin(angle_xy) * math.cos(angle_z) 
    dz = base_speed * math.sin(angle_z) 
 
def draw_circle(bx, by, bz, r, hit_dir): 
    glPushMatrix()
    glTranslatef(bx, by, bz)
    quad = gluNewQuadric()
    gluSphere(quad, r, 20, 20)
    gluDeleteQuadric(quad)
    glPopMatrix()
 
def draw_all_surfaces_with_grid(size): 
    faces = ['bottom', 'top', 'front', 'back', 'left', 'right'] 
    for face in faces: 
        draw_grid(size, face) 
 
def draw_grid(size, face='bottom'): 
    DIV = 10 
    step = size / DIV 
    half = size / 2 
 
    glPushMatrix() 
 
    if face == 'bottom': 
        glTranslatef(0, -half, 0) 
    elif face == 'top': 
        glRotatef(180, 1, 0, 0) 
        glTranslatef(0, -half, 0) 
    elif face == 'front': 
        glRotatef(90, 1, 0, 0) 
        glTranslatef(0, -half, 0) 
    elif face == 'back': 
        glRotatef(-90, 1, 0, 0) 
        glTranslatef(0, -half, 0) 
    elif face == 'left': 
        glRotatef(90, 0, 0, 1) 
        glTranslatef(0, -half, 0) 
    elif face == 'right': 
        glRotatef(-90, 0, 0, 1) 
        glTranslatef(0, -half, 0) 
 
    glBegin(GL_LINES) 
    for i in range(DIV + 1): 
        x = -half + i * step 
        glVertex3f(x, 0, -half) 
        glVertex3f(x, 0, half) 
        z = -half + i * step 
        glVertex3f(-half, 0, z) 
        glVertex3f(half, 0, z) 
    glEnd() 
 
    glPopMatrix() 
 
def draw_plane(): 
    glPushMatrix() 
    glTranslatef(plane_x, plane_y + 0.01, plane_z)  # small lift so it doesn't blend with floor 
    glScalef(plane_w, 0.1, plane_h) 
    glColor3f(1.0, 0.0, 0.0)  # red plane 
    glutSolidCube(1.0) 
    glPopMatrix() 

def draw_text(x, y, text):
    glDisable(GL_LIGHTING)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, scr_w, 0, scr_h)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glColor3f(1, 1, 1)  # White text
    glRasterPos2f(x, y)
    for character in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(character))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_LIGHTING)
 
def draw_func(): 
    global bx, by, bz, hit, hit_dir, cx, cy, cz, scr_h 
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
 
    light0pos = [BOX_W * 0.25, BOX_W * 1.0, BOX_W * 0.5, 0] 
    light0def = [1, 1, 1, 1] 
    light0spe = [1, 1, 1, 1] 
    light0amb = [0.5, 0.5, 1.0, 1.0] 
    glDisable(GL_LIGHTING) 
    glEnable(GL_LIGHTING) 
    glEnable(GL_NORMALIZE) 
    glLightfv(GL_LIGHT0, GL_POSITION, light0pos) 
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light0def) 
    glLightfv(GL_LIGHT0, GL_SPECULAR, light0spe) 
    glLightfv(GL_LIGHT0, GL_AMBIENT, light0amb) 
    glLoadIdentity() 
    
    # Set camera position with rotation
    r = (BOX_W / 2) + 15 
    glTranslatef(0, 0, -r)  # Move back to initial position
    glRotatef(rotate_x, 1, 0, 0)  # Rotate around X axis
    glRotatef(rotate_y, 0, 1, 0)  # Rotate around Y axis
 
    glScalef(1.0, 1.0, 1.0) 
    glDisable(GL_LIGHT0) 
    glDisable(GL_LIGHTING) 
 
    if hit == 0.0: 
        glColor3f(0.0, 0.0, 0.8) 
    else: 
        glColor3f(hit, hit, 0.8 + 0.2 * hit) 
 
    draw_all_surfaces_with_grid(BOX_W) 
    glutWireCube(BOX_W) 
 
    if hit > 0.0: 
        glColor3f(0.0, hit, hit) 
        draw_circle(cx, cy, cz, 0.1 + 2.0 - 2.0 * hit, hit_dir) 
 
    # Draw the plane (paddle) 
    draw_plane() 
 
    glEnable(GL_LIGHTING) 
    glEnable(GL_LIGHT0) 
    glPushMatrix() 
    glTranslatef(bx, by, bz) 
 
    if hit == 0.0: 
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.0, 1.0, 0.0, 1.0]) 
    else: 
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [hit, 1.0 - hit, 0.0, 1.0]) 
        hit -= 0.03 
        if hit <= 0.0: 
            hit = 0.0 
 
    quadric = gluNewQuadric() 
    radius = SPHERE_R 
    slices = 32 
    stacks = 16 
    gluSphere(quadric, radius, slices, stacks) 
 
    glPopMatrix() 
    
    # Draw score
    draw_text(20, scr_h - 30, f"Score: {score}")
    
    # Draw game over message if needed
    if game_over:
        draw_text(scr_w/2 - 100, scr_h/2, f"GAME OVER! Final Score: {score}")
        draw_text(scr_w/2 - 100, scr_h/2 - 30, "Press R to restart")
    
    glutSwapBuffers() 
 
def on_timer(value): 
    global bx, by, bz, dx, dy, dz, cx, cy, cz, hit, hit_dir, score, game_over
    
    if game_over:
        glutPostRedisplay()
        glutTimerFunc(int(1000 / FPS), on_timer, 0)
        return
 
    bx += dx 
    by += dy 
    bz += dz 
 
    hit -= 0.03 
    if hit < 0.0: 
        hit = 0.0 
 
    w = BOX_W / 2.0 
    if bx - SPHERE_R <= -w or bx + SPHERE_R >= w: 
        dx *= -1 
        hit, hit_dir = 1.0, 0 
        cx, cy, cz = bx + (SPHERE_R * (-1 if (bx - SPHERE_R <= -w) else 1)), by, bz
        score += 1  # Increment score for side wall hits
        hit_sound.play()
    if by - SPHERE_R <= -w or by + SPHERE_R >= w: 
        # Check if it's the bottom surface (game over condition)
        if by - SPHERE_R <= -w:
            # Check if paddle missed the ball
            if not (plane_x - plane_w/2 <= bx <= plane_x + plane_w/2) or not (plane_z - plane_h/2 <= bz <= plane_z + plane_h/2):
                game_over = True
                game_over_sound.play()
        dy *= -1 
        hit, hit_dir = 1.0, 1 
        cx, cy, cz = bx, by + (SPHERE_R * (-1 if (by - SPHERE_R <= -w) else 1)), bz
        if by + SPHERE_R >= w:  # Only increment score for top wall hits
            score += 1
            hit_sound.play()
    if bz - SPHERE_R <= -w or bz + SPHERE_R >= w: 
        dz *= -1 
        hit, hit_dir = 1.0, 2 
        cx, cy, cz = bx, by, bz + (SPHERE_R * (-1 if (bz - SPHERE_R <= -w) else 1))
        score += 1  # Increment score for front/back wall hits
        hit_sound.play()
 
    # Check collision with the plane (only when ball going down) 
    if dy < 0 and (abs(by - plane_y) <= SPHERE_R + 0.1): 
        if (plane_x - plane_w/2 <= bx <= plane_x + plane_w/2) and (plane_z - plane_h/2 <= bz <= plane_z + plane_h/2): 
            dy *= -1 
            hit, hit_dir = 1.0, 1 
            cx, cy, cz = bx, by, bz 
 
    glutPostRedisplay() 
    glutTimerFunc(int(1000 / FPS), on_timer, 0) 
 
def keyboard_func(key, x, y): 
    global plane_x, plane_z, game_over, score, bx, by, bz, dx, dy, dz, hit, hit_dir
    
    if game_over and key == b'r':
        bx, by, bz = 0.0, 0.0, 0.0 
        dx, dy, dz = 0.0, 0.0, 0.0 
        init_work()
        return
    
    if game_over:
        return
    
    move_step = 0.5 
 
    if key == b'a': 
        plane_x -= move_step 
    elif key == b'd': 
        plane_x += move_step 
    elif key == b's': 
        plane_z += move_step 
    elif key == b'w': 
        plane_z -= move_step 
 
    # Keep plane inside the box 
    half_w = BOX_W/2 
    plane_x = max(-half_w + plane_w/2, min(half_w - plane_w/2, plane_x)) 
    plane_z = max(-half_w + plane_h/2, min(half_w - plane_h/2, plane_z)) 

def mouse_motion(x, y):
    global rotate_x, rotate_y, last_x, last_y, is_rotating
    
    if is_rotating:
        dx = x - last_x
        dy = y - last_y
        
        rotate_y += dx * 0.5
        rotate_x += dy * 0.5
        
        # Clamp vertical rotation to prevent flipping
        rotate_x = max(-90, min(90, rotate_x))
        
    last_x, last_y = x, y
    glutPostRedisplay()

def mouse_button(button, state, x, y):
    global is_rotating, last_x, last_y
    
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            is_rotating = True
            last_x, last_y = x, y
        else:
            is_rotating = False
 
def main(): 
    glutInit(sys.argv) 
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH) 
    glutInitWindowSize(SCRW, SCRH) 
    glutCreateWindow(b"3D Brick Breaker Style Ball Game with Paddle - PyOpenGL") 
    glMatrixMode(GL_PROJECTION) 
    gluPerspective(75.0, float(SCRW) / float(SCRH), 0.1, 100.0) 
    glMatrixMode(GL_MODELVIEW) 
    glEnable(GL_DEPTH_TEST) 
    
    # Register new callbacks
    glutMotionFunc(mouse_motion)
    glutMouseFunc(mouse_button)
    
    init_work() 
    glutDisplayFunc(draw_func) 
    glutTimerFunc(int(1000 / FPS), on_timer, 0) 
    glutKeyboardFunc(keyboard_func) 
    glutMainLoop() 
 
if __name__ == "__main__": 
    main()