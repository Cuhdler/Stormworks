-- JET v1.0 - small Jet (Andre 08.10.: "ferngesteuertes Flugzeug mit Maussteuerung vom Schiff, mit Kamera")
-- Der Jet startet senkrecht (Nase +y) mit den Boostern. Physik-Sensor (0,3,-18) ist rueckwaerts und kopfueber
--  eingebaut - die Kipp-Werte haengen nur an den Achsen: Nick = -Kippung lokal z, Querlage (rechts runter +) =
--  -Kippung lokal x; Kurs = Kompass + 0,5 U.
-- Befehle (Funk vom Schiff): Zahl 1 Quer (-1..1), 2 Nick (-1..1), 3 Gas (0..1), 4 Seitenruder (-1..1), 5 Zoom (0..1),
--  6 Lebenszeichen (zaehlt je Tick hoch); Bool 1 Triebwerk an, 2 Booster, 3 Licht, 4 Magnete
-- Regler: Soll-Querlage = Quer * 'Querlage max Grad'; Soll-Nick = Nick * 'Nick max Grad' + 'Trimm Grad' + 'Kurve Nick'
--  je Grad Querlage. Ruder = (Soll - Ist - Daempfung * Drehrate) / Band, mal ('Tempo Bezug m/s' / Tempo)^2 (0,3..2,5).
--  Elevons: links = Hoehe + Quer, rechts = Hoehe - Quer ('Hoehe/Quer/Seite Richtung' -1, wenn verkehrt).
-- Funk weg ('Funk weg s' kein neues Lebenszeichen): Notprogramm - Fluegel gerade, 'Notnick Grad', Gas 'Notgas'.
-- Start: nach dem Zuenden der Booster 'Start s' lang Soll-Nick 'Start Nick Grad' (dann normal).
-- Eingang (Composite): Befehle (s. o.), ueberschrieben Zahl 20-26 Physik x, Hoehe, z, Tempo, Kippung lokal z, lokal x,
--  Kompass; 27 Tank (Liter)
-- Ausgang: Zahl 1/2 Ruder links/rechts, 3 Seitenruder, 4 Gas, 5 Kamera-Bildwinkel (unten), 6/7 Funk-Frequenz Befehle
--  (Empfang + Kamera vorn) / Daten (Senden + Kamera unten); Bool 1 Verdichter, 2 Booster, 3 Licht, 4 Magnete, 5 Senden
--  Flugdaten (dasselbe Composite an das Sende-Funkgeraet): Zahl 11 Hoehe m, 12 Tempo m/s, 13 Kurs U, 14 Nick Grad,
--  15 Querlage Grad, 16/17 x/z, 18 Sprit %, 19 Gas, 20 Lebenszeichen-Echo, 21 Steigen m/s; Bool 11 Triebwerk an,
--  12 Notprogramm, 13 Magnete an
N=input.getNumber
B=input.getBool
S=output.setNumber
O=output.setBool
P=property.getNumber
m=math
function cl(v,a,b) return m.max(a,m.min(b,v)) end
hl=-1
hz=0
tk=0
t0=-1e9
ka=0
pr,rr,vs=0,0,0
sm=0

function onTick()
	if not ini then
		ini=1
		qm,nm,tr,kn=P('Querlage max Grad'),P('Nick max Grad'),P('Trimm Grad'),P('Kurve Nick')
		bq,dq,bn,dn=P('Quer Band Grad'),P('Quer Daempfung s'),P('Nick Band Grad'),P('Nick Daempfung s')
		vr,kr=P('Tempo Bezug m/s'),P('Kompass Richtung')
		sh,sq,ss=P('Hoehe Richtung'),P('Quer Richtung'),P('Seite Richtung')
		fw,nn,ng=P('Funk weg s')*60,P('Notnick Grad'),P('Notgas')
		sz,sn=P('Start s')*60,P('Start Nick Grad')
		fb,fd=P('Funk Befehle'),P('Funk Daten')
	end
	tk=tk+1
	local al,v=N(21),N(23)
	local th,ph=-N(24)*360,-N(25)*360
	local hd=((N(26)+.5)*kr)%1
	-- Drehraten (Grad/s) und Steigen, geglaettet
	if tk>1 then
		pr=pr+((th-ta)*60-pr)*.2
		rr=rr+((ph-pa)*60-rr)*.2
		vs=vs+((al-aa)*60-vs)*.1
	end
	ta,pa,aa=th,ph,al
	-- Lebenszeichen
	if N(6)~=hl then
		hl=N(6)
		hz=0
	else
		hz=hz+1
	end
	local fs=hz>fw
	local qc,nc,gs,on=cl(N(1),-1,1),cl(N(2),-1,1),cl(N(3),0,1),B(1)
	if fs then qc,nc,gs,on=0,(nn-tr)/nm,ng,true end
	if B(2) and not k2 and not fs then t0=tk end
	k2=B(2)
	-- Soll-Lage
	local qt=qc*qm
	local nt=nc*nm+tr+kn*m.abs(ph)
	if tk-t0<sz then nt=sn end
	-- Ruder
	local k=cl((vr/m.max(v,1))^2,.3,2.5)
	local a=cl(((qt-ph)-dq*rr)/bq*k,-1,1)
	local e=cl(((nt-th)-dn*pr)/bn*k,-1,1)
	S(1,cl(e*sh+a*sq,-1,1))
	S(2,cl(e*sh-a*sq,-1,1))
	S(3,cl(N(4)*ss,-1,1)*(fs and 0 or 1))
	S(4,on and gs or 0)
	S(5,1-cl(N(5),0,.95))
	S(6,fb)
	S(7,fd)
	O(1,on)
	O(2,B(2) and not fs)
	O(3,B(3))
	O(4,B(4) and not fs)
	O(5,true)
	-- Flugdaten
	ka=m.max(ka,N(27))
	S(11,al)
	S(12,v)
	S(13,hd)
	S(14,th)
	S(15,ph)
	S(16,N(20))
	S(17,N(22))
	S(18,ka>0 and N(27)/ka*100 or 0)
	S(19,on and gs or 0)
	S(20,hl)
	S(21,vs)
	O(11,on)
	O(12,fs)
	O(13,B(4) and not fs)
end
