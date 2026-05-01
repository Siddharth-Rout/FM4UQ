import torch 
import numpy as np
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class BoW:
    def __init__(self, amplitude=1.0, skewness=0.5, angular_velocity=1.0, phase_constant=0.0, device = 'cpu'):
        self.amplitude = amplitude
        self.skewness = skewness
        self.angular_velocity = angular_velocity
        self.phase_constant = phase_constant
        self.device = device

    def state(self, time):
        time = time.to(self.device)
        state_x = self.amplitude * torch.sin(self.angular_velocity * time + self.phase_constant)
        state_y = self.skewness * self.amplitude * torch.cos(self.skewness * self.angular_velocity * time + self.phase_constant)

        return state_x, state_y
    
    def velocity(self, time):
        time = time.to(self.device)
        vel_x = self.angular_velocity * self.amplitude * torch.cos(self.angular_velocity * time + self.phase_constant)
        vel_y = - self.skewness * self.angular_velocity * self.skewness * self.amplitude * torch.sin(self.skewness * self.angular_velocity * time + self.phase_constant)

        return vel_x, vel_y
    
    def speed(self, time):
        vel_x, vel_y = self.velocity(time)
        speed = torch.sqrt(vel_x**2 + vel_y**2)
        return speed

    def plot_state_space(self, time):
        state_x, state_y = self.state(time)
        plt.plot(state_x.cpu(), state_y.cpu())
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.xlim(-self.amplitude - 1 , self.amplitude + 1)
        plt.ylim(-self.amplitude - 1 , self.amplitude + 1)
        plt.title("State Space")
        plt.show()

    def plot_spacetime_x(self, time):
        state_x, _ = self.state(time)
        plt.plot(time.cpu(), state_x.cpu())
        plt.xlabel("time")
        plt.ylabel("X")
        plt.title("Space Time Plot for X")
        plt.show()

    def plot_spacetime_y(self, time):
        _, state_y = self.state(time)
        plt.plot(time.cpu(), state_y.cpu())
        plt.xlabel("time")
        plt.ylabel("Y")
        plt.title("Space Time Plot for Y")
        plt.show()

    def plot_speed(self, time):
        speed = self.speed(time)
        plt.plot(time.cpu(), speed.cpu())
        plt.xlabel("Time")
        plt.ylabel("Speed")
        plt.title("Speed vs Time")
        plt.show()

# amplitude = 2.0
# skewness = 0.25  # 0.75 is interesting with large number of loops, 0.5 is interesting with small number of loops as they don't have a small common multiple
# angular_velocity = 2.0 
# phase_constant = 2.0
# T = 50.0 

# Bow = BoW(amplitude=amplitude, skewness=skewness, angular_velocity=angular_velocity, phase_constant=phase_constant, device=device)
# time = torch.linspace(0, 0.5, 2, device=device)   

# Bow.plot_state_space(time)

# Bow.plot_spacetime_x(time)

# Bow.plot_spacetime_y(time)

# Bow.plot_speed(time)