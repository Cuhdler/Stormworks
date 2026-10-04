-- FLAKRADAR v2.3 - Figet Marena, Flak-Turm hinten (ein Chip je Turm): Spuren fuehren, Turm-Radar steuern.
-- Umbau von AARADAR v4 (Swifter-Flugabwehr, im Spiel erprobt) fuers Schiff: Lage und eigenes Tempo kommen vom
-- Physik-Sensor (Kurs = -Kompass, im Uhrzeigersinn, Norden = +z; Tempo aus der Positionsaenderung wie beim Rescue Heli),
-- das Radar (Basic) sitzt auf dem Flak-Turm und wird im manuellen Modus ueber 'Gimbal Input' gerichtet.
-- v1.3: das Ziel waehlt die Lagezentrale (Bildschirm-Chip: AUTO teilt die Luftziele auf beide Flaks auf, oder Andre
-- weist eines zu) - die Flak schiesst nur noch auf die Luft-Spur ihres eigenen Radars, die am naechsten an dieser
-- Vorgabe liegt (Fangbereich 150 m + 5 % der Entfernung, Hoehe halb gezaehlt; hoeher als 'AA Mindesthoehe m'), und
-- nur mit 'Feuer frei'. Ohne passende Spur zeigt der Strahl auf die Vorgabe; ohne Vorgabe kreist er und sucht (jede
-- Runde eine andere Hoehe: 'AA Suchstufen' Stufen ab 'AA Suchhoehe Grad', je 'AA Suchstufe Grad').
-- v1.4 (Andre: "hardlocken, bis ein anderes Ziel gewaehlt wird"): hat die Flak ihre Spur gefunden, bleibt sie darauf,
-- auch wenn die Vorgabe der Lagezentrale abweicht - bis eine andere Zielnummer kommt (oder die Spur 2 s weg ist).
-- v1.5 (Andre: rechte Flak schoss auf 'Geister'): liegt die eigene Spur zu weit neben der Vorgabe, laesst die Flak sie
-- los und sucht an der Vorgabe neu.
-- v1.7 (Andres Log 03.10. 22:40 im Hafen: die linke Flak fing statt des vorgegebenen Ziels ein stehendes Ding 133 m
-- daneben und liess es nicht los, auch als ihr ein Heli 210 m daneben zugewiesen wurde): Fangbereich 40 m + 10 % der
-- Entfernung (vorher 150 m + 5 %), Hoehe voll gezaehlt (die Vorgabe der Lagezentrale ist nah genau); loslassen, wenn die
-- eigene Spur 1 s lang weiter als 60 m + 20 % neben der Vorgabe liegt (vorher 300 m + 15 %, 2 s).
-- Eingang: Radar-Composite (Ziele 1-6: Zahl 4i-3 Entfernung, 4i-2 Seitenwinkel, 4i-1 Hoehenwinkel; Bool i gemeldet),
--  ueberschriebene Kanaele: 4 Flak-Turm-Drehung (U), 8 Physik x (m), 12 Physik Kompass (U), 16 Physik Nick-Neigung (U),
--  20 Physik Quer-Neigung (U), 24 Physik Hoehe (m), 25 Zielnummer der Vorgabe, 28 Radar-Drehung (U, 'Radar
--  Rotation'), 29-31 Vorgabe Ost/Nord
--  (m, relativ zum Schiff) und Hoehe ueber dem Meer (m), 32 Physik z (m); Bool 10 Vorgabe da, 11 Feuer frei,
--  12 Einzelschuss (v1.9, Leertaste: wird als Bool 4 an FLAK durchgereicht)
-- v2.0: Glaettung der Spur einstellbar ('Spur Alpha', 'Spur Beta'; Flak 0,1 / 0,005 wie bisher) - die Kanonen gegen
--  Schiffe glaetten staerker (Schiffe aendern ihr Tempo langsam; bei 9 s Flugzeit werden 1,5 m/s Tempo-Rauschen 14 m)
-- v2.1: ohne Spur geht die Vorgabe auf 3-5 (Bool 2 aus) - FLAK dreht den Turm schon dorthin; ohne beides 0
-- v2.2 (Andres Test 04.10. im Hafen: die Kanonen hielten ihr Schiff, schossen aber nie - die gehaltene Spur war bei
--  16 vollen Spuren als 'aelteste' verdraengt worden, der Hardlock hielt sie trotzdem fest: eingefroren, Alter 4,
--  Messdauer 0,15 s < 0,4): die gehaltene Spur wird nie verdraengt; ist sie nicht mehr in der Liste, ist sie verloren.
--  'Ziel Tempo max m/s': schneller ist keine Spur (Kanonen 20: im Hafen-Gewimmel gab ein Nachbar-Ding 40 m daneben
--  der Spur Fantasie-Tempo - der Vorhalt schoss 1-2 km daneben; Flak 400 = praktisch frei).
-- v2.3 (Andres Test 04.10.: bei schneller Fahrt zielten BC und AC daneben): die Spuren laufen in der Welt (Ortung +
--  eigener Ort vom Physik-Sensor) - vorher relativ zum Schiff: der Deckel 'Ziel Tempo max m/s' (Kanonen 20) schnitt bei
--  36 m/s eigener Fahrt schon das Relativ-Tempo eines langsamen Schiffs ab, und die starke Glaettung (BC Beta 0,0003)
--  hinkte jeder Aenderung der eigenen Fahrt hinterher. Ausgaenge wie bisher relativ (Tempo = Welt-Tempo - eigenes).
-- Ausgang: Zahl 1/2 Strahl Seite/Hoehe (U, an 'Gimbal Input'), 3-5 Ziel Ost/Nord/Hoch (m, relativ zu uns, jetzt),
--  6-8 dessen Tempo relativ zu uns (m/s), 9 Messdauer s, 10 Entfernung, 11 Hoehe ueber dem Meer, 12 Ticks seit Meldung,
--  13 Spuren, 14/15 naechste Spur Entfernung/Hoehe, 16 Flak-Turm (U, + rechts), 17 Kurs U, 18 Nick U, 19 Roll U,
--  21 Zustand (0 sucht, 1 sucht die Vorgabe, 2 Ziel), 22 Ziel-Nummer (wechselt bei neuem Ziel), 23-25 eigenes Tempo
--  Ost/Nord/Hoch (m/s); Bool 1 Feuer frei, 2 Ziel
N=input.getNumber
B=input.getBool
S=output.setNumber
O=output.setBool
P=property.getNumber
m=math
pi2=m.pi*2
function cl(v,a,b) return m.max(a,m.min(b,v)) end
function wr(v) return (v+.5)%1-.5 end

on=false
T={}
tk=0
sy=0
gy=0
gp=0
ds=0
id=0
ab=0
VE=0
VN=0
VU=0

-- SCHREIBER v2 (in allen Waffen-Skripten gleich; Andre 04.10.: "der Log muss ALLES sagen, sonst ist es ein Ratespiel"):
-- je Tick eine Zeile mit dem, was das Skript sieht und entscheidet (Tick + Werte, leer = 0); alle LT Ticks ein Paket
-- an tools/waffen_logger.py. Versatz LO je Skript anders - zusammen hoechstens eine Anfrage je Tick (mehr stellt das
-- Spiel in eine Warteschlange). Kein Warten auf Antwort (mit 15 Schreibern an einem Port kamen die Antworten kaum an,
-- jeder wartete 2 s - der Log hatte nur 12 % der Zeit). Paketnummer s und Zahl verworfener Zeilen x (Paket laenger als
-- 'Schreiber Zeichen') gehen mit: der PC sieht jede Luecke. Der Bau-Schritt setzt LQ (Name), LT, LO.
-- LG(Kennbuchstabe, Werte-Tabelle, Anzahl) - ohne select/table.unpack, die gibt es in Stormworks nicht (04.10.)
-- Gesendet wird erst, wenn die Antwort aufs letzte Paket da ist (hoechstens 300 Ticks warten), fruehestens LT Ticks
-- danach: so staut sich im Spiel nie eine Warteschlange (04.10. 08:30: Log hinkte Minuten hinterher). w = wie viele
-- Ticks die Antwort aufs vorige Paket brauchte (-1 = keine).
LQ='x' LT=16 LO=0
LB={} LN=0 LS=0 LX=0 LC=0 LM=3000 LW=0 LR=0
LA=LO+1
function httpReply()
	LR=LW
	LW=0
end
function LG(g,t,n)
	if LP==0 then return end
	local z={g..LN}
	for i=1,n do
		local v=t[i]
		v=v==true and 1 or v or 0
		z[i+1]=v==0 and '' or string.format('%.5g',v)
	end
	local s=table.concat(z,',')
	LB[#LB+1]=s
	LC=LC+#s+1
	while LC>LM and #LB>1 do
		LC=LC-#LB[1]-1
		table.remove(LB,1)
		LX=LX+1
	end
end
function LF()
	if not LP then LP,LM=property.getNumber('Schreiber Port'),property.getNumber('Schreiber Zeichen') end
	LN=LN+1
	if LW>0 then
		LW=LW+1
		if LW>300 then
			LW=0
			LR=-1
		end
	end
	if LP>0 and LW==0 and LN>=LA then
		LS=LS+1
		async.httpGet(LP,'/w?q='..LQ..'&s='..LS..'&x='..LX..'&w='..LR..'&d='..table.concat(LB,';'))
		LB={}
		LC=0
		LX=0
		LW=1
		LA=LN+LT
	end
end

function onTick()
	if not ini then
		ini=1
		ats=P('AA Turm Richtung')
		ars=P('AA Radar Richtung')
		aes=P('AA Radar Hoehe Richtung')
		aon=P('AA Radar auf Turm')
		rz=P('AA Radar Null Grad')/360
		ahm=P('AA Mindesthoehe m')
		asu=P('AA Suchtempo')
		sal,sbe=P('Spur Alpha'),P('Spur Beta')
		vmx=P('Ziel Tempo max m/s')
		sh=P('AA Suchhoehe Grad')/360
		sst=P('AA Suchstufe Grad')/360
		sns=m.max(1,P('AA Suchstufen'))
		kr=P('Kompass Richtung')
		x0,z0,h0=N(8),N(32),N(24)
	end
	local ar=N(4)*ats
	local hd,nk,rl,agl,dr=N(12)*kr,N(16),-N(20),N(24),N(28)
	-- eigenes Tempo in der Welt (Ost, Nord, Hoch) aus der Positionsaenderung, geglaettet
	VE=VE+((N(8)-x0)*60-VE)*.25
	VN=VN+((N(32)-z0)*60-VN)*.25
	VU=VU+((agl-h0)*60-VU)*.25
	x0,z0,h0=N(8),N(32),agl
	-- v1.3: Feuer frei und Ziel-Vorgabe kommen vom Bildschirm-Chip (nicht mehr Hotkey 6)
	local cu=B(10)
	on=B(11)
	tk=tk+1

	-- Spuren altern; ohne Meldung seit 6 s fallen sie weg
	local da=false
	for k=#T,1,-1 do
		local q=T[k]
		q.a=q.a+1
		if q.a>360 then table.remove(T,k) elseif q==cq then da=true end
	end
	if not da then cq=nil end
	local RW,dq={}
	do
		for i=1,6 do
			if B(i) then
				local R,a0,e0=N(i*4-3),N(i*4-2),N(i*4-1)
				RW[3*i-2],RW[3*i-1],RW[3*i]=R,a0,e0
				-- Zaehlt das Radar die Winkel ab Strahl statt ab Sockel? Erkennt der Chip selbst (wie beim Swifter).
				if m.abs(dr)>.15 then ds=ds+((m.abs(wr(a0-dr))<m.abs(a0) and 0 or 1)-ds)*.1 end
				if ds>.5 then
					a0=a0+dr
					e0=e0+gp
				end
				local az,el=a0*ars+rz,e0*aes
				local th=(az+ar*aon)*pi2
				local ew=(el+nk*m.cos(th)-rl*m.sin(th))*pi2
				local ps=(hd+az+ar*aon)*pi2
				local p={R*m.cos(ew)*m.sin(ps)+N(8),R*m.cos(ew)*m.cos(ps)+N(32),R*m.sin(ew)+agl}
				-- passende Spur: naechste Vorhersage im Fangbereich (Tempo noch unbekannt: bis 200 m/s; sonst Kurven bis 2 g)
				local bk,bd=nil,1e9
				for k,q in ipairs(T) do
					if q.u~=tk then
						local s,d=q.a/60,0
						for j=1,3 do d=d+(p[j]-q.p[j]-q.v[j]*s)^2 end
						local g=q.b>=.5 and 30+10*s*s or 30+200*s
						if d<g*g and d<bd then bk,bd=q,d end
					end
				end
				if bk then
					local dt=bk.a/60
					if dt<.3 then
						-- dichte Meldungen (Strahl auf dem Objekt): Alpha-Beta-Filter
						for j=1,3 do
							local pr=bk.p[j]+bk.v[j]*dt
							local r=p[j]-pr
							p[j]=pr+sal*r
							bk.v[j]=bk.v[j]+sbe/dt*r
						end
					else
						-- seltene Meldungen: Tempo aus zwei Meldungen
						local f=bk.b>=.5 and .5 or 1
						for j=1,3 do bk.v[j]=bk.v[j]+((p[j]-bk.p[j])/dt-bk.v[j])*f end
					end
					local vv=m.sqrt(bk.v[1]^2+bk.v[2]^2+bk.v[3]^2)
					if vv>vmx then for j=1,3 do bk.v[j]=bk.v[j]*vmx/vv end end
					bk.b=bk.b+dt
				else
					if #T>=16 then
						local o
						for k,q in ipairs(T) do if q~=cq and (not o or q.a>T[o].a) then o=k end end
						table.remove(T,o)
					end
					bk={v={0,0,0},b=0}
					T[#T+1]=bk
				end
				bk.u=tk
				bk.p,bk.a,bk.h=p,0,p[3]
			end
		end
	end

	-- Spuren hochrechnen; Ziel (bq) = Luft-Spur am naechsten an der Vorgabe der Lagezentrale
	local bq,best,nr,nh=nil,1e9,1e9,0
	local cp=cu and {N(29),N(30),N(31)-agl}
	-- Hardlock: neue Zielnummer -> alte Spur loslassen
	local kn=cu and m.floor(N(25)+.5) or 0
	if kn~=kl then cq=nil kl=kn ab=0 end
	for k,q in ipairs(T) do
		local s=q.a/60
		q.E,q.N,q.U=q.p[1]+q.v[1]*s-N(8),q.p[2]+q.v[2]*s-N(32),q.p[3]+q.v[3]*s-agl
		local R=m.sqrt(q.E^2+q.N^2+q.U^2)
		local hg=q.h+q.v[3]*s
		q.R,q.g=R,hg
		if R<nr then nr,nh=R,hg end
		if cp and hg>ahm and q.a<120 then
			local d=m.sqrt((q.E-cp[1])^2+(q.N-cp[2])^2+(q.U-cp[3])^2)
			if d<40+.1*R and d<best then best,bq=d,q end
		end
	end
	if cq and cp and cq.a<120 and cq.g>ahm then
		local d=m.sqrt((cq.E-cp[1])^2+(cq.N-cp[2])^2+(cq.U-cp[3])^2)
		dq=d
		ab=d>60+.2*cq.R and ab+1 or 0
		if ab<60 then bq=cq end
	end
	if bq~=cq then id=id+1 end
	cq=bq

	-- Strahl: auf das Ziel halten, sonst auf die Vorgabe, sonst im Kreis suchen (jede Runde eine andere Hoehe)
	local lk=bq
	if not lk and cp then lk={E=cp[1],N=cp[2],U=cp[3]} end
	if lk then
		local yb=m.atan(lk.E,lk.N)/pi2-hd
		local th=yb*pi2
		gy=wr(yb-ar*aon-rz)*ars
		gp=cl((m.atan(lk.U,m.sqrt(lk.E^2+lk.N^2))/pi2-(nk*m.cos(th)-rl*m.sin(th)))*aes,-.125,.125)
		sy=gy
	else
		sy=wr(sy+asu/60)
		gy=sy
		gp=cl((sh+sst*(m.floor(tk*asu/60)%sns))*aes,-.125,.125)
	end
	S(1,gy) S(2,gp)
	if bq then
		S(3,bq.E) S(4,bq.N) S(5,bq.U) S(6,bq.v[1]-VE) S(7,bq.v[2]-VN) S(8,bq.v[3]-VU)
		S(9,bq.b) S(10,bq.R) S(11,bq.g) S(12,bq.a)
	else
		S(3,cp and cp[1] or 0) S(4,cp and cp[2] or 0) S(5,cp and cp[3] or 0)
	end
	S(13,#T) S(14,#T>0 and nr or 0) S(15,nh)
	S(16,ar) S(17,hd) S(18,nk) S(19,rl)
	S(21,bq and 2 or cp and 1 or 0) S(22,id)
	S(23,VE) S(24,VN) S(25,VU)
	O(1,on)
	O(2,bq~=nil)
	O(4,B(12))
	-- Schreiber: Vorgabe da, Feuer frei, Zielnummer, Vorgabe Ost/Nord/Hoch (relativ), Turm, Kurs, Nick, Roll, Radar-
	-- Drehung, 'ab Strahl'-Schaetzung, Spuren; Ziel Ost/Nord/Hoch, Tempo, Messdauer, Ticks ohne Meldung, Hoehe ueber dem
	-- Meer; bester Abstand einer Spur zur Vorgabe, Abstand der gehaltenen Spur, Loslass-Zaehler, Ziel-Nummer, Gimbal,
	-- Zustand, eigenes Tempo, Ortungen roh (je Platz 1-6 Entfernung, Seite, Hoehe). Alle 8 Ticks 'T': alle Spuren
	-- (Ost, Nord, Hoch, Ticks ohne Meldung, Messdauer)
	local c=cp or {}
	local V={cu,on,kn,c[1],c[2],c[3],ar,hd,nk,rl,dr,ds,#T,bq and bq.E,bq and bq.N,bq and bq.U,bq and bq.v[1],
		bq and bq.v[2],bq and bq.v[3],bq and bq.b,bq and bq.a,bq and bq.g,best<1e9 and best,dq,ab,id,gy,gp,
		bq and 2 or cp and 1 or 0,VE,VN,VU}
	for i=1,18 do V[32+i]=RW[i] end
	LG('',V,50)
	if LN%8==0 then
		local V={}
		for k,q in ipairs(T) do
			local j=5*k-5
			V[j+1],V[j+2],V[j+3],V[j+4],V[j+5]=q.E,q.N,q.U,q.a,q.b
		end
		LG('T',V,80)
	end
	LF()
end
