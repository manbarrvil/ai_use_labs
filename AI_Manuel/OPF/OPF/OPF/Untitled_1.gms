
set

n generadores /n1,n2,n3/
l cargas /l1,l2/
t tiempo /t1,t2,t3,t4/;

scalar
*Contantes que no dependen de conjuntos

SOC_max SOC maximo kwh /10/
P_max_bat Pot. maximo kw /5/
eta_c Rendimiento de carga /0.9/
eta_d Rendimiento de descarga  /0.9/
Pmax_load Potencia maxima carga /4/
delta_t incremento en tiempo /1/;

parameters

a(n)  termino cuadratico coste gen /n1 0, n2 1, n3 1/
b(n)  termino lineal coste gen /n1 0.1, n2 0.15, n3 0.65/
c(n)  termino independiente coste gen /n1 0, n2 0.9, n3 0.8/
Pmax(n) potencia maxima cada gen /n1 5, n2 2, n3 0/
Pmin(n) potencia minima cada gen /n1 1,n2 0.2,n3 0/
lambda(t) porcentaje de carga en cada instante de tiempo /t1 1,t2 0.5,t3 1,t4 0.5/ ;

variables

Pgen(n,t) Define potencia cada generador en cada inst de tiempo
Pd(t) potencia de descarga de la bateria
Pc(t) potencia de carga de la bateria
SOC(t) estado de carga de la bateria
coste(n,t) coste de cada generador en cada instante de tiempo
coste_total coste total de todos los generadores en todos los instantes de tiempo;

Pc.up(t) = P_max_bat;
Pd.up(t) = P_max_bat;
Pc.lo(t) = 0;
Pd.lo(t) = 0;
SOC.up(t)= SOC_max;
SOC.lo(t)= 0;

equations
eq_bal(t) ecuacion de balance
eq_SOC(t) ecuacion del estado de carga
eq_coste(n,t)  ecuacion de coste de cada generador
eq_coste_total ecuacion total de costes
eq_Pmax(n,t) ecuacion potencia maxima generadores
eq_Pmin(n,t) ecuacion potencia minima generadores;


eq_bal(t).. sum(n,Pgen(n,t)) + Pd(t) =e=  lambda(t)*Pmax_load*2 + Pc(t);

eq_SOC(t).. SOC(t) =e= SOC(t-1) + Pc(t)*eta_c*delta_t - Pd(t)/eta_d*delta_t;

eq_Pmax(n,t)..   Pgen(n,t) =l= Pmax(n);

eq_Pmin(n,t)..   Pgen(n,t) =g= Pmin(n);

eq_coste(n,t)..   coste(n,t) =e= a(n)*power(Pgen(n,t),2) + b(n)*Pgen(n,t) + c(n);

eq_coste_total..  coste_total = sum(n,sum(t,coste(n,t)));

model Modelo_costes_gen_bate /all/    ;
solve Modelo_costes_gen_bate minimizing coste_total using MInlp;


