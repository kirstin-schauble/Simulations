import math
import numpy as np
import matplotlib.pyplot as plt

def calculate_position_error(scale_factor_error, turn_rate, speed, duration):
    """
    Calculate the position error due to scale factor error during a turn

    Parameters:
        scale_factor_error (float): Error in the rate gyro scale factor
        turn_rate (float): Rate of the turn in degrees per second
        speed (float): Speed of the vehicle in meters per second
        duration (float): Duration of the turn in seconds

    Returns:
        position_error (float): Position error in meters
    """
    # Calculate true turn radius
    true_rate = math.radians(turn_rate) # Convert turn rate to radians per second
    true_radius = speed / true_rate

    # Calculate perceived turn radius with scale factor error
    perceived_rate = true_rate * (1 + scale_factor_error)
    perceived_radius = speed / perceived_rate

    # Calculate true circumference and perceived circumference
    true_circumference = 2 * math.pi * true_radius
    perceived_circumference = 2 * math.pi * perceived_radius

    # Calculate distance traveled and fraction of circle traveled
    distance_traveled = speed * duration
    true_fraction = distance_traveled / true_circumference
    perceived_fraction = distance_traveled / perceived_circumference

    # Calculate theta angles in radians
    true_theta = 2 * math.pi * true_fraction
    perceived_theta = 2 * math.pi * perceived_fraction

    # Calculate x and y positions of true and perceived trajectories
    true_x = true_radius*np.sin(true_theta)
    true_y = true_radius*np.cos(true_theta)
    perceived_x = perceived_radius*np.sin(perceived_theta)
    perceived_y = perceived_radius*np.cos(perceived_theta)
    
    # Calculate 2D position error in meters
    x_error = (perceived_x - true_x)
    y_error = (perceived_y - true_y)
    position_error = np.sqrt(x_error**2 + y_error**2)

    return position_error

def main():
    # Example inputs
    turn_rate = 10 # degrees per second
    speed = 2.8 # meters per second
    duration = 0.25 # seconds

    # Range of scale factor errors to test
    scale_factor_errors = np.arange(-0.01, 0.011, 0.001)

    # Calculate position error for each scale factor error
    position_errors = []
    for error in scale_factor_errors:
        position_error = calculate_position_error(error, turn_rate, speed, duration)
        position_errors.append(position_error)

    # Plot position error vs. scale factor error
    plt.plot(scale_factor_errors*100, position_errors)
    plt.xlabel('Scale Factor Error (%)')
    plt.ylabel('Position Error (meters)')
    plt.title('Position Error vs. Scale Factor Error')
    plt.show()

if __name__ == '__main__':
    main()