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
        # Randomize the acceleration
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
st.title('Mr. Kolb's Randomized Object Motion Simulator')

# Inputs for the simulation
initial_velocity = st.number_input('Initial Velocity (m/s)', value=0.0)
base_acceleration = st.number_input('Base Acceleration (m/s²)', value=9.81)
time_step = st.number_input('Time Step (s)', value=0.1)
total_time = st.number_input('Total Time (s)', value=10.0)
randomness_factor = st.number_input('Randomness Factor (m/s²)', value=1.0)

# Run the simulation
if st.button('Simulate Randomized Motion'):
    df = simulate_random_motion(initial_velocity, base_acceleration, time_step, total_time, randomness_factor)

    # Display the DataFrame
    st.subheader('Randomized Simulation Data')
    st.write(df)

    # Plot the position vs time
    st.subheader('Position vs Time')
    plt.figure(figsize=(8, 5))
    plt.plot(df['Time (s)'], df['Position (m)'], label='Position (m)')
    plt.xlabel('Time (s)')
    plt.ylabel('Position (m)')
    plt.title('Randomized Object Position Over Time')
    plt.grid(True)
    st.pyplot(plt)

    # Download the data as a CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='random_motion_simulation.csv',
        mime='text/csv'
    )
