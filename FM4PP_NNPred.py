import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
from Lissajous import BoW

# ---------------------------------------------------
# DDPM
# ---------------------------------------------------

class NoiseMLP(nn.Module):
    def __init__(self, hidden_dim=256):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(3, hidden_dim),   # x,y + timestep
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 2)    # predict noise for x,y
        )

    def forward(self, x, t):
        # x shape: [B,2]
        # t shape: [B]
        t = t.float().unsqueeze(1)/1000.0
        inp = torch.cat([x, t], dim=1)
        return self.net(inp)

class NoiseConditionalMLP(nn.Module):
    def __init__(self, hidden_dim=256):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(5, hidden_dim),   # x,y + timestep
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 2)    # predict noise for x,y
        )

    def forward(self, x, x0, t):
        # x shape: [B,2]
        # x0 shape: [B,2]
        # t shape: [B]
        x0 = x0*0.0
        t = t.float().unsqueeze(1)/1000.0
        inp = torch.cat([x, x0, t], dim=1)
        return self.net(inp)
    
def euler_integrator(net, x, N_steps, t0=0, t1=1, device='cpu'):

    dt = (t1 - t0) / N_steps

    t = torch.full((x.shape[0],), t0, device=device)

    x0 = x.clone().detach()

    for step in range(N_steps):
        with torch.no_grad():
            velocity = net(x, x0, t)

            x = x + velocity * dt
            t = t + dt
    return x, t

def RK4_integrator(net, x, N_steps, t0=0, t1=1, device='cpu'):

    dt = (t1 - t0) / N_steps

    t = torch.full((x.shape[0],), t0, device=device)

    x0 = x.clone().detach()

    for step in range(N_steps):
        with torch.no_grad():
            K1 = net(x, x0, t) * dt
            K2 = net(x + 0.5 * K1, x0, t + 0.5 * dt) * dt
            K3 = net(x + 0.5 * K2, x0, t + 0.5 * dt) * dt
            K4 = net(x + K3, x0, t + dt) * dt

            x = x + (K1 + 2*K2 + 2*K3 + K4) / 6

            t = t + dt
    return x, t

device = "cuda" if torch.cuda.is_available() else "cpu"

amplitude = 2.0
skewness = 0.5  # 0.75 is interesting with large number of loops, 0.5 is interesting with small number of loops as they don't have a small common multiple
angular_velocity = 2.0 
phase_constant = 0#2.0
T = 50.0 

timestep = 1.5

Bow = BoW(amplitude=amplitude, skewness=skewness, angular_velocity=angular_velocity, phase_constant=phase_constant, device=device) 

model = NoiseConditionalMLP().to(device)

optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
loss_fn = nn.MSELoss()

epochs = 50000
batch_size = 2560

for step in range(epochs):

    time = torch.rand(batch_size, device=device) * T
    x1, y1 = Bow.state(time)


    X1 = torch.stack([x1, y1], dim=1)  

    X0 = torch.randn_like(X1) # source pure noise

    t = torch.rand(batch_size, device=device)

    xt = X0 + t.unsqueeze(1) * (X1 - X0)

    velocity = model(xt, X0, t)

    loss = loss_fn(velocity, X1 - X0)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if step % 500 == 0:
        print(f"step {step}: loss = {loss.item():.4e}")


N = 20000

time = torch.rand(N, device=device) * T
x_ref, y_ref = Bow.state(time)
x_final_ref, y_final_ref = Bow.state(time + timestep)

X_ref = torch.stack([x_ref, y_ref], dim=1)
X_final_ref = torch.stack([x_final_ref, y_final_ref], dim=1)

N_steps = 1000

sample = X_ref[0:1]

sample_final = X_final_ref[0:1]

# invert
sample_inverse, t = euler_integrator(model, sample, N_steps, t0 = 1.0, t1=0.0, device=device)#, direction='backward')
# samples, t = RK4_integrator(model, X0, N_steps, device=device)

# perturb
sigma = 0.02
ensembles = 1000
inverse_ensemble = sample_inverse + torch.randn(ensembles, 2).to(device) * sigma

#revert
perturbed_samples, t = euler_integrator(model, inverse_ensemble, N_steps, t0 = 0.0, t1=1.0, device=device)

# plt.scatter(x_ref.cpu(), y_ref.cpu(), s=1, alpha=0.5, label='Reference Samples')
# plt.scatter(perturbed_samples[:,0].cpu(), perturbed_samples[:, 1].cpu(), s=1, alpha=0.5, label='Perturbed Input Samples')
# plt.scatter(sample[:,0].cpu(), sample[:, 1].cpu(), s=20, marker='o', alpha=0.5, label='Single Reference Sample')
# plt.legend()
# plt.show()

######################## Prediction from single sample with perturbation ########################

pred_model = NoiseMLP().to(device)

optimizer = torch.optim.Adam(pred_model.parameters(), lr=1e-4)
loss_fn = nn.MSELoss()

epochs = 50000*2
batch_size = 2560

for step in range(epochs):

    if (step + 1) % 80000 == 0:
        optimizer = torch.optim.Adam(pred_model.parameters(), lr=1e-5)

    time = torch.rand(batch_size, device=device) * T
    x0, y0 = Bow.state(time)
    x1, y1 = Bow.state(time + timestep)

    X0 = torch.stack([x0, y0], dim=1)  # source instead of pure noise
    X1 = torch.stack([x1, y1], dim=1)

    
    t = torch.zeros(batch_size, device=device)

    pred = pred_model(X0, t)

    loss = loss_fn(pred, X1)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if step % 500 == 0:
        print(f"step {step}: loss = {loss.item():.4e}")

t = torch.zeros(len(perturbed_samples), device=device)
perturbed_pred_samples = pred_model(perturbed_samples, t)

plt.scatter(x_ref.cpu(), y_ref.cpu(), s=1, alpha=0.5, label='Reference Samples')
plt.scatter(perturbed_samples[:,0].cpu(), perturbed_samples[:, 1].cpu(), s=1, alpha=0.5, label='Perturbed Input Samples')
plt.scatter(perturbed_pred_samples[:,0].cpu().detach().numpy(), perturbed_pred_samples[:, 1].cpu().detach().numpy(), s=1, alpha=0.5, label='Perturbed Predicted Samples')
plt.scatter(sample[:,0].cpu(), sample[:, 1].cpu(), s=20, marker='o', alpha=0.5, label='Single Input Reference Sample')
plt.scatter(sample_final[:,0].cpu(), sample_final[:, 1].cpu(), s=20, marker='X', alpha=0.5, label='Single Input Final Reference Sample')
plt.legend()
plt.show()

breakpoint()