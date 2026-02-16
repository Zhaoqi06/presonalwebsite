import streamlit as st
from streamlit.components.v1 import html
from streamlit_pdf_viewer import pdf_viewer
import pandas as pd
import os
from docx import Document

# 拦截未登录用户
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("请先登录")
    st.switch_page("pages/login.py")

# 使用 selectbox 实现导航
nav = st.sidebar.selectbox("导航栏",
                           ["Mathmatics",  "Collage of English","Article"])
if nav == "Mathmatics":
    # st.markdown("<style>.stApp{background:linear-gradient(123deg,#F1FAEE 0%,#A8DADC 100%);}</style>",unsafe_allow_html=True)
    st.title("欢迎来到学习板块！")
    st.write("在这里有你想知道并且我们有的资料，点击左边导航栏查看详情！")
    # 自定义CSS样式美化
    st.markdown("""
    <style>
        .formula-card {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #4e73df;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .section-title {
            color: #2e59d9;
            border-bottom: 2px solid #4e73df;
            padding-bottom: 8px;
            margin-top: 20px;
        }
        .subsection-title {
            color: #3a3b45;
            margin-top: 15px;
        }
    </style>
    """, unsafe_allow_html=True)

    # 标题
    st.title("📚 高等数学公式手册")
    st.markdown("---")

    # 创建侧边栏导航
    st.sidebar.title("目录")
    sections = [
        "一、极限与等价无穷小",
        "二、导数与微分",
        "三、不定积分与定积分",
        "四、多元函数微分学",
        "五、曲线积分与曲面积分",
        "六、高斯公式、斯托克斯公式、级数",
        "七、微分方程",
        "八、向量与解析几何",
        "九、沃利斯公式"
    ]

    selected = st.sidebar.radio("选择章节", sections)

    # ------------------- 一、极限与等价无穷小 -------------------
    if selected == "一、极限与等价无穷小":
        st.header("极限与等价无穷小", anchor="limit")

        st.markdown('<div class="section-title">重要极限</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.latex(r'\lim_{x \to 0} \frac{\sin x}{x} = 1')
        with col2:
            st.latex(r'\lim_{x \to \infty} \left(1+\frac{1}{x}\right)^x = e')
        st.latex(r'\lim_{x \to 0} (1+x)^{\frac{1}{x}} = e,\quad \lim_{n \to \infty} \left(1+\frac{1}{n}\right)^n = e')

        st.markdown('<div class="section-title">等价无穷小（$x→0$）</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**基本等价**")
            st.latex(r'\sin x \sim x')
            st.latex(r'\tan x \sim x')
            st.latex(r'\arcsin x \sim x')
            st.latex(r'\arctan x \sim x')
            st.latex(r'1-\cos x \sim \frac{1}{2}x^2')

            st.markdown("**三阶展开**")
            st.latex(r'x-\sin x \sim \frac{1}{6}x^3')
            st.latex(r'\tan x-x \sim \frac{1}{3}x^3')
            st.latex(r'\tan x-\sin x \sim \frac{1}{2}x^3')

        with col2:
            st.markdown("**指数对数**")
            st.latex(r'e^x-1 \sim x')
            st.latex(r'a^x-1 \sim x\ln a')
            st.latex(r'\ln(1+x) \sim x')
            st.latex(r'\log_a(1+x) \sim \frac{x}{\ln a}')
            st.latex(r'(1+x)^\alpha-1 \sim \alpha x')

            st.markdown("**其他重要**")
            st.latex(r'x-\ln(1+x) \sim \frac{1}{2}x^2')
            st.latex(r'\arcsin x-x \sim \frac{1}{6}x^3')
            st.latex(r'x-\arctan x \sim \frac{1}{3}x^3')
            st.latex(r'x^m+x^n \sim x^n\ (m,n>0,\ n<m)')

    # ------------------- 二、导数与微分 -------------------
    elif selected == "二、导数与微分":
        st.header("导数与微分", anchor="derivative")

        st.markdown('<div class="section-title">导数定义</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.latex(r"f'(x_0) = \lim_{\Delta x \to 0} \frac{f(x_0+\Delta x)-f(x_0)}{\Delta x}")
        with col2:
            st.latex(r"f'(x_0) = \lim_{x \to x_0} \frac{f(x)-f(x_0)}{x-x_0}")
        st.latex(r"f'(x_0) = \lim_{h \to 0} \frac{f(x_0+h)-f(x_0)}{h}")

        st.markdown('<div class="section-title">基本求导公式</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**常数与幂函数**")
            st.latex(r"(C)' = 0")
            st.latex(r"(x^\mu)' = \mu x^{\mu-1}")
            st.latex(r"(\ln x)' = \frac{1}{x}")
            st.latex(r"(\log_a x)' = \frac{1}{x\ln a}")

        with col2:
            st.markdown("**指数函数与三角函数**")
            st.latex(r"(e^x)' = e^x")
            st.latex(r"(a^x)' = a^x\ln a")
            st.latex(r"(\sin x)' = \cos x")
            st.latex(r"(\cos x)' = -\sin x")
            st.latex(r"(\tan x)' = \sec^2 x")

        with col3:
            st.markdown("**反三角函数**")
            st.latex(r"(\arcsin x)' = \frac{1}{\sqrt{1-x^2}}")
            st.latex(r"(\arccos x)' = -\frac{1}{\sqrt{1-x^2}}")
            st.latex(r"(\arctan x)' = \frac{1}{1+x^2}")
            st.latex(r"(\text{arccot } x)' = -\frac{1}{1+x^2}")

        st.markdown('<div class="section-title">求导法则</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**四则运算**")
            st.latex(r"(u \pm v)' = u' \pm v'")
            st.latex(r"(uv)' = u'v + uv'")
            st.latex(r"(Cu)' = Cu'")
            st.latex(r"\left(\frac{u}{v}\right)' = \frac{u'v - uv'}{v^2}\ (v\neq0)")

        with col2:
            st.markdown("**参数方程求导**")
            st.latex(r"\begin{cases}x=\varphi(t)\\y=\psi(t)\end{cases}")
            st.latex(r"\frac{dy}{dx}=\frac{\psi'(t)}{\varphi'(t)}")
            st.markdown("**高阶导数**")
            st.latex(r"\sin^{(n)}x=\sin\left(x+\frac{n}{2}\pi\right)")
            st.latex(r"\cos^{(n)}x=\cos\left(x+\frac{n}{2}\pi\right)")

        st.markdown('<div class="section-title">几何应用</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.latex(r"\text{切线：}y-f(x_0)=f'(x_0)(x-x_0)")
        with col2:
            st.latex(r"\text{法线：}y-f(x_0)=-\frac{1}{f'(x_0)}(x-x_0)")

    # ------------------- 三、不定积分与定积分 -------------------
    elif selected == "三、不定积分与定积分":
        st.header("不定积分与定积分", anchor="integral")

        tab1, tab2, tab3 = st.tabs(["基本积分公式", "积分方法", "定积分性质"])

        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**幂函数**")
                st.latex(r"\int kdx = kx + C")
                st.latex(r"\int x^\mu dx = \frac{x^{\mu+1}}{\mu+1} + C\ (\mu\neq-1)")
                st.latex(r"\int \frac{1}{x}dx = \ln|x| + C")
                st.markdown("**三角函数**")
                st.latex(r"\int \cos xdx = \sin x + C")
                st.latex(r"\int \sin xdx = -\cos x + C")
                st.latex(r"\int \sec^2 xdx = \tan x + C")

            with col2:
                st.markdown("**指数函数**")
                st.latex(r"\int e^xdx = e^x + C")
                st.latex(r"\int a^xdx = \frac{a^x}{\ln a} + C")
                st.markdown("**其他重要积分**")
                st.latex(r"\int \frac{1}{1+x^2}dx = \arctan x + C")
                st.latex(r"\int \frac{1}{\sqrt{1-x^2}}dx = \arcsin x + C")
                st.latex(r"\int \tan xdx = -\ln|\cos x| + C")

        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**分部积分法**")
                st.latex(r"\int u dv = uv - \int v du")

            with col2:
                st.markdown("**三角代换**")
                st.latex(r"\sqrt{a^2-x^2}\ \Rightarrow\ x=a\sin t")
                st.latex(r"\sqrt{x^2+a^2}\ \Rightarrow\ x=a\tan t")
                st.latex(r"\sqrt{x^2-a^2}\ \Rightarrow\ x=a\sec t")

        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**牛顿-莱布尼茨公式**")
                st.latex(r"\int_a^b f(x)dx = F(x)\bigg|_a^b = F(b)-F(a)")

            with col2:
                st.markdown("**对称性**")
                st.latex(r"f(x)\text{奇函数：}\int_{-a}^a f(x)dx = 0")
                st.latex(r"f(x)\text{偶函数：}\int_{-a}^a f(x)dx = 2\int_0^a f(x)dx")

    # ------------------- 四、多元函数微分学 -------------------
    elif selected == "四、多元函数微分学":
        st.header("多元函数微分学", anchor="multivariable")

        st.markdown('<div class="section-title">全微分</div>', unsafe_allow_html=True)
        st.latex(r"z=f(x,y),\quad dz=\frac{\partial z}{\partial x}dx+\frac{\partial z}{\partial y}dy")

        st.markdown('<div class="section-title">隐函数求偏导</div>', unsafe_allow_html=True)
        st.latex(
            r"F(x,y,z)=0,\quad \frac{\partial z}{\partial x}=-\frac{F_x}{F_z},\ \frac{\partial z}{\partial y}=-\frac{F_y}{F_z}\ (F_z\neq0)")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-title">空间曲线的切线与法平面</div>', unsafe_allow_html=True)
            st.latex(r"\text{曲线：}\begin{cases}x=\varphi(t)\\y=\psi(t)\\z=\omega(t)\end{cases}")
            st.latex(r"\text{切线：}\frac{x-x_0}{\varphi'(t_0)}=\frac{y-y_0}{\psi'(t_0)}=\frac{z-z_0}{\omega'(t_0)}")
            st.latex(r"\text{法平面：}\varphi'(t_0)(x-x_0)+\psi'(t_0)(y-y_0)+\omega'(t_0)(z-z_0)=0")

        with col2:
            st.markdown('<div class="section-title">曲面的切平面与法线</div>', unsafe_allow_html=True)
            st.latex(r"\text{曲面：}F(x,y,z)=0")
            st.latex(r"\text{切平面：}F_x(x_0,y_0,z_0)(x-x_0)+F_y(x_0,y_0,z_0)(y-y_0)+F_z(x_0,y_0,z_0)(z-z_0)=0")
            st.latex(
                r"\text{法线：}\frac{x-x_0}{F_x(x_0,y_0,z_0)}=\frac{y-y_0}{F_y(x_0,y_0,z_0)}=\frac{z-z_0}{F_z(x_0,y_0,z_0)}")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-title">方向导数与梯度</div>', unsafe_allow_html=True)
            st.latex(
                r"\left.\frac{\partial f}{\partial l}\right|_{(x_0,y_0)}=f_x(x_0,y_0)\cos\alpha+f_y(x_0,y_0)\cos\beta")
            st.latex(r"\text{grad}f(x_0,y_0)=f_x(x_0,y_0)\boldsymbol{i}+f_y(x_0,y_0)\boldsymbol{j}")

        with col2:
            st.markdown('<div class="section-title">二元函数极值判定</div>', unsafe_allow_html=True)
            st.latex(r"A=f_{xx}(x_0,y_0),\ B=f_{xy}(x_0,y_0),\ C=f_{yy}(x_0,y_0)")
            st.latex(r"""
            \begin{cases}
            AC-B^2>0 & \text{有极值，}A<0\text{极大，}A>0\text{极小} \\
            AC-B^2<0 & \text{无极值} \\
            AC-B^2=0 & \text{无法确定}
            \end{cases}
            """)

    # ------------------- 五、曲线积分与曲面积分 -------------------
    elif selected == "五、曲线积分与曲面积分":
        st.header("曲线积分与曲面积分", anchor="curve_surface")

        st.markdown('<div class="section-title">坐标变换</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.latex(r"""
            \text{极坐标：}\begin{cases}x=\rho\cos\theta\\y=\rho\sin\theta\end{cases}
            """)
            st.latex(r"""
            \iint_D f(x,y)dxdy=\iint_D f(\rho\cos\theta,\rho\sin\theta)\rho d\rho d\theta
            """)

        with col2:
            st.latex(r"""
            \text{球面坐标：}\begin{cases}x=r\sin\varphi\cos\theta\\y=r\sin\varphi\sin\theta\\z=r\cos\varphi\end{cases}
            """)
            st.latex(r"""
            \iiint_\Omega f(x,y,z)dV=\iiint_\Omega F(r,\varphi,\theta)r^2\sin\varphi drd\varphi d\theta
            """)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-title">曲线积分</div>', unsafe_allow_html=True)
            st.latex(r"""
            \text{对弧长：}\int_L f(x,y)ds=\int_\alpha^\beta f[\varphi(t),\psi(t)]\sqrt{[\varphi'(t)]^2+[\psi'(t)]^2}dt
            """)
            st.latex(r"\begin{cases}x=\varphi(t)\\y=\psi(t)\end{cases}")

        with col2:
            st.markdown('<div class="section-title">曲线积分（对坐标）</div>', unsafe_allow_html=True)
            st.latex(r"""
            \int_L Pdx+Qdy=\int_\alpha^\beta \left[P(\varphi(t),\psi(t))\varphi'(t)+Q(\varphi(t),\psi(t))\psi'(t)\right]dt
            """)

        st.markdown('<div class="section-title">格林公式</div>', unsafe_allow_html=True)
        st.latex(r"""
        \iint_D \left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)dxdy=\oint_L Pdx+Qdy
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-title">曲面积分（对面积）</div>', unsafe_allow_html=True)
            st.latex(r"""
            \iint_\Sigma f(x,y,z)dS=\iint_{D_{xy}} f[x,y,z(x,y)]\sqrt{1+z_x^2+z_y^2}dxdy
            """)

        with col2:
            st.markdown('<div class="section-title">曲面积分（对坐标）</div>', unsafe_allow_html=True)
            st.latex(r"""
            \begin{align*}
            &\iint_\Sigma Rdxdy=\pm\iint_{D_{xy}} R[x,y,z(x,y)]dxdy \\
            &\iint_\Sigma Pdydz=\pm\iint_{D_{yz}} P[x(y,z),y,z]dydz \\
            &\iint_\Sigma Qdzdx=\pm\iint_{D_{zx}} Q[x,y(z,x),z]dzdx
            \end{align*}
            """)

    # ------------------- 六、高斯公式、斯托克斯公式、级数 -------------------
    elif selected == "六、高斯公式、斯托克斯公式、级数":
        st.header("高斯公式、斯托克斯公式、级数", anchor="gauss_series")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-title">高斯公式</div>', unsafe_allow_html=True)
            st.latex(r"""
            \iiint_\Omega \left(\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y}+\frac{\partial R}{\partial z}\right)dV=
            \oiint_\Sigma Pdydz+Qdzdx+Rdxdy
            """)
            st.latex(r"""
            =\oiint_\Sigma (P\cos\alpha+Q\cos\beta+R\cos\gamma)dS
            """)

        with col2:
            st.markdown('<div class="section-title">斯托克斯公式</div>', unsafe_allow_html=True)
            st.latex(r"""
            \iint_\Sigma \begin{vmatrix}dydz&dzdx&dxdy\\
            \frac{\partial}{\partial x}&\frac{\partial}{\partial y}&\frac{\partial}{\partial z}\\
            P&Q&R\end{vmatrix}=\oint_\Gamma Pdx+Qdy+Rdz
            """)

        st.markdown('<div class="section-title">级数敛散性</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.latex(r"""
            \text{等比级数：}\sum_{n=0}^\infty q^n\begin{cases}\text{收敛}&|q|<1\\\text{发散}&|q|\ge1\end{cases}
            """)

        with col2:
            st.latex(r"\text{调和级数：}\sum_{n=1}^\infty \frac{1}{n}\text{发散}")

        with col3:
            st.latex(r"""
            \text{p-级数：}\sum_{n=1}^\infty \frac{1}{n^p}\begin{cases}\text{收敛}&p>1\\\text{发散}&p\le1\end{cases}
            """)

        st.markdown('<div class="section-title">常用幂级数展开</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.latex(r"\frac{1}{1-x}=\sum_{n=0}^\infty x^n\ (-1<x<1)")
            st.latex(r"\frac{1}{1+x}=\sum_{n=0}^\infty (-1)^n x^n\ (-1<x<1)")
            st.latex(r"e^x=\sum_{n=0}^\infty \frac{x^n}{n!}\ (-\infty<x<+\infty)")

        with col2:
            st.latex(r"\sin x=\sum_{n=0}^\infty (-1)^n \frac{x^{2n+1}}{(2n+1)!}\ (-\infty<x<+\infty)")
            st.latex(r"\cos x=\sum_{n=0}^\infty (-1)^n \frac{x^{2n}}{(2n)!}\ (-\infty<x<+\infty)")
            st.latex(r"\ln(1+x)=\sum_{n=0}^\infty (-1)^n \frac{x^{n+1}}{n+1}\ (-1<x\le1)")

    # ------------------- 七、微分方程 -------------------
    elif selected == "七、微分方程":
        st.header("微分方程", anchor="ode")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-title">一阶非齐次线性微分方程</div>', unsafe_allow_html=True)
            st.latex(r"y'+P(x)y=Q(x)")
            st.latex(r"y=e^{-\int P(x)dx}\left(\int Q(x)e^{\int P(x)dx}dx+C\right)")

        with col2:
            st.markdown('<div class="section-title">二阶常系数齐次线性微分方程</div>', unsafe_allow_html=True)
            st.latex(r"y''+py'+qy=0")
            st.latex(r"\text{特征方程：}r^2+pr+q=0")

        st.markdown('<div class="section-title">通解形式</div>', unsafe_allow_html=True)
        st.latex(r"""
        \begin{cases}
        \Delta>0,\ r_1\neq r_2 & y=C_1e^{r_1x}+C_2e^{r_2x} \\
        \Delta=0,\ r_1=r_2 & y=(C_1+C_2x)e^{r_1x} \\
        \Delta<0,\ r=\alpha\pm\beta i & y=e^{\alpha x}(C_1\cos\beta x+C_2\sin\beta x)
        \end{cases}
        """)

    # ------------------- 八、向量与解析几何 -------------------
    elif selected == "八、向量与解析几何":
        st.header("向量与解析几何", anchor="vector_geo")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-title">向量运算</div>', unsafe_allow_html=True)
            st.latex(r"""
            \boldsymbol{a}\cdot\boldsymbol{b}=x_1x_2+y_1y_2+z_1z_2=|\boldsymbol{a}||\boldsymbol{b}|\cos\langle\boldsymbol{a},\boldsymbol{b}\rangle
            """)

        with col2:
            st.markdown('<div class="section-title">向量积</div>', unsafe_allow_html=True)
            st.latex(r"""
            \boldsymbol{a}\times\boldsymbol{b}=\begin{vmatrix}\boldsymbol{i}&\boldsymbol{j}&\boldsymbol{k}\\
            x_1&y_1&z_1\\x_2&y_2&z_2\end{vmatrix}
            """)
            st.latex(r"=(y_1z_2-y_2z_1,z_1x_2-z_2x_1,x_1y_2-x_2y_1)")

        st.markdown('<div class="section-title">平面方程</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.latex(r"\text{点法式：}A(x-x_0)+B(y-y_0)+C(z-z_0)=0")

        with col2:
            st.latex(r"\text{一般式：}Ax+By+Cz+D=0")

        with col3:
            st.latex(r"\text{截距式：}\frac{x}{a}+\frac{y}{b}+\frac{z}{c}=1\ (abc\neq0)")

        st.markdown('<div class="section-title">直线方程</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.latex(r"\text{点向式：}\frac{x-x_0}{m}=\frac{y-y_0}{n}=\frac{z-z_0}{p}")
            st.latex(r"""
            \text{参数式：}\begin{cases}x=x_0+mt\\y=y_0+nt\\z=z_0+pt\end{cases}\ (-\infty<t<+\infty)
            """)

        with col2:
            st.latex(r"""
            \text{一般式：}\begin{cases}A_1x+B_1y+C_1z+D_1=0\\
            A_2x+B_2y+C_2z+D_2=0\end{cases}
            """)

    # ------------------- 九、沃利斯公式 -------------------
    elif selected == "九、沃利斯公式":
        st.header("沃利斯公式", anchor="wallis")

        st.markdown("沃利斯公式（Wallis Formula）用于计算正弦和余弦的幂次积分：")

        st.latex(r"""
        \int_0^{\frac{\pi}{2}} \sin^n xdx=\int_0^{\frac{\pi}{2}} \cos^n xdx
        """)

        st.latex(r"""
        =
        \begin{cases}
        \dfrac{n-1}{n}\cdot\dfrac{n-3}{n-2}\cdot\cdots\cdot\dfrac{3}{4}\cdot\dfrac{1}{2}\cdot\dfrac{\pi}{2} & n\text{为正偶数} \\
        \dfrac{n-1}{n}\cdot\dfrac{n-3}{n-2}\cdot\cdots\cdot\dfrac{4}{5}\cdot\dfrac{2}{3}\cdot1 & n\text{为大于1的正奇数}
        \end{cases}
        """)

        st.markdown("**示例：**")
        col1, col2 = st.columns(2)
        with col1:
            st.latex(
                r"\int_0^{\frac{\pi}{2}} \sin^4 xdx = \frac{3}{4}\cdot\frac{1}{2}\cdot\frac{\pi}{2} = \frac{3\pi}{16}")

        with col2:
            st.latex(r"\int_0^{\frac{\pi}{2}} \sin^5 xdx = \frac{4}{5}\cdot\frac{2}{3}\cdot1 = \frac{8}{15}")


elif nav == "Collage of English":
    import streamlit as st

    # 页面配置
    st.set_page_config(
        page_title="英语语法手册",
        page_icon="📚",
        layout="wide"
    )

    # 自定义CSS样式
    st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
        }
        .level-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-left: 5px solid #667eea;
        }
        .grammar-point {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            border-left: 4px solid #4CAF50;
        }
        .example-box {
            background: #e8f5e9;
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
            border-left: 3px solid #2E7D32;
        }
        .note-box {
            background: #e3f2fd;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            border-left: 3px solid #2196F3;
        }
        .highlight {
            background-color: #fff3cd;
            padding: 2px 5px;
            border-radius: 3px;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

    # 应用标题
    st.markdown('<div class="main-header"><h1>📖 英语语法手册</h1><p>初中语法 | 高中语法 | 专升本语法</p></div>', unsafe_allow_html=True)

    # 侧边栏导航
    st.sidebar.title("🎯 导航菜单")
    level = st.sidebar.selectbox(
        "选择语法级别",
        ["初中语法", "高中语法", "专升本语法"]
    )

    # 在每个级别内部添加子导航
    if level == "初中语法":
        topic = st.sidebar.radio(
            "选择语法专题",
            ["时态基础", "名词和代词", "形容词和副词", "基本句型", "疑问句和否定句"]
        )
    elif level == "高中语法":
        topic = st.sidebar.radio(
            "选择语法专题",
            ["非谓语动词", "定语从句", "名词性从句", "状语从句", "虚拟语气"]
        )
    else:  # 专升本语法
        topic = st.sidebar.radio(
            "选择语法专题",
            ["时态综合", "复合句分析", "非谓语动词进阶", "特殊句型", "一致关系"]
        )

    # 显示语法内容
    st.markdown(f"## 🎯 {level} - {topic}")

    # 初中语法内容
    if level == "初中语法":
        if topic == "时态基础":
            with st.container():
                st.markdown("### 1. 一般现在时")
                st.markdown("**用法：**")
                st.markdown("- 表示经常性、习惯性的动作")
                st.markdown("- 表示客观真理、事实")
                st.markdown("- 表示按计划安排的事情")

                with st.expander("查看例句"):
                    st.markdown("**例句：**")
                    st.markdown("1. I get up at 6:30 every morning. (习惯)")
                    st.markdown("2. The sun rises in the east. (真理)")
                    st.markdown("3. The train leaves at 8:00 tonight. (计划)")

            with st.container():
                st.markdown("### 2. 现在进行时")
                st.markdown("**结构：** am/is/are + doing")
                st.markdown("**用法：**")
                st.markdown("- 表示正在进行的动作")
                st.markdown("- 表示现阶段正在进行的事情")

                with st.expander("查看例句"):
                    st.markdown("**例句：**")
                    st.markdown("1. Look! They are playing basketball.")
                    st.markdown("2. I am studying English these days.")

            # 时态对比
            st.markdown("### 📊 时态对比表")
            col1, col2 = st.columns(2)
            with col1:
                st.info("**一般现在时**")
                st.markdown("结构：V/V-s")
                st.markdown("时间状语：often, always, usually")
                st.markdown("例句：She teaches English.")

            with col2:
                st.info("**现在进行时**")
                st.markdown("结构：am/is/are + V-ing")
                st.markdown("时间状语：now, at the moment")
                st.markdown("例句：She is teaching now.")

        elif topic == "名词和代词":
            st.markdown("### 1. 可数名词与不可数名词")
            col1, col2 = st.columns(2)
            with col1:
                st.success("**可数名词**")
                st.markdown("有单复数形式")
                st.markdown("- apple → apples")
                st.markdown("- book → books")

            with col2:
                st.success("**不可数名词**")
                st.markdown("没有复数形式")
                st.markdown("- water, milk, bread")
                st.markdown("- advice, information")

            st.markdown("### 2. 代词分类")
            st.markdown("""
            | 主格 | 宾格 | 所有格形容词 |
            |------|------|--------------|
            | I    | me   | my           |
            | you  | you  | your         |
            | he   | him  | his          |
            | she  | her  | her          |
            | it   | it   | its          |
            | we   | us   | our          |
            | they | them | their        |
            """)

        elif topic == "基本句型":
            st.markdown("### 英语五种基本句型")
            data = {
                "句型": ["主谓", "主谓宾", "主谓双宾", "主谓宾补", "主系表"],
                "结构": ["S + V", "S + V + O", "S + V + IO + DO", "S + V + O + C", "S + V + P"],
                "例句": ["Birds fly.", "I love you.", "She gave me a book.", "We call him Tom.", "She is a teacher."]
            }
            st.table(data)

    # 高中语法内容
    elif level == "高中语法":
        if topic == "非谓语动词":
            st.markdown("### 1. 动词不定式 (to do)")
            st.markdown("**用法：**")
            st.markdown("- 作主语：To learn English is important.")
            st.markdown("- 作宾语：I want to go home.")
            st.markdown("- 作宾补：He asked me to help him.")

            st.markdown("### 2. 动名词 (doing)")
            st.markdown("**用法：**")
            st.markdown("- 作主语：Swimming is good for health.")
            st.markdown("- 作宾语：I enjoy reading books.")

            st.warning("**易错点提示**")
            st.markdown("remember + to do (动作未发生)")
            st.markdown("remember + doing (动作已发生)")

            st.markdown("### 非谓语动词用法对比")
            cols = st.columns(3)
            with cols[0]:
                st.success("**不定式 to do**")
                st.markdown("表目的、将来")
                st.markdown("常用动词：want, hope, decide")

            with cols[1]:
                st.success("**动名词 doing**")
                st.markdown("表一般性、经常性")
                st.markdown("常用动词：enjoy, finish, avoid")

            with cols[2]:
                st.success("**分词 doing/done**")
                st.markdown("表主动/被动关系")
                st.markdown("作定语、状语")

        elif topic == "定语从句":
            st.markdown("### 1. 关系代词用法")
            data = {
                "关系代词": ["that", "which", "who", "whom", "whose"],
                "先行词": ["人或物", "物", "人", "人", "人或物"],
                "在从句中的作用": ["主/宾", "主/宾", "主/宾", "宾", "定语"]
            }
            st.table(data)

            st.markdown("**例句：**")
            st.markdown("1. The book that/which I borrowed is interesting.")
            st.markdown("2. The man who is standing there is my teacher.")
            st.markdown("3. This is the student whom I met yesterday.")

            st.markdown("### 2. 关系副词用法")
            st.markdown("**where** - 表示地点")
            st.markdown("**when** - 表示时间")
            st.markdown("**why** - 表示原因")

            st.markdown("**例句：**")
            st.markdown("1. This is the house where I was born.")
            st.markdown("2. I'll never forget the day when we met.")
            st.markdown("3. That's the reason why I was late.")

        elif topic == "虚拟语气":
            st.markdown("### 虚拟语气基本形式")

            st.markdown("**与现在事实相反：**")
            st.markdown("结构：if + 过去式, would/could/might + do")
            st.markdown("例句：If I were you, I would study harder.")

            st.markdown("**与过去事实相反：**")
            st.markdown("结构：if + had done, would/could/might + have done")
            st.markdown("例句：If you had come earlier, you would have met her.")

            st.markdown("**与将来事实相反：**")
            st.markdown("结构：if + should/were to + do, would/could/might + do")
            st.markdown("例句：If it should rain tomorrow, we would stay at home.")

    # 专升本语法内容
    elif level == "专升本语法":
        if topic == "复合句分析":
            st.markdown("### 1. 名词性从句综合")

            st.markdown("**主语从句：**")
            st.markdown("- What he said is true.")
            st.markdown("- That he passed the exam surprised us.")

            st.markdown("**宾语从句：**")
            st.markdown("- I know that you are right.")
            st.markdown("- She asked me whether I would go.")

            st.markdown("**表语从句：**")
            st.markdown("- The fact is that he doesn't know.")
            st.markdown("- That's why he was late.")

            st.markdown("### 2. 从句连接词辨析")
            data = {
                "连接词": ["that", "whether/if", "what", "who", "when"],
                "词性": ["连词", "连词", "代词", "代词", "副词"],
                "功能": ["只起连接作用", "是否，引导宾语从句", "所...的事/物", "谁，作主语", "什么时候"]
            }
            st.table(data)

        elif topic == "一致关系":
            st.markdown("### 主谓一致三原则")

            st.markdown("**语法一致原则：**")
            st.markdown("- A boy is playing.")
            st.markdown("- Two boys are playing.")

            st.markdown("**意义一致原则：**")
            st.markdown("- The family is big. (整体)")
            st.markdown("- The family are watching TV. (成员)")

            st.markdown("**就近一致原则：**")
            st.markdown("- Either you or I am wrong.")
            st.markdown("- Neither he nor they have come.")

            st.markdown("**特殊用法：**")
            st.markdown("1. Each of the students has a book.")
            st.markdown("2. More than one student has finished.")
            st.markdown("3. Many a student likes English.")

        elif topic == "特殊句型":
            st.markdown("### 1. 强调句型")
            st.markdown("**结构：** It is/was + 被强调部分 + that/who + 其他")

            st.markdown("**原句：** I met Tom in the park yesterday.")
            st.markdown("**强调主语：** It was I that/who met Tom in the park yesterday.")
            st.markdown("**强调宾语：** It was Tom that I met in the park yesterday.")

            st.markdown("### 2. 倒装句")
            st.markdown("**完全倒装：**")
            st.markdown("- Here comes the bus.")
            st.markdown("- Out rushed the children.")

            st.markdown("**部分倒装：**")
            st.markdown("- Never have I seen such a beautiful place.")
            st.markdown("- Only in this way can you succeed.")

    # 添加练习区域
    st.markdown("---")
    st.markdown("## 💡 语法练习")

    if level == "初中语法":
        with st.expander("初中语法练习题"):
            st.markdown("### 一、选择题")
            answer1 = st.radio(
                "1. She usually ______ TV in the evening.",
                ["watch", "watches", "is watching", "watching"]
            )

            answer2 = st.radio(
                "2. Look! The children ______ in the park.",
                ["play", "plays", "are playing", "is playing"]
            )

            if st.button("提交答案"):
                if answer1 == "watches" and answer2 == "are playing":
                    st.success("回答正确！")
                else:
                    st.error("有错误答案，请检查。")

    elif level == "高中语法":
        with st.expander("高中语法练习题"):
            st.markdown("### 句子改写")
            st.markdown("1. 将下列句子改为定语从句：")
            st.markdown("   The boy is my brother. He is playing basketball.")

            user_answer = st.text_input("你的答案：")

            if st.button("检查答案"):
                if "who" in user_answer.lower() or "that" in user_answer.lower():
                    st.success("很好！参考答案：The boy who is playing basketball is my brother.")
                else:
                    st.info("需要包含关系代词 who 或 that")

    elif level == "专升本语法":
        with st.expander("专升本语法练习题"):
            st.markdown("### 选择题")
            answer = st.radio(
                "It is I who ______ responsible for the project.",
                ["am", "is", "are", "be"]
            )

            if st.button("提交"):
                if answer == "am":
                    st.success("正确！强调句型中，谓语动词要与被强调的主语一致。")
                else:
                    st.error("错误，正确答案是'am'")

    # 侧边栏工具
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔧 学习工具")

    if st.sidebar.button("📋 错题本"):
        st.sidebar.info("错题本功能开发中...")

    if st.sidebar.button("🎯 随机测试"):
        st.sidebar.info("随机测试功能开发中...")

    # 学习进度
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 学习进度")

    if level == "初中语法":
        st.sidebar.progress(85)
        st.sidebar.caption("初中语法掌握度：85%")
    elif level == "高中语法":
        st.sidebar.progress(70)
        st.sidebar.caption("高中语法掌握度：70%")
    else:
        st.sidebar.progress(60)
        st.sidebar.caption("专升本语法掌握度：60%")

    # 底部信息
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #666;'>📚 英语语法手册 v1.0 | 持续更新中...</div>", unsafe_allow_html=True)

elif nav == "Article":
    st.title("论文")
    with st.expander("智能流水车间调度与优化的仿真模拟——基于Python的遥控器生产线建模与优化"):
        st.subheader("第一届全国大学生仿真建模应用挑战赛")
        # 使用 pdf_viewer 替代 st.pdf()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        docx_file_path = os.path.join(script_dir, "..", "document", "ACSFJM2512633.pdf")
        pdf_path = os.path.normpath(docx_file_path)
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_viewer(f.read(), width=700, height=600)
        else:
            st.error(f"PDF文件未找到：{pdf_path}")

    with st.expander("基于大数据分析的三种重大慢性病的相关风险评估与防控策略研究"):
        st.subheader("2025 年第十五届APMCM 亚太地区大学生数学建模竞赛（中文赛项）")
        # 使用 pdf_viewer 替代 st.pdf()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        docx_file_path = os.path.join(script_dir, "..", "document",
                                      "基于大数据分析的三种重大慢性病的相关风险评估与防控策略研究.pdf")
        pdf_path = os.path.normpath(docx_file_path)
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_viewer(f.read(), width=700, height=600)
        else:
            st.error(f"PDF文件未找到：{pdf_path}")

    with st.expander("基于大数据分析的三种重大慢性病的相关风险评估与防控策略研究"):
        st.subheader("2025 年第七届中青杯全国大学生数学解模竞赛")
        # 使用 pdf_viewer 替代 st.pdf()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        docx_file_path = os.path.join(script_dir, "..", "document",
                                      "B202501829.pdf")
        pdf_path = os.path.normpath(docx_file_path)
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_viewer(f.read(), width=700, height=600)
        else:
            st.error(f"PDF文件未找到：{pdf_path}")
