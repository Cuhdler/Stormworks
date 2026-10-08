-- KI KARTE v1.0 - KI Landkreuzer (08.10.2026): Touch-Karte im Cockpit (Monitor 3x3 = 96x96 Pixel oder 5x3 = 160x96).
-- Zeigt die Karte um den eigenen Ort (Norden oben), den Panzer als Pfeil in Fahrtrichtung, die Wegpunkte mit Nummer
-- (der aktuelle gelb), die Route (im Revier-Modus zurueck zum ersten), den Revier-Kreis um die Heimat (nur im
-- Revier-Modus), die Schutzzone um die Heimat (rot gestrichelt: Ziele darin beschiesst er nicht), das aktuelle Ziel
-- (Strich vom Panzer; Revier-Punkt lila Kreis; im Kampf der Feind als rotes Kreuz) und oben den Zustand der KI mit Tempo.
-- Bedienung (ein Finger):
--  - Karte kurz antippen = Wegpunkt an dieser Stelle (ki_fahren nimmt hoechstens 8; zaehlt beim Loslassen)
--  - Finger 1,5 s auf der Karte halten (der blaue Kreis waechst) = Freund-Punkt: dort ist eine weitere Schutzzone wie
--    um die Heimat (z. B. Hafen, Basis); dasselbe an einem Freund-Punkt = wieder weg. Hoechstens 4, blau gestrichelt.
--  - Knoepfe unten: 'Loeschen' (zweimal tippen binnen 3 s: alle Wegpunkte weg - einmal ist zu leicht aus Versehen),
--    '-' weiter weg, '+' naeher dran, 'Revier' (Revier-Modus an/aus; gruen = an)
-- Die Umrechnung Pixel -> Welt (map.screenToMap) passiert in onDraw (dort gehoeren die Karten-Befehle sicher hin);
-- der Tipp geht im naechsten Tick raus. Eingaenge nur in onTick (in onDraw: 'draw error').
-- Eingang (Composite) = Ausgang von ki_fahren (Zahl 3-28, 31/32, Bool 1-4), vom Chip ueberschrieben: Zahl 1/2 Touch
--  x/y (Monitor-Zahl 3/4; statt Antrieb L/R), 29/30 eigener Ort Ost/Nord (Physik-Sensor Zahl 1/3; statt der
--  Rohbefehle), Bool 32 Touch gedrueckt (Monitor-Bool 1). Die Monitor-Groesse kommt aus screen.getWidth/getHeight.
-- Ausgang: Zahl 23/24 Tipp Ost/Nord, 25 Befehl (1 Wegpunkte loeschen, 2 Revier-Modus um); Bool 3 Tipp-Puls,
--  5 Befehl-Puls (je 1 Tick; gleiche Kanaele wie die Eingaenge von ki_fahren); Zahl 1-8 Freund-Punkte Ost/Nord,
--  9 ihre Zahl (an das Klebe-Skript)
N=input.getNumber
B=input.getBool
S=output.setNumber
O=output.setBool
m=math
st=screen
pi2=m.pi*2
function cl(v,a,b) return m.max(a,m.min(b,v)) end
function C(r,g,b,a) st.setColor(r,g,b,a or 255) end
function M(a,b) return map.mapToScreen(x,z,zm,w,h,a,b) end
NA={'AUS','HAND','WEGPUNKT','REVIER','AUSWEICHEN','ZURUECK','KAMPF','BATTERIE','GEFAHR','WARTET'}
W={}
F={}
x,z,hd,zs,gx,gz,hx,hz,rv,nw,wi,vf=0,0,0,0,0,0,0,0,0,0,1,0
w,h,bh=96,96,13
tl,lz,pm,zm,zr=false,0,false,1,0

function onTick()
	if not ini then ini=1 zm,zr=cl(property.getNumber('Zoom Start'),.1,50),property.getNumber('Schutzzone m') end
	local tx,ty=N(1),N(2)
	zs,gx,gz,hx,hz,rv=m.floor(N(3)+.5),N(4),N(5),N(7),N(8),N(9)
	nw,wi=m.floor(cl(N(10),0,8)),m.floor(N(11)+.5)
	for i=1,8 do W[i]={N(10+2*i),N(11+2*i)} end
	x,z,hd,vf=N(29),N(30),N(31),N(32)
	pm=B(3)
	-- Beruehrung: nur auf die Flanke (Finger kommt auf)
	local t,c=B(32),0
	if t and not tl then
		if ty>=h-bh then
			-- Knopfleiste: 30 % Loeschen, 20 % -, 20 % +, 30 % Revier
			local f=tx/w
			if f<.3 then
				if lz>0 then c,lz=1,0 else lz=180 end
			elseif f<.5 then zm=m.min(zm*2,50)
			elseif f<.7 then zm=m.max(zm/2,.1)
			else c=2 end
		elseif ty>7 then
			tp,th={tx,ty},0
		end
	end
	-- Finger auf der Karte: beim Loslassen kurz = Wegpunkt, ab 1,5 s = Freund-Punkt
	if tp then
		if t then th=th+1 else
			if th<90 then tq=tp else fq=tp end
			tp=nil
		end
	end
	tl=t
	if lz>0 then lz=lz-1 end
	-- Tipp aus onDraw (schon in Weltkoordinaten) als 1-Tick-Puls weitergeben
	S(23,ta or 0) S(24,tb or 0) O(3,ta~=nil)
	ta=nil
	S(25,c) O(5,c>0)
	-- Freund-Punkt umschalten (aus onDraw, schon in Weltkoordinaten): einer in 150 m = weg, sonst neu
	if fa then
		local k
		for i,p in ipairs(F) do if (p[1]-fa)^2+(p[2]-fb)^2<22500 then k=i end end
		if k then table.remove(F,k) elseif #F<4 then F[#F+1]={fa,fb} end
		fa=nil
	end
	for i=1,4 do
		local p=F[i] or {0,0}
		S(2*i-1,p[1]) S(2*i,p[2])
	end
	S(9,#F)
end
-- gestrichelter Kreis
function DK(a,b,r)
	for i=0,r>0 and 23 or -1,2 do
		local p,q=i*pi2/24,(i+1)*pi2/24
		st.drawLine(a+r*m.cos(p),b+r*m.sin(p),a+r*m.cos(q),b+r*m.sin(q))
	end
end

function onDraw()
	w,h=st.getWidth(),st.getHeight()
	bh=m.max(12,m.floor(h/7))
	st.drawMap(x,z,zm)
	if tq then
		ta,tb=map.screenToMap(x,z,zm,w,h,tq[1],tq[2])
		tq=nil
	end
	if fq then
		fa,fb=map.screenToMap(x,z,zm,w,h,fq[1],fq[2])
		fq=nil
	end
	-- Revier-Kreis, Schutzzone (gestrichelt)
	local a,b=M(hx,hz)
	if pm then
		C(0,200,0)
		st.drawCircle(a,b,M(hx+rv,hz)-a)
	end
	local r=M(hx+zr,hz)-a
	C(255,60,60)
	DK(a,b,r)
	C(80,160,255)
	for _,p in ipairs(F) do
		local c,d=M(p[1],p[2])
		DK(c,d,r)
		st.drawText(c-2,d-2,'F')
	end
	if tp then st.drawCircle(tp[1],tp[2],2+th/9) end
	-- Route
	for i=1,nw do
		local j=i%nw+1
		if i<nw or pm and nw>2 then
			a,b=M(W[i][1],W[i][2])
			local c,d=M(W[j][1],W[j][2])
			C(0,150,255,i<nw and 255 or 110)
			st.drawLine(a,b,c,d)
		end
	end
	-- Strich zum aktuellen Ziel
	local px,py=M(x,z)
	a,b=M(gx,gz)
	if zs>1 and zs~=7 then
		C(255,220,0,150)
		st.drawLine(px,py,a,b)
		if zs==6 then
			C(255,0,0)
			st.drawLine(a-3,b-3,a+4,b+4)
			st.drawLine(a-3,b+3,a+4,b-4)
		elseif zs==3 or nw<1 then
			C(220,0,255)
			st.drawCircle(a,b,3)
		end
	end
	-- Wegpunkte mit Nummer (aktueller gelb)
	for i=1,nw do
		a,b=M(W[i][1],W[i][2])
		if i==wi then C(255,220,0) else C(0,200,255) end
		st.drawCircleF(a,b,2)
		st.drawText(a+3,b-6,tostring(i))
	end
	-- eigener Panzer: Pfeil in Fahrtrichtung (Bildschirm: x rechts = Ost, y unten = Sued)
	local s,c=m.sin(hd*pi2),m.cos(hd*pi2)
	C(255,255,255)
	st.drawTriangleF(px+6*s,py-6*c,px-3*s-3*c,py+3*c-3*s,px-3*s+3*c,py+3*c+3*s)
	-- Kopfzeile: Zustand, Tempo km/h, Wegpunkt
	C(0,0,0,180)
	st.drawRectF(0,0,w,7)
	C(255,255,255)
	st.drawText(1,1,(NA[zs+1] or '?')..' '..m.floor(m.abs(vf)*3.6+.5))
	if nw>0 then st.drawText(w-25,1,wi..'/'..nw) end
	-- Knoepfe
	local k,l={0,.3,.5,.7,1},{lz>0 and 'OK?' or w>130 and 'Loeschen' or 'Loe','-','+',w>130 and 'Revier' or 'Rev'}
	for i=1,4 do
		a=k[i]*w
		local bw=(k[i+1]-k[i])*w
		if i==1 then
			if lz>0 then C(200,0,0) else C(90,40,40) end
		elseif i==4 then
			if pm then C(0,130,0) else C(70,70,70) end
		else C(30,50,110) end
		st.drawRectF(a+1,h-bh,bw-2,bh)
		C(255,255,255)
		st.drawTextBox(a+1,h-bh,bw-2,bh,l[i],0,0)
	end
end
