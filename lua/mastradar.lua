-- MASTRADAR v2.2 - Figet Marena: ein Radar (Phalanx) am Mast im manuellen Modus. Ein Skript je Radar; der Bau-Schritt
-- setzt RN (Nummer 1-6), RS (Seitenvorzeichen: -1 = gespiegelt eingebaut), PB (Hoehe des Strahls beim Suchen, Grad)
-- und PH (Startphase der Drehung, U).
-- v2 (Andre 03.10.): Radar 1 sucht immer (kreist auf PB); Radar 2-6 halten je ein Ziel fest, das ihnen die
-- Lagezentrale gibt ('Lock', Bool 11): der Strahl zeigt auf die Vorgabe (Zahl 29/30) und das Radar meldet nur die
-- Ortung am naechsten an der Strahlmitte. Ohne Ziel suchen sie mit (kreisen auf PB). v2.2: Radar 6 (Platz fuer
-- Raketen) sucht bis dahin hoch mit, Radar 1 bleibt flach (vorher abwechselnd).
-- Kreisen mit 'Such Tempo' (U/s, hoechstens 0,28 - so schnell dreht der Schirm).
-- Frische Ortung: die 'Zeit seit Meldung' eines Platzes ist gefallen (neue Meldung) oder Entfernung/Winkel haben sich
-- geaendert (wie beim Radar boat) - und sie ist so klein wie die kleinste je gesehene (behaelt das Radar alte Ziele in
-- der Liste und sortiert um, zaehlen die nicht als neu). Beim Suchen kommen die frischen in eine Warteschlange, je
-- Tick geht die aelteste raus (aelter als 0,25 s: verworfen).
-- Winkel ab Strahl oder ab Sockel? Erkennt der Chip selbst: streicht der Strahl ueber ein Ziel, wandert eine Meldung
-- ab Strahl mit (um die Strahl-Drehung, andersherum), eine ab Sockel bleibt stehen; oder zeigt der Strahl mehr als
-- 0,12 U von vorn weg: Meldung nahe der Strahlrichtung = ab Sockel, nahe 0 = ab Strahl. Jede solche Beobachtung ist
-- eine Stimme, es gilt die Mehrheit. Alle 6 Radare sind gleich: was eines herausfand, meldet die Lagezentrale an alle
-- zurueck (Bool 9/10). Solange es keiner weiss, gehen keine Ortungen raus.
-- Bezug ist der Schirm selbst: der Chip rechnet mit, wie er dem Befehl folgt (0,03 rad je Tick wie im Spiel); beim
-- Suchen wird erst weitergedreht, wenn er den Befehl eingeholt hat.
-- Eingang: Radar Data (Ziele 1-7: Zahl 4i-3 Entfernung, 4i-2 Seitenwinkel, 4i-1 Hoehenwinkel, 4i Zeit seit Meldung;
--  Bool i gemeldet), ueberschrieben: Zahl 29/30 Lock-Richtung (U ab Bug + rechts / U gegen das Deck), Bool 9/10
--  Lagezentrale weiss 'ab Strahl' / 'ab Sockel', 11 Lock
-- Ausgang: Zahl 1/2 Strahl Seite/Hoehe (U, an 'Gimbal Input'), 3 Seite ab Bug (U, + rechts), 4 Hoehe gegen das Deck (U),
--  5 Entfernung (m), 6 Alter der Ortung (Ticks); Bool 1 Ortung gueltig, 2 selbst erkannt 'ab Strahl', 3 'ab Sockel'
N=input.getNumber
B=input.getBool
S=output.setNumber
O=output.setBool
P=property.getNumber
m=math
function wr(v) return (v+.5)%1-.5 end
function cl(v,a,b) return m.max(a,m.min(b,v)) end
RN=0 RS=1 PB=0 PH=0

tz=1e9
tk=0
cb,cs=0,0
dy,dp=0,0
sm=.03/m.pi/2
W={}
L={}

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
		asu=P('Such Tempo')
		sy=PH
		gy,gp=sy*RS,PB/360
		for i=1,7 do L[i]={t=-1,R=0,a=0,f=-9,fa=0,g=0,fR=0} end
	end
	tk=tk+1
	-- Schirm folgt dem letzten Befehl; er ist der Bezug (gb, pb)
	dy=wr(dy+cl(wr(gy-dy),-sm,sm))
	dp=dp+cl(gp-dp,-sm,sm)
	local gb,pb=dy,dp
	local lo=B(11)
	local la,le=N(29),N(30)
	if lo then
		gy,gp=wr(la*RS),cl(le,-.125,.125)
		sy=la
	else
		if m.abs(wr(gy-dy))<.01 then sy=wr(sy+asu/60) end
		gy,gp=sy*RS,PB/360
	end
	for k=#W,1,-1 do
		W[k][4]=W[k][4]+1
		if W[k][4]>15 then table.remove(W,k) end
	end
	local bw,bd=nil,1e9
	local om,nm,RW=0,0,{}
	for i=1,7 do
		local R,a0,e0,t0=N(4*i-3),N(4*i-2),N(4*i-1),N(4*i)
		local l=L[i]
		local ok=B(i) and R>0
		if ok then tz=m.min(tz,t0) om=om+2^(i-1) end
		if ok and t0<=tz+1e-4 and (t0<l.t or R~=l.R or a0~=l.a) then
			nm=nm+2^(i-1)
			RW[3*i-2],RW[3*i-1],RW[3*i]=R,a0,e0
			local v
			if m.abs(gb)>.12 then
				v=m.abs(wr(a0-gb))<m.abs(a0) and 0 or 1
			elseif tk-l.f<=3 and m.abs(wr(gb-l.g))>.003 and m.abs(R-l.fR)<5+.02*R then
				local da,dg=wr(a0-l.fa),wr(gb-l.g)
				v=m.abs(da+dg)<m.abs(da) and 1 or 0
			end
			if v==1 then cb=cb+1 elseif v==0 then cs=cs+1 end
			if cb+cs>0 then ds=cb>cs and 1 or 0 end
			l.f,l.fa,l.g,l.fR=tk,a0,gb,R
			local d=ds or (B(9) and 1) or (B(10) and 0)
			if d then
				if d>.5 then a0=a0+gb e0=e0+pb end
				local q={wr(a0*RS),e0,R,0}
				if lo then
					-- Lock: nur die Ortung am naechsten an der Strahlmitte
					local x=wr(q[1]-la)^2+(q[2]-le)^2
					if x<bd then bw,bd=q,x end
				else
					W[#W+1]=q
				end
			end
		end
		l.t,l.R,l.a=ok and t0 or -1,R,N(4*i-2)
	end
	if lo then W={bw} end
	S(1,gy) S(2,gp)
	local q=table.remove(W,1)
	if q then
		S(3,q[1]) S(4,q[2]) S(5,q[3]) S(6,q[4])
	end
	O(1,q~=nil) O(2,ds==1) O(3,ds==0)
	-- Schreiber: haelt?, ab Strahl (1 Sockel, 2 Strahl), Lock-Richtung, Befehl, Schirm (Modell), Stimmen, Ortungen
	-- da (Bits) / neu (Bits), Ausgabe, neue Ortungen roh (Entfernung, Seite, Hoehe je Platz 1-7)
	local V={lo,ds and ds+1,la,le,gy,gp,dy,dp,cb,cs,om,nm,q and q[1],q and q[2],q and q[3]}
	for i=1,21 do V[15+i]=RW[i] end
	LG('',V,36)
	LF()
end
