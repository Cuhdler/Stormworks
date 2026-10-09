-- KI-STATUS v1.0 - KI Landkreuzer: Anzeige auf dem kleinen Monitor 2x3 rechts am Sitz (liegt flach auf seinem Gelenk).
-- Zeigt, was die Fahr-KI gerade macht und was ihre Sensoren melden - fuer den ersten Test im Spiel gedacht
-- (z. B. ob ein Laser 0 meldet = nicht verkabelt / kein Strom).
-- Eingang (Composite): derselbe wie KI_FAHREN (Zahl 1-3 Ort, 9-15 Laser, 16 Batterie; Bool 1 KI an, 2 Sitz besetzt,
--  4 Ziel, 6 Nach Hause, 10 Master Arm, 11 Schutzzone sperrt vom Klebe-Skript), ueberschrieben: Zahl 26 Zustand, 27 Zahl Wegpunkte, 28 Soll-
--  Tempo, 29 aktueller Wegpunkt, 30 Lenkbefehl, 31 Fahrbefehl (roh, + rechts / + vor), 32 Tempo vorwaerts (von
--  KI_FAHREN gerechnet); Bool 7 Fahrt
--  aktiv, 9 Revier
-- Schreiber v2 wie in den Waffen-Skripten (Messstelle 'ki', an tools/waffen_logger.py; Eigenschaft 'Schreiber Port',
-- 0 = aus): je Tick eine Zeile mit allem, was die Fahr-KI sieht und tut - fuer die Auswertung der ersten Fahrten.
-- Video: Monitor 2x3 (64 x 96 Pixel, hochkant) und Helm des Steuersitzes (breit: dort nur eine Zeile unten)
-- Unten zwischen den Motor-Balken: N Nick (+ = Bug hoch), R Roll (+ = rechts tief), K Kurs (Grad, 0 Nord, 90 Ost) - so,
-- wie die Fahr-KI sie sieht (mit 'Nick/Roll/Kompass Richtung'). Zum Pruefen der Vorzeichen am Hang.
-- Batterie-Restzeit: alle 10 s wird gemessen, wie viel Ladung weg ist (geglaettet); 'BAT 83% 45M' = bei diesem
-- Verbrauch noch etwa 45 Minuten bis leer (bis 'nach Hause' bei 'Heim Batterie' entsprechend weniger).
-- Rot 'L!' / 'R!' hinter dem Kurs: die KI hat gemerkt, dass die linke/rechte Seite falsch herum dreht, und es selbst
-- umgedreht (Bool 13/14) - dann im KI-Chip 'Rad Richtung links/rechts' dauerhaft umdrehen.
-- Vorzeichen-Pruefung aus der eigenen Fahrspur (alle 0,5 s, nur beim Fahren): K-Zeile rot = Kurs passt gespiegelt zur
-- Fahrtrichtung ('Kompass Richtung' falsch), N/R-Zeile rot = Bug geht bergauf runter ('Nick Richtung' falsch), rot
-- 'D!' = bei Lenkbefehl rechts dreht die Spur links (Motor-Kabel 'Links'/'Rechts' vertauscht). Zaehler je Probe +1
-- passt / -1 falsch (+-10), rot ab -5. Im Helm stehen dieselben Warnungen am Ende der Zeile (K! N! D! L! R!).
N=input.getNumber
B=input.getBool
st=screen
ZN={'AUS','HAND','WEGPUNKT','REVIER','AUSWEICHEN','ZURUECK','KAMPF','BATTERIE','GEFAHR','WARTET','LASER?'}
L={'VL','VM','VR','LI','RE','UN','HI'}
W={}
kz,nz,dd=0,0,0
function WI(a) return (a+180)%360-180 end
function V(z,g,f) return math.max(-10,math.min(10,z+(g and 1 or f and -1 or 0))) end
-- SCHREIBER v2 (in allen Waffen-Skripten gleich; Andre 04.10.: "der Log muss ALLES sagen, sonst ist es ein Ratespiel"):
-- je Tick eine Zeile mit dem, was das Skript sieht und entscheidet (Tick + Werte, leer = 0); alle LT Ticks ein Paket
-- an tools/waffen_logger.py. Der Bau-Schritt setzt LQ (Name), LT, LO. LG(Kennbuchstabe, Werte-Tabelle, Anzahl).
-- Gesendet wird erst, wenn die Antwort aufs letzte Paket da ist (hoechstens 300 Ticks warten), fruehestens LT Ticks
-- danach. w = wie viele Ticks die Antwort aufs vorige Paket brauchte (-1 = keine).
LQ='ki' LT=16 LO=10
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
		NR,RR,KR=property.getNumber('Nick Richtung'),property.getNumber('Roll Richtung'),property.getNumber('Kompass Richtung')
	end
	for i=1,32 do W[i]=N(i) end
	ni,ro,ku=W[5]*NR*360,W[6]*RR*360,(W[4]*KR*360)%360
	ul,ur=B(13),B(14)
	-- Vorzeichen aus der Spur: Fahrtrichtung c (aus dem Ort, bei Rueckwaerts-Befehl umgedreht) gegen Kurs, Steigung gegen
	-- Nick, Drehung der Spur gegen Lenkbefehl
	tk=(tk or 0)+1
	if tk%30==0 then
		local dx,dz,r=W[1]-(qx or W[1]),W[3]-(qz or W[3]),W[31]>0 and 1 or -1
		local s=(dx*dx+dz*dz)^.5
		if qx and s>.5 and s<30 and math.abs(W[31])>.2 then
			local c=math.deg(math.atan(r*dx,r*dz))%360
			kz=V(kz,math.abs(WI(ku-c))<30,math.abs(WI(-ku-c))<30)
			local g=math.deg(math.atan(r*(W[2]-qh),s))
			if math.abs(g)>3 then nz=V(nz,g*ni>0,g*ni<0) end
			if qc and math.abs(W[30])>.3 then
				local d=WI(c-qc)
				if math.abs(d)>1 then dd=V(dd,d*W[30]>0,d*W[30]<0) end
			end
			qc=c
		else qc=nil end
		qx,qz,qh=W[1],W[3],W[2]
	end
	-- Batterie-Verbrauch je Tick (alle 600 Ticks gemessen, geglaettet)
	if tk%600==0 then
		local b=W[16]
		if b0 and b>0 and b<=b0 then dv=dv and dv*.7+(b0-b)/600*.3 or (b0-b)/600 end
		b0=b
	end
	-- Schreiber (Port 0 = aus): Zustand, Ort x/z/Hoehe, Kurs Grad, Tempo ist/soll, Fahr-/Lenkbefehl roh, 7 Laser,
	-- Batterie, Wegpunkt/Zahl, Nick/Roll Grad, KI an, Waffen frei, Schutzzone, Sitz, nach Hause, umgelernt L/R
	LG('',{W[26],W[1],W[3],W[2],ku,W[32],W[28],W[31],W[30],W[9],W[10],W[11],W[12],W[13],W[14],W[15],W[16],W[29],W[27],
		ni,ro,ki,wa,sz,sb,hm,ul,ur},28)
	LF()
	ki,sb,zi,hm,fa,wa,rv,sz=B(1),B(2),B(4),B(6),B(7),B(10),B(9),B(11)
end
function f(v)
	if v<=0 then return '--' end
	if v>=1000 then return '>1k' end
	return string.format(v<10 and '%.1f' or '%.0f',v)
end
function onDraw()
	if not W[1] then return end
	local w,h=st.getWidth(),st.getHeight()
	local z=math.floor((W[26] or 0)+.5)
	if w>100 then
		-- Helm (Headset Video am Steuersitz, breiter Bildschirm): nur eine Zeile ganz unten, wie die Schiffs-Anzeige
		local b=W[16] or 0
		local t=string.format('KI %s  WP %d/%d  V %.0f/%.0f  %s%s%s',ki and (ZN[z+1] or z) or 'PAUSE',math.floor(W[29] or 0),
			math.floor(W[27] or 0),W[32] or 0,W[28] or 0,b>0 and string.format('BAT %.0f%%',b*100) or '',wa and '  WAFFEN FREI' or sz and '  SCHUTZZONE' or '',
			zi and '  ZIEL' or '')..(kz<-5 and ' K!' or '')..(nz<-5 and ' N!' or '')..(dd<-5 and ' D!' or '')..
			(ul and ' L!' or '')..(ur and ' R!' or '')
		st.setColor(0,0,0,160)
		st.drawRectF(0,h-8,#t*5+4,8)
		st.setColor(z==8 and 255 or 120,z==8 and 80 or 255,z==8 and 80 or 120)
		st.drawText(2,h-7,t)
		return
	end
	st.setColor(0,0,0)
	st.drawClear()
	local c=(z==8 or z==10) and {255,60,60} or z==6 and {255,160,0} or z==0 and {120,120,120} or {80,255,80}
	st.setColor(c[1],c[2],c[3])
	st.drawText(1,1,ZN[z+1] or ('Z'..z))
	st.setColor(200,200,200)
	st.drawText(1,8,(ki and 'KI AN' or 'KI PAUSE')..(sb and ' S' or ''))
	st.drawText(1,15,string.format('V %.1f/%.0f',W[32] or 0,W[28] or 0))
	st.drawText(1,22,'WP '..math.floor(W[29] or 0)..'/'..math.floor(W[27] or 0)..(rv and ' REV' or ''))
	local b=W[16] or 0
	st.drawText(1,29,'BAT '..(b>0 and string.format('%.0f%%',b*100) or '?')..(dv and dv>0 and b>0 and string.format(' %.0fM',b/dv/3600) or ''))
	st.setColor(wa and 255 or sz and 80 or 120,wa and 80 or sz and 160 or 120,wa and 80 or sz and 255 or 120)
	st.drawText(1,36,wa and 'WAFFEN FREI' or sz and 'SCHUTZZONE' or 'WAFFEN AUS')
	if zi then st.setColor(255,160,0) st.drawText(1,43,'ZIEL') end
	if hm then st.setColor(80,160,255) st.drawText(w-21,43,'HEIM') end
	st.setColor(160,160,255)
	for i=1,7 do
		local y=50+((i-1)%4)*7
		local x=(i<=4) and 1 or 33
		st.drawText(x,y,L[i]..' '..f(W[8+i] or 0))
	end
	st.setColor(200,200,120)
	if nz<-5 then st.setColor(255,60,60) end
	st.drawText(9,81,string.format('N%+.0f R%+.0f',ni,ro))
	st.setColor(200,200,120)
	if kz<-5 then st.setColor(255,60,60) end
	st.drawText(9,88,string.format('K%03.0f',ku))
	st.setColor(255,60,60)
	local t=(ul and 'L!' or '')..(ur and 'R!' or '')..(dd<-5 and 'D!' or '')
	st.drawText(math.min(34,w-7-#t*5),88,t)
	-- Motoren: zwei Balken (links/rechts, + = vorwaerts, wie die KI es meint - unabhaengig von der Einbau-Richtung)
	for k=0,1 do
		local v=math.max(-1,math.min(1,(W[31] or 0)+(k==0 and 1 or -1)*(W[30] or 0)))
		local x=k==0 and 2 or w-6
		st.setColor(60,60,60)
		st.drawRectF(x,h-16,4,15)
		st.setColor(v>=0 and 80 or 255,v>=0 and 200 or 100,80)
		local l=math.floor(math.abs(v)*7+.5)
		if v>=0 then st.drawRectF(x,h-9-l,4,l) else st.drawRectF(x,h-9,4,l) end
	end
end
