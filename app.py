import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Function to simulate motion
def simulate_motion(initial_velocity, acceleration, time_step, total_time):
    times = np.arange(0, total_time + time_step, time_step)
    positions = initial_velocity * times + 0.5 * acceleration * times**2
    velocities = initial_velocity + acceleration * times
    accelerations = np.full_like(times, acceleration)

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
st.title('Object Motion Simulator')

# Inputs for the simulation
initial_velocity = st.number_input('Initial Velocity (m/s)', value=0.0)
acceleration = st.number_input('Acceleration (m/s²)', value=9.81)
time_step = st.number_input('Time Step (s)', value=0.1)
total_time = st.number_input('Total Time (s)', value=10.0)

# Run the simulation
if st.button('Simulate Motion'):
    df = simulate_motion(initial_velocity, acceleration, time_step, total_time)

    # Display the DataFrame
    st.subheader('Simulation Data')
    st.write(df)

    # Plot the position vs time
    st.subheader('Position vs Time')
    plt.figure(figsize=(8, 5))
    plt.plot(df['Time (s)'], df['Position (m)'], label='Position (m)')
    plt.xlabel('Time (s)')
    plt.ylabel('Position (m)')
    plt.title('Object Position Over Time')
    plt.grid(True)
    st.pyplot(plt)

    # Download the data as a CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='motion_simulation.csv',
        mime='text/csv'
    )
