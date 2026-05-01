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
        t = t.float().unsqueeze(1) / 1000.0
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
        t = t.float().unsqueeze(1) / 1000.0
        inp = torch.cat([x, x0, t], dim=1)
        return self.net(inp)

class DDPM:
    def __init__(self, T=1000, beta_start=1e-4, beta_end=0.02, device="cpu"):
        self.T = T
        self.device = device

        self.betas = torch.linspace(beta_start, beta_end, T).to(device)
        self.alphas = 1. - self.betas
        self.alpha_hat = torch.cumprod(self.alphas, dim=0)

    def sample_timesteps(self, n):
        return torch.randint(1, self.T, (n,), device=self.device)

    def add_noise(self, x0, t):
        """
        q(x_t | x_0)
        """
        sqrt_alpha_hat = torch.sqrt(self.alpha_hat[t]).unsqueeze(1)
        sqrt_one_minus = torch.sqrt(1 - self.alpha_hat[t]).unsqueeze(1)

        eps = torch.randn_like(x0)
        xt = sqrt_alpha_hat * x0 + sqrt_one_minus * eps
        return xt, eps

    @torch.no_grad()
    def sample(self, model, n, x0=None):
        """
        Generate new 2D samples
        """
        model.eval()

        if x0 is None:
            x = torch.randn(n, 2).to(self.device)
        else:
            x = x0

        for i in reversed(range(1, self.T)):
            t = torch.full((n,), i, device=self.device, dtype=torch.long)

            pred_noise = model(x, x0, t)  # Pass x0 as an additional input

            alpha = self.alphas[t].unsqueeze(1)
            alpha_hat = self.alpha_hat[t].unsqueeze(1)
            beta = self.betas[t].unsqueeze(1)

            if i > 1:
                z = torch.randn_like(x)
            else:
                z = torch.zeros_like(x)

            x = (
                (1 / torch.sqrt(alpha))
                * (x - ((1 - alpha) / torch.sqrt(1 - alpha_hat)) * pred_noise)
                + torch.sqrt(beta) * z
            )

        model.train()
        return x



# def sample_real_data(n):
#     c1 = torch.randn(n // 2, 2) * 0.3 + torch.tensor([2.0, 2.0])
#     c2 = torch.randn(n // 2, 2) * 0.3 + torch.tensor([-2.0, -2.0])
#     return torch.cat([c1, c2], dim=0)

device = "cuda" if torch.cuda.is_available() else "cpu"

amplitude = 2.0
skewness = 0.5  # 0.75 is interesting with large number of loops, 0.5 is interesting with small number of loops as they don't have a small common multiple
angular_velocity = 2.0 
phase_constant = 0#2.0
T = 50.0 

timestep = 1.5

Bow = BoW(amplitude=amplitude, skewness=skewness, angular_velocity=angular_velocity, phase_constant=phase_constant, device=device) 

model = NoiseConditionalMLP().to(device)
diffusion = DDPM(device=device)

optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
loss_fn = nn.MSELoss()

epochs = 50000
batch_size = 2560

for step in range(epochs):

    time = torch.rand(batch_size, device=device) * T
    x0, y0 = Bow.state(time)

    x1, y1 = Bow.state(time + timestep)


    X0 = torch.stack([x0, y0], dim=1)  # source instead of pure noise
    X1 = torch.stack([x1, y1], dim=1)

    # x0 = sample_real_data(batch_size).to(device)

    t = diffusion.sample_timesteps(batch_size)
    xt, noise = diffusion.add_noise(X1, t)

    pred = model(xt, X0, t)

    loss = loss_fn(pred, noise)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if step % 500 == 0:
        print(f"step {step}: loss = {loss.item():.4f}")



time = torch.rand(100000, device=device) * T
x0, y0 = Bow.state(time)
x1 , y1 = Bow.state(time + timestep)

X0 = torch.stack([x0, y0], dim=1)
X1 = torch.stack([x1, y1], dim=1)

set = X0[0:2]
set = set.repeat(1000, 1)
set_output = X1[0:2]
set_output = set_output.repeat(1000, 1)

samples = diffusion.sample(model, n= set.shape[0], x0 = set).cpu() 

plt.scatter(x0.cpu(), y0.cpu(), s=0.2, alpha=0.5, label='Reference Samples')
plt.scatter(set[:, 0].cpu(), set[:, 1].cpu(), s=15, marker='X', alpha=1.0, label='Input Samples')
plt.scatter(samples[:, 0], samples[:, 1], s=0.2, marker='o', alpha=0.25, label='Generated Samples')
plt.scatter(set_output[:, 0].cpu(), set_output[:, 1].cpu(), s=15, marker='^', alpha=1.0, label='Output Samples')
plt.legend()
plt.show()

breakpoint()