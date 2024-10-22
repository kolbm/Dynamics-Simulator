import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

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
base_acceleration = st.number_input('Base Acceleration (m/s²)', value=-10.0, help="The average acceleration applied to the object. Default is -10 m/s² for simulating gravity.")
time_step = st.number_input('Time Step (s)', value=0.1, help="The interval for calculating the object's position, velocity, and acceleration.")
total_time = st.number_input('Total Time (s)', value=10.0, help="The total duration for the simulation in seconds.")

# Checkbox for enabling/disabling randomness
use_randomness = st.checkbox('Include randomness in acceleration', value=True)
randomness_factor = st.number_input('Randomness Factor (m/s²)', value=1.0 if use_randomness else 0.0, disabled=not use_randomness, help="Adds variability to the acceleration. Set to 0 for deterministic motion.")

# Error handling: Ensure time_step and total_time are positive
if time_step <= 0 or total_time <= 0:
    st.error("Time step and total time must be positive values.")
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
