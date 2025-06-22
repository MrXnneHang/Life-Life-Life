github 无法渲染部分 latex, 或者说它对格式实在太过苛求。

用图解法求解下列线性规划问题，并指出问题是具有唯一最解、无穷多最优解、无界解还是无可行解?
$\left.\left(1\right)\max z=x_{1}+3x_{2}\\\left\{\begin{array}{l}5x_{1}+10x_{2}\leqslant50\\x_{1}+x_{2}\geqslant1\\x_{2}\leqslant4\\x_{1},x_{2}\geqslant0\end{array}\right.\right.$<br>
$\begin{aligned}&\left(3\right)\max z=2x_{1}+2x_{2}\\&\left.\left\{\begin{array}{c}x_{1}-x_{2}\geqslant-1\\-0.5x_{1}+x_{2}\leqslant2\\x_{1},x_{2}\geqslant0\end{array}\right.\right.\end{aligned}$<br>

$(1)$<br>

$\max z=x_{1}+3x_{2}$<br>
$\text{s.t. } 5x_{1}+10x_{2}\leqslant50 \quad (\text{L1})$<br>
$x_{1}+x_{2}\geqslant1 \quad (\text{L2})$<br>
$x_{2}\leqslant4 \quad (\text{L3})$<br>
$x_{1},x_{2}\geqslant0$<br>

$\text{s.t. } 5x_{1}+10x_{2}\leqslant50 \quad (\text{L1})$<br>
当 $x_{1}=0$ 时，$2x_{2}=10 \implies x_{2}=5$。得到点 $(0,5)$。
当 $x_{2}=0$ 时，$x_{1}=10$。得到点 $(10,0)$。
连接 $(0,5)$ 和 $(10,0)$ 得到直线 L1。可行域在直线的左下方。

$x_{1}+x_{2}\geqslant1 \quad (\text{L2})$<br>
当 $x_{1} = 0$ 时, $x_{2} = 1$。得到点 $(0,1)$。
当 $x_{2} = 0$ 时, $x_{1} = 1$。得到点 $(1,0)$。
连接 $(0,1)$ 和 $(1,0)$ 得到直线 L2。可行域在直线的右上方。

$x_{2}\leqslant4 \quad (\text{L3})$<br>
可行域在直线的下方。

$x_{1},x_{2}\geqslant0$<br>
可行域在第一象限

·顶点 A: $x_1$轴与 L2 的交点。当$x_2=0$时，由$x_1+x_2=1\Longrightarrow x_1=1.$所以 A=(1,0)。
·顶点 B: $x_1$轴与 L1 的交点。当$x_2=0$时，由$5x_1+10x_2=50\implies5x_1=50\implies x_1=10.$<br>
所以 B=(10,0)。
·顶点 C:L1 与 L3 的交点。由$x_{2}=4$代入$5x_1+ 10x_2= 50\Longrightarrow 5x_1+ 40= 50$ $\Longrightarrow 5x_1=10\implies x_{1}=2.$所以 C=$(2,4)_{\circ}$<br>
·顶点 D：$x_{2}$轴与 L3 的交点。当$x_1=0$时，由$x_{2}=4.$所以 D=(0,4)。
·顶点 E：$x_2$ 轴与 L2 的交点。当$x_1=0$ 时，由$x_1+x_2=1\Longrightarrow x_2=1$.所以 E=(0,1)。

可行域的顶点是：A(1,0), B(10,0), C(2,4), D(0,4), E(0,1)。

计算目标函数在每个顶点的值

目标函数$z=x_1+3x_{2\circ}$<br>

$\cdot$ $A( 1, 0) {: }z= 1+ 3( 0) = 1$<br>

$\cdot$ $B( 10, 0) {: }z= 10+ 3( 0) = 10$<br>

$\cdot$ $C( 2, 4)  {: } z= 2+ 3( 4) = 2+ 12= 14$<br>

$\cdot$ $D( 0, 4) {: }z= 0+ 3( 4) = 12$<br>

$\cdot$ $E( 0, 1) {: }z= 0+ 3( 1) = 3$<br>

最大值为 14,在顶点$\mathfrak{C}(2,4)$处取得。因此，该线性规划问题的最优解为$\mathbf{x}_1=2,\mathbf{x}_2=4$,最大目标函数值为$\mathbf{z}=14_{\circ}$由于只有一个顶点使得目标函数达到最大值，所以问题具有唯一最优解。

$(3)$<br>

$\max z=2x_{1}+2x_{2}$<br>
$\text{s.t. } x_{1}-x_{2}\geqslant-1 \quad (\text{L1})$<br>
$-0.5x_{1}+x_{2}\leqslant2 \quad (\text{L2})$
$x_{1},x_{2}\geqslant0$<br>
