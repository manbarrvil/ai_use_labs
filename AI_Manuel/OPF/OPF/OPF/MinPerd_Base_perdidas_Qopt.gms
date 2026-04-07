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
Vmax = 1.1 ;
Vmin = 0.9 ;
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
          COS_PHI_CONV tangente de phi
          COS_PHI
*          r_link_pmin(n,n)   Mínimo flujo de p activa en link de continua (flujo inverso)
*          r_link_pmax(n,n)   Máximo flujo de p activa en link de continua
*          r_link_smax        Máximo flujo de p aparente en link de continua
          ;

FdC=-1;
*tangente de phi para f.d.p=1,0.9,0.8,0.7 (inductivo y capacitivo). Esta en orden
COS_PHI_CONV= 1;
*COS_PHI=-0.7;

*COS_PHI_CONV=0.4843;
*COS_PHI=0.9;

*COS_PHI_CONV=0.75;
*COS_PHI=0.8;

*COS_PHI_CONV=1.0202;
*COS_PHI=0.7;

*COS_PHI_CONV=-0.4843;
*COS_PHI=0.9;

*COS_PHI_CONV=-0.75;
*COS_PHI=0.8;

*COS_PHI_CONV=-1.0202;
*COS_PHI=0.7;

P(ND) = DATNUD(ND,'P');
Q(ND) = DATNUD(ND,'Q');
p0(NG) = DATGEN(NG, 'p0') ;

SGmax(NG) = DATGEN(NG, 'pmax') ;
SGmin(NG) = DATGEN(NG, 'pmin') ;

$ontext
p0('gp3')= 0;
p0('gp4')= 0;
p0('gp5')= 0;
p0('gb5')= 0;
p0('gfc5')= 0;
p0('gp6')= 0;
p0('gwt7')= 0;
p0('gp8')= 0;
p0('gp9')= 0;
p0('GCHPD9')= 0;
p0('GCHPFC9 ')= 0;
p0('gp10')= 0;
p0('gb10')= 0;
p0('gfc10')= 0;
p0('gp11')= 0;
$offtext

****** añadimos cargas en los siguientes nudos:
*P('8') = DATNUD('8','P');
*Q('8') = DATNUD('8','Q');
*P('6') = DATNUD('6','P');
*Q('6') = DATNUD('6','Q') ;
*P('13') = DATNUD('13','P');
*P('F15') = P_CC ;

*Acutalización de datos Ensayo PRICE ÚNION FENOSOSA. Sensibilidad AV/AQ

*P('11') = 0;
*Q('11') = 0;
*P('3') = 0;
*Q('3') = 0;
*P('5') = 0;
*Q('5') = 0;
*P('6') = 20000*FdC*COS_PHI/Sb;
*Q('6') = P('6')*FdC*COS_PHI_CONV/Sb;
*P('7') = 0;
*Q('7') = 0;
*P('8') = 0;
*Q('8') = 0;
*P('9') = 0;
*Q('9') = 0;
*P('10') = 0;
*Q('10') = 0;

$ontext
*P('1') = 0;
*Q('1') = 0;
*P('2') = 0;
*Q('2') = 0;
*P('3') = 12500/Sb*FdC;
Q('3') = 0;
P('4') = 0;
Q('4') = 0;
*P('5') = 12500/Sb*FdC;
Q('5') = 0;
*P('6') = 12500/Sb*FdC;
Q('6') = 0;
*P('7') = 12500/Sb*FdC;
Q('7') = 0;
*P('8') = 12500/Sb*FdC;
Q('8') = 0;
*P('9') = 12500/Sb*FdC;
Q('9') = 0;
*P('10') = 12500/Sb*FdC;
Q('10') = 0;
P('11') = 12500/Sb*FdC;
Q('11') = 0;
P('12') = 0;
Q('12') = 0;
P('13') = 0;
Q('13') = 0;
P('14') = 0;
Q('14') = 0;
P('F15') = P_CC ;

p0('gp3')= 0;
p0('gp4')= 0;
p0('gp5')= 0;
p0('gb5')= 0;
p0('gfc5')= 0;
p0('gp6')= 0;
p0('gwt7')= 0;
p0('gp8')= 0;
p0('gp9')= 0;
p0('GCHPD9')= 0;
p0('GCHPFC9 ')= 0;
p0('gp10')= 0;
p0('gb10')= 0;
p0('gfc10')= 0;
p0('gp11')= 0;
$offtext

IMAX(ni,nf) = SUM[nl$(kl(nl,ni,nf)), DATLIN(nl,ni,nf,'flmax')] / Ib ;

** para incluir la carga en continua cuando no hay smartie:
IMAX('15','F15') = 100 / Ib ;
IMAX('8','F8') = 100 / Ib ;
IMAX('14','F14') = 100 / Ib ;
IMAX('0','1') = 100 / Ib ;
IMAX('0','12') = 100 / Ib ;

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

           ;
*-------------------------------------------------------------------------------
FREE VARIABLE obj;
POSITIVE VARIABLE vb1, vb2, vb3;

*** Limites de las variables
vv.lo(N) = Vmin; vv.up(N) = Vmax;
d.lo(N) = -pi; d.up(N) = pi;
vv.l(N) = 1; d.l(N) = 0; d.fx('0') = 0 ;

pgen.fx(NG) = 0 ; !DATGEN(ng, 'p0') ;
qgen.fx(NG) = 0 ;
*** slack
pgen.lo(SL) = -100 ; pgen.up(SL) = 100 ;
qgen.lo(SL) = -100 ; qgen.up(SL) = 100 ;

*** Vesp en barras de la subestacion
vv.fx('0') = V_SUBEST ;
*vv.fx('1') = V_SUBEST ;
*vv.fx('12') = V_SUBEST ;

***  ir2
*ir2.lo(NI,NF) = -imax(NI,NF)**2; ir2.up(NI,NF) = imax(NI,NF)**2;

POSITIVE VARIABLE Lambda, LambdaG(NG);
Lambda.lo = 1.0;
Lambda.fx = 1.0;
LambdaG.lo (NG) = 1.0;
LambdaG.fx('GFC5')  = 1;
LambdaG.fx('GFC10')  = 1;
LambdaG.fx('GP4')  = 1;
LambdaG.fx('GF15')  = 1;
LambdaG.fx('GF8')  = 1;
LambdaG.fx('GF14')  = 1;
*LambdaG.fx('GF0')  = 1;
LambdaG.up(NG)$(DATGEN(NG,'P0')=0) = 1.0  ;
*LambdaG.fx('GB5') = 1 ; LambdaG.fx('GB10') = 1 ;
*LambdaG.fx('GFC5') = 1 ; LambdaG.fx('GFC10') = 1 ;
*LambdaG.fx(NG) = 1.0 ;

********************************************************************************
VARIABLE Pgen2(NG), Qgen2(NG) ;
*Pgen2.fx(NG)=0;
*Qgen2.fx(NG)=0 ;
Pgen2.fx(NG) = DATGEN(ng, 'p0') ;
Qgen2.fx('GFC5') = 0 ;
Qgen2.fx('GFC10') = 0 ;
Qgen2.fx('GP4') = 0 ;
Qgen2.fx('GF15') = 0 ;
Qgen2.fx('GF8') = 0 ;
Qgen2.fx('GF14') = 0 ;

*Qgen2.fx(NG) = DATGEN(ng, 'p0')*0 ;
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
             eir2    intensidad de rama al cuadrado;
;

eqobj..      obj =e= sum(SL,pgen(SL));

*eqobj..      obj =e= -SUM(NG, LambdaG(NG)) ;   ! objetivo maximizar PENETRACION

eqp(ND)..     SUM(NDGR(ng,nd), pgen(NG) + pgen2(NG)) - Lambda*P(ND)
                     =E= vv(ND)*(va1(ND)+va2(ND));

eqa1(ND)..    va1(ND) =E= sum(NF,vv(NF)*Yg(ND,NF)*cos(d(ND)-d(NF)));

eqa2(ND)..    va2(ND) =E= sum(NF,vv(NF)*Yb(ND,NF)*sin(d(ND)-d(NF)));

eqq(ND)..     SUM(NDGR(ng,nd), qgen(NG) + qgen2(NG)) - Lambda*Q(ND)
                     =E= vv(ND)*(va3(ND)+va4(ND));

eqa3(ND)..    va3(ND) =E= sum(NF,vv(NF)*Yg(ND,NF)*sin(d(ND)-d(NF)));

eqa4(ND)..    va4(ND) =E= sum(NF,-vv(NF)*Yb(ND,NF)*cos(d(ND)-d(NF)));

eqb1(ND)..           vb1(ND) =E= vv(ND)**2;

eqb2(KL(NL,NI,NF))..   vb2(NI,NF) =E= 2*vv(NI)*vv(NF);

eqb3(KL(NL,NI,NF))..   vb3(NI,NF) =E= cos(d(NI)-d(NF));

eq_i1(ND)..     i1(ND) =e= sqrt(power(P(ND),2)  + power(Q(ND),2))/vv(ND) ;

eq_i2..     i2 =e= sqrt(power(Pgen('gf14'),2) + power(Qgen('gf14'),2))/vv('F14')   ;

eir2(KL(NL,NI,NF))..    ir2(NI,NF) =e= sqrt(power(vv(NI)*cos(d(NI))-vv(NF)*cos(d(NF)),2)+power(vv(NI)*sin(d(NI))-vv(NF)*sin(d(NF)),2))*sqrt((gij(NI,NF)**2+power(bij(NI,NF),2)));

*eir2(KL(NL,NI,NF))..    ir2(NI,NF) =e= power((vv(NI)*cos(d(NI))-vv(NF)*cos(d(NF))),2)+power((vv(NI)*sin(d(NI))-vv(NF)*sin(d(NF))),2);


*eir2(KL(NL,NI,NF))..    ir2(NI,NF) =e= (gij(NI,NF)**2+Yb(NI,NF)**2)*(vb1(NI)+vb1(NF)-vb2(NI,NF)*vb3(NI,NF));

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
EQUATION     sgmax_n  máxima potencia aparente inyectada por generador  ;

sgmax_n(ng)..   power(pgen2(ng),2) + power(qgen2(ng),2)  =L= (SGmax(ng))**2  ;

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
SUM_G_INI = SUM(NG, G_INI(NG)) ;
SUM_G_FIN = SUM(NG, G_FIN(NG)) ;
Irama(NI,NF) = ir2.l(NI,NF)*Ib;
OPTION V:4, PERD:0, PCONV:0, QCONV:0, dLAMBDA:3, dLAMBDAG:3;



DISPLAY PERD, V, Irama, PCONV , QCONV, dLAMBDAG, G_INI, G_FIN, G_DIF  ;
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

PUT '- Intensidades en las ramas' /
LOOP(NI,LOOP(NF, PUT NI.TL NF.TL Irama(NI,NF):<:4 /) );


PUT / ;

PUT '- P y Q inyectada desde la subestación (W y var)' /
PUT 'P: ' PSE:< /
PUT 'Q: ' QSE:< /