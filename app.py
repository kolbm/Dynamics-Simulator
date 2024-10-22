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

# Function to simulate motion with randomization
def simulate_random_motion(initial_velocity, base_acceleration, time_step, total_time, randomness_factor):
    times = np.arange(0, total_time + time_step, time_step)
    positions = []
    velocities = []
    accelerations = []
    
    current_position = 0
    current_velocity = initial_velocity
    
    for t in times:
        # Randomize the acceleration if randomness is applied
        random_acceleration = base_acceleration + random.uniform(-randomness_factor, randomness_factor)
        accelerations.append(random_acceleration)
        
        # Update velocity and position
        current_velocity += random_acceleration * time_step
        velocities.append(current_velocity)
        
        current_position += current_velocity * time_step
        positions.append(current_position)
    
    # Create a DataFrame
    data = {
        'Time (s)': times,
        'Position (m)': positions,
        'Velocity (m/s)': velocities,
        'Acceleration (m/s²)': accelerations
    }
    df = pd.DataFrame(data)
    return df

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

# Option to choose between time or height input
input_method = st.radio("Choose input method:", options=["Time", "Height"])

if input_method == "Time":
    total_time = st.number_input('Total Time (s)', value=10.0, help="The total duration for the simulation in seconds.")
else:
    height = st.number_input('Drop Height (m)', value=10.0, help="The height from which the object is dropped.")
    total_time = calculate_fall_time(height, initial_velocity, base_acceleration)
    if total_time is None:
        st.error("The drop height or initial velocity results in no real solution. Please adjust your parameters.")
    else:
        st.write(f'Calculated fall time: {total_time:.2f} seconds')

# Checkbox for enabling/disabling randomness
use_randomness = st.checkbox('Include randomness in acceleration', value=True)
randomness_factor = st.number_input('Randomness Factor (m/s²)', value=1.0 if use_randomness else 0.0, disabled=not use_randomness, help="Adds variability to the acceleration. Set to 0 for deterministic motion.")

# Error handling: Ensure time_step and total_time are positive
time_step = st.number_input('Time Step (s)', value=0.1, help="The interval for calculating the object's position, velocity, and acceleration.")
if time_step <= 0:
    st.error("Time step must be a positive value.")
elif total_time is not None and total_time <= 0:
    st.error("Total time must be a positive value.")
else:
    # Run the simulation
    if st.button('Simulate Motion'):
        df = simulate_random_motion(initial_velocity, base_acceleration, time_step, total_time, randomness_factor if use_randomness else 0.0)

        # Display the DataFrame
        st.subheader('Simulation Data')
        st.write(df)

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
