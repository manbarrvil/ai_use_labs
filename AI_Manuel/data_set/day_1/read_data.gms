* Data input for PES2012
* The data comes from tables in CSV format.
*
$ONMULTI
$ONEMPTY
$EOLCOM !
*** RED EN ESTUDIO ***
*$ SETGLOBAL rsyst EDF1994
*$ SETGLOBAL rsyst 60bus_MGC
* Declaración de conjuntos básicos (nudos, líneas, trafos, generadores)
SET     ND  nombre de los nudos del sistema /  0 * 15, F15, F8, F14  /
*$INCLUDE ND.CSV
*        /
        NL  nombre de las lineas del sistema /
$INCLUDE NL.CSV
        /
*        NT nombre de los trafos del sistema   /
*$INCLUDE NT.CSV
*        /
        NG nombre de los generadores   /
$INCLUDE NG.CSV
        /   ;

ALIAS(nd,ni,nf,n,nn,n2)   ;

SET NG / GF0, GF15, GF8, GF14 / ;  ! Generadores ficticios modelan la inyeccion desde la S/E
                        ! y la inyeccion de cada convertidor  - SE SUMA AL NG QUE VIENE DEL $INCLUDE
SET SL(NG) generadores que modelan las inyecciones desde las SE  ;
SL('GF0') = YES ;
SET GS(NG) generadores que modelan la inyeccion de cada convertidor  ;
GS('GF15') = YES ; GS('GF8') = YES ; GS('GF14') = YES ;
SET NL / TC1, TC2, TC3  /  ;  ! transformadores de conexion al convertidor

* Inclusión de datos
TABLE BUS_DATA(nd, *)
$ONDELIM
$INCLUDE BUS_DATA.CSV
$OFFDELIM

TABLE LINE_DATA(nl, nd, nd, *)
$ONDELIM
$INCLUDE LINE_DATA.CSV
$OFFDELIM

TABLE GEN_DATA(ng, nd, *)
$ONDELIM
$INCLUDE GEN_DATA.txt
$OFFDELIM

TABLE LOADH_DATA(nd, *)
$ONDELIM
$INCLUDE LOAD_H_DATA.txt
$OFFDELIM

TABLE LOADI_DATA(nd, *)
$ONDELIM
$INCLUDE LOAD_I_DATA.txt
$OFFDELIM

* Tuplas que declaran la ubicación y estado de líneas, trafos y generadores
SET KL(nl, nd, nd) lineas presentes  ;
kl(nl,ni,nf) $ LINE_DATA(nl,ni,nf,'status') = YES  ;
kl('tc1', '8','F8') = YES; kl('tc2','14','F14') = YES  ;
kl('tc3','15','F15')  = YES ;
kl('Line_01','0','1') = YES ; kl('Line_02','0','12') = YES ;

*SET KTRFO(nt, nd, nd)  trafos presentes  ;
*ktrfo(nt, ni, nf) $  TRFO_DATA(nt, ni, nf, 'status') = YES  ;

SET NDGR(ng,nd)  localización de generadores en nudos   ;
ndgr(ng, nd) $ GEN_DATA(ng, nd,'P') = YES   ;
ndgr('GF0','0') = YES;
ndgr('GF15','F15') = YES;  ndgr('GF8','F8') = YES  ; ndgr('GF14','F14') = YES;

DISPLAY KL, NDGR, NG
*SET SLACK(nd) nudo slack  /
*$INCLUDE SLACK.CSV