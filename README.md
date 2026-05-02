# FM4UQ
Flow matching for sampling perturbed initial states and sensitivity analysis of dynamical systems.

System: <br>
$$\ddot{x} + \omega^2 x = 0$$ <br>
$$\ddot{y} + k^2 \omega^2 y = 0$$ <br>

Amplitude = 2 <br>
k = 0.5 <br>
$$\omega$$ = 2 <br>

Exact Solution (Parametric): <br>
$$x = 2sin(2t) $$ <br>
$$y = cos(t) $$ <br>

Exact Solution (State Space): <br>
$$x^2 = 16y^2 \(1-y^2\) $$ <br>

So, residual = $$ x^2 - 16y^2 \(1-y^2\) $$. <br>
Also, amplitude = 8y^2/ (16y^2 - x^2)^(0.5) <br>


| Metric  | Diffusion  | Ours  | 
|---|---|---|
|Residual   | 1.6158e-02  | 6.7683e-04  |
|Mean Squared Residual   | 5.4663e-03  | 2.7638e-06  |
|Amplitude   | 1.177e+00  | 1.997e+00  |
|Mean Squared Error of Amplitude | 8.173e+01  | 3.664e-02  |

![Forcasting using diffusion.](./diffusion.png) Forcasting using diffusion

![Forcasting using our method.](./ours.png) Forcasting using our method


