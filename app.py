import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import math

# Dictionary for gravitational accelerations on different planets (all negative for downward direction)
planetary_gravity = {
    'Mercury': -3.7,
    'Venus': -8.87,
    'Earth': -9.81,
    'Moon': -1.62,
    'Mars': -3.71,
    'Jupiter': -24.79,
    'Saturn': -10.44,
    'Uranus': -8.69,
    'Neptune': -11.15,
    'Other (Custom)': None  # This option will allow custom input
}

# Function to calculate total fall time based on height, initial velocity, and acceleration
def calculate_fall_time(height, initial_velocity, acceleration):
    # Using the equation of motion: h = v0 * t + 0.5 * a * t^2, solve for t
    discriminant = initial_velocity**2 - 2 * acceleration * height
    if discriminant < 0:
        return None  # No real solution
    t1 = (-initial_velocity + math.sqrt(discriminant)) / acceleration
    t2 = (-initial_velocity - math.sqrt(discriminant)) / acceleration
    # Take the positive time (t2 in most cases due to downward acceleration)
    return max(t1, t2)

# Function to simulate motion with randomization and calculate the fall time
def simulate_random_motion(initial_velocity, base_acceleration, time_step, randomness_factor, start_height):
    times = []
    positions = []
    velocities = []
    accelerations = []
    
    current_position = start_height  # Start at the designated height
    current_velocity = initial_velocity
    fall_time = None
    t = 0  # Starting time

    while current_position > 0:  # Simulate until the object reaches the ground
        times.append(t)

        # Randomize the acceleration if randomness is applied
        random_acceleration = base_acceleration + random.uniform(-randomness_factor, randomness_factor)
        accelerations.append(random_acceleration)
        
        # Update velocity and position
        current_velocity += random_acceleration * time_step
        velocities.append(current_velocity)
        
        current_position += current_velocity * time_step
        current_position = max(0, current_position)  # Ensure position does not go below zero
        positions.append(current_position)
        
        t += time_step  # Increment time

    fall_time = t  # Record the time when the object hits the ground

    # Create a DataFrame
    data = {
        'Time (s)': times,
        'Position (m)': positions,
        'Velocity (m/s)': velocities,
        'Acceleration (m/s²)': accelerations
    }
    df = pd.DataFrame(data)
    return df, fall_time

# Streamlit app
st.image("https://github.com/kolbm/Dynamics-Simulator/blob/main/logo.jpg?raw=true")
st.title("Mr. Kolb's Dynamics Simulator")

# Inputs for the simulation with clarifications
st.subheader("Simulation Parameters")
initial_velocity = st.number_input('Initial Velocity (m/s)', value=0.0, help="The velocity of the object at time zero.")

# Drop-down for planetary gravitational acceleration (all accelerations are downward)
planet = st.selectbox('Select a planet or choose "Other" for custom acceleration:', list(planetary_gravity.keys()))

# Set the base acceleration based on planet selection
if planet == 'Other (Custom)':
    base_acceleration = st.number_input('Custom Acceleration (m/s²)', value=-9.81, help="Enter a custom acceleration. Default is -9.81 m/s² for Earth-like gravity.")
else:
    base_acceleration = planetary_gravity[planet]
    st.write(f'Downward gravitational acceleration on {planet}: {base_acceleration} m/s²')

# Option to choose between time or height input (default to "Height")
input_method = st.radio("Choose input method:", options=["Height", "Time"], index=0)

if input_method == "Time":
    total_time = st.number_input('Total Time (s)', value=10.0, help="The total duration for the simulation in seconds.")
    start_height = 0  # Default start height is zero if time-based input is used
else:
    start_height = st.number_input('Drop Height (m)', value=10.0, help="The height from which the object is dropped.")
    calculated_fall_time = calculate_fall_time(start_height, initial_velocity, base_acceleration)
    if calculated_fall_time is None:
        st.error("The drop height or initial velocity results in no real solution. Please adjust your parameters.")
    else:
        st.markdown(f'**Calculated fall time (no randomness): {calculated_fall_time:.2f} seconds**')

# Checkbox for enabling/disabling randomness
use_randomness = st.checkbox('Include randomness in acceleration', value=True)
randomness_factor = st.number_input('Randomness Factor (m/s²)', value=1.0 if use_randomness else 0.0, disabled=not use_randomness, help="Adds variability to the acceleration. Set to 0 for deterministic motion.")

# Error handling: Ensure time_step and total_time are positive
time_step = st.number_input('Time Step (s)', value=0.1, help="The interval for calculating the object's position, velocity, and acceleration.")
if time_step <= 0:
    st.error("Time step must be a positive value.")
elif calculated_fall_time is not None and calculated_fall_time <= 0:
    st.error("Total time must be a positive value.")
else:
    # Run the simulation
    if st.button('Simulate Motion'):
        df, simulated_fall_time = simulate_random_motion(initial_velocity, base_acceleration, time_step, randomness_factor if use_randomness else 0.0, start_height)

        # Display the DataFrame
        st.subheader('Simulation Data')
        st.write(df)

        if simulated_fall_time is not None:
            st.markdown(f'**Simulated fall time (with randomness): {simulated_fall_time:.2f} seconds**')

            # Display the difference between calculated and simulated fall times
            fall_time_difference = abs(calculated_fall_time - simulated_fall_time)
            st.markdown(f'**Difference between calculated and simulated fall time: {fall_time_difference:.2f} seconds**')
        else:
            st.write("The object never hit the ground within the simulated time.")

        # Plot the position vs time
        st.subheader('Position vs Time')
        plt.figure(figsize=(8, 5))
        plt.plot(df['Time (s)'], df['Position (m)'], label='Position (m)', color='blue')
        plt.xlabel('Time (s)')
        plt.ylabel('Position (m)')
        plt.title('Object Position Over Time')
        plt.grid(True)
        plt.legend()  # Add a legend for clarity
        st.pyplot(plt)

        # Plot the velocity vs time
        st.subheader('Velocity vs Time')
        plt.figure(figsize=(8, 5))
        plt.plot(df['Time (s)'], df['Velocity (m/s)'], label='Velocity (m/s)', color='orange')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity (m/s)')
        plt.title('Object Velocity Over Time')
        plt.grid(True)
        plt.legend()  # Add a legend for clarity
        st.pyplot(plt)

        # Plot the acceleration vs time
        st.subheader('Acceleration vs Time')
        plt.figure(figsize=(8, 5))
        plt.plot(df['Time (s)'], df['Acceleration (m/s²)'], label='Acceleration (m/s²)', color='green')
        plt.xlabel('Time (s)')
        plt.ylabel('Acceleration (m/s²)')
        plt.title('Object Acceleration Over Time')
        plt.grid(True)
        plt.legend()  # Add a legend for clarity
        st.pyplot(plt)

        # Download the data as a CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name='motion_simulation.csv',
            mime='text/csv'
        )
