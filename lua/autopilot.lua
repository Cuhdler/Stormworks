-- AUTOPILOT v1.2 - Figet Marena (Andre 08.10.: "Autopilot mit Kurs und Tempo halten, 2D-Karte der Welt, Wegpunkte auf
-- der Karte; Knopf 'Activate Autopilot' schaltet ihn an/aus, 'Reset' loescht die Route").
-- v1.1 (Andre 08.10.): kein Touch mehr - am Control Handle bewegt der Blick ein Kreuz auf der Karte, Leertaste = Wegpunkt
--  dazu, nochmal an derselben Stelle = weg, hoch/runter = Zoom; die Karte folgt nicht dem Schiff, solange jemand den Griff
--  haelt. Bug-Laser standardmaessig aus, Knopf 'Automatic anti kollision' schaltet ihn (und das Ausweichen) an/aus.
-- v1.2 (Andre: "Zoomen per hoch/runter geht nicht"; Log: Zoom-Stufe blieb 33 s am Griff bei 3): Zoom schon ab 0,2 auf
--  der Achse (Tastatur-Achsen steigen beim Druecken erst an, ein kurzer Tipp blieb wohl unter 0,5), erst unter 0,1
--  wieder scharf; zusaetzlich Hotkey 3/4 am Griff; Log hat alle 4 Griff-Achsen und Hotkey 3/4.
-- Der Chip sitzt zwischen Fahrersitz und Schiffsfuehrung: aus = das Sitz-Signal geht unveraendert durch (Umschalter im
-- Chip, nicht ueber dieses Skript); an = Achse 1 (A/D, Ruder) und Achse 2 (W/S, Fahrhebel) kommen von hier.
-- Kurs halten: Ruder = (Kursfehler - 'Kurs Daempfung s' * Drehrate) / 'Kurs Band Grad' + kleiner I-Anteil.
-- Tempo halten: PI-Regler gibt den Soll-Hebel (0..1), W/S-Pulse schieben den Fahrhebel der Schiffsfuehrung dorthin.
--  Den Hebel rechnet das Skript genau wie die Schiffsfuehrung mit (W/S mal 'Hebel Tempo', Hotkey 2 und Motoren aus =
--  null, Hotkey 1 schaltet die Motoren).
-- Beim Einschalten: Soll-Kurs = jetziger Kurs, Soll-Tempo = jetziges Tempo. A/D verstellt den Soll-Kurs (und verlaesst
--  die Route), W/S das Soll-Tempo. Hotkey 2 (Stopp) schaltet den Autopiloten aus.
-- Karte (Monitor 5x3): Nord oben. Griff los = Schiff in der Mitte. Am Griff: Kreuz folgt dem Blick ('Blick X/Y U' =
--  Bildrand, Hotkey 1 = jetziger Blick ist die Mitte), Blick knapp ueber den Rand schiebt die Karte ('Rand Tempo px/s'),
--  Hotkey 2 = zurueck aufs Schiff; Leertaste = Wegpunkt am Kreuz dazu bzw. weg; W/S oder Pfeil hoch/runter = Zoom
--  (auch Hotkey 3 naeher / 4 weiter).
--  Mit Wegpunkten faehrt der Autopilot sie der Reihe nach ab (erreicht = naeher als 'Wegpunkt Radius m', dann weg - nur
--  bei Autopilot an); nach dem letzten Kurs halten und mit 'Am Ziel stoppen' 1 anhalten. Neuer Wegpunkt = Route wieder
--  aufnehmen. Reset = alle Wegpunkte weg.
-- Anti-Kollision (Knopf, beim Laden aus): Laser am Bug schwenkt in 9 Schritten ueber +-'Laser Schwenk U' (je 'Laser
--  Ticks'), Hoehe: 'Laser Winkel Grad' ueber waagerecht, das Nicken gleicht der Pivot Y aus ('Laser Hoehe Richtung' -1:
--  Pivot Y plus kippt nach unten - so bei Andres Laser, Log 08.10.; der Laser sieht durchs Wasser bis zum Meeresboden).
--  Treffer in der Gasse vor dem Schiff (+-'Gasse halb m') naeher als 'Warnen ab m' bzw. Tempo * 'Warnen Vorlauf s' =
--  Hindernis: zur freieren Seite 'Ausweichen Grad' drehen (bleibt 'Ausweichen halten s' nach dem letzten Treffer) und
--  langsamer, ab 'Stopp ab m' Hebel auf null. Treffer tiefer als 'Wasser bis m' ueber dem Meer zaehlen nicht. Treffer =
--  rote Punkte auf der Karte (stehen sie nicht auf der Kueste: 'Laser Seite' umdrehen).
-- Eingang (Composite): Sitz (Zahl 1-6, Bool 1-6, 31, 32), ueberschrieben Zahl 7-12 Physik x, Hoehe, z, Nick, Kompass,
--  Tempo; 13/14 Griff Blick X/Y; 15 Laser-Entfernung; 16/17 Griff W/S, Pfeil hoch/runter; 18/19 Griff A/D, Pfeil
--  links/rechts (nur Log); Bool 10 Griff Leertaste, 11 Knopf Autopilot, 12 Reset, 13 Knopf Anti-Kollision, 14 Griff
--  besetzt, 15-18 Griff Hotkey 1-4
-- Ausgang: Zahl 1/2 Laser-Pivot X/Y, 3 Ruder (Achse 1), 4 Fahrhebel (Achse 2); Bool 1 Autopilot an (Umschalter),
--  2 Monitor an, 3 Laser an; Video an den Monitor 5x3
N=input.getNumber
B=input.getBool
S=output.setNumber
O=output.setBool
P=property.getNumber
m=math
F=string.format
pi2=2*m.pi
KN=.5144
function cl(v,a,b) return m.max(a,m.min(b,v)) end
function wr(v) return (v+180)%360-180 end
ap=false
md=0
kz=0
vz=0
hb=0
on=false
Ik=0
Iv=0
yr=0
W={}
Z={.5,1,2,5,10,20,50}
zi=3
D={}
H={}
for k=1,9 do D[k]=0 end
lk=1
lr=1
lc=0
ao=0
ah=0
X,Y,HD,V,MW,MH,WD,BL=0,0,0,0,160,96,0,false
MX,MY,CX,CY,cx0,cy0,zt,CD=0,0,80,48,0,0,0,0
ak=false
gb=false
tk=0

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
		kr=P('Kompass Richtung')
		kb=P('Kurs Band Grad')
		kd=P('Kurs Daempfung s')
		ki=P('Kurs I')/60
		kt=P('Kurs Tempo Grad/s')/60
		vt=P('Tempo Schritt kn/s')*KN/60
		vm=P('Tempo max kn')*KN
		vp=P('Tempo P')
		vi=P('Tempo I')/60
		ht=P('Hebel Tempo')/60
		hr=P('Rueckwaerts max')
		wrd=P('Wegpunkt Radius m')
		zs=P('Am Ziel stoppen')
		sw=P('Laser Schwenk U')
		sg=P('Laser Seite')
		dw=m.max(2,P('Laser Ticks'))
		lw=P('Warnen ab m')
		lv=P('Warnen Vorlauf s')
		ds=P('Stopp ab m')
		br=P('Gasse halb m')
		ag=P('Ausweichen Grad')
		aht=P('Ausweichen halten s')*60
		lz=P('Laser vor Physik m')
		ly=P('Laser ueber Physik m')
		wg=P('Wasser bis m')
		te=P('Laser Winkel Grad')/360
		pr=P('Laser Hoehe Richtung')
		gx=P('Blick X U')
		gy=P('Blick Y U')
		bx=P('Blick X Richtung')
		by=P('Blick Y Richtung')
		rt=P('Rand Tempo px/s')/60
	end
	tk=tk+1
	local a1,a2,h1,h2=N(1),N(2),B(1),B(2)
	local x,al,y,nk,v=N(7),N(8),N(9),N(10),N(12)
	local hd=(N(11)*kr)%1*360
	if tk>1 then yr=yr+(wr(hd-HD)*60-yr)*.1 end
	X,Y,HD,V=x,y,hd,v
	-- Motoren an/aus wie die Schiffsfuehrung (fuer den Hebel)
	if h1 and not k1 then on=not on end
	k1=h1
	-- Knoepfe
	if B(11) and not k2 then
		ap=not ap
		if ap then
			kz=hd
			vz=v
			Iv=cl(hb,0,1)
			Ik=0
			md=#W>0 and 1 or 0
		end
	end
	k2=B(11)
	if B(12) and not k3 then
		W={}
		md=0
	end
	k3=B(12)
	if h2 then ap=false end
	-- Knopf Anti-Kollision: Bug-Laser und Ausweichen an/aus
	if B(13) and not k5 then ak=not ak end
	k5=B(13)
	-- Griff: Kreuz folgt dem Blick, knapp ueber den Rand (0,9 bis 1,6) schiebt die Karte; Leertaste = Wegpunkt dazu/weg;
	-- hoch/runter oder Hotkey 3/4 = Zoom (gehalten alle 0,4 s); Hotkey 1 = Blick-Mitte; Hotkey 2 oder Griff los = Karte
	-- aufs Schiff
	gb=B(14)
	local z=Z[zi]
	if not gb or B(16) then MX,MY=x,y end
	if gb then
		if B(15) then cx0,cy0=N(13),N(14) end
		local u,q=(N(13)-cx0)*bx/gx,(N(14)-cy0)*by/gy
		local mp=map.screenToMap(MX,MY,z,MW,MH,MW/2+1,MH/2)-MX
		if m.abs(u)>.9 and m.abs(u)<1.6 then MX=MX+(u>0 and 1 or -1)*cl((m.abs(u)-.9)/.3,0,1)*rt*mp end
		if m.abs(q)>.9 and m.abs(q)<1.6 then MY=MY+(q>0 and 1 or -1)*cl((m.abs(q)-.9)/.3,0,1)*rt*mp end
		CX,CY=m.floor(MW/2+cl(u,-1,1)*(MW/2-1)+.5),m.floor(MH/2-cl(q,-1,1)*(MH/2-1)+.5)
		local wx,wy=map.screenToMap(MX,MY,z,MW,MH,CX,CY)
		CD=m.sqrt((wx-x)^2+(wy-y)^2)
		if B(10) and not k4 then
			local wt=0
			for i,p in ipairs(W) do
				local sx,sy=map.mapToScreen(MX,MY,z,MW,MH,p[1],p[2])
				if (sx-CX)^2+(sy-CY)^2<40 then wt=i end
			end
			if wt>0 then
				table.remove(W,wt)
			elseif #W<20 then
				W[#W+1]={wx,wy}
				md=1
			end
		end
		local g=N(16)+N(17)+(B(17) and 1 or 0)-(B(18) and 1 or 0)
		if m.abs(g)>.2 then
			if zt<=0 then
				zi=cl(zi+(g>0 and -1 or 1),1,#Z)
				zt=25
			end
			zt=zt-1
		elseif m.abs(g)<.1 then
			zt=0
		end
	end
	k4=B(10)
	-- Route
	local wb=0
	WD=0
	if #W>0 then
		local dx,dy=W[1][1]-x,W[1][2]-y
		WD=m.sqrt(dx*dx+dy*dy)
		wb=m.deg(m.atan(dx,dy))%360
		if WD<wrd and ap then
			table.remove(W,1)
			if #W==0 and md==1 then
				kz=wb
				if zs>0 then vz=0 end
			end
		end
	end
	if #W==0 then md=0 end
	if md==1 then kz=wb end
	if ap then
		if m.abs(a1)>.05 then
			md=0
			kz=(kz+a1*kt)%360
		end
		vz=cl(vz+a2*vt,0,vm)
	end
	-- Laser: Hoehe gegen das Nicken ausgleichen (Strahl 'Laser Winkel Grad' ueber waagerecht); Feld lk lesen (Pivot
	-- steht seit dw Ticks), naechstes Feld
	local py=cl((te-nk)*pr,-.125,.125)
	lc=lc+1
	local ld,lh,lf=0,0,lk
	if not ak then
		lc=0
		ah=0
		for k=1,9 do
			D[k]=0
			H[k]=nil
		end
	elseif lc>=dw then
		lc=0
		ld=N(15)
		local q,r=(hd/360+(lk-5)/4*sw*sg)*pi2,m.rad(hd)
		lh=al+ly+lz*m.sin(nk*pi2)+ld*m.sin((nk+py*pr)*pi2)
		D[lk]=0
		H[lk]=nil
		if ld>20 and ld<3990 and lh>wg then
			D[lk]=ld
			H[lk]={x+lz*m.sin(r)+ld*m.sin(q),y+lz*m.cos(r)+ld*m.cos(q),tk}
		end
		if lk+lr<1 or lk+lr>9 then lr=-lr end
		lk=lk+lr
	end
	-- Hindernis in der Gasse?
	local rg,dn,sl,sr=m.max(lw,v*lv),1e9,0,0
	for k=1,9 do
		local d,a=D[k],(k-5)/4*sw*sg*pi2
		if d>0 and d*m.cos(a)<rg and m.abs(d*m.sin(a))<br then dn=m.min(dn,d*m.cos(a)) end
		local f=d>0 and d or 4000
		if a<0 then sl=sl+f elseif a>0 then sr=sr+f end
	end
	BL=dn<1e9
	if BL then
		if ao==0 then ao=sr>=sl and ag or -ag end
		ah=aht
	elseif ah>0 then
		ah=ah-1
	else
		ao=0
	end
	-- Kurs halten
	local e,u1,u2=wr(kz+ao-hd),0,a2
	if ap then
		if m.abs(e)<10 then Ik=cl(Ik+e*ki,-.3,.3) end
		u1=cl((e-kd*yr)/kb+Ik,-1,1)
	else
		Ik=0
	end
	-- Tempo halten (bei Hindernis langsamer)
	local ve=vz
	if BL then ve=m.min(vz,m.max(0,(dn-ds)/lv)) end
	local e2=ve-v
	local L=cl(Iv+vp*e2,0,1)
	if ap then
		if (L>0 or e2>0) and (L<1 or e2<0) then Iv=cl(Iv+vi*e2,0,1) end
		u2=cl((L-hb)/ht,-1,1)
	end
	hb=cl(hb+u2*ht,-hr,1)
	if h2 or not on then hb=0 end
	-- Laser-Pivot fuers naechste Feld
	S(1,(lk-5)/4*sw)
	S(2,py)
	S(3,u1)
	S(4,u2)
	O(1,ap)
	O(2,true)
	O(3,ak)
	if tk%4==0 then
		LG('',{ap,md,hd,kz,ao,e,yr,u1,v/KN,vz/KN,ve/KN,L,hb,u2,x,y,#W,WD,wb,a1,a2,on,BL,dn<1e9 and dn,lf,ld,lh,nk,ak,gb,N(13),N(14),CX,CY,zi,N(18),N(16),N(19),N(17),B(17),B(18)},41)
	end
	LF()
end

function onDraw()
	local s=screen
	local w,h=s.getWidth(),s.getHeight()
	MW,MH=w,h
	local z=Z[zi]
	s.drawMap(MX,MY,z)
	local function M(p,q) return map.mapToScreen(MX,MY,z,w,h,p,q) end
	local c,r=M(X,Y)
	-- Laser-Treffer
	s.setColor(255,40,0)
	for k=1,9 do
		local q=H[k]
		if q then
			local px,py=M(q[1],q[2])
			s.drawRectF(px-1,py-1,3,3)
		end
	end
	-- Route
	local lx,ly=c,r
	for i,p in ipairs(W) do
		local px,py=M(p[1],p[2])
		s.setColor(255,200,0,140)
		s.drawLine(lx,ly,px,py)
		s.setColor(255,200,0)
		s.drawCircle(px,py,2)
		s.drawText(px+4,py-2,''..i)
		lx,ly=px,py
	end
	-- Soll-Kurs (gruen), Schiff (weiss)
	local a=m.rad(kz+ao)
	if ap then
		s.setColor(0,255,120,150)
		s.drawLine(c,r,c+m.sin(a)*40,r-m.cos(a)*40)
	end
	a=m.rad(HD)
	local si,co=m.sin(a),m.cos(a)
	s.setColor(255,255,255)
	s.drawTriangleF(c+si*6,r-co*6,c-si*3+co*3,r+co*3+si*3,c-si*3-co*3,r+co*3-si*3)
	-- Kreuz (Griff)
	if gb then
		s.setColor(255,255,0)
		s.drawLine(CX-5,CY,CX-1,CY)
		s.drawLine(CX+2,CY,CX+6,CY)
		s.drawLine(CX,CY-5,CX,CY-1)
		s.drawLine(CX,CY+2,CX,CY+6)
		s.drawText(1,h-12,F('X%.1fKM',CD/1000))
	end
	-- Anzeige
	s.setColor(0,0,0,170)
	s.drawRectF(0,0,57,#W>0 and 25 or 19)
	if ap then s.setColor(0,255,120) else s.setColor(255,90,90) end
	s.drawText(1,1,ap and (md==1 and 'AP ROUTE' or 'AP KURS') or 'AP AUS')
	s.setColor(255,255,255)
	s.drawText(1,7,F('S%03d %2dKN',m.floor(kz+.5)%360,m.floor(vz/KN+.5)))
	s.drawText(1,13,F('I%03d %2dKN',m.floor(HD+.5)%360,m.floor(V/KN+.5)))
	if #W>0 then s.drawText(1,19,F('WP%d %.1fKM',#W,WD/1000)) end
	if BL then
		s.setColor(255,0,0)
		s.drawText(1,h-6,'HINDERNIS')
	end
	s.setColor(0,0,0,170)
	s.drawRectF(w-32,0,32,7)
	if ak then s.setColor(0,255,120) else s.setColor(150,150,150) end
	s.drawText(w-31,1,ak and 'AK AN' or 'AK AUS')
	-- Massstab
	local pm,d=(M(MX+1000,MY)-w/2)/1000,100
	for _,q in ipairs({250,500,1000,2500,5000,10000,25000}) do
		if q*pm<=40 then d=q end
	end
	local L=d*pm
	s.drawLine(w-2-L,h-2,w-1,h-2)
	s.drawText(w-2-L,h-8,d<1000 and d..'M' or F('%gKM',d/1000))
end
