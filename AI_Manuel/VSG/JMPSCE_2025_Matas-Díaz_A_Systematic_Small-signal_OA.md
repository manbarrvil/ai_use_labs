102 

JOURNAL OF MODERN POWER SYSTEMS AND CLEAN ENERGY, VOL. 13, NO. 1, January 2025 

## A Systematic Small-signal Analysis Procedure for Improving Synchronization Stability of Grid-forming Virtual Synchronous Generators 

Francisco Jesús Matas-Díaz, Manuel Barragán-Villarejo, and José María Maza-Ortega 

_**Abstract**_ **— The integration of converter-interfaced generators (CIGs) into power systems is rapidly replacing traditional syn‐ chronous machines. To ensure the security of power supply, modern power systems require the application of grid-forming technologies. This study presents a systematic small-signal anal‐ ysis procedure to assess the synchronization stability of gridforming virtual synchronous generators (VSGs) considering the power system characteristics. Specifically, this procedure offers guidance in tuning controller gains to enhance stability. It is ap‐ plied to six different grid-forming VSGs and experimentally tested to validate the theoretical analysis. This study concludes with key findings and a discussion on the suitability of the ana‐ lyzed grid-forming VSGs based on the power system character‐ istics.** 

_**Index Terms**_ **— Voltage source converter (VSC), grid-forming controller, virtual synchronous generator (VSG), small-signal stability analysis.** 

## I. INTRODUCTION 

**T** HE transition to a power system dominated by renew‐able energy sources (RESs) interfaced with power elec‐ tronics converters is an indisputable fact. These new convert‐ er-interfaced generators (CIGs) have been installed across all voltage levels, from transmission to distribution networks [1]. This transition makes the modern power system suscepti‐ ble to large frequency and voltage deviations due to the re‐ duced inertia and damping [2], limited primary frequency re‐ sponse (PFR) stemming from the maximum power point (MPP) operation [3], and new instabilities emerging from CIG dynamics [4]. As a result, the new functionalities of CIGs are required to ensure a safe and reliable operation of the power system [5]. 

Fortunately, new operation modes of CIGs have been de‐ veloped to address the technical challenges associated with 

Manuscript received: March 23, 2024; revised: July 16, 2024; accepted: No‐ vember 14, 2024. Date of CrossCheck: November 14, 2024. Date of online pub‐ lication: January 30, 2025. 

This work was supported by Grant PID2021-124571OB-I00 funded by MICIU/AEI/10.13039/501100011033 and by FEDER, EU. This article is distributed under the terms of the Creative Commons Attribu‐ tion 4.0 International License (http://creativecommons.org/licenses/by/4.0/). F. J. Matas-Díaz, M. Barragán-Villarejo, and J. M. Maza-Ortega (correspond‐ ing author) are with the Department of Electrical Engineering, University of Se‐ ville, 41004 Sevilla, Spain (e-mail: fmatas@us.es; manuelbarragan@us.es; jm‐ maza@us.es). 

large-scale RES integration. Among these, the grid-forming control has gained prominence [6]. Unlike conventional gridfollowing CIGs, which function as AC current sources, the grid-forming CIGs operate as AC voltage sources. In this manner, the grid-forming controller of CIG is in charge of providing the amplitude, frequency, and phase for this volt‐ age source. To achieve this, the grid-forming controller com‐ prises an outer control loop (OCL) that generates setpoints for the inner control loop (ICL) [7]. The OCL is responsible for controlling the active power to maintain the grid synchro‐ nization and the reactive power to regulate the voltage at the point of interconnection (POI). Meanwhile, the ICL is re‐ sponsible for controlling the voltage and/or current at POI according to the setpoints provided by the OCL. Although most grid-forming controllers of CIG adhere to this hierarchi‐ cal structure, they differ in terms of specific implementations [7], [8]. 

The OCLs comprise the active power control loops (AP‐ CLs) and reactive power control loops (RPCLs). The most common APCLs for grid synchronization are: ① droop con‐ trol [9], ② power synchronization control [10], ③ enhanced direct power control [11], ④ synchronverter [12], and ⑤ synchronous power control [13]. The droop control is a wellestablished technique for microgrids, whereas the power syn‐ chronization control is one of the first proposals based on the synchronous generator emulation. The implementation of the synchronverter, i.e., virtual synchronous generator (VSG), is based on the swing equation [14] or a proportional-inte‐ gral (PI) controller [15], which is termed as S-VSG or PIVSG for simplicity in this paper, respectively. The primary difference between them is that the PI-VSG allows the iner‐ tial response to be independent from the PFR. The synchro‐ nous power control computes the VSG angle as a second-or‐ der transfer function of the active power error, thereby in‐ creasing the flexibility in VSG control. On the other hand, the RPCLs for voltage regulation can be categorized into three types: ① droop control [16], ② PI-based control [17], and ③ cascaded control with droop and PI regulators [18]. 

Regarding the ICL, various controllers are presented: ① open-loop controller [19], ② single voltage controller [20], ③ single current controller with virtual admittance [21], [22], and ④ cascaded voltage controller with both voltage and current control loops [23]. The main disadvantage of the first two controllers is their lack of current controllability, which can result in overcurrent during events with fast dy‐ 


$$
\begin{array}{r l}{{\frac{\lambda{\mathcal{L}}}{4{\mathsf{N}}\times}}}&{{}>\mathrm{overat~or~Moorsere~PowasR~Svsrsus}}\\ {{\frac{\lambda{\mathsf{R}}\times}{{\mathsf{R}}\cdot{\mathsf{R}}\cdot{\mathsf{R}}\cdot{\mathsf{R}}\cdot{\mathsf{R}}}\cdot{\mathsf{R}}}}\end{array}
$$


DOI: 10.35833/MPCE.2024.000316 

MATAS-DÍAZ _et al_ .: A SYSTEMATIC SMALL-SIGNAL ANALYSIS PROCEDURE FOR IMPROVING SYNCHRONIZATION STABILITY... 

103 

namics such as short-circuit faults. 

The combination of different OCL and ICL blocks results in a plethora of grid-forming controllers of CIGs. Therefore, it is required to assess the performance of these controllers systematically considering the following aspects [7]: ① syn‐ chronization stability, ② overcurrent management or fault ride-through capability, and ③ the transition between island‐ ed and grid-connected modes. Focusing on the synchroniza‐ tion stability, it has been shown that the grid-forming CIGs can maintain synchronism in weak grids, but they often fail to maintain stability in stiff grids. This instability arises be‐ cause even minor phase differences between the CIG and power grid can lead to significant active power fluctuations [24]. Several studies have attempted to address this issue us‐ ing simplified small-signal impedance models that neglect the ICL dynamics [25]. However, these approaches are inade‐ quate for stability studies [26], as they merely predict the in‐ put-output dynamics at the converter terminals without con‐ sidering how the state variables influence the oscillation modes that determine the system stability margins [27]. Ac‐ cordingly, [28] proposes a small-signal model with a singleinput single-output (SISO) stability analysis approach for a specific CIG implementation. In addition, the stability of grid-forming CIGs has been addressed by small-signal analy‐ sis based on state-space models. Using this small-signal anal‐ ysis technique, [29] evidences that the interaction of feed-for‐ ward terms in cascade controllers in the ICL may lead to in‐ stability regardless of the grid short-circuit ratio (SCR). However, this analysis does not consider the OCL dynamics, which are crucial for a comprehensive stability analysis, as discussed in [19] and [30]-[33]. These studies show that the grid SCR is a critical parameter that can significantly affect the stability of grid-forming CIGs. The findings of these studies are relevant but it is questionable whether they can be generalized across all the possible combinations of OCL and ICL blocks to implement a grid-forming VSG. Similarly, an analytical design approach for a grid-forming controller based on power synchronization control with a voltage-con‐ trolled ICL is presented in [34]. However, this approach uses a specific combination of OCL and ICL blocks that limits its applicability to certain ranges of grid impedances, making it challenging to extend to other types of grid-forming control‐ lers. 

However, recent studies suggest that the SCR may not pro‐ vide accurate estimations of system impedance or strength in converter-dominated power systems. This is mainly because the short-circuit current contributions from voltage source converters (VSCs) and synchronous generators are different. Moreover, it is uncertain how to effectively utilize the SCR information to design the CIG controllers [35], [36]. Despite these recent investigations, the SCR is still being used for characterizing the grid for stability studies [37], but, given the aforementioned uncertainty, modern power systems will require stability analysis covering a wide SCR range. 

Considering this background, the specific contributions of this study can be summarized as follows. 

1) The stability ranges are identified for different types of grid-forming VSGs based on the value _SCR_ and ratio _R/X_ of the grid through a small-signal analysis. 

2) A systematic procedure is proposed based on the analy‐ sis of participation factors, which extends the operating range of grid-forming VSGs by identifying the control state variables with the major weight on the oscillation modes causing system instability. 

3) The control loops that cause synchronization instability for each type of grid-forming VSG are identified. This will show that the ICL dynamics of grid-forming VSGs cannot be neglected in the stability analysis. 

4) The proposed systematic procedure for improving the synchronization stability of grid-forming VSGs is experimen‐ tally validated. 

The remainder of this paper is organized as follows. Sec‐ tion II presents the state-space modeling of grid-forming VSGs. Section III outlines the systematic small-signal analy‐ sis procedure to evaluate the effects of _SCR_ and _R/X_ on the stability range, which is applied to a case study. From this analysis, the controller gains are re-tuned to extend the sta‐ bility range for networks with different characteristics. Sec‐ tion IV describes the experimental validation. Section V dis‐ cusses considerations and important properties of grid-form‐ ing VSGs that should be additionally considered beyond the findings obtained from the small-signal analysis. Section VI concludes by describing the main findings and gives an as‐ sessment of the most suitable OCL-ICL combinations based on power system characteristics. 

## II. STATE-SPACE MODELING OF GRID-FORMING VSGS 

This section details the state-space model of a grid-con‐ nected VSC and the most common OCLs and ICLs to imple‐ ment a grid-forming VSG. The differential equations of the grid-forming VSGs are modeled in the _dq_ frame, synchro‐ nized with the VSG angle _θvsg_ . The models of the APCL and RPCL are nonlinear. Consequently, the linearization of the state-space model is required prior to implementing the sys‐ tematic small-signal analysis procedure proposed in Section III. 

## _A. Grid-connected VSC model_ 

The CIG considered in this study is a three-phase threewire VSC connected to the grid via an LCL coupling filter, which includes a series damping resistor alongside the capac‐ itor, as illustrated in Fig. 1. 


$$
\begin{array}{l l}{{\nu_{k}}}&{{\nu_{l k}}}\\ {{\frac{\Gamma_{\mp}^{+}}{\Gamma}\displaystyle\displaystyle\frac{\vert\displaystyle\bar{\Lambda}\rightarrow}{\vert\displaystyle\frac{\bar{\Lambda}}{\bar{\Lambda}}\vert}\displaystyle\right\vert\displaystyle\frac{\nu_{t,a b c}}{\bar{\Lambda}\vert}\displaystyle\vert\displaystyle\overbrace{\nu_{t,a b c}}^{}\displaystyle L_{s}_{\nu}\displaystyle\langle\displaystyle\frac{R_{s}}{\Lambda}\rangle\displaystyle\frac{\nu_{s,a b c}}{\vert\displaystyle\bar{R}_{d}}\displaystyle\prod_{\bar{s},a b c}\:\sqrt{\mathrm{Power}}}\\ {{\frac{\vert\vphantom\Gamma_{\mp}^{+}}{\mathrm{VSC}}}\displaystyle\left\langle\displaystyle\frac{\bar{\nu}\Omega}{\Lambda}\right)}\end{array}
$$


Fig. 1. One-line diagram of a three-phase three-wire grid-connected VSC. 

The differential equations for the grid-connected VSC in the _dq_ frame are given as: 


$$
\nu_{t}=R_{t}\dot{l_{t}}+L_{t}\frac{\mathrm{d}\dot{l_{t}}}{\mathrm{d}t}+{\omega_{\mathrm{vsg}}}L_{t}\dot{l_{t}}+\nu_{m}\qquad\qquad\qquad(1)
$$


JOURNAL OF MODERN POWER SYSTEMS AND CLEAN ENERGY, VOL. 13, NO. 1, January 2025 

104 


$$
\left.\begin{array}{l l}{{\ }}&{{\ }}\\ {{\hat{l}_{c}=C\,{\frac{\mathrm{d}\nu_{m}}{\mathrm{d}t}}+{\omega}_{\mathrm{veg}}C\nu_{m}-C R_{d}{\frac{\mathrm{d}\hat{l}_{c}}{\mathrm{d}t}}}\\ {{\ }}&{{\ }}&{{\ }}\\ {{\nu_{m}=R_{s}\hat{l}_{s}+L_{s}{\frac{\mathrm{d}\hat{l}_{s}}{\mathrm{d}t}}+{\omega}_{\mathrm{vg}}L_{s}\hat{l}_{s}+\nu_{s}}\end{array}\right.\qquad\qquad(2)
$$


T T where _**v** t_ = [ _vtd_  _vtq_ ] is the VSC voltage; _**v** m_ = [ _vmd_  _vmq_ ] is T the voltage of RC branch; _**v** s_ = [ _vsd_  _vsq_ ] is the grid-side in‐ T ductor voltage; _**i** t_ = [ _itd_  _itq_ ] is the VSC-side current; _**i** s_ = T T [ _[i] sd_[] _[i] sq_ ] is the grid-side current; and _**i** c_ = [ _icd_  _icq_ ] is the ca‐ pacitor current; _ωvsg_ is the angular speed of VSG; _**L** t_ = é **êê** ë _L_[0] _t_ - 0 _Lt_ ù **úú** û and _**L** s_ =[é] **êê** ë _L_[0] _s_ - 0 _Ls_ ù **úú** û are the VSC and grid-side in‐ ductances, which are along with inner resistances _Rt_ and _Rs_ , - _C_ ù respectively; and _Rd_ and _**C**_ =[é] **êê** ë _C_[0] 0 **úú** û are the damping resis‐ tance and capacitance of the coupling filter, respectively. 

The power grid is modeled based on its Thevenin equiva‐ lent as: 


$$
\begin{array}{c c}{{\nu_{s}=R_{g}\dot{\imath}_{s}+L_{g}\frac{\mathrm{d}\dot{\imath}_{s}}{\mathrm{d}t}+L_{g}\omega_{\mathrm{ug}}\dot{\imath}_{s}+\nu_{g}}}&{{(4)}}\\ {{\mathrm{where}\ \nu_{g}=\left[\nu_{g d},\nu_{g q}\right]^{\mathrm{T}}\mathrm{~is~the~grid~voltage,~and~}L_{g}=\left[\begin{array}{c c}{{0}}&{{-L_{g}}}\\ {{L_{g}}}&{{0}}\\ {{\mathrm{and~}R_{g}\ \mathrm{~are~the~sratance,~respectively.}}}\end{array}\right]}}\end{array}
$$


The state-space model of the grid-connected VSC is repre‐ sented in (1)-(4) and contains six state variables: 


$$
\begin{array}{c c c c c}{{X_{f}=\left[\dot{l}_{I d}}}&{{\dot{l}_{I q}}}&{{\dot{l}_{s q}}}&{{\dot{l}_{s q}}}&{{\nu_{m d}}}&{{\i}}&{{\i}}&{{\i}}&{{\i}}&{{\i}}\\ {{X_{f}=\left[\dot{l}_{I d}\right.}}&{{\dot{l}_{t q}}}&{{\i}}&{{\i}}\\ {{\i}}&{{\i}}&{{\i}}&{{\i}}&{{\i}}&{{\i}}\end{array}\right.}}&{{\qquad}}&{{\i}}&{{\i}}\end{array}
$$


## _B. OCLs_ 

Regarding the OCL, the APCL provides the angular speed and angle of virtual rotor, i. e., _ωvsg_ and _θvsg_ , respectively, whereas the RPCL provides the virtual electromotive force, i.e., _E_ . The OCL control schemes, comprising two possible implementations based on S-VSG [38]-[40] or PI-VSG [15], are shown in Fig. 2(a). 


![](JMPSCE_2025_Matas-Díaz_A_Systematic_Small-signal_OA_fig/JMPSCE_2025_Matas-Díaz_A_Systematic_Small-signal_OA.pdf-0003-10.png)


**----- Start of picture text -----**<br>
OCL ICL<br>APCL (S-VSG) p [*] +� p + ω 10 +�+ Js D 1 ++ � ω 0 1 s ωθvsgvsg VC-ICL ei s + � Z + v v m * + v � m + kpv vc + [k] ωs [iv] vcvsg v m + + C + + ++ i s i t *+ �+ i t kpi vc + ωvsg [k] s i [ii] vct + + L + t + ++ vv mt<br>APCL (PI-VSG) p [*] + �+ kpp + [k] s [i][p] Δ ω + ++ ωvsg CC-ICL e + �+ Y v LPF i s *+�+ kpi cc + [k] s [ii] cc + ++ + ++ v t<br>p ω 0 1 s θvsg v s i s ωvsg i s L f v s<br>RPCL (S-VSG or PI-SVG) q [*] + � q + kpq + [k] s [i][q] Δ E + E +0 + E OL-ICL ie s + ssR +� ω + tvr v tvrr v t<br>(a) (b)<br>**----- End of picture text -----**<br>


Fig. 2. Diagrams of OCL and ICL blocks considered for analyzed grid-forming VSGs. (a) OCL. (b) ICL. 

Both S-VSG and PI-VSG consider that the grid voltage ro‐ tates at the nominal frequency _ω_ 0, which acts as a perturba‐ tion with no influence on the system dynamics [41], i.e., _ω_ 0 is a constant parameter. In this manner, the phase difference between the grid voltage _θg_ and the electromotive force an‐ gle _θvsg_ can be defined as _ψ_ [42]: 


$$
\left|\frac{\psi\!\!\!\slash=\theta_{g}-\theta_{w g}}{\mathrm{d}t}\qquad\qquad\qquad\qquad\qquad(6)
$$


The OCL formulation based on the S-VSG or PI-VSG is presented as follows. _1) S-VSG_ 

The APCL based on S-VSG can be expressed as: 


$$
\left.\begin{array}{l l}{\left|J\omega_{0}{\frac{\mathrm{d}\omega_{\mathrm{veg}}}{\mathrm{d}t}}=p^{\ast}-p-D\left(\omega_{\mathrm{vsg}}-\omega_{0}\right)}\\ {\left|{\frac{\mathrm{d}\theta_{\mathrm{veg}}}{\mathrm{d}t}}=\omega_{\mathrm{vsg}}}\end{array}\right.}\qquad\qquad(7)
$$


where _p_ is the measured active power; _p_[*] is the active power 

reference, i.e., virtual mechanical power; _J_ is the rotational inertia; and _D_ is the damping coefficient. Combining (6) and (7) leads to: 


$$
\begin{array}{l l}{{}}&{{\ }}\\ {{\left|{\frac{\mathrm{d}\omega_{\mathrm{vog}}}{\mathrm{d}t}}=p^{*}-p+D{\frac{\mathrm{d}\psi}{\mathrm{d}t}}}\\ {{\left|{\frac{\mathrm{d}\psi}{\mathrm{d}t}}=\omega_{\mathrm{us}}-\omega_{\mathrm{vs}}}}\end{array}\right.}}&{{\qquad\qquad(8)
$$


The RPCL consists of a PI controller, which can be formu‐ lated as: 


$$
\left\begin{array}{c c}{{\left|E=k_{p q}\frac{\mathrm{d}\xi_{q}}{\mathrm{d}t}+k_{i q}\xi_{q}+E_{0}\qquad}}&{{\qquad\qquad\quad(9)}}\\ {{\left|\frac{\mathrm{d}\xi_{q}}{\mathrm{d}t}=q^{*}-q\qquad}}&{{\qquad\qquad(9)}}\end{array}\right.
$$


where _ξq_ is the integral of reactive power error; _q_ is the mea‐ sured reactive power; _q_[*] is the reactive power reference; _E_ 0 is the rated electromotive force; and _kpq_ and _kiq_ are the pro‐ portional and integral gains of PI controller in the RPCL, re‐ spectively. 

MATAS-DÍAZ _et al_ .: A SYSTEMATIC SMALL-SIGNAL ANALYSIS PROCEDURE FOR IMPROVING SYNCHRONIZATION STABILITY... 

105 

Therefore, the S-VSG introduces three state variables in the state-space model: 


$$
{\bf\nabla}_{\mathrm{s.vsg}}=\left[\psi\quad\omega_{\mathrm{vsg}}\quad\xi_{q}\right]^{\mathrm{T}}\qquad\qquad\qquad\qquad\left(10\right)
$$


## _2) PI-VSG_ 

The APCL based on PI-VSG, consisting of a PI controller applied to the active power error, can be written as: 


$$
\begin{array}{c c}{{\left|\frac{\mathrm{d}\psi}{\mathrm{d}t}=-k_{\rho\rho}\frac{\mathrm{d}\xi_{\rho}}{\mathrm{d}t}-k_{i\rho}\xi_{\rho}}}&{{\qquad\qquad}}&{{\qquad(11)}}\\ {{\left|\frac{\mathrm{d}\xi_{\rho}}{\mathrm{d}t}=p^{*}-p}}&{{\qquad\qquad}}&{{\qquad(11)}}\end{array}\right.
$$


where _ξp_ is the integral of active power error; and _kpp_ and _kip_ are the proportional and integral gains of PI controller in the APCL, respectively. 

The RPCL of PI-VSG is identical to that of the S-VSG. Therefore, the PI-VSG introduces three state variables in the state-space model: 


$$
\begin{array}{c c}{{X_{\mathrm{pi.\vsg}}=\left[\psi\,\quad\zeta_{p}\quad\zeta_{p}\quad\zeta_{q}\right]^{\mathsf{T}}\qquad\qquad\qquad\qquad\qquad\left(1\bar{\Lambda}\right)}}\end{array}
$$


## _C. ICLs_ 

Three types of ICLs are considered for the grid-forming VSG: ① voltage controller by means of cascaded controller [24], ② current controller with a virtual admittance [21], and ③ an open-loop voltage controller [19], which are termed as VC-ICL, CC-ICL, and OL-ICL for simplicity, re‐ spectively. The control scheme for each type of ICL is shown in Fig. 2(b). 

## _1) VC-ICL_ 

A cascaded voltage controller composed of voltage and current control loops is used to control the capacitor voltage of the LCL filter. The voltage reference of RC branch _**v**_[*] _m_[ is ] computed as [43]: 


$$
\begin{array}{l l}{{}}&{{\nu_{m}^{*}=e-Z_{\nu}i_{s}}}\\ {{}}&{{}}&{{\mathrm{~~where~}\;\;Z_{\nu}=\left[R_{\nu}\;\;\;-X_{\nu}\right]\;\;\mathrm{~ts~the~~virtual~~impedance;~~and~~}e=[0,}}\\ {{}}&{{}}\\ {{}}&{{}}&{{}}\\ {{}}&{{}}&{{}}\\ {{}}&{{}}\end{array}
$$


A PI voltage controller provides the setpoints to the cur‐ rent control loop: 


$$
\left.\begin{array}{l l}{\left|\displaystyle{\binom{i}{l}}_{t}^{*}=k_{p v}^{\nu c}{\frac{\mathrm{d}\widetilde\zeta_{\nu}}{\mathrm{d}t}}+k_{i\nu}^{\nu c}\widetilde\zeta_{\nu}+\omega_{\nu\mathrm{e}}C\nu_{m}+\widetilde{l}_{s}~~~~~~~~~~~~~~~~~(14)}\end{array}\right.
$$


T where _**ξ** v_ = [ _ξvd_  _ξvq_ ] is the integral of the voltage error; _**i** t_[*][ is ] the VSC-side current reference; and _kpv[vc]_[ and ] _[k][ vc] iv_[ are the pro‐] portional and integral gains of the PI voltage controller in VC-ICL, respectively. 

The tracking of _**i** t_[*][ is carried out in the current control loop, ] which is based on a PI current controller and modeled as: 


$$
\left.\begin{array}{l l}{{\displaystyle\Big|{\nu_{t}=k_{p i}^{~\mathrm{wc}}{\frac{\mathrm{d}\tilde{\zeta}_{i}}{\mathrm{d}t}}+k_{i i}^{~\nu c}\zeta_{i}+\omega_{\mathrm{wg}}{\cal L}_{t}\dot{l}_{t}+\nu_{m}}}&{{~~~}}&{{~~~~~(15)}}\end{array}\right.
$$


T where _**ξ** i_ = [ _ξid_  _ξiq_ ] is the integral of the current error; and _kpi[vc]_[ and ] _[k][ vc] ii_[ are the proportional and integral gains of the PI ] current controller in VC-ICL, respectively. 

Based on (13)-(15), the VC-ICL adds four new state vari‐ ables to the state-space model: 


$$
\begin{array}{c c c}{{\mathrm{~}}}&{{\zeta_{i q}\quad\left.\bar{\zeta}_{i d}\quad\bar{\zeta}_{i q}\right]^{\mathrm{T}}\qquad\qquad\qquad}}&{{\qquad(16)\qquad}}\end{array}
$$


## _2) CC-ICL_ 

CC-ICL controls the grid-side inductor current of LCL fil‐ ter. To achieve this, a PI controller is applied to the current error. The grid-side current reference _**i** s_[*][ is obtained using a ] virtual admittance and a low-pass filter (LPF) as: 


$$
i_{s}^{\log}=V_{\psi}\left(e-\nu_{s}\right)\qquad\qquad\qquad\qquad\qquad\qquad\left(17\right)
$$



$$
i_{s}^{\log}=\tau_{l_{d}/{\overline{{{l}}}}}{\frac{\mathrm{d}{\widehat{l}}_{s}^{\ast}}{\mathrm{d}t}}+{\hat{l}}_{s}^{\ast}\qquad\qquad\qquad\qquad\qquad(18)
$$


where _τlpf_ is the time constant of LPF; _**i** s[vsg]_[ is the input cur‐] rent of LPF; and _**Y** v_ =[é] **êê** ë - _[G] B[v] v GBvv_ ù **úú** û is the virtual admittance 

matrix, with _Gv_ and _Bv_ being the virtual conductance and susceptance, respectively. The differential equations of the PI current controller, including the cross-coupling cancellation and feed-forward terms, are expressed as: 


$$
\left|\begin{array}{l l}{{\nu_{i}=k_{p i}^{c c}\frac{\bar{\mathrm{g}}_{i}}{\mathrm{d}t}+k_{i i}^{c c}\tilde{\mathrm{g}}_{i}+\omega_{\nu g}L_{j i}{\dot{\lambda}}_{s}+\nu_{s}}}&{{\qquad\qquad(19)}}\\ {{\left|\frac{\mathrm{d}\tilde{\mathrm{g}}_{i}}{\mathrm{d}t}=\dot{\iota}_{s}^{*}-i_{s}}}&{{\qquad\qquad(19)}}\end{array}\right.
$$


where _**L** f_ = _**L** t_ + _**L** s_ ; and _kpi[cc]_[ and ] _[k][ cc] ii_[ are the proportional and ] integral gains of the PI current controller in CC-ICL, respec‐ tively. 

Therefore, based on (17)-(19), the CC-ICL adds four state variables to the state-space model: 


$$
{\cal X}_{c c}=\left[i_{s d}^{\ast}\quad i_{s q}^{\ast}\quad\xi_{i d}^{x}\quad\zeta_{i q}^{z}\right]^{\mathrm{T}}\qquad\qquad\qquad\qquad(20)
$$


## _3) OL-ICL_ 

The OL-ICL directly applies the virtual electromotive force _E_ to the VSC terminals. A slight modification of _E_ is proposed using a transient virtual resistor (TVR) to provide more damped current dynamics [39]. The TVR consists of a first-order high-pass filter, which is formulated as: 

_Rtvr_ dd _**i** ts_[=] dd _**v** tr_[+] _[ ω][tvr]_ _**[v]**[r]_ (21) T where _**v** r_ = [ _vrd_  _vrq_ ] is the output voltage of TVR; and _Rtvr_ and _ωtvr_ are the gain and cut-off frequency of high-pass fil‐ ter, respectively. Then, the VSC terminal voltage is comput‐ ed as: 


$$
\nu_{t}=e-\nu_{r}\qquad\qquad\qquad\qquad\qquad\qquad(22)
$$


The OL-ICL introduces two new state variables to the state-space model: 


$$
{\bf x}_{o l}=\biggl[\,\nu_{r d}\quad\nu_{r q}\,\biggr]^{\mathrm{T}}\qquad\qquad\qquad\qquad\qquad\qquad(23)
$$


It is important to note that for different ICLs, the power terms used in the corresponding OCL blocks are computed at different nodes, i.e., at the capacitor branch of LCL filter for the VC-ICL, at the POI for the CC-ICL, and at the VSC 

JOURNAL OF MODERN POWER SYSTEMS AND CLEAN ENERGY, VOL. 13, NO. 1, January 2025 

106 

terminals for the OL-ICL. 

Therefore, six state-space models of grid-forming VSG are derived based on the selected OCL and ICL blocks, which can be formulated in a generalized form as: 


$$
\begin{array}{l l}{{\left|\begin{array}{l l}{{\dot{x}_{\mathrm{oCL-1CL}}=A x_{\mathrm{oCL-3CL}}+B u}}\\ {{\left|\left.u=\left[\left.p^{*}}}\end{array}\right|}}&{{\qquad}}&{{\qquad(24)}}\end{array}\right.
$$


where _**A**_ and _**B**_ are the state-space matrices; and the state vector _**x**_ OCL - ICL is composed of the state variables of grid-con‐ nected VSC in (5), the state variables of OCL in (10) or (12), and state variables of ICL in (16), (20), or (23). 

III. SYSTEMATIC SMALL-SIGNAL ANALYSIS PROCEDURE FOR SYNCHRONIZATION STABILITY 

This section presents a systematic small-signal analysis procedure to ensure the synchronization stability and good dynamic performance of the grid-forming VSGs in power systems with different _SCR_ and _R/X_ . 

## _A. Proposed Systematic Procedure_ 

This subsection presents the steps of the proposed system‐ atic procedure for improving the synchronization stability of grid-forming VSGs. The fundamentals of the small-signal analysis are presented in Supplementary Material A. The pro‐ posed systematic procedure consists of the following steps. 

_Step 1_ : validate the linear model against the original non‐ linear model by comparing the dynamic performance of some key magnitudes, such as the active and reactive power used in the OCL. 

_Step 2_ : identify stable and unstable regions over a wide range of _SCR_ and _R_ / _X_ through a small-signal analysis based on the linear model. 

_Step 3_ : identify the eigenvalues associated with the critical oscillation modes at the boundary between stable and unsta‐ ble regions. These eigenvalues are those that lead the system to unstable operation. 

_Step 4_ : based on these critical oscillation modes, detect the critical state variables by analyzing their corresponding participation factors for the unstable region identified in _Step 3_ . In particular, the critical state variables are those with the largest participation factors in the critical oscillation modes. De‐ tailed information on the computation and interpretation of par‐ ticipation factors can be found in Supplementary Material A. 

_Step 5_ : perform a sensitivity analysis of the controller gains associated with the critical state variables within the unstable region identified in _Step 3_ to increase the synchroni‐ zation stability range of the grid-forming VSG. 

## _B. Case Study_ 

This subsection presents a case study using a CIG with the parameters shown in Table I to illustrate the application of the proposed systematic procedure. The controller gains of the grid-forming VSG are selected according to the state of the art. Specifically, the APCL and RPCL gains of PIVSG as well as the control parameters of CC-ICL are ob‐ tained from [42]. The S-VSG gains are calculated following [15], considering the same inertia constant as that of the PIVSG and a damped response. The TVR in the OL-ICL is ob‐ tained from [39], the VC-ICL gains are computed using the 

best pole location [24], and the virtual impedance is calculat‐ ed using a sensitivity analysis [42]. The equilibrium point _**x**_ 0 is used to linearize the system considering the input vector _**u**_ 0 = [ 9  kW  4.5  kvar ]. 

## TABLE I 

SYSTEM PARAMETERS FOR CASE STUDY 

|Parameter<br>Value|Parameter<br>Value|
|---|---|
|_Lt_(mH)<br>_Rt_(Ω)<br>_Ls_(mH)<br>_Rs_(Ω)<br>_Rv_(Ω)<br>_kpp_(rad/s·W-1)<br>_J_(kg×m2)<br>_kpq_(V/W)<br>_Rtvr_(Ω)<br>_ω_0(rad/s)<br>_Rd_(Ω)<br>_Cf_(μF)<br>_E_0(V)<br>_Vg_(V)<br>1.25<br>0.04<br>1.25<br>0.04<br>0<br>0.0012<br>2.03<br>0.0016<br>0.09<br>100π<br>10<br>4<br>230<br>2<br>230<br>2|_Xv_(Ω)<br>_kip_(rad/s·W-1)<br>_D_(sNm/rad)<br>_kiq_(V/W)<br>_ωtvr_(rad/s)<br>_τlpf_(ms)<br>_k cc_<br>_pi_ (V/A)<br>_k cc_<br>_ii_ (V/A)<br>_Gv_(S)<br>_Bv_(S)<br>_k vc_<br>_pv_(A/V)<br>_k vc_<br>_iv_ (A/V)<br>_k vc_<br>_pi_ (V/A)<br>_k vc_<br>_ii_  (V/A)<br>0.08<br>0.0016<br>47.36<br>0.0163<br>60<br>1.6<br>1.25<br>40<br>0<br>1.25<br>0.1<br>0.1<br>0.1<br>15.1|



_Step 1_ : the linear model is validated by comparing its step response with that of the nonlinear model. Figure 3 com‐ pares the step response of linear and nonlinear models with ac‐ tive and reactive power step changes of D _p_[*] = 0.5 kW and D _q_[*] = 0.5 kvar, respectively, with respect to the input vector _**u**_ 0. 

|0<br>9.6<br>9.4<br>9.2<br>9.0<br>8.8<br>_p_(kW)||||0.25<br>0.50||0.75<br>1.00<br>5.00<br>4.75<br>4.50<br>4.25|_q_(kvar)|
|---|---|---|---|---|---|---|---|
|0<br>9.6<br>9.4<br>9.2<br>9.0<br>8.8<br>_p_(kW)||||0.25<br>0.50<br>Time (s)<br>Time (s)<br>(a)||0.75<br>1.00<br>5.00<br>4.75<br>4.50<br>4.25|_q_(kvar)|
|(b)<br>Linear model:<br>Nonlinear model:<br>_p_(OL-ICL);<br>_p_(OL-ICL);<br>_q_(OL-ICL);<br>_q_(OL-ICL);<br>_q_(CC-ICL);<br>_q_(CC-ICL);<br>_q_(VC-ICL)<br>_q_(VC-ICL)<br>_p_(VC-ICL)<br>_p_(VC-ICL)<br>_p_(CC-ICL);<br>_p_(CC-ICL);||||||||



Fig. 3. Step response of linear and nonlinear models to active and reactive power step changes of D _p_[*] = 0.5 kW and D _q_[*] = 0.5 kvar. (a) S-VSG. (b) PIVSG. 

The active power and reactive power are computed at the midpoint of the LCL filter to which the capacitor is connect‐ ed. The active and reactive power step changes are applied to all the combinations of OCL and ICL blocks at different time instants in a compact manner without overlaps. In addi‐ tion, note that the steady-state active power and reactive power for each ICL are different, since the power involved in the OCL depends on the implemented ICL, as previously 

MATAS-DÍAZ _et al_ .: A SYSTEMATIC SMALL-SIGNAL ANALYSIS PROCEDURE FOR IMPROVING SYNCHRONIZATION STABILITY... 

107 

described in Section II. Figure 3 demonstrates that all the lin‐ ear models accurately match the dynamics of the respective nonlinear models. Therefore, it is possible to perform a rigor‐ ous stability and dynamic performance analysis using the lin‐ ear models. 

_Step 2_ : the objective of this step is to evaluate the stabili‐ ty of the six grid-forming VSGs with different combinations of OCL and ICL blocks in different power grids. According to the implemented OCL and ICL blocks, the six grid-form‐ ing VSGs can be termed as S-VC, S-CC, S-OL, PI-VC, PICC, and PI-OL. A wide range of _SCR_ and _R/X_ is used to characterize different power grids. According to the standard IEEE Std. 1204-1997 [44], the threshold between a strong and a weak grid can be set to be _SCR_ = 3, which means that a system is very weak when _SCR_ < 3 and very strong when 

_SCR_ > 3. In addition, the standard IEEE Std. 519-2014 [45] assigns typical ranges to high-voltage (HV), medium-voltage (MV), and low-voltage (LV) networks based on the ratio be‐ tween the maximum short-circuit current and the maximum demand load current for the fundamental frequency at the POI. This ratio can be considered identical to _SCR_ for rated voltage values, so the _SCR_ ranges for HV, MV, and LV grids are: _SCRHV_ Î [ 0  50], _SCRMV_ Î [ 0  1000], and _SCRLV_ Î [ 0  1000], respectively. Therefore, the performance of the six grid-forming VSGs is evaluated with _SCR_ Î [1  800] and _R/X_ Î [ 0.06  1.91], which covers all the voltage levels. Fig‐ ure 4 illustrates the stable region for the six grid-forming VSGs within these intervals. 

Figure 4 also illustrates areas that correspond to HV, MV, and LV grids with pairs of _SCR_ and _R/X_ based on [45]. 


![](JMPSCE_2025_Matas-Díaz_A_Systematic_Small-signal_OA_fig/JMPSCE_2025_Matas-Díaz_A_Systematic_Small-signal_OA.pdf-0006-06.png)


**----- Start of picture text -----**<br>
Weak grid Strong grid Weak grid Strong grid Weak grid Strong grid<br>1.91 1.91 1.91<br>1.59 1.59 1.59<br>1.27 1.27 1.27<br>0.95 0.95 0.95<br>0.64 0.64 0.64<br>0.32 0.32 0.32<br>0.25 0.25 0.25<br>0.19 0.19 0.19<br>0.13 0.13 0.13<br>0.06 0.06 0.06<br>1 3.13 6.25 15 50 800 1 3.13 6.25 15 50 800 1 3.13 6.25 15 50 800<br>2.5 4.15 12.5 25 265 2.5 4.15 12.5 25 265 2.5 4.15 12.5 25 265<br>SCR SCR SCR<br>(a) (b) (c)<br>Weak grid Strong grid Weak grid Strong grid Weak grid Strong grid<br>1.91 1.91 1.91<br>1.59 1.59 1.59<br>1.27 1.27 1.27<br>0.95 0.95 0.95<br>0.64 0.64 0.64<br>0.32 0.32 0.32<br>0.25 0.25 0.25<br>0.19 0.19 0.19<br>0.13 0.13 0.13<br>0.06 0.06 0.06<br>1 3.13 6.25 15 50 800 1 3.13 6.25 15 50 800 1 3.13 6.25 15 50 800<br>2.5 4.15 12.0 25 265 2.5 4.15 12.5 25 265 2.5 4.15 12.0 25 265<br>SCR SCR SCR<br>(d) (e) (f)<br>Stable region; Unstable region; HV grid; MV grid; LV grid<br>Initial value of  SCR  and  R/X  for experimental test; Final value of  SCR  and  R/X  for experimental test<br>R/X R/X R/X<br>R/X R/X R/X<br>**----- End of picture text -----**<br>


Fig. 4. Stable region for six grid-forming VSGs within _SCR_ Î [1  800] and _R/X_ Î [ 0.06  1.91]. (a) S-VC. (b) S-CC. (c) S-OL. (d) PI-VC. (e) PI-CC. (f) PIOL. 

The results for the PI-VSG show that the ICLs based on voltage control, i.e., PI-OL and PI-VC, are generally stable for LV grids, i.e., with high _R/X_ , except for very high _SCR_ . This stability is compromised when the power grid becomes inductive for _R/X_ < 0.19, regardless of _SCR_ . In addition, it is observed that both PI-OL and PI-VC are unstable when _SCR_ > 25 regardless of _R/X_ . This means that PI-OL and PIVC are not recommended for CIGs connected to grids with low impedance and/or high reactance, i.e., HV grids. Regard‐ ing the PI-CC, the system is stable with medium/high _SCR_ and medium/low _R/X_ , i.e., HV and MV grids, achieving full stability for _SCR_ > 25 regardless of _R/X_ . In addition, a large _R/X_ contributes to the system stability, irrespective of _SCR_ . 

This suggests that PI-CC is not suitable for networks with high impedance and/or high reactance. In the case of the S- VSG, the ICLs based on voltage control, i.e., S-VC and S- OL, follow a similar pattern to PI-VC and PI-OL. However, they guarantee stability across the entire range of _SCR_ and _R/ X_ . This does not happen in the S-CC, whose performance is very similar to the PI-CC, but achieving a wider stable re‐ gion for _SCR_ > 6.25 regardless of _R/X_ . This analysis derives that the performance is similar among the following groups of grid-forming VSGs: ① PI-OL and PI-VC, ② PI-CC and S-CC, and ③ S-OL and S-VC. In addition to the informa‐ tion provided by this small-signal stability analysis, it is pos‐ sible to provide some physical insights about the perfor‐ 

JOURNAL OF MODERN POWER SYSTEMS AND CLEAN ENERGY, VOL. 13, NO. 1, January 2025 

108 

mance of these groups. PI-OL and PI-VC perform like volt‐ age sources. Accordingly, their stability deteriorates in stiff networks with high _SCR_ , as two voltage sources coupled via a small impedance may experience significant active power variations due to minor phase differences. In this regard, in‐ creasing the coupling impedance, i.e., reducing _SCR_ , the sta‐ ble region of the system widens. By contrast, PI-CC and S- CC behave like a current source from the view of synchroni‐ zation. They may perform well when connected to stiff grids but deteriorate in weak grids with low _SCR_ . The performanc‐ es of S-OL and S-VC are similar to their counterparts based on the PI-VSG, i.e., PI-OL and PI-VC, respectively. Howev‐ er, due to the selected damping coefficient _D_ , they offer a fully stable operation within the analyzed intervals of _SCR_ and _R/X_ . For this reason, no further steps of the proposed procedure are applied to these grid-forming VSGs. 

_Step 3_ : according to Fig. 4, the boundaries between the stable and unstable regions are clearly identified for each grid-forming VSG. The pair of _SCR_ = 25 and _R/X_ = 0.32 is chosen as a representative point to identify the eigenvalues that cause the system to become unstable for PI-OL and PIVC. This instability is related to the eigenvalues with posi‐ tive real parts, i.e., _λ_ 5 and _λ_ 6, as shown in Table II. 

TABLE II 

CRITICAL OSCILLATION MODES OF GRID-FORMING VSGS 

|VSG|_SCR_|_R/X_|Eigenvalue|Re(_λ_)|_fk_(Hz)|_ζk_|
|---|---|---|---|---|---|---|
|PI-OL|25.00|0.32|_λ_5,_λ_6|14.92|67.21|-0.035|
|PI-VC<br>PI-CC<br>S-CC|25.00<br>6.25<br>6.25|0.32<br>0.32<br>0.32|_λ_5,_λ_6<br>_λ_3,_λ_4<br>_λ_3, _λ_4|27.80<br>5.40<br>14.54|97.59<br>1140.00<br>1140.00|-0.045<br>-0.001<br>-0.002|



Table II also lists the frequency _fk_ and damping _ζk_ of the oscillation mode associated with this pair of complex eigen‐ values. Note that the frequencies of the critical oscillation mode are below 100 Hz for both PI-OL and PI-VC. In the case of PI-CC and S-CC, the instability is analyzed using 

the pair of _SCR_ = 6.25 and _R/X_ = 0.32. For these two gridforming VSGs, the eigenvalues with positive real parts that cause system instability are _λ_ 3 and _λ_ 4, with the frequency of this critical oscillation mode exceeding 1000 Hz, as shown in Table II. 

_Step 4_ : once the critical oscillation modes of each gridforming VSG have been identified, an in-depth analysis is performed within the boundary between the stable and unsta‐ ble regions. Figure 5(a) represents the evolution of the eigen‐ values associated with the critical oscillation mode of PIOL, i.e., _λ_ 5 and _λ_ 6, when _SCR_ increases from 1 to 800 and _R_ / _X_ decreases from 1.91 to 0.06. Note that, according to Fig. 4, these variations shift the system from a stable to an unsta‐ ble region, which is confirmed in Fig. 5, as the real parts of _λ_ 5 and _λ_ 6 become positive. Table III shows the participation factors of state variables _x_ related to the analyzed grid-form‐ ing VSGs for both stable and unstable scenarios. In the case of PI-OL, the participation factor of the state variable _ψ_ in the oscillation mode associated with _λ_ 5 and _λ_ 6 is the largest one in the unstable scenario of _SCR_ = 800 and _R/X_ = 0.06. This means that _ψ_ is the state variable with the highest con‐ tribution to this unstable mode. This state variable is associ‐ ated with the APCL in the OCL, which is consistent with the low-frequency oscillation mode of _λ_ 5 and _λ_ 6, as the OCL has slow dynamics. These conclusions can be extended to the PI-VC, which has a similar performance to the PI-OL, as depicted in Table III. 


$$
\left.{\begin{array}{l l l l}{{\frac{c}{\pi}}\right.500}\\ {{\frac{c}{\pi}}}&{{0}}\\ {{\frac{\pi}{\pi}}}&{{0}}\\ {{\frac{\pi}{\frac{\pi}{\pi}}}}&{{\frac{1}{\frac{\pi}{\pi}}\cdot\ddots}}&{{\ddots}}&{{\sqrt{0}}}\\ {{\frac{\pi}{\frac{\pi}{\pi}}}}&{{0}}\\ {{\frac{\pi}{\frac{\pi}{\pi}}}}&{{\sqrt{\frac{\pi}{\frac{\pi}{\pi}}}}&{{\sqrt{\frac{\pi}{\frac{\pi}{\pi}}}}}&{{\frac{\pi}{\frac{\pi}{\frac{\pi}{\pi}}}}}&{{\frac{\pi}{\frac{\pi}{\frac{\pi}{\pi}}}\cdot\ddots}}}&{{x}}\\ {{\frac{\frac{\pi}{\pi}{\pi}{\sqrt{\pi}}}{(0)}}&{\sqrt{\frac{\pi}{\pi}}{\sqrt{\pi}}\frac{\frac{\pi}{\pi}{\sqrt{\pi}}}{\sqrt{\frac{\pi}{\pi}{\pi}{\pi}{\frac{\pi}{\sqrt{\pi}}}\pi}\end{array}}}&{\end{array}}}}\end{array}\end{array}}}\\ {\end{array}\right.
$$


**----- Start of picture text -----**<br>
500 20<br>10<br>λ 5 λ 3<br>0 0<br>λ 6 -10 λ 4<br>-500 -20<br>-600 -400 -200 0 200 -10 -5 0 5 10<br>Real axis Real axis<br>SCR  increases and  R / X  decreases SCR  decreases and  R / X  increases<br>(a) (b)<br>Imaginary axis Imaginary axis<br>**----- End of picture text -----**<br>


Fig. 5. Evolution of eigenvalues associated with critical oscillation mode of PI-OL and PI-CC when _SCR_ and _R/X_ change. (a) PI-OL. (b)PI-CC. 

TABLE III 

PARTICIPATION FACTORS OF STATE VARIABLES RALATED TO GRID-FORMING VSGS FOR BOTH STABLE AND UNSTABLE SCENARIOS 

|_x_|Participation factor|Participation factor|Participation factor|Participation factor|Participation factor|Participation factor|Participation factor|Participation factor|
|---|---|---|---|---|---|---|---|---|
||PI-OL(_λ_5,_λ_6)||PI-VC(_λ_5,_λ_6)||PI-CC(_λ_3,_λ_4 )||S-CC(_λ_3,_λ_4)||
||_SCR_=1,_R_/_X_=<br>1.91 (stable)|_SCR_=800,_R_/_X_=<br>0.06 (unstable)|_SCR_=1,_R_/_X_=<br>1.91 (stable)|_SCR_=800,_R_/_X_=<br>0.06 (unstable)|_SCR_=800,_R_/_X_=<br>1.91 (stable)|_SCR_=1,_R_/_X_=<br>0.06 (unstable)|_SCR_=800,_R_/_X_=<br>1.91 (stable)|_SCR_=1,_R_/_X_=<br>0.06 (unstable)|
|_ψ_<br>_ω_<br>_ξp_<br>_ξq_<br>_ξvd_<br>_ξvq_<br>_i_*<br>_sd_<br>_i_*<br>_sq_<br>_ξid_<br>_ξiq_<br>_vrd_<br>_vrq_|0.03<br>0<br>0<br>0.01<br>0.01<br>0.18<br>0<br>0<br>0.03<br>0.03<br>0.03<br>0<br>0<br>0<br>0<br>0<br>0<br>0.23<br>0<br>0.01<br>0<br>0<br>0<br>0<br>0<br>0<br>0<br>0<br>0<br>0<br>0<br>0<br>0<br>0<br>0.18<br>0.18<br>0<br>0<br>0<br>0<br>0<br>0<br>0<br>0<br>0<br>0<br>0<br>0<br>0.18<br>0.18<br>0<br>0||||||||



MATAS-DÍAZ _et al_ .: A SYSTEMATIC SMALL-SIGNAL ANALYSIS PROCEDURE FOR IMPROVING SYNCHRONIZATION STABILITY... 

109 

Similarly, the sensitivity analysis of the critical oscillation mode of the PI-CC associated with the complex eigenvalues _λ_ 3 and _λ_ 4 is shown in Fig. 5(b). The evaluation range is iden‐ tical to that of the PI-OL, but both _SCR_ and _R_ / _X_ decrease, from 800 to 1 and 1.91 to 0.06, respectively, to move from a stable rgion to an unstable region according to Fig. 4. At the initial values of _SCR_ = 800 and _R/X_ = 1.91, the system is sta‐ ble and then tends to instability as the _SCR_ and _R/X_ de‐ crease. In this case, the state variables with the largest partic‐ ipation factors are _i_[*] _sd_[ and ] _[i]_[*] _sq_[, as shown in Table III. These ] state variables correspond to the filtered current references obtained from the virtual admittance in (17) and (18) in the ICL. This result is consistent with the oscillation mode asso‐ ciated with eigenvalues _λ_ 3 and _λ_ 4, as the ICL is characterized by fast dynamics. This analysis can be extended to the S-CC because its performance is very similar to that of the PI-CC. _Step 5_ : the aim of this step is to increase the stability range and improve the dynamic performance of grid-forming VSGs affected by the network impedance variation. This is accomplished by re-tuning the controller gains based on the small-signal analysis. 

The stability problems of the PI-OL and PI-VC are related to the APCL in OCL; therefore, according to (11), re-tuning their PI controller gains is logical. The proportional gain _kpp_ is modified, as the integral gain _kip_ is directly related to the inertia constant, i.e.  _kip_ = 1/ ( 2 _H_ ) and cannot be modified so that the VSG inertial response remains unaffected. Figure 6 shows how the eigenvalues _λ_ 5 and _λ_ 6, related to the critical oscillation modes of the PI-OL and PI-VC, shift to the left when _kpp_ decreases from 1.2 ´ 10[-][3] to 7.8 ´ 10[-][5] rad/s·W[-][1] , thereby stabilizing the system and progressively increasing the damping of this oscillation mode. _SCR_ = 25 and _R/X_ = 0.32 are selected to represent the boundary between the sta‐ ble and unstable regions used in _Step 3_ . In addition, it is al‐ so observed that the eigenvalues _λ_ 7 and _λ_ 8 become complex and a new low-frequency oscillation mode at approximately 2 Hz appears when _kpp_ = 2.5 ´ 10[-][4] rad/s·W[-][1] . From this anal‐ ysis, the new proportional gain is set to be _kpp_ = 2.5 ´ 10[-][4] rad/s·W[-][1] , ensuring greater damping of _λ_ 5 and _λ_ 6 with‐ out exciting _λ_ 7 and _λ_ 8. 


$$
\begin{array}{l l l}{{\frac{\pi}{\xi}}}&{{\mathrm{{\frac{\varphi}{\xi}}}\mathrm{{\frac{\varphi}{\bar{z}}}}\mathrm{{\frac{\varphi}{\hat{z}}}}\mathrm{{\frac{\varphi}{\hat{z}}}}\mathrm{{\frac{\varphi}{\hat{z}}}}\mathrm{{\frac{\varphi}{\hat{z}}}}\mathrm{{\frac{\varphi}{\hat{z}}}}\mathrm{{\frac{\varphi}{\hat{z}}}}\mathrm{{\frac{\varphi}{\hat{z}}}}\mathrm{{\frac{\varphi}{\hat{z}}}}\mathrm{{\frac{\varphi}{\hat{z}}}}\mathrm{{\frac{\varphi}{\hat{z}}}}\mathrm{{\frac{\varphi}{\hat{z}}}}\mathrm{{\frac{\varphi}{\hat{z}}{\hat{z}}}}\mathrm{{\frac{\varphi}{\hat{z}}}}\mathrm{{\frac{\varphi}{\hat{z}}}}\mathrm{{\frac{\varphi}{\hat{z}}}}}\mathrm{{\frac{\hat{\bfy}}{\bf{z}}}}}\mathrm{\frac{\frac{\bf{\varphi}}{\bf{\bf\hat{\mathrm{\bfz}}}}}}}}}\\ {\end{array}
$$


**----- Start of picture text -----**<br>
500 500<br>-2502500 λ 7 λ 8 λλ 65 -2502500 λ 7 λ 8 λλ 65<br>-500 -500<br>-150 -100 -50 0 50 -100 -50 0 50 100<br>Real axis Real axis<br>k decreases k decreases<br>pp  pp<br>(a) (b)<br>Imaginary axis Imaginary axis<br>**----- End of picture text -----**<br>


Fig. 6. Evolution of eigenvalues for PI-OL and PI-VC when _kpp_ decreases. (a) PI-OL. (b) PI-VC. 

The instability of S-CC and PI-CC is fundamentally differ‐ ent because the root of this problem lies within the virtual admittance and its LPF. Therefore, the targeted control pa‐ rameters to be re-tuned are _Gv_ , _Bv_ , and _τlpf_ . Note that increas‐ ing _Gv_ destabilizes the system, whereas decreasing _Bv_ and/or increasing _τlpf_ have a stabilizing effect [42]. The eigenvalue analysis is performed using the grid parameters given in 

_Step 3_ , with _SCR_ = 6.25 and _R/X_ = 0.32. In this regard, Fig. 7(a) shows that, for the PI-CC, the eigenvalues _λ_ 3, _λ_ 4, _λ_ 7, and _λ_ 8 shift to the left when _Bv_ decreases from 12.5 to 0.25 S. By contrast, _λ_ 5 and _λ_ 6 shift to the right, leading to an oscillation mode with lower natural frequency and damping. A similar changing trend of eigenvalues _λ_ 3 - _λ_ 6 occurs when _τlpf_ increas‐ es from 0.8 to 5.4 ms, as shown in Fig. 7(b). Regarding _λ_ 7 and _λ_ 8, they follow a curved trajectory and begin moving to the right when _τlpf_ = 4 ms. From this analysis, the selected control parameters for PI-CC and S-CC are _τlpf_ = 2.4 ms and _Bv_ = 0.25 S. 


![](JMPSCE_2025_Matas-Díaz_A_Systematic_Small-signal_OA_fig/JMPSCE_2025_Matas-Díaz_A_Systematic_Small-signal_OA.pdf-0008-08.png)


**----- Start of picture text -----**<br>
500 500<br>0 λ 7 0 λ 7<br>λ 8 λ 8<br>-500 -500<br>-400 -200 0 -250-225-200-175<br>10000 10000<br>0 λ 5 λ 3 0 λ 5 λ 3<br>λ 6 λ 4 λ 6 λ 4<br>-10000<br>-20000 -10000 0 10000 -10000 -5000 0 5000<br>Real axis Real axis<br>Bv  decreases τlpf  increases<br>(a) (b)<br>Imaginary axis Imaginary axis<br>**----- End of picture text -----**<br>


Fig. 7. Evolution of eigenvalues for PI-CC. (a) _Bv_ decreases. (b) _τlpf_ in‐ creases. 

These re-tuned control parameters significantly extend the stable region for all grid-forming VSGs, as shown in Fig. 8. 

## IV. EXPERIMENTAL RESULTS 

This section aims to experimentally validate the stability and dynamic response of the grid-forming VSGs to sudden changes in grid impedance. 

The experimental validation of the six grid-forming VSGs is conducted using a testbed based on the single-line dia‐ gram shown in Fig. 9. It consists of a three-phase three-wire VSC supplied from a 750 V DC voltage source. The VSC setpoints are the same as those used in the theoretical analy‐ sis, namely, _**u**_ 0 = [ 9  kW  4.5  kvar ]. The controller gains are listed in Table I considering the re-tuning process. The VSC is connected through an LCL filter to a grid composed of two radial feeders supplied by a controllable AC source with a phase-neutral voltage of 230 V and a frequency of 50 Hz. 

The experimental tests evaluate the stability of different grid-forming VSGs against variations in the grid impedance. Initially, in scenario _A_ , the contactor N1 is closed and N2 is open, and the power system is characterized by _SCRA_ = 10 and ( _R X_ ) _A_ = 1.59. At a given time, the contactor N2 is closed, connecting both feeders in parallel, namely scenario _B_ . This drastically changes the power system characteristics to _SCRB_ = 90 and ( _R X_ ) _B_ = 0.65. The initial and final _SCR_ and _R/X_ for experimental test are marked in Figs. 4 and 8. 

The evolution of the active and reactive power of each grid-forming VSG is presented in Fig. 10. At the beginning of the tests (scenario _A_ ), all the grid-forming VSGs adequate‐ ly track the power setpoints. The corresponding injected cur‐ rents are shown in Fig. 11. 

JOURNAL OF MODERN POWER SYSTEMS AND CLEAN ENERGY, VOL. 13, NO. 1, January 2025 

110 


![](JMPSCE_2025_Matas-Díaz_A_Systematic_Small-signal_OA_fig/JMPSCE_2025_Matas-Díaz_A_Systematic_Small-signal_OA.pdf-0009-02.png)


**----- Start of picture text -----**<br>
Weak grid Strong grid Weak grid Strong grid Weak grid Strong grid<br>1.91 1.91 1.91<br>1.59 1.59 1.59<br>1.27 1.27 1.27<br>0.95 0.95 0.95<br>0.64 0.64 0.64<br>0.32 0.32 0.32<br>0.25 0.25 0.25<br>0.19 0.19 0.19<br>0.13 0.13 0.13<br>0.06 0.06 0.06<br>1 3.13 6.25 15 50 800 1 3.13 6.25 15 50 800 1 3.13 6.25 15 50 800<br>2.5 4.15 12.5 25 265 2.5 4.15 12.5 25 265 2.5 4.15 12.5 25 265<br>SCR SCR SCR<br>(a) (b) (c)<br>Weak grid Strong grid Weak grid Strong grid Weak grid Strong grid<br>1.91 1.91 1.91<br>1.59 1.59 1.59<br>1.27 1.27 1.27<br>0.95 0.95 0.95<br>0.64 0.64 0.64<br>0.32 0.32 0.32<br>0.25 0.25 0.25<br>0.19 0.19 0.19<br>0.13 0.13 0.13<br>0.06 0.06 0.06<br>1 3.13 6.25 15 50 800 1 3.13 6.25 15 50 800 1 3.13 6.25 15 50 800<br>2.5 4.15 12.5 25 265 2.5 4.15 12.5 25 265 2.5 4.15 12.5 25 265<br>SCR SCR SCR<br>(d) (e) (f)<br>Stable region; Unstable region; HV grid; MV grid; LV grid<br>Initial value of  SCR  and  R/X  for experimental test; Final value of  SCR  and  R/X  for experimental test<br>Stable region with re-tuned control parameters. (a) S-VC. (b) S-CC. (c) S-OL. (d) PI-VC. (e) PI-CC. (f) PI-OL.<br>Grid-forming N1 L 1 R 1 Power grid<br>VSC<br>N2 L 2 R 2<br>(a)<br>VSC and LCL<br>filter Feeder characteristics.<br>(b) (c)<br>R/X R/X R/X<br>R/X R/X R/X<br>**----- End of picture text -----**<br>


Fig. 8. Stable region with re-tuned control parameters. (a) S-VC. (b) S-CC. (c) S-OL. (d) PI-VC. (e) PI-CC. (f) PI-OL. 

This experimental performance aligns with the small-sig‐ nal analysis results, as presented in Table IV. When the power system characteristics of the experimental tests are considered, the critical oscillation modes reveal that volt‐ age-controlled ICLs (OL-ICL and VC-ICL) exhibit lower damping after the power system changes, leading to larger transients. The small-signal analysis results for the S-CC and PI-CC are fully aligned with the experimental test giv‐ en the large damping after the change in power system characteristics. 

## V. DISCUSSION 

Fig. 9. Experimental testbed. (a) One-line diagram. (b) VSC and LCL fil‐ ter. (c) Feeder. 

This section discusses some other features, in addition to synchronization stability, of the analyzed grid-forming VSGs that must be considered. These features depend on the imple‐ mented OCL and ICL blocks and their corresponding param‐ eterization. In this regard, the fact that the initial settings of the controllers analyzed in this study are chosen according to the state of the art must be highlighted. 

Then, the contactor N2 is closed at _t_ = 0.25 s (scenario _B_ ), resulting in a transient response in each grid-forming VSG before they return to their corresponding setpoints. First, the analyzed grid-forming VSGs are stable, as indicated in the theoretical analysis, because the change of power system characteristics is within the identified stable region depicted in Fig. 8. Second, even though each grid-forming VSG ex‐ hibits a particular transient response, some conclusions can be drawn based on the implemented ICL block. Those imple‐ mentations relying on voltage control (OL-ICL and VC-ICL) exhibit an under-damped response with a significant power overshoot. This effect is much more noticeable in the PI-VC, which may lead to undesired VSC overcurrent, as shown in Fig. 11. By contrast, the S-CC and PI-CC show a welldamped response with a slight disturbance when the grid SCR changes. 

Regarding the OCL, the S-VSG leads to wider stability ar‐ eas compared with PI-VSG, even the PI-VSG gains are tuned, as shown in Fig. 8. The reason is that, although both S-VSG and PI-VSG have the same inertia constant, the S- VSG is parameterized with a value of the damping coeffi‐ cient _D_ , which results in a larger damping for the S-VSG compared with that achieved by the proportional gain _kpp_ in the PI-VSG. However, this superior performance of the S- VSG in terms of synchronization stability is accompanied by two major drawbacks. 

MATAS-DÍAZ _et al_ .: A SYSTEMATIC SMALL-SIGNAL ANALYSIS PROCEDURE FOR IMPROVING SYNCHRONIZATION STABILITY... 

111 


![](JMPSCE_2025_Matas-Díaz_A_Systematic_Small-signal_OA_fig/JMPSCE_2025_Matas-Díaz_A_Systematic_Small-signal_OA.pdf-0010-02.png)


**----- Start of picture text -----**<br>
15 15 15<br>10 10 10<br>5 5 5<br>0 0.5 1.0 1.5 0 0.5 1.0 1.5 0 0.5 1.0 1.5<br>Time (s) Time (s) Time (s)<br>(a) (b) (c)<br>15 15 15<br>10 10 10<br>5 5 5<br>0 0.5 1.0 1.5 0 0.5 1.0 1.5 0 0.5 1.0 1.5<br>Time (s) Time (s) Time (s)<br>(d) (e) (f)<br>Active power; Reactive power<br>Active power (kW),  reactive power (kvar) Active power (kW),  reactive power (kvar) Active power (kW),  reactive power (kvar)<br>Active power (kW),  reactive power (kvar) Active power (kW),  reactive power (kvar) Active power (kW),  reactive power (kvar)<br>**----- End of picture text -----**<br>


Fig. 10. Evolution of active and reactive power of each grid-forming VSG. (a) S-VC. (b) S-CC. (c) S-OL. (d) PI-VC. (e) PI-CC. (f) PI-OL. 


![](JMPSCE_2025_Matas-Díaz_A_Systematic_Small-signal_OA_fig/JMPSCE_2025_Matas-Díaz_A_Systematic_Small-signal_OA.pdf-0010-04.png)


**----- Start of picture text -----**<br>
50 50 50<br>25 25 25<br>0 0 0<br>-25 -25 -25<br>-50 -50 -50<br>0.20 0.25 0.30 0.35 0.20 0.25 0.30 0.35 0.20 0.25 0.30 0.35<br>Time (s) Time (s) Time (s)<br>(a) (b) (c)<br>50 50 50<br>25 25 25<br>0 0 0<br>-25 -25 -25<br>-50 -50 -50<br>0.20 0.25 0.30 0.35 0.20 0.25 0.30 0.35 0.20 0.25 0.30 0.35<br>Time (s) Time (s) Time (s)<br>(d) (e) (f)<br>Phase a; Phase b; Phase c<br>Current (A) Current (A) Current (A)<br>Current (A) Current (A) Current (A)<br>**----- End of picture text -----**<br>


Fig. 11. Evolution of injected current of each grid-forming VSG. (a) S-VC. (b) S-CC. (c) S-OL. (d) PI-VC. (e) PI-CC. (f) PI-OL. 

TABLE IV 

CRITICAL OSCILLATION MODES FOR SMALL-SIGNAL ANALYSIS OF EXPERIMENTAL TEST 

|VSG|Mode|Scenario_A_|Scenario_A_|
|---|---|---|---|
|||_fk_(Hz)|_ζk_<br>_fk_(Hz)|
|S-VC<br>S-CC<br>S-OL<br>PI-VC<br>PI-CC<br>PI-OL<br>_λ_5,_λ_6<br>_λ_3,_λ_4<br>_λ_5,_λ_6<br>_λ_5,_λ_6<br>_λ_3,_λ_4<br>_λ_5, _λ_6||||



First, the damping and PFR in the S-VSG are coupled, making it impossible to define these two design parameters separately without introducing additional modifications into the APCL. Thus, a large damping coefficient _D_ , which is re‐ quired because of the POI characteristics, may lead to a large PFR. This in turn may produce a CIG overload in the event of a frequency disturbance. By contrast, the damping and PFR of the PI-VSG are fully decoupled and thus can be set independently. Second, due to the larger damping, the dy‐ namic response of the S-VSG to a reference step change is 

slower than that of the PI-VSG, as shown in Fig. 3. There‐ fore, the damping coefficient required for the S-VSG must be used considering a trade-off among the required synchro‐ nization stability margins, PFR, and dynamic response. 

Regarding the ICLs, they must be considered to assess the synchronization stability of grid-forming VSGs, as evidenced in the conducted small-signal analysis. The analytical results reveal that the grid-forming VSGs adopting OL-ICL exhibit a superior performance, regardless of the selected OCL, as shown in Fig. 8. Nevertheless, the OL-ICL lacks control ca‐ pability over the VSC voltage and current. Therefore, the al‐ ternative and non-straightforward protection schemes are re‐ quired to protect the grid-forming CIG from overloads and/ or overvoltage. This limitation does not apply to the VC-ICL and CC-ICL, which can effectively control the VSC voltage and current, respectively, when properly tuned. Note that each ICL computes the active and reactive power of the gridforming CIG at different nodes. As a result, only the CCICL ensures that the reference power of the grid-forming VSG are injected into the POI. 

Finally, Table V summarizes the main properties of each grid-forming VSG, including synchronization stability and other properties based on the proposed systematic procedure. 

JOURNAL OF MODERN POWER SYSTEMS AND CLEAN ENERGY, VOL. 13, NO. 1, January 2025 

112 

## TABLE V 

SYNCHRONIZATION STABILITY AND OTHER PROPERTIES OF GRID-FORMING VSGS 

|VSG|Stability|HVgrid|MVgrid|LVgrid|Property|
|---|---|---|---|---|---|
||||||+Inertial response|
|S-OL|Well-damped oscillation modes|√|√|√|-Coupled damping and PFR|
||||||-Lack of voltage or current control|
||||||+Inertial response|
|S-VC|Well-damped oscillation modes|√|√|√|-Coupled damping and PFR<br>+Voltage control|
||||||+Inverter current control|
||1) No low-frequency critical oscillation modes||||+Inertial response|
|S-CC|2) Poorly-damped high-frequency oscillation<br>modes with low_SCR_|√|√|×|-Coupled damping and PFR<br>+_PQ_control at the POI|
||3) Robustness with high_SCR_||||+Grid current control|
||||||+Inertial response|
|PI-OL|1) Well-damped oscillation modes<br>2) Robustness with low_SCR_|√|√|√|+Decoupled damping and PFR<br>+Faster time response|
||||||-Lack of voltage or current control|
||||||+Inertial response|
||1) Poorly-damped low-frequency oscillation||||+Decoupled damping and PFR|
|PI-VC|mode with high_SCR_and low_R/X_|×|√|√|+Faster time response|
||2) Robustness with low_SCR_||||+Voltage control|
||||||+Inverter current control|
|PI-CC|1) No low-frequency critical oscillation mode<br>2) Poorly-damped high-frequency oscillation<br>modes with low_SCR_<br>3) Robustness with high_SCR_|√|√|×|+Inertial response<br>+Decoupled damping and PFR<br>+Faster time response<br>+_PQ_control at the POI<br>+Grid current control|



Note: the symbol √ represents that the grid-forming VSG is applicable to HV, MV, or LV grid; the symbol × represents that the grid-forming VSG is not ap‐ – plicable to HV, MV, or LV grid; the symbol + represents the advantages; and the symbol represents the disadvantages. 

## VI. CONCLUSION 

This study proposes a systematic small-signal analysis procedure to evaluate and improve the synchronization stabil‐ ity of grid-forming VSGs. The proposed systematic proce‐ dure is applied to six grid-forming VSGs, derived using dif‐ ferent combinations of OCL and ICL blocks. Given that the synchronization stability is extremely sensitive to power sys‐ tem characteristics, the analysis considers a wide range of _SCR_ and _R/X_ to draw general conclusions. 

The proposed systematic procedure enhances the synchro‐ nization stability of grid-forming VSGs, providing insights into how controller gains should be re-tuned for this pur‐ pose. The application of the proposed systematic procedure reveals that the S-VSG, parameterized according to state-ofthe-art practices, has a broader stable region as compared with PI-VSG. This is caused by a large damping coefficient, which is required because of the POI characteristics. This pa‐ rameter may lead to a slower transient response and a larger PFR, which could cause a CIG overload in the event of a frequency disturbance. In addition, the ICLs play a crucial role in the stability of grid-forming VSGs. For the ICLs based on voltage control, i.e., VC-ICL and OC-ICL, the sta‐ bility is determined by low-frequency oscillation modes asso‐ ciated with the APCL. By contrast, the stability of grid-form‐ ing VSGs with ICLs based on current control, i.e., CC-ICL, is linked to high-frequency oscillation modes associated with the current controller. Therefore, the synchronization stabili‐ ty of grid-forming VSGs does not solely depend on low-fre‐ quency modes as traditionally defined, as high-frequency modes can also emerge due to the rapid control actions with‐ 

in the ICLs. Finally, VC-ICL and OC-ICL are more suitable for networks with medium/low _SCR_ , whereas CC-ICL is more effective for networks with medium/high _SCR_ . In gen‐ eral, a high _R/X_ improves stability across all grid-forming VSGs, as expected. 

Future research will focus on extending this systematic analysis to other aspects of grid-forming VSGs, including power system dynamics and unbalanced operation. 

## REFERENCES 

- [1] J. M. Maza-Ortega, E. Acha, S. García _et al._ , “Overview of power electronics technology and applications in power generation transmis‐ sion and distribution,” _Journal of Modern Power Systems and Clean Energy_ , vol. 5, no. 4, pp. 499-514, Jul. 2017. 

- [2] H. Bevrani, H. Golpîra, A. R. Messina _et al_ ., “Power system frequen‐ cy control: an updated review of current solutions and new challeng‐ es,” _Electric Power Systems Research_ , vol. 194, p. 107114, May 2021. 

- [3] H. Gu, R. Yan, and T. K. Saha, “Minimum synchronous inertia re‐ quirement of renewable power systems,” _IEEE Transactions on Power Systems_ , vol. 33, no. 2, pp. 1533-1543, Mar. 2018. 

- [4] N. Hatziargyriou, J. Milanovic, C. Rahmann _et al_ ., “Definition and classification of power system stability – revisited & extended,” _IEEE Transactions on Power Systems_ , vol. 36, no. 4, pp. 3271-3281, Jul. 2021. 

- [5] D. Liu, X. Zhang, and C. K. Tse, “Effects of high level of penetration of renewable energy sources on cascading failure of modern power systems,” _IEEE Journal on Emerging and Selected Topics in Circuits and Systems_ , vol. 12, no. 1, pp. 98-106, Mar. 2022. 

- [6] H. Zhang, W. Xiang, W. Lin _et al_ ., “Grid forming converters in renew‐ able energy sources dominated power grid: control strategy, stability, application, and challenges,” _Journal of Modern Power Systems and Clean Energy_ , vol. 9, no. 6, pp. 1239-1256, Nov. 2021. 

- [7] R. Rosso, X. Wang, M. Liserre _et al_ ., “Grid-forming converters: con‐ trol approaches, grid-synchronization, and future trends – a review,” _IEEE Open Journal of Industry Applications_ , vol. 2, pp. 93-109, Apr. 2021. 

MATAS-DÍAZ _et al_ .: A SYSTEMATIC SMALL-SIGNAL ANALYSIS PROCEDURE FOR IMPROVING SYNCHRONIZATION STABILITY... 

113 

- [8] D. Sun, H. Liu, S. Gao _et al_ ., “Comparison of different virtual inertia control methods for inverter-based generators,” _Journal of Modern Power Systems and Clean Energy_ , vol. 8, no. 4, pp. 768-777, Jul. 2020. 

- [9] H. Xin, L. Huang, L. Zhang _et al_ ., “Synchronous instability mecha‐ nism of _P_ - _f_ droop-controlled voltage source converter caused by cur‐ rent saturation,” _IEEE Transactions on Power Systems_ , vol. 31, no. 6, pp. 5206-5207, Nov. 2016. 

- [10] L. Zhang, L. Harnefors, and H. P. Nee, “Power-synchronization con‐ trol of grid-connected voltage-source converters,” _IEEE Transactions on Power Systems_ , vol. 25, no. 2, pp. 809-820, May 2010. 

- [11] M. Ndreko, S. Rüberg, and W. Winter, “Grid forming control for sta‐ ble power systems with up to 100% inverter based generation: a para‐ digm scenario using the IEEE 118-bus system,” in _Proceedings of 17th International Wind Integration Workshop_ , Stockholm, Sweden, Oct. 2018, pp. 1-6. 

- [12] S. Dong and Y. Chen, “Adjusting synchronverter dynamic response speed via damping correction loop,” _IEEE Transactions on Energy Conversion_ , vol. 32, no. 2, pp. 608-619, Jun. 2017. 

- [13] P. Rodríguez, C. Citro, J. I. Candela _et al_ ., “Flexible grid connection and islanding of SPC-based PV power converters,” _IEEE Transactions on Industry Applications_ , vol. 54, no. 3, pp. 2690-2702, May 2018. 

- [14] M. Chen, D. Zhou, and F. Blaabjerg, “Modelling, implementation, and assessment of virtual synchronous generator in power systems,” _Jour‐ nal of Modern Power Systems and Clean Energy_ , vol. 8, no. 3, pp. 399-411, May 2020. 

- [15] G. C. Kryonidis, K. N. D. Malamaki, J. M. Mauricio _et al_ ., “A new perspective on the synchronverter model,” _International Journal of Electrical Power & Energy Systems_ , vol. 140, p. 108072, Sept. 2022. 

- [16] A. J. Roscoe, M. Yu, A. Dyśko _et al_ ., “A VSM (virtual synchronous machine) convertor control model suitable for RMS studies for resolv‐ ing system operator/owner challenges,” in _Proceedings of 15th Wind Integration Workshop_ , Vienna, Austria, Nov. 2016, pp. 1-8. 

- [17] D. Remon, A. M. Cantarellas, E. Rakhshani _et al_ ., “An active power synchronization control loop for grid-connected converters,” in _Pro‐ ceedings of 2014 IEEE PES General Meeting_ , National Harbor, USA, Jul. 2014, pp. 1-5. 

- [18] M. Ndreko, S. Rüberg, and W. Winter, “Grid forming control scheme for power systems with up to 100% power electronic interfaced gener‐ ation: a case study on Great Britain test system,” _IET Renewable Pow‐ er Generation_ , vol. 14, no. 8, pp. 1268-1281, Jun. 2020. 

- [19] C. Li, Y. Yang, Y. Cao _et al_ ., “Frequency and voltage stability analysis of grid-forming virtual synchronous generator attached to weak grid,” _IEEE Journal of Emerging and Selected Topics in Power Electronics_ , vol. 10, no. 3, pp. 2662-2671, Jun. 2022. 

- [20] J. C. Olives-Camps, J. M. Mauricio, M. Barragán-Villarejo _et al_ ., “Voltage control of four-leg VSC for power system applications with nonlinear and unbalanced loads,” _IEEE Transactions on Energy Con‐ version_ , vol. 35, no. 2, pp. 640-650, Jun. 2020. 

- [21] P. Rodriguez, I. Candela, C. Citro _et al_ ., “Control of grid-connected power converters based on a virtual admittance control loop,” in _Pro‐ ceedings of 2013 15th European Conference on Power Electronics and Applications_ , Lille, France, Sept. 2013, pp. 1-10. 

- [22] G. C. Kryonidis, J. M. Mauricio, K. N. D. Malamaki _et al_ ., “Use of ultracapacitor for provision of inertial response in virtual synchronous generator: design and experimental validation,” _Electric Power Sys‐ tems Research_ , vol. 223, p. 109607, Oct. 2023. 

- [23] F. J. Matas-Díaz, M. Barragán-Villarejo, J. C. Olives-Camps _et al_ ., “Virtual conductance based cascade voltage controller for VSCs in is‐ landed operation mode,” _Journal of Modern Power Systems and Clean Energy_ , vol. 10, no. 6, pp. 1704-1713, Nov. 2022. 

- [24] T. Qoria, F. Gruson, F. Colas _et al_ ., “Tuning of cascaded controllers for robust grid-forming voltage source converter,” in _Proceedings of 2018 Power Systems Computation Conference_ , Dublin, Ireland, Jun. 2018, pp. 1-7. 

- [25] Z. Liu, J. Liu, D. Boroyevich _et al_ ., “Small-signal terminal-characteris‐ tics modeling of three-phase droop-controlled inverters,” in _Proceed‐ ings of 2016 IEEE Energy Conversion Congress and Exposition_ , Mil‐ waukee, USA, Sept. 2016, pp. 1-7. 

- [26] S. J. Yague, A. García-Cerrada, and P. P. Farré, “Comparison between modal analysis and impedance-based methods for analysing stability of unbalanced microgrids with grid-forming electronic power convert‐ ers,” _Journal of Modern Power Systems and Clean Energy_ , vol. 11, no. 4, pp. 1269-1281, Jul. 2023. 

- [27] X. Wang and F. Blaabjerg, “Harmonic stability in power electronicbased power systems: concept, modeling, and analysis,” _IEEE Transac‐ tions on Smart Grid_ , vol. 10, no. 3, pp. 2858-2870, May 2019. 

- [28] J. Yu, S. Wang, Z. Liu _et al_ ., “Accurate small-signal terminal charac‐ teristic model and SISO stability analysis approach for parallel gridforming inverters in islanded microgrids,” _IEEE Transactions on Pow‐ er Electronics_ , vol. 38, no. 5, pp. 6597-6612, May 2023. 

- [29] M. H. Ravanji, D. B. Rathnayake, M. Z. Mansour _et al_ ., “Impact of voltage-loop feedforward terms on the stability of grid-forming invert‐ ers and remedial actions,” _IEEE Transactions on Energy Conversion_ , vol. 38, no. 3, pp. 1554-1565, Sept. 2023. 

- [30] X. Gao, D. Zhou, A. Anvari-Moghaddam _et al_ ., “A comparative study of grid-following and grid-forming control schemes in power electron‐ ic-based power systems,” _Power Electronics and Drives_ , vol. 8, no. 1, pp. 1-20, Jan. 2023. 

- [31] X. Gao, D. Zhou, A. Anvari-Moghaddam _et al_ ., “Stability analysis of grid-following and grid-forming converters based on state-space mod‐ el,” in _Proceedings of 2022 International Power Electronics Confer‐ ence_ , Himeji, Japan, May 2022, pp. 422-428. 

- [32] X. Gao, D. Zhou, A. Anvari-Moghaddam _et al_ ., “Stability analysis of grid-following and grid-forming converters based on state-space model‐ ling,” _IEEE Transactions on Industry Applications_ , vol. 60, no. 3, pp. 4910-4920, May 2024. 

- [33] W. Wang, X. Shi, G. Wu _et al_ ., “Interaction between grid-forming con‐ verters with AC grids and damping improvement based on loop shap‐ ing,” _IEEE Transactions on Power Systems_ , vol. 39, no. 1, pp. 19051917, Jan. 2024. 

- [34] F. Zhao, T. Zhu, L. Harnefors _et al_ ., “Closed-form solutions for gridforming converters: a design-oriented study,” _IEEE Open Journal of Power Electronics_ , vol. 5, pp. 186-200, Jan. 2024. 

- [35] O. Damanik, Ö. C. Sakinci, G. Grdenić _et al_ ., “Evaluation of the use of short-circuit ratio as a system strength indicator in converter-domi‐ nated power systems,” in _Proceedings of 2022 IEEE PES Innovative Smart Grid Technologies Conference Europe_ , Novi Sad, Serbia, Oct. 2022, pp. 1-5. 

- [36] C. Henderson, A. Egea-Alvarez, T. Kneuppel _et al_ ., “Grid strength im‐ pedance metric: an alternative to SCR for evaluating system strength in converter dominated systems,” _IEEE Transactions on Power Deliv‐ ery_ , vol. 39, no. 1, pp. 386-396, Feb. 2024. 

- [37] R. Aljarrah, B. B. Fawaz, Q. Salem _et al_ ., “Issues and challenges of grid-following converters interfacing renewable energy sources in low inertia systems: a review,” _IEEE Access_ , vol. 12, pp. 5534-5561, Jan. 2024. 

- [38] M. B. Frasetyo, F. D. Wijaya, and E. Firmansyah, “Review on virtual synchronous generator model and control for improving microgrid sta‐ bility,” in _Proceedings of 2021 7th International Conference on Elec‐ trical Energy Systems_ , Chennai, India, Feb. 2021, pp. 397-402. 

- [39] Y. Lamrani, F. Colas, T. van Cutsem _et al_ . (2024, Jan.). A comparative study of grid-forming controls and their effects on small-signal stabili‐ ty. [Online]. Available: https://www. techrxiv. org/doi/full/10.36227/ techrxiv.22006310.v2Jan.2024. 

- [40] K. Mahmoud, P. Astero, P. Peltoniemi _et al_ ., “Promising grid-forming VSC control schemes toward sustainable power systems: comprehen‐ sive review and perspectives,” _IEEE Access_ , vol. 10, pp. 130024130039, Dec. 2022. 

- [41] Y. Li, Y. Xia, Y. Ni _et al_ ., “Transient stability analysis for grid-form‐ ing VSCs based on nonlinear decoupling method,” _Sustainability_ , vol. 15, no. 15, p. 11981, Aug. 2023. 

- [42] F. J. Matas-Díaz, M. Barragán-Villarejo, J. M. Maza-Ortega _et al_ ., “Active harmonic filtering with selective overcurrent limitation for grid-forming VSCs: stability analysis and experimental validation,” _IEEE Transactions on Industry Applications_ , vol. 60, no. 3, pp. 47624775, May 2024. 

- [43] L. Huang, C. Wu, D. Zhou _et al_ ., “Impact of virtual admittance on small-signal stability of grid-forming inverters,” in _Proceedings of 2021 6th IEEE Workshop on the Electronic Grid_ , New Orleans, USA, Nov. 2021, pp. 1-8. 

- [44] _IEEE Guide for Planning DC Links Terminating at AC Locations Hav‐ ing Low Short-circuit Capacities_ , IEEE Std 1204-1997, pp. 1-216, 1997. 

- [45] _IEEE Recommended Practice and Requirements for Harmonic Control in Electric Power Systems_ , IEEE Std 519-2014 (Revision of IEEE Std 519-1992), pp. 1-29, 2014. 

**Francisco Jesús Matas-Díaz** received the B. S. degree in aerospace engi‐ neering, the Master degree in power systems, and the Ph.D. degree in elec‐ trical engineering from the University of Seville, Seville, Spain, in 2017, 2020, and 2024, respectively, where he is currently a Research Assistant at the Department of Electrical Engineering. His research interests include con‐ 

JOURNAL OF MODERN POWER SYSTEMS AND CLEAN ENERGY, VOL. 13, NO. 1, January 2025 

114 

trol of power converters and provision of ancillary services related to power quality, hardware-in-the-loop (HIL) testing, and experimental validation of power converters. 

**Manuel Barragán-Villarejo** received the B.S. and Ph.D. degrees in electri‐ cal engineering from the University of Seville, Seville, Spain, in 2008 and 2014, respectively. Since 2008, he has been with the Department of Electri‐ cal Engineering, University of Seville, where he is currently an Associate Professor. His research interests include exploitation and control of power 

converters for smart grid management and grid integration of distributed re‐ newable energy sources. 

**José María Maza-Ortega** received the B. S. and Ph. D. degrees from the University of Seville, Seville, Spain, in 1996 and 2001, respectively. Since 1997, he has been with the Department of Electrical Engineering, Universi‐ ty of Seville, where he is currently a Full Professor. His research interests include power quality, harmonic filter, integration of renewable energies, and power electronics. 

