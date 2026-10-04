-- BILD v3.3 - Figet Marena, grosser Bildschirm am Steuersitz (Monitor 9x5), in drei Teilen - nur Anzeige, nichts zum
-- Antippen (Andre 03.10.: "muss simpler werden"):
-- links 3D-Radar (Schiff in der Mitte, Bug oben; Luftziele auf einem Strich, je hoeher desto laenger). Zoomt selbst:
--  die groesste Reichweite, bei der alle Ziele darin mindestens ZA Pixel auseinander liegen; Ziele dahinter stehen als
--  Pfeil am Rand (Richtung stimmt). Rotes Quadrat = darauf zielt gerade eine Waffe (Farbpunkte darunter: welche).
-- Mitte Kamera der gewaehlten Waffe (Video ueber die Video Switchboxes, der Chip zeichnet darueber).
-- Rechts Zielliste (Platz 1-5, L/S = Luft/See, km, Richtung ab Bug, Hoehe; rote Umrandung = wird beschossen, Farb-
--  striche = welche Waffe; leere Plaetze zeigen ihre Art: 1-2 Luft, 3-4 See, 5 Raketen), darunter gewaehlte Waffe,
--  Master Arm, BEDROHUNG.
-- Waffen: 1 Battle Cannon, 2 AC vorn (gegen Schiffe bis 8 km), 3 Flak L, 4 Flak R (gegen Luft bis 3 km). Farben: BC
--  orange, AC lila, Flak L hellblau, Flak R weiss.
-- v2.4: Waffen nehmen nur Ziele, die sich einmal bewegt haben (Lage Bool 15+k; ein Heli, der danach in der Luft steht,
--  bleibt Ziel; Dinge, die nie fuhren/flogen - Kraene, abgestellte Fahrzeuge im Hafen - nicht); die sind auf dem Radar
--  und in der Liste grau. v2.5: Kanonen erst ab 150 m (nicht ins eigene Umfeld), Flaks ohne Mindestabstand.
-- v2.7 (Andres Log: Flaks warteten ewig auf Ziele, die sie nicht finden oder nicht beschiessen durften): meldet eine
--  Flak 4 s lang 'sucht' oder 'zu flach' (Sperrprofil), ist dieses Ziel 20 s lang nicht fuer sie - die andere Flak darf
--  es nehmen, sie selbst nimmt ein anderes (oder keins).
-- v2.8 (Andres Log 04.10.: Flak R liess ihren Heli rechts fallen - 50-%-Regel - fuer einen Heli genau voraus, den
--  keine Flak erreicht; die hinteren Tuerme schiessen nach vorn erst ab ~30 Grad, quer uebers Schiff ab ~19 Grad):
--  BILD kennt die Sperrprofile beider Flaks (wie in den Flak-Chips, beim Bauen eingesetzt) und gibt einer Flak nur
--  Ziele, deren Hoehenwinkel von ihrem Turm aus darueber liegt. Luftziele, die keine Flak erreicht: dunkles Orange.
-- Zielwahl (alles selbst): jede Waffe nimmt das naechste passende Ziel und bleibt dabei, solange es passt; sie wechselt
--  nur, wenn ein anderes weniger als halb so weit weg ist. Zwei Kanonen nehmen verschiedene Ziele, wenn es mehrere
--  gibt; die beiden Flaks NIE dasselbe - bei nur einem Luftziel nimmt es nur die Flak auf seiner Seite; Flaks
--  bevorzugen ihre Seite.
-- Schiessen nur mit Master Arm (Schalter am Instrument Panel, ueber den Waffenwahl-Chip) - dann schiessen alle Waffen
--  selbst. v3.0 (Andre 04.10.: "erst schiessen, wenn Leertaste gedrueckt, finde ich nicht gut - ich habe ja Master
--  Arm"): die Wahl (H5 oder Monitor 2x3) bestimmt nur noch die Kamera. v3.1 (Andre): Leertaste mit gewaehlter Waffe
--  (und Master Arm) = diese schiesst einmal (Bool 12+w einen Tick lang, je Druck einmal); die Automatik laeuft weiter.
-- v3.2 (Kanonen vorn bekommen Chips): Reichweite je Waffe BC 6 km, AC 2 km, Flaks 3 km.
-- v3.3 (Andres Test: beide Kanonen bekamen ein Ziel achtern, das sie durch die Bruecke nie sahen): Kanonen nur Ziele
--  innerhalb GS (U ab Bug, beidseitig; beim Bauen aus ihren Sperrprofilen: BC ~105 Grad, AC ~145 Grad).
-- Eingang: Ausgang der Lagezentrale (Zahl 1-15 Ziele, 16-20 Kennungen, 31 Kurs; Bool 1-5 lebt, 6-10 Luft,
--  25 Bedrohung), ueberschrieben: Zahl 21/22 Flak L/R gepackt (Zustand*100000+Entfernung), 23 Waffenwahl-Monitor
--  (1 = keine Waffe, 2-5 = Waffe 1-4, solange getippt); Bool 26 Master Arm, 28 H5, 30 Leertaste, 31 jemand im Sitz;
--  Video: gewaehlte Kamera
-- Ausgang 'Bedienung': Zahl 2 Waffe, 3 deren Ziel (Platz), 4-6 dessen Ost/Nord/Hoehe; je Waffe w (1-4) 3+4w Kennung
--  des Ziels (0 = keins), 4+4w..6+4w Ost/Nord (m, relativ zum Schiff)/Hoehe ueber dem Meer; 23 Kurs, 24/25 Flak L/R
--  Zustand; Bool 1 Master Arm, 2-4 Video Switchboxes (2: BC statt AC vorn, 3: Flak L statt R, 4: vorn statt Flak),
--  4+w Feuer frei, 8+w Ziel da, 12+w Einzelschuss (ein Tick)
N=input.getNumber
B=input.getBool
S=output.setNumber
O=output.setBool
m=math
st=screen
pi2=m.pi*2
fm=string.format
function C(r,g,b,a) st.setColor(r,g,b,a or 255) end
function R(x,y,w,h) st.drawRectF(x,y,w,h) end
function T(x,y,s) st.drawText(x,y,s) end

RZ={200,300,500,700,1000,1500,2000,3000,4000,6000,8000,10000}
-- Sperrprofile Flak L/R (je 5 Grad Richtung ab Bug ein Zeichen: Grad + 48, aufgerundet) und Lage der Tuerme zum
-- Physik-Sensor (m: rechts (L gespiegelt), vorn, hoch; tiefster Rohrwinkel Grad) - der Bau-Schritt setzt die Werte ein
PL='0'
PR='0'
GS={0,0}
FX,FZ,FH,FE=0,0,0,0
ZA=10
rr=4000
WN={"BATTLE CANNON","AC VORN","FLAK L","FLAK R"}
WF={{255,140,0},{190,90,255},{0,210,255},{255,255,255}}
wf=0 hl=false tk=0 hd=0 thr=false wl=0 ma=false ab=false ws=0 fL=0 fR=0 al=0
A={0,0,0,0}
AI={0,0,0,0}
FS={0,0,0,0}
FA={0,0,0,0}
BL={{},{},{},{}}
w,h=288,160
Z={}
for k=1,5 do Z[k]={l=false,sh=0,id=0} end

-- erreicht Flak a (3/4) Ziel t? Hoehenwinkel von ihrem Turm ueber dem Sperrprofil in seiner Richtung (1 Grad Zugabe:
-- das Rohr steht wegen der Flugbahn hoeher als die Sichtlinie)
function frei(a,t)
	local h=hd*pi2
	local f=t.E*m.sin(h)+t.N*m.cos(h)-FZ
	local r=t.E*m.cos(h)-t.N*m.sin(h)-(a==3 and -FX or FX)
	local i=m.floor(m.atan(r,f)/pi2*72+.5)%72
	return m.atan(t.U-al-FH,m.sqrt(f*f+r*r))/pi2*360+1>m.max((string.byte(a==3 and PL or PR,i+1) or 48)-48,FE)
end
-- passt Ziel k fuer Waffe a? (lebt, Luft fuer Flak / See fuer Kanonen, in Reichweite, Flak erreicht es)
function passt(a,k)
	local t=Z[k]
	return k>0 and t.l and t.mv and (a>=3)==t.a and t.d<({6000,2000,3000,3000})[a] and (a>=3 or t.d>150)
		and (BL[a][t.id] or 0)<tk and (a<3 or frei(a,t)) and (a>2 or m.abs((t.b+.5)%1-.5)<GS[a])
end
-- Kosten: Entfernung, Flak auf der falschen Seite +800 m
function ko(a,k)
	local s=m.sin(Z[k].b*pi2)
	return Z[k].d+((a==3 and s>.2 or a==4 and s<-.2) and 800 or 0)
end
-- Zielwahl fuer zwei Waffen a, b einer Art; e: nie beide auf dasselbe (Flak)
function zw(a,b,e)
	local c={}
	for k=1,5 do if passt(a,k) or passt(b,k) then c[#c+1]=k end end
	for _,x in ipairs({a,b}) do
		-- behalten, solange es passt - ueber die Kennung (v2.2: ein Ziel kann den Platz wechseln)
		local k0=0
		for k=1,5 do if AI[x]>0 and Z[k].id==AI[x] then k0=k end end
		A[x]=passt(x,k0) and k0 or 0
	end
	if e and #c==1 and A[a]==0 and A[b]==0 then
		-- nur ein Luftziel: nur die Flak auf seiner Seite (darf die es gerade nicht: die andere)
		local x=m.sin(Z[c[1]].b*pi2)<0 and a or b
		if not passt(x,c[1]) then x=a+b-x end
		A[x]=c[1]
	end
	for _,x in ipairs({a,b}) do
		local o,bk,bv=A[a+b-x],0,1e9
		for _,k in ipairs(c) do
			local v=ko(x,k)+(k==o and 5000 or 0)
			if v<bv and not (e and k==o) and passt(x,k) then bk,bv=k,v end
		end
		-- wechseln nur, wenn das andere weniger als halb so weit weg ist - oder (Kanonen) beide auf demselben sind und
		-- es ein zweites Ziel gibt (dann verteilen)
		if A[x]==0 or bk>0 and bk~=A[x] and (Z[bk].d<.5*Z[A[x]].d or A[x]==o and bk~=o) then A[x]=bk end
		AI[x]=A[x]>0 and Z[A[x]].id or 0
	end
end

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
	tk=tk+1
	hd,al=N(31),N(32)
	thr=B(25)
	ma,ab=B(26),B(30)
	fL,fR=N(21),N(22)
	for k=1,5 do
		local t,q=Z[k],3*k
		local pk=N(q)
		t.E,t.N,t.U,t.id=N(q-2),N(q-1),pk%20000-100,N(15+k)
		t.l,t.a,t.mv=B(k),B(5+k),B(15+k)
		t.d=m.sqrt(t.E^2+t.N^2)
		t.b=(m.atan(t.E,t.N)/pi2-hd)%1
		t.sh=t.a and m.min(h*.55,2.5*m.sqrt(m.max(t.U,0))) or 0
		t.fr=t.a and (frei(3,t) or frei(4,t))
	end
	-- Radar-Zoom: groesste Reichweite, bei der alle Ziele darin mindestens ZA px auseinander liegen
	if tk%30==1 then
		local rx=m.floor(w/3)/2-4
		rr=RZ[1]
		for _,r in ipairs(RZ) do
			local ok=true
			for i=1,4 do
				for j=i+1,5 do
					local p,q=Z[i],Z[j]
					if p.l and q.l and p.d<r and q.d<r then
						local dx=(p.d*m.sin(p.b*pi2)-q.d*m.sin(q.b*pi2))/r*rx
						local dy=(p.d*m.cos(p.b*pi2)-q.d*m.cos(q.b*pi2))/r*rx*.42+p.sh-q.sh
						if dx*dx+dy*dy<ZA*ZA then ok=false end
					end
				end
			end
			if not ok then break end
			rr=r
		end
	end
	-- H5: naechste Waffe; Waffenwahl-Monitor: neuer Wunsch
	if B(28) and not hl then wf=(wf+1)%5 end
	hl=B(28)
	local wq=m.floor(N(23)+.5)
	if wq~=wl and wq>=1 and wq<=5 then wf=wq-1 end
	wl=wq
	-- Flak meldet 4 s lang 'sucht' / 'zu flach' fuer dasselbe Ziel: 20 s lang nicht fuer sie
	for w=3,4 do
		local z=m.floor((w==3 and fL or fR)/1e5)
		FS[w]=AI[w]>0 and AI[w]==FA[w] and (z==1 or z==4) and FS[w]+1 or 0
		FA[w]=AI[w]
		if FS[w]>240 then
			BL[w][AI[w]]=tk+1200
			FS[w],A[w],AI[w]=0,0,0
		end
	end
	zw(1,2,false)
	zw(3,4,true)
	ws=B(31) and wf or 0
	local sq=ab and not sl and ma and wf>0
	sl=ab
	S(2,wf)
	local lk=wf>0 and A[wf] or 0
	S(3,lk)
	for a=0,4 do
		local k=a>0 and A[a] or lk
		local t=Z[k]
		local q=a>0 and 3+4*a or 3
		if a>0 then
			S(q,AI[a])
			O(4+a,ma and k>0)
			O(8+a,k>0)
			O(12+a,sq and a==wf)
		end
		if t then S(q+1,t.E) S(q+2,t.N) S(q+3,t.U) else S(q+1,0) S(q+2,0) S(q+3,0) end
	end
	S(23,hd) S(24,m.floor(fL/1e5)) S(25,m.floor(fR/1e5))
	O(1,ma) O(2,wf==1) O(3,wf==3) O(4,wf<3)
	-- Schreiber: Wahl, gewaehlt+Sitz, Master Arm, Leertaste, Sitz, Zoom, Flak L/R Zustand und Entfernung, Ziel (Platz)
	-- und Kennung je Waffe, Zaehler 'sucht/zu flach' L/R, erreichbar fuer Flak L/R (Bits je Platz), passt je Waffe
	-- (Bits), Feuer frei (Bits), Kennungen der Plaetze, Sperre L/R je Platz (Ticks)
	local fm,pm,bl,fz={0,0},{0,0,0,0},{},0
	for a=1,4 do if ma and A[a]>0 then fz=fz+2^(a-1) end end
	for k=1,5 do
		local t=Z[k]
		for a=1,4 do if passt(a,k) then pm[a]=pm[a]+2^(k-1) end end
		if t.l and t.a then
			for a=3,4 do
				if frei(a,t) then fm[a-2]=fm[a-2]+2^(k-1) end
				bl[2*k+a-4]=m.max((BL[a][t.id] or 0)-tk,0)
			end
		end
	end
	local V={wf,ws,ma,ab,B(31),rr,m.floor(fL/1e5),fL%1e5,m.floor(fR/1e5),fR%1e5,A[1],A[2],A[3],A[4],AI[1],AI[2],AI[3],
		AI[4],FS[3],FS[4],fm[1],fm[2],pm[1],pm[2],pm[3],pm[4],fz,Z[1].id,Z[2].id,Z[3].id,Z[4].id,Z[5].id}
	for i=1,10 do V[32+i]=bl[i] end
	LG('',V,42)
	LF()
end

function onDraw()
	w,h=st.getWidth(),st.getHeight()
	local pw=m.floor(w/3)
	local bl=tk%30<15
	-- links: 3D-Radar
	C(0,12,8) R(0,0,pw,h)
	local cx,cy,rx,ty=pw/2,h*.7,pw/2-4,.42
	C(0,70,30)
	for f=.5,1,.5 do
		for i=0,23 do
			local a,b=i/24*pi2,(i+1)/24*pi2
			st.drawLine(cx+rx*f*m.sin(a),cy-rx*f*ty*m.cos(a),cx+rx*f*m.sin(b),cy-rx*f*ty*m.cos(b))
		end
	end
	st.drawLine(cx,cy,cx,cy-rx*ty)
	C(0,200,90) st.drawTriangleF(cx,cy-3,cx-2,cy+2,cx+2,cy+2)
	T(1,1,rr<1000 and fm("%dM",rr) or fm("%gKM",rr/1000))
	T(pw-21,1,fm("%03d",m.floor(hd%1*360+.5)%360))
	for k=1,5 do
		local t=Z[k]
		if t.l then
			local d=m.min(t.d/rr,1)
			local sx,sy=m.sin(t.b*pi2),m.cos(t.b*pi2)
			local gx,gy=cx+sx*d*rx,cy-sy*d*rx*ty
			local sh=t.sh
			if not t.mv then C(110,110,110) elseif t.fr then C(255,190,0) elseif t.a then C(150,85,25) else C(60,200,255) end
			if t.d>rr then
				-- hinter der Reichweite: Pfeil am Rand nach aussen
				sh=0
				st.drawTriangleF(gx+sx*4,gy-sy*2,gx-sy*2,gy-sx*2,gx+sy*2,gy+sx*2)
			else
				if sh>0 then st.drawLine(gx,gy,gx,gy-sh) R(gx-1,gy,2,1) end
				if t.a then st.drawTriangleF(gx,gy-sh-2,gx-2,gy-sh+2,gx+3,gy-sh+2) else R(gx-1,gy-1,3,3) end
			end
			T(gx+3,gy-sh-6,""..k)
			local zi=false
			for a=1,4 do
				if A[a]==k then
					zi=true
					C(WF[a][1],WF[a][2],WF[a][3]) R(gx-6+3*a,gy-sh+5,2,2)
				end
			end
			if zi then C(255,30,20) st.drawRect(gx-4,gy-sh-4,8,8) end
		end
	end
	-- Mitte: Kamera (kommt als Video), darueber Fadenkreuz und Waffen-Zustand
	local mx,my=pw+pw/2,h/2
	if wf==0 then
		C(0,0,0) R(pw,0,pw,h)
		C(150,150,150) T(pw+14,my-3,"KEINE WAFFE")
	else
		C(0,0,0,150) R(pw,0,pw,9)
		C(WF[wf][1],WF[wf][2],WF[wf][3]) T(pw+2,2,WN[wf])
		C(0,255,80)
		st.drawLine(mx-10,my,mx-3,my) st.drawLine(mx+4,my,mx+11,my)
		st.drawLine(mx,my-10,mx,my-3) st.drawLine(mx,my+4,mx,my+11)
		local s,k="",A[wf]
		if wf>=3 then
			local v=wf==3 and fL or fR
			local z=m.floor(v/1e5)
			s=({"WARTET","SUCHT","ZIEL","FEUER","ZU FLACH"})[z+1] or ""
			if z>=2 then s=s..fm(" %.1fKM",v%1e5/1000) end
		end
		C(0,0,0,150) R(pw,h-24,pw,24)
		C(255,255,255) T(pw+2,h-22,s)
		if k>0 then T(pw+2,h-15,fm("ZIEL %d %s %.1fKM",k,Z[k].a and "L" or "S",Z[k].d/1000)) end
		C(255,80,60)
		if not ma then T(pw+2,h-8,"MASTER ARM AUS") end
	end
	-- rechts: Zielliste, Waffe, Master Arm, Bedrohung
	local x0=2*pw
	C(0,12,8) R(x0,0,w-x0,h)
	C(120,200,140) T(x0+2,1,"# T   KM RI  HOCH")
	local rh=m.floor((h-58)/5)
	for k=1,5 do
		local t,y=Z[k],9+(k-1)*rh
		if t.l then
			if not t.mv then C(110,110,110) elseif t.fr then C(255,190,0) elseif t.a then C(150,85,25) else C(60,200,255) end
			T(x0+2,y+(rh-5)/2,fm("%d %s%5.1f %03d %4s",k,t.a and "L" or "S",m.min(t.d/1000,99.9),m.floor(t.b*360+.5)%360,t.a and m.floor(t.U+.5) or "-"))
			local zi=false
			for a=1,4 do
				if A[a]==k then
					zi=true
					C(WF[a][1],WF[a][2],WF[a][3]) R(w-11+2*a,y+2,1,rh-5)
				end
			end
			if zi then C(255,30,20) st.drawRect(x0+1,y,w-x0-3,rh-2) end
		else
			C(40,60,45) T(x0+2,y+(rh-5)/2,k..({" L"," L"," S"," S"," R"})[k])
		end
	end
	local wn=wf>0 and WN[wf] or "KEINE WAFFE"
	C(20,50,30) R(x0+2,h-48,w-x0-4,14)
	if wf>0 then C(WF[wf][1],WF[wf][2],WF[wf][3]) else C(150,150,150) end
	T(x0+(w-x0)/2-#wn*2.5,h-44,wn)
	if ma then C(170,20,10) else C(40,40,40) end
	R(x0+2,h-32,w-x0-4,14)
	C(255,255,255) T(x0+(w-x0)/2-(ma and 32 or 35),h-28,ma and "MASTER ARM AN" or "MASTER ARM AUS")
	if thr and bl then C(220,0,0) R(x0+2,h-16,w-x0-4,14) C(255,255,255) T(x0+(w-x0)/2-22,h-12,"BEDROHUNG") end
	C(0,90,40) st.drawLine(pw,0,pw,h) st.drawLine(x0,0,x0,h)
end
