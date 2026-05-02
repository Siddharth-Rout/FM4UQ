# FM4UQ
Flow matching for sampling perturbed initial states and sensitivity analysis of dynamical systems.

System: 
$$\ddot{x} + 4x = 0$$
$$\ddot{y} + y = 0$$

Exact Solution (Parametric):
$$x = 2sin(2t) $$
$$y = cos(t) $$

Exact Solution (State Space):
$$x^2 = 16y^2 \(1-y^2\) $$

| Metric  | Diffusion  | Ours  | 
|---|---|---|
|Residual   | 1.6158e-02  | 6.7683e-04  |
|Mean Squared Residual   | 5.4663e-03  | 2.7638e-06  |
|A   | 1.177e+00  | 1.997e+00  |
|Mean Squared Error of A | 8.173e+01  | 3.664e-02  |

![Forcasting using diffusion.](./diffusion.png) Forcasting using diffusion

![Forcasting using our method.](./ours.png) Forcasting using our method


