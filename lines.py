import math

# def create_line(frame, )

def estimate_distance_from_screen(face_bounds):
    x, y, w, h = face_bounds
    # 200 -> 3 ft? 
    # 275 -> 2.5 ft
    # 350 -> 2 ft 
    # 450 -> 1.5 ft 
    # 550 -> 1 ft 
    # 650 =  ft  
    
    return 650 + 8 * x




def get_projected_point(point_a, point_camera, theta, e):
    # point_a: 3D position that will be projected
    # point_camera: 3D position of the camera 
    # theta: the orientation of the camera
    # e: the display surface position relative to the camera pinhole
    #  
    # return b: the 2D projection of a 
    c_x, c_y, c_z = point_camera
    a_x, a_y, a_z = point_a 
    theta_x, theta_y, theta_z = theta 
    e_x, e_y, e_z = e


    x = a_x - c_x 
    y = a_y - c_y 
    z = a_z - c_z

    d_x = c_y * (math.sin(theta_z) * y + c_z * x) - math.sin(theta_y) * z 
    d_y = math.sin(theta_x) * (c_y * z + math.sin(theta_y) * (math.sin(theta_z) * y + c_z * x)) + c_x * (c_z * y - math.sin(theta_z) * x)
    d_z = c_x * (c_y * z + math.sin(theta_y) * (math.sin(theta_z) * y + c_z * x)) - math.sin(theta_x) * (c_z * y - math.sin(theta_z) * x)

    b_x = ( e_z / d_z ) * d_x + e_x
    b_y = ( e_z / d_z ) * d_y + e_y
    return (b_x, b_y)