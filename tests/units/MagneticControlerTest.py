from src.magnetic_controller import MagneticController

print(MagneticController._calculate_angle(None, [0,0,-1], [0,1,0], lambda x: x[1:]))
