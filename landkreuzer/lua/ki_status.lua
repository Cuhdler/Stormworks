-- KI-STATUS v1.0 - KI Landkreuzer: Anzeige auf dem kleinen Monitor 2x3 rechts am Sitz (liegt flach auf seinem Gelenk).
-- Zeigt, was die Fahr-KI gerade macht und was ihre Sensoren melden - fuer den ersten Test im Spiel gedacht
-- (z. B. ob ein Laser 0 meldet = nicht verkabelt / kein Strom).
-- Eingang (Composite): derselbe wie KI_FAHREN (Zahl 1-3 Ort, 9-15 Laser, 16 Batterie; Bool 1 KI an, 2 Sitz besetzt,
--  4 Ziel, 6 Nach Hause, 10 Master Arm, 11 Schutzzone sperrt vom Klebe-Skript), ueberschrieben: Zahl 26 Zustand, 27 Zahl Wegpunkte, 28 Soll-
--  Tempo, 29 aktueller Wegpunkt, 30 Lenkbefehl, 31 Fahrbefehl (roh, + rechts / + vor), 32 Tempo vorwaerts (von
--  KI_FAHREN gerechnet); Bool 7 Fahrt
--  aktiv, 9 Revier
-- Video: Monitor 2x3 (64 x 96 Pixel, hochkant) und Helm des Steuersitzes (breit: dort nur eine Zeile unten)
-- Unten zwischen den Motor-Balken: N Nick (+ = Bug hoch), R Roll (+ = rechts tief), K Kurs (Grad, 0 Nord, 90 Ost) - so,
-- wie die Fahr-KI sie sieht (mit 'Nick/Roll/Kompass Richtung'). Zum Pruefen der Vorzeichen am Hang.
-- Rot 'L!' / 'R!' hinter dem Kurs: die KI hat gemerkt, dass die linke/rechte Seite falsch herum dreht, und es selbst
-- umgedreht (Bool 13/14) - dann im KI-Chip 'Rad Richtung links/rechts' dauerhaft umdrehen.
N=input.getNumber
B=input.getBool
st=screen
ZN={'AUS','HAND','WEGPUNKT','REVIER','AUSWEICHEN','ZURUECK','KAMPF','BATTERIE','GEFAHR','WARTET','LASER?'}
L={'VL','VM','VR','LI','RE','UN','HI'}
W={}
function onTick()
	if not ini then
		ini=1
		NR,RR,KR=property.getNumber('Nick Richtung'),property.getNumber('Roll Richtung'),property.getNumber('Kompass Richtung')
	end
	for i=1,32 do W[i]=N(i) end
	ni,ro,ku=W[5]*NR*360,W[6]*RR*360,(W[4]*KR*360)%360
	ul,ur=B(13),B(14)
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
			zi and '  ZIEL' or '')
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
	st.drawText(1,29,'BAT '..(b>0 and string.format('%.0f%%',b*100) or '?'))
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
	st.drawText(9,81,string.format('N%+.0f R%+.0f',ni,ro))
	st.drawText(9,88,string.format('K%03.0f',ku))
	st.setColor(255,60,60)
	st.drawText(34,88,(ul and 'L!' or '')..(ur and 'R!' or ''))
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
