# FM4UQ
Flow matching for sampling perturbed initial states and sensitivity analysis of dynamical systems.

System: 2-mode Harmonic Oscillator<br>
$$\ddot{x} + \omega^2 x = 0$$ <br>
$$\ddot{y} + k^2 \omega^2 y = 0$$ <br>

Amplitude $$A = 2$$ <br>
Skewness factor $$k = 0.5$$ <br>
Angular Velocity $$\omega = 2$$ <br>

Exact Solution (Parametric): <br>
$$x = 2sin(2t) $$ <br>
$$y = cos(t) $$ <br>

Exact Solution (State Space): <br>
$$x^2 = 16y^2 \(1-y^2\) $$ <br>

So, residual ($x_1$ , $y_1$) = $${x_1}^2 - 16{y_1}^2 (1-{y_1}^2)$$ . <br> <br> 
Also, amplitude  ($x_1$ , $y_1$) = $$\frac{8y_1^2}{(16y_1^2 - x_1^2)^{0.5}}$$ . <br> <br>


| Metric  | Diffusion  | Ours  | 
|---|---|---|
|Residual   | 1.6158e-02  | 6.7683e-04  |
|Mean Squared Residual   | 5.4663e-03  | 2.7638e-06  |
|Amplitude   | 1.177e+00  | 1.997e+00  |
|Mean Squared Error of Amplitude | 8.173e+01  | 3.664e-02  |

![Forcasting using diffusion.](./diffusion.png) Forcasting using diffusion

![Forcasting using our method.](./ours.png) Forcasting using our method


|	s = 0.001	| s = 0.005 |	s = 0.01	| s = 0.02 | s = 0.05 |	s = 0.1	| s = 0.2	| s = 0.5 |
|----|----|----|----|----|----|----|----|
| Residual |	-8.22E-04 |	-7.97E-04 |	-8.29E-04 |	-9.40E-05 |	2.55E-03 |	 -1.1334e-03  |	-2.58E-03 |	-2.60E-01 |
| Mean Squared Residual |	7.01E-07 |	1.22E-06 |	3.01E-06 |	1.10E-04 |	2.38E-04 |	2.05E-04 |	7.39E-04 |	7.30E+00 |
| A |	2.00E+00 |	2.00E+00 |	2.00E+00 |	2.00E+00 |	2.00E+00 |	2.00E+00 |	2.00E+00 |	2.02E+00 |
| Mean Squared Error of A |	1.14E-03 |	1.50E-03 |	2.36E-03 |	1.43E-02 |	2.09E-02 |	1.95E-02 |	3.45E-02 |	3.78E-01 |

