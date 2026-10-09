-- JET STEUERUNG v1.0 - Figet Marena (Andre 08.10.: "ferngesteuertes Flugzeug mit Maussteuerung, Kamera; eigener Sitz";
-- Bild auf den 3x3-Monitor vor dem zweiten Sitz im Steuerungsraum)
-- Zweiter Sitz (-5,16,-26): Maus (Blick) = Steuerknueppel - Blick rechts/links = Querlage, hoch/runter = Nick
--  ('Blick X/Y U' = voller Ausschlag, 'Totzone' innen nichts; Hotkey 6 = jetziger Blick ist die Mitte). Losgelassen
--  (Blick in der Mitte) haelt der Jet Fluegel gerade und Nick 'Trimm Grad' (Regler im Jet).
--  W/S Gas (bleibt stehen), A/D Seitenruder, Pfeil hoch/runter Zoom (Kamera unten), Leertaste Booster (nur mit
--  Triebwerk an), Hotkey 1 Triebwerk an/aus, 2 Licht, 3 Magnete (beim Laden an = festhalten), 4 Kamera vorn/unten.
-- Funk: Befehle auf 'Funk Befehle' (Senden), Flugdaten auf 'Funk Daten' (Empfang); Video-Empfaenger auf der Frequenz der
--  gewaehlten Kamera (vorn = 'Funk Befehle', unten = 'Funk Daten' - so stellt sie auch der Jet-Chip ein).
-- Bild: Kamerabild, darueber Mitte, Knueppel-Kreis, Horizont (Nick/Querlage), Tempo kn, Hoehe m, Kurs, Gas, Sprit,
--  Entfernung zum Schiff; "KEIN SIGNAL", wenn das Lebenszeichen-Echo 1 s steht; "NOTPROGRAMM", wenn der Jet ohne
--  Funk fliegt.
-- Eingang (Composite): Flugdaten vom Jet (Zahl 11-21, Bool 11-13, s. lua/jet.lua), ueberschrieben Zahl 1-4 Sitz Achse
--  1-4, 5/6 Blick X/Y, 7/8 Schiff x/z, 9 Funk-Signal; Bool 1-6 Sitz Hotkey 1-6, 7 Leertaste, 8 Sitz besetzt; Video
--  vom Video-Empfaenger
-- Ausgang: Befehle (Zahl 1-6, Bool 1-4 - s. lua/jet.lua) an das Sende-Funkgeraet; Zahl 10/11/12 Frequenz Senden /
--  Empfang / Video; Bool 10 Senden an, 11 Monitor an; Video (Kamerabild mit Anzeige) an den Monitor 3x3
N=input.getNumber
B=input.getBool
S=output.setNumber
O=output.setBool
P=property.getNumber
m=math
F=string.format
function cl(v,a,b) return m.max(a,m.min(b,v)) end
function tz(v) return m.abs(v)<dz and 0 or (v-dz*(v>0 and 1 or -1))/(1-dz) end
on=false
li=false
mg=true
ka=1
gs=0
zm=0
cx0,cy0=0,0
qc,nc=0,0
tk=0
el=-1
ez=0
T={}
for i=11,21 do T[i]=0 end
KM=0

-- SCHREIBER v2 (in allen Waffen-Skripten gleich; Andre 04.10.: "der Log muss ALLES sagen, sonst ist es ein Ratespiel"):
-- je Tick eine Zeile mit dem, was das Skript sieht und entscheidet (Tick + Werte, leer = 0); alle LT Ticks ein Paket
-- an tools/waffen_logger.py. Der Bau-Schritt setzt LQ (Name), LT, LO. LG(Kennbuchstabe, Werte-Tabelle, Anzahl).
-- Gesendet wird erst, wenn die Antwort aufs letzte Paket da ist (hoechstens 300 Ticks warten), fruehestens LT Ticks
-- danach. w = wie viele Ticks die Antwort aufs vorige Paket brauchte (-1 = keine).
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
		gx,gy,dz=P('Blick X U'),P('Blick Y U'),P('Totzone')
		bx,by=P('Blick X Richtung'),P('Blick Y Richtung')
		gt,zt=P('Gas Tempo')/60,P('Zoom Tempo')/60
		fb,fd=P('Funk Befehle'),P('Funk Daten')
	end
	tk=tk+1
	local sb=B(8)
	-- Maus-Knueppel
	if B(6) and not k6 then cx0,cy0=N(5),N(6) end
	k6=B(6)
	QX=cl((N(5)-cx0)*bx/gx,-1,1)
	QY=cl((N(6)-cy0)*by/gy,-1,1)
	qc,nc=0,0
	if sb then qc,nc=tz(QX),tz(QY) end
	-- Gas, Zoom, Tasten
	gs=cl(gs+N(2)*gt,0,1)
	zm=cl(zm+N(4)*zt,0,1)
	if B(1) and not k1 then on=not on end
	if B(2) and not k2 then li=not li end
	if B(3) and not k3 then mg=not mg end
	if B(4) and not k4 then ka=3-ka end
	k1,k2,k3,k4=B(1),B(2),B(3),B(4)
	-- Flugdaten; Echo des Lebenszeichens (1 s gleich = kein Signal)
	for i=11,21 do T[i]=N(i) end
	FS=B(12)
	if N(20)~=el then
		el=N(20)
		ez=0
	else
		ez=ez+1
	end
	KS=ez>60
	KM=m.sqrt((N(16)-N(7))^2+(N(17)-N(8))^2)/1000
	S(1,qc)
	S(2,nc)
	S(3,gs)
	S(4,sb and cl(N(1),-1,1) or 0)
	S(5,zm)
	S(6,tk)
	O(1,on)
	O(2,sb and on and B(7))
	O(3,li)
	O(4,mg)
	S(10,fb)
	S(11,fd)
	S(12,ka==1 and fb or fd)
	O(10,true)
	O(11,true)
	if tk%4==0 then
		LG('',{qc,nc,gs,N(1),zm,on,li,mg,ka,sb and B(7),T[11],T[12],T[13],T[14],T[15],T[18],T[21],FS,KS,N(9),KM,QX,QY},23)
	end
	LF()
end

function onDraw()
	local s=screen
	local w,h=s.getWidth(),s.getHeight()
	local c,r=w/2,h/2
	-- Horizont: Nick 1,5 px je Grad, um die Querlage gedreht
	local a=m.rad(T[15])
	local dy=T[14]*1.5
	local si,co=m.sin(a),m.cos(a)
	s.setColor(0,255,120,150)
	local hx,hy=c+si*dy,r+co*dy
	s.drawLine(hx-co*30,hy+si*30,hx+co*30,hy-si*30)
	-- Mitte und Knueppel
	s.setColor(255,255,255,180)
	s.drawLine(c-6,r,c-2,r)
	s.drawLine(c+2,r,c+6,r)
	s.drawLine(c,r-6,c,r-2)
	s.setColor(255,200,0)
	s.drawCircle(c+QX*30,r-QY*30,3)
	-- Werte
	s.setColor(0,0,0,150)
	s.drawRectF(0,0,w,7)
	s.drawRectF(0,h-14,w,14)
	s.setColor(255,255,255)
	s.drawText(1,1,F('%3dKN',m.floor(T[12]/.5144+.5)))
	s.drawText(w-31,1,F('%4dM',m.floor(T[11]+.5)))
	s.drawText(c-9,1,F('%03d',m.floor(T[13]*360+.5)%360))
	s.drawText(1,h-13,F('GAS%3d%%',m.floor(gs*100+.5)))
	s.drawText(w-41,h-13,F('SPRIT%3d',m.floor(T[18]+.5)))
	s.drawText(1,h-6,ka==1 and 'VORN' or F('UNTEN Z%d',m.floor(zm*10+.5)))
	s.drawText(w-31,h-6,F('%.1fKM',KM))
	if not on then
		s.setColor(255,120,0)
		s.drawText(c-30,h-24,'TRIEBWERK AUS')
	end
	if KS then
		s.setColor(255,0,0)
		s.drawText(c-27,r+10,'KEIN SIGNAL')
	elseif FS then
		s.setColor(255,0,0)
		s.drawText(c-27,r+10,'NOTPROGRAMM')
	end
end
