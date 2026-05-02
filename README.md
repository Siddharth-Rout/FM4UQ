# FM4UQ
Flow matching for sampling perturbed initial states and sensitivity analysis of dynamical systems.

System: <br>
$$\ddot{x} + 4x = 0$$ <br>
$$\ddot{y} + y = 0$$ <br>

Exact Solution (Parametric): <br>
$$x = 2sin(2t) $$ <br>
$$y = cos(t) $$ <br>

Exact Solution (State Space): <br>
$$x^2 = 16y^2 \(1-y^2\) $$ <br>

| Metric  | Diffusion  | Ours  | 
|---|---|---|
|Residual   | 1.6158e-02  | 6.7683e-04  |
|Mean Squared Residual   | 5.4663e-03  | 2.7638e-06  |
|A   | 1.177e+00  | 1.997e+00  |
|Mean Squared Error of A | 8.173e+01  | 3.664e-02  |

![Forcasting using diffusion.](./diffusion.png) Forcasting using diffusion

![Forcasting using our method.](./ours.png) Forcasting using our method


