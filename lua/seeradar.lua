-- SEERADAR v2.1 - Figet Marena: Radar 6 (Phalanx am Mast, manueller Modus) kreist flach und zeigt auf dem Monitor
-- 3x3 ein 2D-Radar (Andre 06.10.: "nur Boden- und Seeziele, mit dem Strich und dem Verblassen"). Reine Anzeige.
-- Bild: Bug oben, eigenes Schiff in der Mitte; Seeziele blau, Bodenziele gruen; der Strich zeigt, wohin das Radar
-- gerade schaut; ein Ziel ist hell, wenn der Strich es gerade gefunden hat, und wird dunkler, bis er wieder drueber
-- geht; 'Vergessen s' (12) ohne Ortung -> weg.
-- v2.0 (Andre 06.10.): Reichweite automatisch in 4 Stufen 1 / 2,5 / 5 / 10 km - die groesste, bei der keine zwei
--  See- oder Bodenziele naeher als 'Abstand Pixel' beieinander liegen ("wichtig ist nur, dass sich nie Punkte zu nah
--  aneinander befinden"); Ziele dahinter als schwacher Punkt am Rand. Antippen waehlt das naechste See-/Bodenziel
--  (innerhalb 'Auswahl Pixel'; daneben tippen = abwaehlen): ist am grossen Bildschirm eine der vorderen Kanonen gewaehlt
--  (Bedienung Zahl 2: 1 BC, 2 AC), zielt und schiesst diese 'Geschuetz Zeit s' (20) lang darauf (der Chip-Teil
--  UEBERGABE setzt das Ziel in ihre Bedienung) - danach oder wenn das Ziel 1,5 Runden nicht mehr geortet wurde, wieder
--  Automatik; ohne Kanone gehen seine Koordinaten X (Ost) / Y (Nord) an zwei Zahl-Ausgaenge und den Monitor 1x2.
--  Rot umrandet = gewaehlt, orange = eine Kanone schiesst darauf. Radar-Ziele 1-5 (Kanaele 21-24 belegt).
--  v2.1 (Andre: "man muss auch Ziele am Rand anklicken koennen"): Ziele hinter der Reichweite stehen als Punkt auf dem
--  Rand und lassen sich dort antippen wie die anderen.
-- v1.1 (Andres Test 06.10.: "kopfueber; man muss klar erkennen, wohin das Schiff zeigt"): der Monitor liegt flach links
-- neben dem Sitz, sein Bild-Oben zeigt zum Sitz - 'Bild drehen' (Viertel im Uhrzeigersinn, 2 = halbe Drehung) dreht
-- alles, auch die Schrift (eigene Pixel-Schrift, drawText kann nicht drehen); durchscheinender Strich zum Bug, groesseres
-- Schiff.
-- v1.2: Schreiber zusaetzlich jede Sekunde die ersten 8 Kontakte (Ost/Nord relativ zum Schiff, Hoehe, Art) - Zeile 'K'
-- Radar 6 ist gespiegelt eingebaut: zaehlt Seite und Gimbal gespiegelt (RS -1, wie MASTRADAR); Winkel ab Sockel
-- (Andres Logs 03./04.10.). Der Schirm folgt dem Gimbal-Befehl mit 0,03 rad je Tick; gedreht wird erst weiter, wenn
-- er den Befehl eingeholt hat (Modell wie MASTRADAR).
-- Frische Ortung: 'Zeit seit Meldung' so klein wie die kleinste je gesehene und neu (gesunken, oder Entfernung/
-- Winkel anders) - das Radar behaelt alte Ziele in der Liste.
-- Ortung -> Welt (Ost, Nord, Hoehe ueber dem Meer) mit Kurs, Nick, Roll (wie die Lage). Zuordnung: naechster Kontakt
-- im Fangbereich 30 m + 2 % der Entfernung + 30 m/s seit der letzten Ortung (hoechstens 300 m), sonst neuer Kontakt;
-- die erste Ortung einer neuen Runde setzt den Kontakt dorthin, die weiteren glaetten.
-- Hoehe = Mittel der Ortungen (bis 50). Art: Luft = hoeher als 'Luft ab m' + 1 % der Entfernung oder schneller als
-- 'Luft Tempo m/s' (Tempo von Runde zu Runde, ab der dritten) - wird nicht gezeigt; Land = hoeher als 'See Hoehe max
-- m' + 0,1 % der Entfernung (Lage-Log: Schiffe um -2 m, Bodenziele 14-16 m); sonst See.
-- Eingang (Composite): Radar Data (Ziel i 1-5: Zahl 4i-3 Entfernung, 4i-2 Seite, 4i-1 Hoehe, 4i Zeit seit Meldung;
--  Bool i gemeldet), ueberschrieben: Zahl 21/22 Touch x/y (Pixel), 23 gewaehlte Waffe (Bedienung Zahl 2), 25-30 Physik
--  x, Hoehe, z, Nick, Roll, Kompass; Bool 32 Monitor beruehrt
-- Ausgang: Zahl 1/2 Gimbal Seite/Hoehe (U) an Radar 6; 3 Kanone, die gerade auf die Auswahl schiesst (0 keine, 1 BC,
--  2 AC), 4/5/6 Auswahl Ost/Nord relativ zum Schiff / Hoehe ueber dem Meer (m), 7 Ziel-Kennung (100 + Zaehler),
--  8/9 Koordinaten X (Ost) / Y (Nord) der letzten Auswahl ohne Kanone; Bool 1 Koordinaten da; Video an den Monitor 3x3
N=input.getNumber
B=input.getBool
S=output.setNumber
P=property.getNumber
m=math
pi2=2*m.pi
function wr(v) return (v+.5)%1-.5 end
function cl(v,a,b) return m.max(a,m.min(b,v)) end
RS=-1
tz=1e9
tk=0
sy,gy,dy=0,0,0
sm=.03/pi2
L={}
K={}
RW={1000,2500,5000,10000}
rr=10000
tp=false
X,Z,HD,SB=0,0,0,0
WD,HT=96,96
dw,dz,did=0,0,0
KX,KY,kv=0,0,false

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

-- Art eines Kontakts: 0 See, 1 Land, 2 Luft
function art(c)
	local d=m.sqrt((c.p[1]-X)^2+(c.p[2]-Z)^2)
	if c.h>la+.01*d or c.w>=2 and c.v>lv then return 2 end
	return c.h>sh+.001*d and 1 or 0
end
-- Ortung p (Welt) in Entfernung R einarbeiten; gibt 1 zurueck, wenn ein neuer Kontakt entstand
function ortung(p,R)
	local b,bd=nil,1e18
	for _,c in ipairs(K) do
		local g=30+.02*R+m.min(30*(tk-c.s)/60,300)
		local d=(c.p[1]-p[1])^2+(c.p[2]-p[2])^2
		if d<g*g and d<bd then b,bd=c,d end
	end
	if not b then
		if #K>=60 then
			local o=1
			for k,c in ipairs(K) do if c.s<K[o].s then o=k end end
			K[o].weg=true
			table.remove(K,o)
		end
		K[#K+1]={p={p[1],p[2]},h=p[3],n=1,s=tk,r={p[1],p[2]},q=tk,v=0,w=0}
		return 1
	end
	-- Tempo von Runde zu Runde (Bezug hoechstens alle 1 s neu)
	local dt=(tk-b.q)/60
	if dt>=1 then
		local v=m.sqrt((p[1]-b.r[1])^2+(p[2]-b.r[2])^2)/dt
		b.v=b.w>0 and b.v+(v-b.v)*.5 or v
		b.w=b.w+1
		b.r,b.q={p[1],p[2]},tk
	end
	-- erste Ortung einer neuen Runde: Kontakt springt hin (sonst hinkt er einem fahrenden Ziel nach und die naechste
	-- Ortung faellt aus dem Fangbereich), danach glaetten
	local f=tk-b.s>=60 and 1 or .3
	b.p[1]=b.p[1]+(p[1]-b.p[1])*f
	b.p[2]=b.p[2]+(p[2]-b.p[2])*f
	b.n=b.n+1
	b.h=b.h+(p[3]-b.h)/m.min(b.n,50)
	b.s=tk
	return 0
end

-- Entfernung eines Kontakts vom Schiff
function ab(c) return m.sqrt((c.p[1]-X)^2+(c.p[2]-Z)^2) end
-- Bildpunkt (rechts, oben vom Mittelpunkt, vor dem Drehen) eines Kontakts bei Reichweite rg und Halbmesser R Pixel
function bp(c,rg,R)
	local d=ab(c)
	local b=(m.atan(c.p[1]-X,c.p[2]-Z)/pi2-HD)*pi2
	return d/rg*R*m.sin(b),d/rg*R*m.cos(b),d
end

function onTick()
	if not ini then
		ini=1
		asu=P('Such Tempo')
		pb=P('Strahl Hoehe Grad')/360
		vg=P('Vergessen s')*60
		mind,rmax=P('Mindestabstand m'),P('Reichweite max m')
		sh,la,lv=P('See Hoehe max m'),P('Luft ab m'),P('Luft Tempo m/s')
		kr,ru=P('Kompass Richtung'),P('Radar ueber Physik m')
		zp,ap,gz=P('Abstand Pixel'),P('Auswahl Pixel'),P('Geschuetz Zeit s')*60
		Q=m.floor(P('Bild drehen')+.5)%4
		per=60/m.max(asu,.01)
		for i=1,5 do L[i]={t=-1,R=0,a=0} end
	end
	tk=tk+1
	-- Schirm folgt dem letzten Befehl; weiterdrehen, wenn er ihn eingeholt hat
	dy=wr(dy+cl(wr(gy-dy),-sm,sm))
	if m.abs(wr(gy-dy))<.01 then sy=wr(sy+asu/60) end
	gy=sy*RS
	S(1,gy)
	S(2,pb)
	SB=wr(dy*RS)
	local x,al,z=N(25),N(26),N(27)
	local nk,rl,hd=N(28),-N(29),N(30)*kr
	X,Z,HD=x,z,hd
	local fr,nn=0,0
	for i=1,5 do
		local R,a0,e0,t0=N(4*i-3),N(4*i-2),N(4*i-1),N(4*i)
		local l=L[i]
		local ok=B(i) and R>0
		if ok then tz=m.min(tz,t0) end
		if ok and t0<=tz+1e-4 and (t0<l.t or R~=l.R or a0~=l.a) and R>mind and R<rmax then
			local az=wr(a0*RS)
			local th=az*pi2
			local ew=(e0+nk*m.cos(th)-rl*m.sin(th))*pi2
			local ps=(hd+az)*pi2
			fr=fr+1
			nn=nn+ortung({x+R*m.cos(ew)*m.sin(ps),z+R*m.cos(ew)*m.cos(ps),al+ru+R*m.sin(ew)},R)
		end
		l.t,l.R,l.a=ok and t0 or -1,R,a0
	end
	for k=#K,1,-1 do
		if tk-K[k].s>vg then
			K[k].weg=true
			table.remove(K,k)
		end
	end
	-- Zeichnen-Liste fuer onDraw (dort keine Eingaenge lesen)
	local A={0,0,0}
	for _,c in ipairs(K) do
		c.a=art(c)
		A[c.a+1]=A[c.a+1]+1
	end
	local R=m.min(WD,HT)/2-1
	-- Reichweite (jede Sekunde): groesste Stufe, bei der alle See-/Bodenziele darin mindestens zp Pixel auseinander liegen
	if tk%60==1 then
		rr=RW[1]
		for _,r in ipairs(RW) do
			local ok,g=true,(zp*r/R)^2
			for i=1,#K-1 do
				local p=K[i]
				if p.a<2 and ab(p)<r then
					for j=i+1,#K do
						local q=K[j]
						if q.a<2 and ab(q)<r and (p.p[1]-q.p[1])^2+(p.p[2]-q.p[2])^2<g then ok=false end
					end
				end
			end
			if not ok then break end
			rr=r
		end
	end
	-- Antippen: naechstes See-/Bodenziel waehlen; vordere Kanone gewaehlt -> sie schiesst gz Ticks darauf, sonst
	-- Koordinaten ausgeben
	local t=B(32)
	if t and not tp then
		local dx,dy=N(21)-WD/2,HT/2-N(22)
		for _=1,Q do dx,dy=-dy,dx end
		local b,bd=nil,ap*ap
		for _,c in ipairs(K) do
			local x,y,d=bp(c,rr,R)
			if d>rr then x,y=x*rr/d,y*rr/d end
			if c.a<2 and (x-dx)^2+(y-dy)^2<bd then b,bd=c,(x-dx)^2+(y-dy)^2 end
		end
		sel,dw=b,0
		if b then
			local wp=m.floor(N(23)+.5)
			if wp==1 or wp==2 then
				dw,dz,did=wp,gz,did+1
			else
				KX,KY,kv=b.p[1],b.p[2],true
			end
		end
	end
	tp=t
	if sel and sel.weg then sel=nil end
	if dw>0 then
		dz=dz-1
		if dz<=0 or not sel or tk-sel.s>1.5*per then dw=0 end
	end
	S(3,dw)
	if sel then S(4,sel.p[1]-X) S(5,sel.p[2]-Z) S(6,sel.h) end
	S(7,100+did) S(8,KX) S(9,KY)
	output.setBool(1,kv)
	-- Schreiber: Strahl (ab Bug), Befehl, Ortungen frisch / neue Kontakte, Kontakte See/Land/Luft, Reichweite,
	-- Kurs, Strahl-Modell eingeholt?
	LG('',{SB,gy,fr,nn,A[1],A[2],A[3],rr,hd,m.abs(wr(gy-dy))<.01,dw,dz/60,KX,KY,sel and ab(sel)},15)
	if tk%60==0 then
		local V={}
		for k=1,m.min(#K,8) do
			local c=K[k]
			V[4*k-3],V[4*k-2],V[4*k-1],V[4*k]=c.p[1]-X,c.p[2]-Z,c.h,c.a+1
		end
		LG('K',V,#V)
	end
	LF()
end

-- Pixel-Schrift 3x5 (Zeile fuer Zeile, 1 = Punkt) fuer die Reichweite, damit sie sich mit dem Bild dreht
FT={["0"]="111101101101111",["1"]="010110010010111",["2"]="111001111100111",["5"]="111100111001111",
	["."]="000000000000010",K="101101110101101",M="101111111101101"}
function onDraw()
	local s=screen
	local w,h=s.getWidth(),s.getHeight()
	local cx,cy=w/2,h/2
	local r=m.min(w,h)/2-1
	local rg=rr
	WD,HT=w,h
	-- Punkt (rechts, oben) vom Mittelpunkt aus -> Bildschirm, um Q Viertel im Uhrzeigersinn gedreht
	local function pt(dx,dy)
		for _=1,Q or 0 do dx,dy=dy,-dx end
		return cx+dx,cy-dy
	end
	local function li(x1,y1,x2,y2)
		local a,b=pt(x1,y1)
		local c,d=pt(x2,y2)
		s.drawLine(a,b,c,d)
	end
	s.setColor(0,0,0)
	s.drawClear()
	s.setColor(0,45,25)
	s.drawCircle(cx,cy,r)
	s.drawCircle(cx,cy,r/2)
	-- durchscheinender Strich zum Bug
	s.setColor(255,255,255,45)
	li(0,0,0,r)
	-- Radar-Strich mit zwei schwaecheren Nachzieh-Strichen
	for j=2,0,-1 do
		local b=(SB-j*.015)*pi2
		local f=1-j*.35
		s.setColor(0,170*f,90*f)
		li(0,0,r*m.sin(b),r*m.cos(b))
	end
	for _,c in ipairs(K) do
		if c.a and c.a<2 then
			local lx,ly,d=bp(c,rg,r)
			local f=cl(1-(tk-c.s)/per,.2,1)
			if c.a==1 then s.setColor(40*f,230*f,60*f) else s.setColor(40*f,130*f,255*f) end
			-- dahinter: auf dem Rand (schwaecher)
			if d>rg then
				lx,ly,f=lx*rg/d,ly*rg/d,f*.6
				if c.a==1 then s.setColor(40*f,230*f,60*f) else s.setColor(40*f,130*f,255*f) end
			end
			local x,y=pt(lx,ly)
			s.drawRectF(x-1,y-1,2,2)
			if c==sel then
				if dw>0 then s.setColor(255,140,0) else s.setColor(255,40,40) end
				s.drawRect(x-4,y-4,7,7)
			end
		end
	end
	-- eigenes Schiff: Dreieck, Spitze zum Bug
	s.setColor(255,255,255)
	local a,b=pt(0,5)
	local c,d=pt(-3,-3)
	local e,f=pt(3,-3)
	s.drawTriangleF(a,b,c,d,e,f)
	-- Reichweite oben links (in Bild-Richtung)
	s.setColor(150,150,150)
	local t=string.format('%gKM',rg/1000)
	for k=1,#t do
		local g=FT[string.sub(t,k,k)]
		for i=1,15 do
			if string.sub(g,i,i)=='1' then
				local x,y=pt(-r+(k-1)*4+(i-1)%3,r-m.floor((i-1)/3))
				s.drawRectF(x,y,1,1)
			end
		end
	end
end
