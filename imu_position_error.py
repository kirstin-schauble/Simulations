"""
This is a simple simulation of cross-track position error based on IMU bias instability and angle random walk.
To run, set desired IMU specs, time, and velocity in main() and run the script.

Author: Kirstin Schauble - kirstin.schauble@anellophotonics.com
"""

import numpy as np
import matplotlib.pyplot as plt

def imu_position_error(bi, arw, T, dt, velocity, incl_bi, incl_arw):
    # Initialize variables
    t = np.arange(0, T, dt)
    N = len(t)

    for j in range(len(bi)):
        for k in range(len(arw)):
            # Initialize variables
            angle_bi = np.zeros(N)
            angle_arw = np.zeros(N)
            error_bi = np.zeros(N)
            error_arw = np.zeros(N)
            error = np.zeros(N)

            # Create legend labels
            if len(bi) > 1:
                legend_label = f'BI = {bi[j]} deg/hr'
            elif len(arw) >1:
                legend_label = f'ARW = {arw[k]} deg/rt(hr)'
            else:
                # legend_label = f'BI = {bi[j]} deg/hr; ARW = {arw[k]} deg/rt(hr)'
                legend_label = f'Velocity = {velocity} mph'

            # convert velocity, BI and ARW units
            velocity_mps = velocity/2.237 # mph to m/s
            bi_rad = [x * np.pi/180 / 3600 for x in bi] # deg/hr to rad/s
            arw_rad = [x * np.pi/180 / np.sqrt(3600) for x in arw] # deg/rthr to rad/rtsec


            for i in range(1, N):
                # add error from BI
                if incl_bi:
                    angle_bi[i] = angle_bi[i-1] + bi_rad[j] * dt # rad
                    error_bi[i] = error_bi[i-1] + velocity_mps * np.tan(angle_bi[i]) * dt # m

                # add angle error from ARW
                if incl_arw:
                    angle_arw[i] = arw_rad[k] * np.sqrt(t[i]) # rad
                    error_arw[i] = t[i] * velocity_mps * np.tan(angle_arw[i]) # m

                # total error
                error[i] = error_bi[i] + error_arw[i]

            # Plot
            plt.plot(t/60, error, label=legend_label)
            plt.legend()
    
    return error, t


def main():
    #Specs to include in simulation
    incl_bi = True
    incl_arw = True

    #IMU specs
    bi = [0.3] # bias instability in deg/hr
    arw = [0.03] # angle rangom walk in deg/rthr

    #Other parameters
    T = 3000 # total simulation time in seconds
    velocity = 30 # mph

    dt = 1 # time step in seconds
    error, t = imu_position_error(bi, arw, T, dt, velocity, incl_bi, incl_arw)

    plt.xlabel('Time (min)')
    plt.ylabel('Cross-track Error (m)')
    plt.grid()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()