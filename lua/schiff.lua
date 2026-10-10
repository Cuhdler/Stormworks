-- SCHIFF v3.7 - Figet Marena: 4 Diesel ohne ZE-Regler (L1 unten links, L2 oben links, R1 unten rechts, R2 oben rechts),
-- je Motor Gemisch, Anlasser, Leerlauf, Kupplung, Temperatur-Regler; 8 Gaenge aus 3 Getrieben, Rueckwaertsgang je
-- Seite, Lenk-Schub, Ruder, Bugstrahlruder
-- Eingang (Composite, im Chip zusammengefuehrt):
--  Zahl 1-4 Sitz Achse 1-4 (A/D, W/S, Pfeil links/rechts, Pfeil hoch/runter), 5 Tempo m/s, 6 Kompass,
--  je Motor i (1 L1, 2 L2, 3 R1, 4 R2) ab 3+4i: RPS, Temperatur, Luft, Treibstoff im Zylinder
--  Bool 1-6 Sitz Hotkey 1-6, 8 Sitz besetzt
--  v2.7 vom Wellen-Skript (lua/wellen.lua): Zahl 24 Gas-Abzug (0..1, Drehzahl halten bei Schrauben in der Luft), v3.5 Zahl 25
--  Batterie-Ladung (0..1),
--  Bool 9 Schaltsperre (Schrauben draussen und kurz danach)
-- Ausgang: je Motor ab 3i-2: Air Manifold, Fuel Manifold, Kupplung; 13 Ruder, 14 Bugstrahlruder, 15-28 Anzeige
--  Bool 1 Motoren an (Pumpen, Luefter), 1+i Anlasser Motor i, 6/7 Rueckwaertsgang links/rechts, 8 Anzeige Seite 2,
--  9/10/11 Getriebe A/B/C an (Gear Switch, beide Seiten), 12 Schaltsperre (fuer den Fahrtenschreiber)
-- Hotkey 4 = Helm-Anzeige umschalten (Seite 2: Gemisch-Diagnose)
-- Gaenge: 3 Getriebe je Seite (aus 1:1 / an 'Getriebe A/B/C', Pfeil zum Motor) in allen Kombinationen = 8 Gaenge,
--  nach Uebersetzung sortiert. Automatik: ueber 'Hoch ab RPS' hoch (nur wenn der Motor danach noch ueber 'Runter unter
--  RPS' liegt; in Wellen sperrt das Wellen-Skript - v3.2: die alte Bedingung 'Tempo faellt nicht' merkte sich einen
--  Tempo-Ausreisser von 67 kn und liess ihn bei 54.5 kn ewig in Gang 5, Fahrt 02.10. 21:09), darunter runter; je 'Schaltzeit s' warten. Hotkey 3 = Automatik aus/an, von Hand Pfeil hoch/runter.
--  Rueckwaerts und Hebel auf null: Gang 1.
-- Hotkey 1 = Motoren an/aus, Hotkey 2 = Stopp, W/S = Fahrhebel (bleibt stehen; unter null = rueckwaerts bis
-- 'Rueckwaerts max'), A/D = Ruder, Lenk-Schub und Bugstrahlruder ('Bugstrahl beim Lenken'), Pfeil links/rechts =
--  Bugstrahlruder von Hand
-- Fahrhebel = Leistung (Anteil der vollen Treibstoffmenge), keine Drehzahl-Grenze im Betrieb; ausgekuppelt 'Leerlauf
--  RPS', 'RPS Notgrenze' nur gegen Durchdrehen. Grenze ist die Temperatur, ueber 'Motor heiss Grad' auskuppeln.
-- Temperatur-Regler v3.4: EINE Gas-Grenze fuer alle 4 Motoren (Schiff faehrt gerade). Erlaubter Anstieg je Motor =
--  ('Temp Ziel' - Temperatur) / 'Temp Anflug s'; die Grenze folgt dem Motor, der am staerksten darueber liegt (Anstieg
--  aus der ueber 2 s geglaetteten Temperatur, nochmals 3 s gemittelt). v3.3 regelte jeden Motor allein auf 95 Grad und schaukelte: Seiten abwechselnd 10 % / 55 %
--  Gas, 18-29 kn, Schiff zog hin und her (Fahrt 07.10.). Ziel 70: bis 75 Grad volle Leistung, bei 80-85 nur noch
--  ca. die Haelfte (Gang 7 Vollgas 60 -> 48 kn, gleiche Drosseln).
-- E-Motoren v3.5 (Andre: zwei grosse E-Motoren an der Welle vor den Getrieben, statt der kleinen Generatoren): sie bekommen
--  den Teil des Fahrhebels, den die Temperatur-Grenze den Dieseln wegnimmt (mal 'E-Motor Anteil'; ohne Gas-Abzug der
--  Wellen); Zahl 20 = E-Gas 0..1 (der Chip gibt es je Seite mal 'E-Motor Richtung L/R' an die Motoren). Batterie (Zahl 25,
--  ueber den Flossen-Chip) unter 'E-Motor ab Batterie': aus, erst 5 % darueber wieder an (Anlasser, Pumpen, Luefter
--  brauchen den Strom); Bool 13 = E-Motor wuerde gebraucht, ist aber deshalb aus. 'E-Motor Test' 1: Diesel bleiben ausgekuppelt, E-Gas = Fahrhebel.
-- v3.6 (Andre: "der E-Motor hat nicht gleich viel Power - kann der Chip merken, ob wir langsamer werden?"): Tempo halten
--  statt fester Aufteilung - drosselt die Temperatur die Diesel, gilt das Tempo dieses Moments als Soll (Hebel waehrend-
--  dessen verstellt: Soll mal (Hebel neu/alt)^0,4 - Fahrten 07./08.10.: 44 % Gas = 70 % Tempo), ein langsamer PI-Regler ('E Tempo P/I') gibt so viel E-Gas, dass es gehalten wird,
--  hoechstens 'E-Motor Anteil'. Laeuft weiter, bis die Diesel nicht mehr gedrosselt sind und das E-Gas abgebaut ist.
-- v3.6 Fahrhebel: die Sitz-Achse W/S steigt beim Druecken in ca. 3 s an und faellt nach dem Loslassen langsam ab (Log
--  09.10.) - der Hebel lief zaeh an und nach dem Loslassen weiter. Von Hand jetzt: Achse steigt oder steht = Taste
--  gedrueckt = volle Hebel-Geschwindigkeit, faellt = Hebel bleibt stehen. Der Autopilot (Bool 10, vom Autopilot-Chip)
--  schiebt fein wie bisher.
-- v3.7 Temperatur-Treppe (Test, Andre 10.10.: "die beste Dauer-Geschwindigkeit bei gehaltener Temperatur suchen"):
--  'Temp Treppe' 1: der Regler haelt nacheinander 75, 85, 95 Grad je 3 min (gezaehlt, solange der heisseste Motor
--  hoechstens 2 Grad darunter ist), danach 'Temp Ziel'; E-Motoren dabei aus (nur Diesel messen).
-- Gemisch: Treibstoff = Luft * Q / Luftverhaeltnis. v3.2: Q fest 7.1 (darauf liefen alle 4 Motoren in ruhiger Fahrt;
--  Andre: 'es soll immer gleich bleiben') - Ventile im festen Verhaeltnis. Mit 'Gemisch Regler' > 0 (z. B. 2e-4) regelt
--  der Chip Q je Motor wieder so nach, dass die gemessene Stoechiometrie im Zylinder das Ziel 'Gemisch' trifft (0.5
--  kraeftig, 0.2 sparsam). Die gemessene schwankt aber mit Drehzahl und beim Gasgeben stark, der Regler lief ihr nach:
--  Luft und Treibstoff im Zylinder werden ueber ca. 0.3 s gemittelt. v3.1: Regler 5-mal langsamer: in Gang 4 schwankte das
--  gemessene Gemisch mit der Drehzahl zwischen -0.1 und 1.3 im 3-s-Takt, der Regler gab im Takt bis 2.4 % Treibstoff dazu
--  und schaukelte mit (Fahrt 02.10. 20:50). v3.0 mittelte stattdessen 3 s - dann hielt er den kurzen Fett-Moment beim
--  Gasgeben zu lange fuer echt und magerte L1 von Q 7.1 auf 5.4 ab (Leistungsloch nach dem Schalten, Fahrt 21:03).
-- Anlasser: sofort nach 'an' (nach Abwuergen 1 s spaeter), bis der Motor 0.5 s ueber 3/4 Leerlauf laeuft;
--  hoechstens 8 s am Stueck, dann 2 s Pause.
-- Rueckwaerts: der Gang einer Seite wechselt erst, wenn beide Kupplungen dieser Seite offen sind.
-- Lenk-Schub: beim Lenken bekommt die kurveninnere Seite bis zu 'Lenk-Schub' weniger Gas (negativ = andere Seite).
N=input.getNumber
B=input.getBool
S=output.setNumber
O=output.setBool
P=property.getNumber
m=math
function cl(v,a,b) return m.max(a,m.min(b,v)) end

on=false
hb=0
ru=0
t=0
-- je Seite: Rueckwaertsgang eingelegt, Ticks mit offenen Kupplungen
RV={false,false}
W={0,0}
-- Anzeige-Seite 2 (Gemisch-Diagnose); Gang, Automatik, Zeiten fuer hoch/runter/Sperre nach dem Schalten
pg=false
G=1
au=true
ut=0
dt=0
lk=0
-- je Motor: Kupplung, Zeit ohne Drehzahl, Ausfall, Gas-Grenze (Temperatur); Regler: I Integral, FS geglaettete
-- Einspritzung, FM letzte Treibstoff-Drossel, Q Gemisch-Verhaeltnis (nachgeregelt), T1 Ticks seit Startversuch,
-- T2 Ticks mit Drehzahl, ST Anlasser, LA/TA gemittelte Luft/Treibstoff im Zylinder
-- TP/TR je Motor: geglaettete Temperatur, Anstieg Grad/s; TL gemeinsame Gas-Grenze
K,Z,A,TP,TR,I,FS,FM,Q,T1,T2,ST,LA,TA={},{},{},{},{},{},{},{},{},{},{},{},{},{}
TL=1
TS=1
TT=0
EM=0
EA=false
A2=0
EI=0
eh=0
VR=0
GV=0
for i=1,4 do
	K[i]=0 Z[i]=0 A[i]=false TP[i]=0 TR[i]=0 I[i]=0 FS[i]=0 FM[i]=1e-7 Q[i]=7.1 T1[i]=60 T2[i]=0 ST[i]=false LA[i]=0 TA[i]=0
end

function onTick()
	if not ini then
		ini=1
		ht=P('Hebel Tempo')/60
		hr=P('Rueckwaerts max')
		rmax=P('Ruder max')
		rsig=P('Ruder Richtung')
		rt=P('Ruder Tempo')/60
		bsig=P('Bugstrahl Richtung')
		bm=P('Bugstrahl beim Lenken')
		ls=P('Lenk-Schub')
		kab=P('Kupplung ab RPS')
		kz=P('Kupplung Zeit s')*60
		hot=P('Motor heiss Grad')
		az=P('Motor Ausfall s')*60
		tz=P('Temp Ziel')
		tf=P('Temp Anflug s')
		tk=P('Temp Regel')/60
		ea=P('E-Motor ab Batterie')
		ef=P('E-Motor Anteil')
		et=P('E-Motor Test')>0
		tt=P('Temp Treppe')>0
		tz0=tz
		if tt then ef=0 tz=75 end
		ekp=P('E Tempo P')
		eki=P('E Tempo I')
		idl=P('Leerlauf RPS')
		rn=P('RPS Notgrenze')
		st=P('Gemisch')
		gq=P('Gemisch Regler')
		hoch=P('Hoch ab RPS')
		runt=P('Runter unter RPS')
		sz=P('Schaltzeit s')*60
		-- 8 Gaenge: {Uebersetzung, Getriebe-Bits}, aufsteigend
		ga={P('Getriebe A'),P('Getriebe B'),P('Getriebe C')}
		GR={}
		for c=0,7 do
			local r=1
			for k=1,3 do if m.floor(c/2^(k-1))%2==1 then r=r*ga[k] end end
			GR[c+1]={r,c}
		end
		table.sort(GR,function(a,b) return a[1]<b[1] end)
	end
	local a1,a2,a3=N(1),N(2),N(3)
	local h1,h2=B(1),B(2)
	-- Hotkey 1: Motoren an/aus (beim Druecken umschalten)
	if h1 and not k1 then on=not on t=0 end
	k1=h1
	t=t+1
	-- Fahrhebel: W/S halten verstellt ihn, Hotkey 2 = Stopp
	local wv=a2
	if not B(10) then wv=(m.abs(a2)>.02 and m.abs(a2)>=m.abs(A2)-1e-4 and a2*A2>=0) and (a2>0 and 1 or -1) or 0 end
	A2=a2
	hb=cl(hb+wv*ht,-hr,1)
	if h2 or not on then hb=0 end
	local rw,g=hb<0,m.abs(hb)
	-- Ruder mit begrenztem Tempo
	ru=ru+cl(a1*rmax-ru,-rt,rt)
	-- Lenk-Schub: kurveninnere Seite weniger Gas
	local l=cl(a1,-1,1)*(ls<0 and -1 or 1)
	local gs={g*(1-m.abs(ls)*m.max(0,-l)),g*(1-m.abs(ls)*m.max(0,l))}
	-- Gaenge: Motor-RPS (hoechste), eingekuppelt?
	if B(3) and not k3 then au=not au end
	k3=B(3)
	local a4,r,ek=N(4),0,false
	for i=1,4 do r=m.max(r,N(3+4*i)) ek=ek or K[i]>=1 end
	lk=lk+1
	-- Wellen: keine Schaltung, solange die Schrauben draussen sind und kurz danach (Sperre wie nach dem Schalten)
	if B(9) then lk=0 end
	if au then
		if g<=.02 or rw then G=1 end
		if ek and r>hoch then ut=ut+1 else ut=0 end
		if ek and r<runt then dt=dt+1 else dt=0 end
		if lk>sz*2 then
			if ut>sz and G<8 and r*GR[G][1]/GR[G+1][1]>=runt*1.1 then G=G+1 lk=0 ut=0 end
			if dt>sz and G>1 then G=G-1 lk=0 dt=0 end
		end
	else
		if a4>.5 and not k6 and G<8 then G=G+1 end
		if a4<-.5 and not k7 and G>1 then G=G-1 end
		if rw then G=1 end
	end
	k6=a4>.5
	k7=a4<-.5
	for k=1,3 do O(8+k,m.floor(GR[G][2]/2^(k-1))%2==1) end
	-- Temperatur-Regler: e = kleinster Spielraum (erlaubter minus gemessener Anstieg) aller laufenden Motoren
	local e,th=1,0
	for i=1,4 do
		local rps,tmp=N(3+4*i),N(4+4*i)
		if TP[i]==0 then TP[i]=tmp end
		local d=(tmp-TP[i])/120
		TP[i]=TP[i]+d
		TR[i]=TR[i]+(d*60-TR[i])/180
		if rps>=1 then e=m.min(e,(tz-TP[i])/tf-TR[i]) th=m.max(th,TP[i]) end
	end
	-- v3.7 Treppe: je Stufe 3 min nahe am Ziel, dann 10 Grad hoeher; nach 95 Grad 'Temp Ziel'
	if tt and TS<4 then
		if th>=tz-2 then TT=TT+1 end
		if TT>10800 then TS=TS+1 TT=0 tz=TS<4 and 65+10*TS or tz0 end
	end
	-- v3.6: heissester Motor mehr als 8 Grad unter dem Ziel: Grenze folgt dem Hebel sofort (vorher 3 %/s bei 60 Grad -
	-- das echte Gas hing hinter dem Hebel her); naeher am Ziel regelt sie langsam
	TL=cl(TL+(th<tz-8 and m.max(e,0)>0 and 1/60 or e*tk),.1,1)
	-- eingekuppelt nicht ueber dem gewuenschten Gas hochlaufen (sonst wirkt die Grenze nach dem Gasgeben erst spaet)
	if ek then TL=m.min(TL,m.max(gs[1],gs[2])+.05) end
	-- E-Motoren: Rest des Hebels, den die Diesel wegen der Temperatur nicht duerfen; Batterie-Schutz; Test = nur E
	local eb=N(25)
	if eb<ea then EA=false elseif eb>ea+.05 then EA=true end
	-- Tempo halten: Soll = Tempo beim Beginn der Drosselung (oder nach einer Hebel-Aenderung), PI auf das Tempo
	local v,lim=N(5),on and ek and not et and TL<g-.01
	if lim and not LM then VR=v GV=g elseif lim and m.abs(g-GV)>.02 then VR=VR*(g/m.max(GV,.01))^.4 GV=g end
	-- Hebel ohne Drosselung verstellt, ausgekuppelt oder Motoren aus: Tempo halten vorbei
	if not lim and m.abs(g-GV)>.02 or not (on and ek) then EI=0 end
	if lim or EI>.01 then
		local ev=VR-v
		EI=cl(EI+ev*eki/60,0,ef)
		eh=cl(ev*ekp+EI,0,ef)
	else
		EI=0
		eh=0
	end
	LM=lim
	local es=on and m.min(et and g or eh*(1-N(24)),1) or 0
	EW=not EA and es>.02
	EM=EM+cl((EA and es or 0)-EM,-.02,.02)
	-- Rueckwaertsgang je Seite erst umlegen, wenn beide Kupplungen der Seite 0.1 s offen sind
	for s=1,2 do
		if RV[s]~=rw then
			if K[2*s-1]<=0 and K[2*s]<=0 then W[s]=W[s]+1 else W[s]=0 end
			if W[s]>5 then RV[s]=rw end
		else
			W[s]=0
		end
	end
	for i=1,4 do
		local s=i<3 and 1 or 2
		local b=3+4*i
		local rps,tmp,air,fuel=N(b),N(b+1),N(b+2),N(b+3)
		-- Luft und Treibstoff im Zylinder mitteln (schwanken mit dem Takt)
		LA[i]=LA[i]+(air-LA[i])*.05
		TA[i]=TA[i]+(fuel-TA[i])*.05
		-- Ausfall: laeuft seit dem Anlassen (15 s) nicht, oder bleibt 'Motor Ausfall s' lang unter 2 RPS
		if on and t>900 and rps<2 then Z[i]=Z[i]+1 else Z[i]=0 end
		A[i]=Z[i]>az
		-- Kupplung: Motor laeuft, nicht im Notfall heiss, Fahrt gewuenscht, richtiger Gang; langsam ein, sofort aus
		if on and rps>=kab and tmp<hot and g>.02 and not A[i] and RV[s]==rw and not et then K[i]=m.min(K[i]+1/kz,1) else K[i]=0 end
		local am,fm,th,fx,mx=1e-7,1e-7,0,1,0
		-- laeuft oder wird angelassen: Treibstoff und Luft geben
		if on and (rps>=1 or ST[i]) then
			local T=cl(tmp,0,100)
			local af=14+T/100-2*st-.03*T*st
			-- Gemisch nachregeln: zu fett (gemessen ueber Ziel) -> Q kleiner = weniger Treibstoff je Luft; nur gueltige
			-- Messwerte, hoechstens 0.2 % je Tick (v2.5; mit 1 % schaukelte sich in Gang 4 Q/Drehzahl/Tempo auf, Fahrt 01.10.)
			if LA[i]>1e-6 and TA[i]>1e-6 then
				mx=(T+1400-100*LA[i]/TA[i])/(3*T+200)
				if mx>-6 and mx<6 then Q[i]=cl(Q[i]*m.exp(cl((st-mx)*gq,-.002,.002)),1,60) end
			end
			-- fx: meiste Treibstoff-Drossel bei Luft 1
			fx=cl(Q[i]/af,1e-4,1)
			-- Drehzahlregler (PI mit Einspritz-Anpassung wie ZE): ausgekuppelt Leerlauf, eingekuppelt nur Notgrenze
			FS[i]=FS[i]+cl(m.min(fuel/FM[i],.1)-FS[i],-.001,.001)
			local mu=.0015/(FS[i]+.0015)
			local e=(K[i]>0 and rn or idl)-rps
			local u=e*.1*mu+I[i]
			if u>0 and u<1 then I[i]=cl(I[i]+e*.002*mu,0,m.max(FM[i],.1)) end
			th=m.min(cl(u,0,1),(K[i]>0 and m.min(gs[s],TL)*(1-N(24)) or TL)*fx)
			am=cl(th*af/Q[i],1e-4,1)
			fm=cl(th,1e-7,fx)
		else
			I[i]=0
		end
		FM[i]=fm
		-- Anlasser
		if rps>=idl*.75 then T2[i]=m.min(T2[i]+1,30) else T2[i]=0 end
		if T2[i]>=30 then T1[i]=0 elseif not on then T1[i]=60 else T1[i]=T1[i]+1 end
		local c=T1[i]%600
		ST[i]=on and T2[i]<30 and tmp<hot and c>=60 and c<540
		local o=3*i-2
		S(o,am)
		S(o+1,fm)
		S(o+2,K[i])
		O(1+i,ST[i])
		-- Anzeige gepackt (ganze Zahlen, bleiben im Composite exakt): RPS*10*1000+Temperatur und
		-- Zustand*1e6+Gas%*1000+(Gemisch+2)*100. Zustand: 0 OK, 1 HEISS, 2 AUSFALL, 3 TEMP, 4 LEER, 5 KUPPELT, 6 ---
		local z=(tmp==0 and rps==0) and 6 or A[i] and 2 or tmp>=hot and 1 or K[i]>0 and TL<gs[s]-.01 and 3 or K[i]>=1 and 0 or K[i]>0 and 5 or 4
		S(19+2*i,m.floor(cl(rps,0,999)*10+.5)*1000+m.floor(cl(tmp,0,999)+.5))
		S(20+2*i,z*1e6+m.floor(cl(th/fx,0,1)*100+.5)*1000+m.floor(cl(mx+2,0,9.99)*100+.5))
		-- Diagnose: Q*10*1000+Luft-Drossel %
		S(28+i,m.floor(Q[i]*10+.5)*1000+m.floor(am*100+.5))
	end
	-- Hotkey 4: Anzeige-Seite
	if B(4) and not k4 then pg=not pg end
	k4=B(4)
	O(8,pg)
	O(12,B(9))
	O(13,EW)
	O(1,on)
	O(6,RV[1])
	O(7,RV[2])
	S(13,ru*rsig)
	S(14,cl(a3+a1*bm,-1,1)*bsig)
	-- Anzeige: 15 an (0 aus, sonst Uebersetzung*10*10000+Gang*100+Automatik*10+1), 16 Hebel (-: rueckwaerts),
	-- 17 Tempo m/s, 18 Kurs Grad, 19 Ruder (Anteil), 20 Bugstrahl
	S(15,on and m.floor(GR[G][1]*10+.5)*10000+G*100+(au and 10 or 0)+1 or 0) S(16,hb) S(17,N(5)) S(18,(N(6)*360)%360) S(19,rmax>0 and ru/rmax or 0) S(20,EM)
end
