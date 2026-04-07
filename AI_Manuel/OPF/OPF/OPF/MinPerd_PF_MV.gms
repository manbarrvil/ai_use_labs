** SMARTIE 3 TERMINALES CON PÉRDIDAS -- MAX_GEN
*********
*$if not set caso $goto no_vsc
*$if "%caso%"=="vsc_pq" $goto vsc_pq
*$if "%caso%"=="vsc_qq" $goto vsc_qq
*$if "%caso%"=="vsc_p"  $goto vsc_p
*********
$onempty
$offlisting

Gij('8','F8') = Gij('8','F8') * 100 ;
Gij('14','F14') = Gij('14','F14') * 100 ;

SCALAR Vmax   Tensión máxima en cada nudo
       Vmin   Tensión mínima en cada nudo
       V_SUBEST   tensión en barras de la SE
       S_VSC  Potencia nominal convertidores
       P_CC   Consumo de potencia en continua
       ;
Vmax = 1.5;
Vmin = 0.1 ;
V_SUBEST = 400/400 ;
SBASE=100000;
S_VSC = 20000 / SBASE  ;
P_CC = 0 ;

* Solo si es necesario cambiar de base
*$ontext
SCALAR  Sb   VA /100000/
        Ub   V /400/
        Ib A /144/;

Ib = Sb/sqrt(3)/Ub;
*$offtext

PARAMETER
          V(n)        Tensión de nudos PV
          P(n)        Consumo de potencia activa en cada nudo
          Q(n)        Consumo de potencia reactiva en cada nudo
          p0(ng)       Generacion cada nudo
          SGmax(ng)
          SGmin(ng)
          imax(n,n)   Límite de corriente en cada rama
          K(n)        Modelo el termino lineal de perdidas del serie
          K1(n)       Modelo el termino lineal de perdidas del paralelo
          FdC         Factor de carga
          FdG         Factor de generacion
          COS_PHI_CONV tangente de phi
          COS_PHI
*          r_link_pmin(n,n)   Mínimo flujo de p activa en link de continua (flujo inverso)
*          r_link_pmax(n,n)   Máximo flujo de p activa en link de continua
*          r_link_smax        Máximo flujo de p aparente en link de continua
          ;
FdG=1;
FdC=4;
P(ND) = DATNUD(ND,'P')*1;
Q(ND) = DATNUD(ND,'Q')*1;
p0(NG) = DATGEN(NG, 'p0')*FdG;

SGmax(NG) = DATGEN(NG, 'pmax')*FdC ;
SGmin(NG) = DATGEN(NG, 'pmin')*FdC ;

IMAX(ni,nf) = 100 / Ib ;

** para incluir la carga en continua cuando no hay smartie:
*IMAX('15','F15') = 100 / Ib ;
*IMAX('8','F8') = 100 / Ib ;
*IMAX('14','F14') = 100 / Ib ;
*IMAX('0','1') = 100 / Ib ;
*IMAX('0','12') = 100 / Ib ;

PARAMETER Yg(ND,ND)
          Yb(ND,ND);

Yg(ni,nf)$(ord(ni)=ord(nf)) = sum(N2,gij(ni,N2)+gij(N2,ni));

Yg(ni,nf)$(ord(ni)<>ord(nf)) = -gij(ni,nf)-gij(nf,ni);

Yb(ni,nf)$(ord(ni)=ord(nf)) = sum(N2,bij(ni,N2)+bij(N2,ni) + bsh(ni,ni)/2);

Yb(ni,nf)$(ord(ni)<>ord(nf)) = -bij(ni,nf)-bij(nf,ni);

********************************************************************************
*                            V A R I A B L E S
********************************************************************************
VARIABLES  obj       objetivo
           Pgen(NG)   activa generada
           Qgen(NG)   reactiva generada
           vv(N)     tension nodal
           d(N)      angulo de la tension nodal
           va1(N)    variable auxiliar 1
           va2(N)    variable auxiliar 2
           va3(N)    variable auxiliar 3
           va4(N)    variable auxiliar 4
           vb1(N)    variable auxiliar b1
           vb2(N,N)  variable auxiliar b2
           vb3(N,N)  variable auxiliar b3
           ir2(N,N)  intensidad de rama al cuadrado
           i2        intensidad nudo 2
           i1(N)        intensidad nudo 1
           ir2_r(N,N)  parte real intensidad
           ir2_i(N,N)  parte imaginaria intensidad

           ;
*-------------------------------------------------------------------------------
FREE VARIABLE obj;
POSITIVE VARIABLE vb1, vb2, vb3;

*** Limites de las variables
vv.lo(N) = Vmin; vv.up(N) = Vmax;
d.lo(N) = -pi; d.up(N) = pi;
vv.l(N) = 1; d.l(N) = 0; d.fx('1') = 0 ;

*Escenarios dinamicos
*pgen.fx(NG) = 0 ; !DATGEN(ng, 'p0') ;
*qgen.fx(NG) = 0 ;
*Escenarios estaticos
pgen.fx(NG) = 0 ;
qgen.fx(NG) = 0 ;
*** slack
pgen.lo(SL) = -100 ; pgen.up(SL) = 100 ;
qgen.lo(SL) = -100 ; qgen.up(SL) = 100 ;

*** Vesp en barras de la subestacion
vv.fx('1') = V_SUBEST ;
*vv.fx('1') = V_SUBEST ;
*vv.fx('12') = V_SUBEST ;

***  ir2
*ir2.lo(NI,NF) = -imax(NI,NF)**2; ir2.up(NI,NF) = imax(NI,NF)**2;

POSITIVE VARIABLE Lambda, LambdaG(NG);
Lambda.lo = 1.0; Lambda.fx = 1.0;
LambdaG.up(NG)$(DATGEN(NG,'P0')=0) = 1.0  ;
LambdaG.fx('GB5') = 1 ; LambdaG.fx('GB10') = 1 ;
LambdaG.fx('GFC5') = 1 ; LambdaG.fx('GFC10') = 1 ;
LambdaG.fx(NG) = 1.0 ;

********************************************************************************
VARIABLE Pgen2(NG), Qgen2(NG) ;
*Qgen2.fx(NG)=0 ;
Pgen2.fx(NG) = DATGEN(ng, 'p0')*FdG;
*Qgen2.fx(NG) = sqrt(SGmax(ng)**2-power(DATGEN(ng, 'p0'),2));

Qgen2.lo(NG)=-0.1;
Qgen2.l(NG)=0.1;

*$ontext

Qgen2.fx('GP3')=0;
Qgen2.fx('GP4')=0;
Qgen2.fx('GP5')=0;
Qgen2.fx('GFC5')=0;
Qgen2.fx('GP6')=0.0;
Qgen2.fx('GP8')=0;
Qgen2.fx('GP9')=0;
Qgen2.fx('GCHPFC9')=0;
Qgen2.fx('GP10')=0;
Qgen2.fx('GFC10')=0;
Qgen2.fx('GP11')=0.0;

Qgen2.fx('GB5')=0.0;
*Qgen2.fx('GWT7')=0.0 ;
Qgen2.fx('GCHPD9')=0.0 ;
Qgen2.fx('GB10')=0.0 ;

*$offtext

Qgen2.fx('GF15') = 0 ;
Qgen2.fx('GF8') = 0 ;
Qgen2.fx('GF14') = 0 ;
Qgen2.fx('GF0') = 0  ;
Qgen2.fx('GWT7') = 0  ;




********************************************************************************
*                           E C U A C I O N E S
********************************************************************************

EQUATIONS    eqobj   ecuacion objetivo
             eqp     balance activa
             eqq     balance reactiva
             eqa1    ecuacion auxiliar 1
             eqa2    ecuacion auxiliar 2
             eqa3    ecuacion auxiliar 3
             eqa4    ecuacion auxiliar 4
             eqb1    ecuacion auxiliar b1
             eqb2    ecuacion auxiliar b2
             eqb3    ecuacion auxiliar b3
             eq_i2 intensidad i2
             eq_i1 intensidad i1
             e_ir_max
             eir2    intensidad de rama al cuadrado
*             eir2_r  parte real intensidad
*             eir2_i  parte imaginaria intensidad
;

eqobj..      obj =e= sum(SL,pgen(SL));

*eqobj..      obj =e= -SUM(NG, LambdaG(NG)) ;   ! objetivo maximizar PENETRACION

eqp(ND)..     SUM(NDGR(ng,nd), pgen(NG) + LambdaG(NG)*pgen2(NG)) - Lambda*P(ND)
                     =E= vv(ND)*(va1(ND)+va2(ND));

eqa1(ND)..    va1(ND) =E= sum(NF,vv(NF)*Yg(ND,NF)*cos(d(ND)-d(NF)));

eqa2(ND)..    va2(ND) =E= sum(NF,vv(NF)*Yb(ND,NF)*sin(d(ND)-d(NF)));

eqq(ND)..     SUM(NDGR(ng,nd), qgen(NG)+qgen2(NG)) - Lambda*Q(ND)
                     =E= vv(ND)*(va3(ND)+va4(ND));

eqa3(ND)..    va3(ND) =E= sum(NF,vv(NF)*Yg(ND,NF)*sin(d(ND)-d(NF)));

eqa4(ND)..    va4(ND) =E= sum(NF,-vv(NF)*Yb(ND,NF)*cos(d(ND)-d(NF)));

eqb1(ND)..           vb1(ND) =E= vv(ND)**2;

eqb2(KL(NL,NI,NF))..   vb2(NI,NF) =E= 2*vv(NI)*vv(NF);

eqb3(KL(NL,NI,NF))..   vb3(NI,NF) =E= cos(d(NI)-d(NF));

eq_i1(ND)..     i1(ND) =e= sqrt(power(P(ND),2)  + power(Q(ND),2))/vv(ND) ;

eq_i2..     i2 =e= sqrt(power(Pgen('gf14'),2) + power(Qgen('gf14'),2))/vv('F14')   ;

eir2(KL(NL,NI,NF))..    ir2(NI,NF) =e= sqrt(power(vv(NI)*cos(d(NI))-vv(NF)*cos(d(NF)),2)+power(vv(NI)*sin(d(NI))-vv(NF)*sin(d(NF)),2))*sqrt((gij(NI,NF)**2+power(bij(NI,NF),2)));

*eir2(KL(NL,NI,NF))..    ir2(NI,NF) =e= sqrt(power(vv(NI)*cos(d(NI))-vv(NF)*cos(d(NF)),2)+power(vv(NI)*sin(d(NI))-vv(NF)*sin(d(NF)),2))*sqrt((gij(NI,NF)**2+power(bij(NI,NF),2)));
e_ir_max(KL(NL,NI,NF))..  ir2(NI,NF) =l= IMAX(ni,nf)  ;

*eir2(KL(NL,NI,NF))..    ir2(NI,NF) =e= power((vv(NI)*cos(d(NI))-vv(NF)*cos(d(NF))),2)+power((vv(NI)*sin(d(NI))-vv(NF)*sin(d(NF))),2);
*eir2_r(KL(NL,NI,NF))..    ir2_r(NI,NF) =e= -(vv(NF)*cos(d(NF))/gij(NI,NF) -   vv(NI)*cos(d(NI))/gij(NI,NF) + vv(NF)*sin(d(NF))/bij(NI,NF) - vv(NI)*sin(d(NI))/bij(NI,NF))*(gij(NI,NF)**2+power(bij(NI,NF),2))  ;
*                                          -(R*VF_r                       - R*VI_r                         + VF_i*X                       - VI_i*X)                      /(R^2 + X^2)
*eir2_i(KL(NL,NI,NF))..    ir2_i(NI,NF) =e= -(vv(NF)*sin(d(NF))/gij(NI,NF) -   vv(NI)*sin(d(NI))/gij(NI,NF) - vv(NF)*cos(d(NF))/bij(NI,NF) + vv(NI)*cos(d(NI))/bij(NI,NF))*(gij(NI,NF)**2+power(bij(NI,NF),2)) ;
*                                          -(R*VF_i                       - R*VI_i                         - VF_r*X                       + VI_r*X)                      /(R^2 + X^2)
*eir2(KL(NL,NI,NF))..    ir2(NI,NF) =e= sqrt((gij(NI,NF)**2+Yb(NI,NF)**2)*(vb1(NI)+vb1(NF)-vb2(NI,NF)*vb3(NI,NF)));
*eir2(KL(NL,NI,NF))..    ir2(NI,NF) =e= sqrt(power(ir2_r(NI,NF),2)+power(ir2_i(NI,NF),2));

********************************************************************************
*                  D E F I N I C I O N     M O D E L O
********************************************************************************

$if not set caso $goto no_vsc
$if "%caso%"=="vsc_pq" $goto vsc_pq
$if "%caso%"=="vsc_qq" $goto vsc_qq
$if "%caso%"=="vsc_p"  $goto vsc_p

$LABEL VSC_QQ

       EQUATION    qgen_n     Igual Q inyectada en los nudos n_link ;
                   qgen_n..   SUM(gs, Qgen(gs)) =E=  0 ;

$LABEL VSC_PQ
       qgen.up(gs) = S_VSC ; qgen.lo(gs) = -S_VSC  ;

$LABEL VSC_P
       pgen.up(gs) = S_VSC ;  pgen.lo(gs) = -S_VSC  ;
*       pgen.up(gs) = 0 ;  pgen.lo(gs) = 0  ;
       Pgen.fx('GF15') = 0.0 ; Qgen.fx('GF15') = 0.0 ;
*       pgen.up('GF8') = S_VSC;  pgen.lo('GF8') = -S_VSC;
*       pgen.up('GF6') = S_VSC;  pgen.lo('GF6') = -S_VSC;
*       pgen.up('GF14') = S_VSC;  pgen.lo('GF14') = -S_VSC;

       EQUATION    pgen_n  potencia inyectada en los nudos del smartie ;
*                   pgen_n..   SUM(GS, Pgen(gs)) =E= -(3*c + P_CC) * 0   ;
*                   pgen_n..   SUM(GS, Pgen(gs)) =E= -(2*c)   ;
                   pgen_n..   SUM(GS, Pgen(gs)) =E= 0   ;

EQUATION     smax_n  máxima potencia aparente de cada convertidor  ;
smax_n(gs)..   POWER(Pgen(gs),2) + Power(Qgen(gs),2) =L= S_VSC**2;

$label no_vsc
EQUATION     sgmax_n  máxima potencia aparente inyectada por generador
*             sgmax_n1
*             sgmax_n2
*             sgmax_n3

;

sgmax_n(ng)..   power(pgen2(ng),2) + power(qgen2(ng),2)  =L= (SGmax(ng))**2  ;
*sgmax_n(ng)..    power(qgen2(ng),2)  =l= (SGmax(ng))**2-power(pgen2(ng),2)  ;
*sgmax_n('GB5')..   power(qgen2('GB5'),2)  =E= (SGmax('GB5'))**2 - power(pgen2('GB5'),2)  ;
*sgmax_n1('GWT7')..   power(qgen2('GWT7'),2)  =E= (SGmax('GWT7'))**2 - power(pgen2('GWT7'),2)  ;
*sgmax_n2('GB10')..   power(qgen2('GB10'),2)  =E= (SGmax('GB10'))**2 - power(pgen2('GB10'),2)  ;
*sgmax_n3('GCHPD9')..   power(qgen2('GCHPD9'),2)  =E= (SGmax('GCHPD9'))**2 - power(pgen2('GCHPD9'),2)  ;

*********************************
*********************************
MODEL OPF /ALL/;
OPTION nlp=conopt;
OPTION sysout=on;
OPF.scaleopt =1;
SOLVE OPF MINIMIZING OBJ USING NLP;
*********************************
*********************************


PARAMETER dLAMBDA incremento de cargabilidad
          dLAMBDAG(NG) incremento de generación distribuida
          PERD perdidas en W
          V    tensiones en pu
          PCONV potencia activa inyectada por convertidores en kW
          QCONV potencia reactiva inyectada por convertidores en kvar
          PSE   potencia desde la subestacion en MW
          QSE   potencia reactiva desde la subestacion en Mvar
          G_INI(NG) generacion inicial
          G_FIN(NG) generacion final tras optimizacion
          G_DIF(NG) diferencia generacion final - inicial
          SUM_G_INI suma generacion inicial
          SUM_G_FIN suma generacion final
          Irama intensidad por cada rama
          QGEN_2(NG) reactiva geneda por los generadores
          PGEN_2(NG) activa generada por los generadores
          PLOAD(ND)  activa consumida por las cargas
          QLOAD(ND)  reactiva consumida por las cargas
;
dLAMBDA = lambda.l  ;
dLAMBDAG(NG) = lambdag.l(NG) ;
PERD = [ SUM(NG,Pgen.L(ng)) + SUM(ng,Pgen2.l(ng)) - SUM(ND,P(ND)) ] * SBASE   ;
V(nd) = vv.l(nd)   ;
PCONV(GS) = Pgen.L(gs) * SBASE  ;
QCONV(GS) = Qgen.L(gs) * SBASE  ;
PSE = Pgen.l('GF0') * SBASE ;
QSE = Qgen.l('GF0') * SBASE ;
G_INI(NG) = Pgen2.l(NG) * SBASE  ;
G_FIN(NG) = Pgen2.l(NG) * LambdaG.l(NG) * SBASE ;
G_DIF(NG) = G_FIN(NG) - G_INI(NG) ;
QGEN_2(NG)=  Qgen2.l(NG) * SBASE ;
PGEN_2(NG)=  Pgen2.l(NG) * SBASE * LambdaG.l(NG) ;
PLOAD(ND) = Lambda.l*P(ND)* SBASE;
QLOAD(ND) = Lambda.l*Q(ND)* SBASE;
SUM_G_INI = SUM(NG, G_INI(NG)) ;
SUM_G_FIN = SUM(NG, G_FIN(NG)) ;
Irama(NI,NF) = ir2.l(NI,NF)*Ib;
OPTION V:4, PERD:0, PCONV:0, QCONV:0, dLAMBDA:3, dLAMBDAG:3;

DISPLAY PERD, V, Irama, PCONV , QCONV, dLAMBDAG, G_INI, G_FIN, G_DIF, QGEN_2,  PGEN_2,  PLOAD, QLOAD;
*DISPLAY PERD, V, PCONV , QCONV, dLAMBDAG, G_INI, G_FIN, G_DIF  ;

*$ONTEXT
*Putdir=paraAle\minuto0003 --NUM=1
FILE RESULT_Base_%NUM%;
PUT RESULT_Base_%NUM% ;

PUT '---PERD ' PERD:< /

*PUT '---V_VSC1 ' V('F8'):<:4 /
*PUT '---V_VSC2 ' V('F14'):<:4 /

*PUT '---P_VSC1 ' PCONV('GF8'):< /
*PUT '---P_VSC2 ' PCONV('GF14'):< /

*PUT '---Q_VSC1 ' QCONV('GF8'):< /
*PUT '---Q_VSC2 ' QCONV('GF14'):< /


PUT / ;

PUT '- Tensiones de nudos en pu' /
LOOP(ND, PUT ND.TL V(ND):<:4 /) ;

PUT / ;

*PUT '- Intensidades en las ramas' /
*LOOP(NI,LOOP(NF, PUT NI.TL NF.TL Irama(NI,NF):<:4 /) );
PUT / ;
PUT / '- Reactiva generada en Var' /
LOOP(NG, PUT NG.TL QGEN_2(NG):<:4 /) ;
PUT / ;

PUT / ;

PUT / '- Potencia generada en W' /
LOOP(NG, PUT NG.TL PGEN_2(NG):<:4 /) ;
PUT / ;

PUT / ;

PUT / '- Reactiva consumida en var' /
LOOP(ND, PUT ND.TL QLOAD(ND):<:4 /) ;
PUT / ;

PUT / ;

PUT / '- Activa consumida en W' /
LOOP(ND, PUT ND.TL PLOAD(ND):<:4 /) ;
PUT / ;

PUT / ;

PUT '- P y Q inyectada desde la subestación (W y var)' /
PUT 'P: ' PSE:< /
PUT 'Q: ' QSE:< /