# ---- Cam1 position 1 (cam1 far distance (upstream) from focus, cam2 at focus), motors at 1&2 (in order laser reaches them)
# ---- SVD singular values: Y(352,5.54), X(77,3.9)
"""
y_cam1_pix_to_motor1_steps = -7.5  # How many motor steps on motor 1 does a 1 pixel y-shift on camera 1 correspond to?
y_cam1_pix_to_motor3_steps = -12.5  # etc.
y_cam2_pix_to_motor1_steps = -13
y_cam2_pix_to_motor3_steps = -20    # These numbers have units of (motor_steps / camera_pixels)

x_cam1_pix_to_motor2_steps = 6    # How many motor steps on motor 2 does a 1 pixel x-shift on camera 1 correspond to?
x_cam1_pix_to_motor4_steps = 6.5    # etc.
x_cam2_pix_to_motor2_steps = 13
x_cam2_pix_to_motor4_steps = 11
"""

# ---- Cam1 position 2 (cam1 medium distance (upstream) from focus, cam2 at focus), motors at 1&2 (in order laser reaches them)
# ---- SVD singular values: Y(300,6.8), X(173,4.81)
"""
y_cam1_pix_to_motor1_steps = -10.7  # How many motor steps on motor 1 does a 1 pixel y-shift on camera 1 correspond to?
y_cam1_pix_to_motor3_steps = -14.9  # etc.
y_cam2_pix_to_motor1_steps = -13
y_cam2_pix_to_motor3_steps = -20    # These numbers have units of (motor_steps / camera_pixels)

x_cam1_pix_to_motor2_steps = 8.5    # How many motor steps on motor 2 does a 1 pixel x-shift on camera 1 correspond to?
x_cam1_pix_to_motor4_steps = 8.1    # etc.
x_cam2_pix_to_motor2_steps = 13
x_cam2_pix_to_motor4_steps = 11
"""

# ---- Cam1 position 3 (cam1 at focus, cam2 at focus), motors at 1&2 (in order laser reaches them)
# ---- SVD singular values: Y(619,7.67), X(354,5.42)
"""
y_cam1_pix_to_motor1_steps = -13.1  # How many motor steps on motor 1 does a 1 pixel y-shift on camera 1 correspond to?
y_cam1_pix_to_motor3_steps = -19.1  # etc.
y_cam2_pix_to_motor1_steps = -13
y_cam2_pix_to_motor3_steps = -20    # These numbers have units of (motor_steps / camera_pixels)

x_cam1_pix_to_motor2_steps = 10.6   # How many motor steps on motor 2 does a 1 pixel x-shift on camera 1 correspond to?
x_cam1_pix_to_motor4_steps = 9.55    # etc.
x_cam2_pix_to_motor2_steps = 13
x_cam2_pix_to_motor4_steps = 11
"""

# ---- Cam1 position 4 (cam1 medium distance (downstream) from focus, cam2 at focus), motors at 1&2 (in order laser reaches them)
# ---- SVD singular values: Y(219,8.89), X(361,6.3)
"""
y_cam1_pix_to_motor1_steps = -19.4  # How many motor steps on motor 1 does a 1 pixel y-shift on camera 1 correspond to?
y_cam1_pix_to_motor3_steps = -24.9  # etc.
y_cam2_pix_to_motor1_steps = -13
y_cam2_pix_to_motor3_steps = -20    # These numbers have units of (motor_steps / camera_pixels)

x_cam1_pix_to_motor2_steps = 14.2   # How many motor steps on motor 2 does a 1 pixel x-shift on camera 1 correspond to?
x_cam1_pix_to_motor4_steps = 12.9   # etc.
x_cam2_pix_to_motor2_steps = 13
x_cam2_pix_to_motor4_steps = 11
"""

# ---- Motors 2&3 (cam1 close but not at focus (downstream), cam2 at focus, mir1 upstream, mir2 downstream)
# ---- SVD singular values: Y(292,9.73), X(503,5.47)
"""
y_cam1_pix_to_motor1_steps = -23.5  # How many motor steps on motor 1 does a 1 pixel y-shift on camera 1 correspond to?
y_cam1_pix_to_motor3_steps = -20.5  # etc.
y_cam2_pix_to_motor1_steps = -17.7
y_cam2_pix_to_motor3_steps = -17.7  # These numbers have units of (motor_steps / camera_pixels)

x_cam1_pix_to_motor2_steps = 11.2  # How many motor steps on motor 2 does a 1 pixel x-shift on camera 1 correspond to?
x_cam1_pix_to_motor4_steps = 11.7  # etc.
x_cam2_pix_to_motor2_steps = 10.5
x_cam2_pix_to_motor4_steps = 10.5
"""

# ---- Motors 2&3 (cam1 close but not at focus (downstream), cam2 at focus, mir1 upstream, mir2 downstream)
    # ---- After recalibrating some X values, no physical changes from last one
# ---- SVD singular values: Y(292,9.73), X(107,6.55)
"""
y_cam1_pix_to_motor1_steps = -23.5  # How many motor steps on motor 1 does a 1 pixel y-shift on camera 1 correspond to?
y_cam1_pix_to_motor3_steps = -20.5  # etc.
y_cam2_pix_to_motor1_steps = -17.7
y_cam2_pix_to_motor3_steps = -17.7  # These numbers have units of (motor_steps / camera_pixels)

x_cam1_pix_to_motor2_steps = 14.5  # How many motor steps on motor 2 does a 1 pixel x-shift on camera 1 correspond to?
x_cam1_pix_to_motor4_steps = 15.0  # etc.
x_cam2_pix_to_motor2_steps = 10.5
x_cam2_pix_to_motor4_steps = 14.0
"""

# ---- First setup after changing to Z shape setup. Cam1 close to focus, Cam2 at focus. Mot1 far from lens, Mot2 close to lens
# ---- SVD singular values: Y(123,6.18), X(142,5.60)
"""
y_cam1_pix_to_motor1_steps = -14.7  # How many motor steps on motor 1 does a 1 pixel y-shift on camera 1 correspond to?
y_cam1_pix_to_motor3_steps = -11.4  # etc.
y_cam2_pix_to_motor1_steps = -12.3
y_cam2_pix_to_motor3_steps = -11.7  # These numbers have units of (motor_steps / camera_pixels)

x_cam1_pix_to_motor2_steps = 16.3  # How many motor steps on motor 2 does a 1 pixel x-shift on camera 1 correspond to?
x_cam1_pix_to_motor4_steps = 9.5  # etc.
x_cam2_pix_to_motor2_steps = 13.4
x_cam2_pix_to_motor4_steps = 9.3
"""