-- LAGE v3.4 - Figet Marena, Lagezentrale (Andre 03.10.): Radar 1 am Mast sucht (kreist), Radar 2-6 halten je ein
-- Ziel fest (Platz 1-5 = Radar 2-6). Hoechstens 5 Ziele, also passt immer alles auf den Bildschirm.
-- v2.2: Plaetze nach Art (Andre: 5 Schiffe gelockt, die Helis daneben wurden ignoriert): Platz 1-2 nur Luftziele (fuer
-- die Flaks), 3-4 nur Seeziele (fuer die Kanonen), 5 frei fuer Raketen (spaeter; bis dahin sucht Radar 6 mit).
-- Jede Ortung ohne passendes Ziel kommt erst in den Topf (Kandidaten, hoechstens 6, nicht angezeigt) und wird dort
-- verfolgt, bis ihre Art feststeht: Luft = hoeher als 'Luft sicher ab m' + 1 % der Entfernung, oder hoeher als 'Luft ab
-- m' + 0,5 % und waagerecht schneller als 15 m/s + 0,2 % (einmal Luft bleibt Luft); See = sonst, sobald das Tempo
-- gemessen ist (zweite Ortung). Dann bekommt sie einen freien Platz ihrer Art; sind beide belegt, den mit dem
-- entfernteren Ziel - aber nur, wenn sie naeher als 90 % davon ist (das verdraengte kommt in den Topf). Wird ein
-- Seeziel spaeter als Luftziel erkannt, zieht es auf einen Luft-Platz um (oder in den Topf).
-- v2.2: Das haltende Radar fuehrt NUR sein eigenes Ziel nach (Andre: Ziel 2 sprang herum und wechselte die Art - sein
-- Radar verlor das Ziel und meldete ein anderes im breiten Strahl, das daran haengen blieb); fremde Ortungen verwirft
-- es; sein Fangbereich ist eng (25 m + 1,5 % der Entfernung + hoechstens 60 m, Hoehe voll). Alle anderen Ortungen
-- (Such-Radare): zum naechsten Ziel oder Kandidaten im Fangbereich: 30 m + 1,2 % der Entfernung + was es seitdem
-- geflogen sein kann (unbekanntes Tempo: 120 m/s, hoechstens 250 m; sonst 30 m/s + 2 g, hoechstens 200 m); Hoehe halb,
-- bei Luftzielen und allem ueber 20 m voll. v2.6 (Andres Log: ein Platz sprang mit '175 m/s' zwischen einem stehenden
-- Ding und einem Heli hin und her): eine seltene Ortung, die das bekannte Tempo um mehr als 50 m/s aendern wuerde,
-- gehoert nicht zu diesem Ziel.
-- Filter wie die Flak (FLAKRADAR, im Spiel erprobt): dichte Ortungen per Alpha-Beta, seltene per Tempo aus zwei.
-- Ein Ziel faellt weg, wenn es 'Ziel vergessen s' lang nicht geortet wurde. Ortungen weiter als 'Radar Reichweite m'
-- zaehlen nicht. Doppelte Ziele (naeher als 40 m + 1 %) werden zusammengelegt. Jedes Ziel hat eine Kennung (bleibt
-- beim Umziehen; die Waffen merken so, wenn ein Platz ein anderes Ziel bekommt).
-- v2.4 (Andres Log 03.10.: zwei stehende Dinge im Hafen, 190 m / 15 m hoch und 226 m / 37 m hoch, hielten beide
-- Luft-Plaetze, die fliegenden Helis dahinter blieben draussen): 'bewegt' = ein Ziel ist seit seiner ersten Ortung
-- weiter als 15 m + 0,5 % der Entfernung gekommen (bleibt - ein Heli, der heranfliegt und dann in der Luft steht,
-- bleibt Ziel; ein Tempo aus verrauschten Ortungen reicht dafuer nicht). Stehende zaehlen beim Platz-Vergleich 5-mal so weit weg - ein bewegtes verdraengt sie; die Waffen nehmen
-- nur bewegte (Bildschirm-Chip). Luft erst nach zweiter Ortung (eine einzelne Ortung kann in der Hoehe weit daneben
-- liegen; so wurde ein stehendes Ding in 15 m Hoehe fuer immer 'Luft'), sofort nur ueber 'Luft immer ab m'.
-- Schneller als 45 m/s ist immer Luft (so schnell faehrt kein Schiff, auch nicht tief ueber dem Wasser).
-- v2.9 (Andres Log 04.10. 08:43 im Hafen, ohne Heli: zwei stehende Dinge 190 m / 300 m, 15 m hoch, hielten beide
-- Luft-Plaetze als 'Luft, bewegt' - im Topf hatte das Such-Radar zwei verschiedene Dinge einer Spur zugeordnet, Tempo
-- 51 und 64 m/s; das haltende Radar zielte dem falschen Tempo nach und fand das Ding nie wieder):
--  - Tempo zaehlt fuer 'Luft' erst nach 60 dichten Ortungen des haltenden Radars oder 3 seltenen mit passendem Tempo;
--    'bewegt' = seit der 30. dichten Ortung des haltenden Radars weiter als 15 m + 0,5 % gekommen
--  - haltendes Radar: Ortung nah am letzten Ort, aber weit von der Vorhersage -> Tempo war falsch, auf 0; 0,5 s ohne
--    Ortung -> Tempo 0 (das Radar zielt wieder auf den letzten Ort statt dem Tempo nach)
--  - dicht gemessen stehende Luftziele zaehlen beim Platz-Vergleich 20-mal so weit (sonst 5-mal): jeder Heli
--    verdraengt sie (bei See-Zielen nicht: dort tauschten stehende Schiffe sonst staendig die Plaetze)
-- v3.0 (Andres Test 04.10. 09:01): ein Heli schwebte 435 m links in 150 m Hoehe und bekam keine Flak (nie 'bewegt'):
--  Luftziele hoeher als 'Stehend Ziel ab m' ueber dem Meer sind auch stehend ein Ziel (Bool 15+k heisst jetzt 'Ziel'
--  fuer die Waffen). Stehende Dinge im Hafen wurden 'bewegt': beim Wechsel auf ein anderes Radar (die Radare sitzen
--  verschieden am Mast - dasselbe Ding liegt 10-14 m anders) und wenn das haltende Radar nach 2 s ohne Ortung ein
--  anderes Ding 36 m daneben fing. Jetzt: neuer Platz -> 'bewegt' neu messen; See-Ziele brauchen 40 m + 1 %;
--  Fangbereich des haltenden Radars waechst mit (Tempo + 5 m/s) * Zeit statt 15 m/s * Zeit.
-- v3.3 (Andres Test 04.10. ~14:25: ein sehr tief fliegender Eurofighter und ein Hubschrauber wurden als Schiff von BC
--  und AC beschossen - im Log kreisten sie 2-5 m ueber dem Meer, gemessenes Tempo sprang 0..80 m/s): Strecken-Tempo vx
--  je Platz (waagerechte Strecke in 2,5 s, abklingendes Maximum); schneller als 'See Tempo max m/s' ist kein Schiff -
--  nie Kanonen-Ziel, und ein Luftziel bleibt Luft, auch unter 10 m. Fahrende Schiffe im Log: 6-13 m/s.
-- v3.2 (Andres zwei Tests 04.10. ~14:05: BC und AC schossen auf Bodenziele - #10 1-1,6 km, #11 308 m, beide 14-16 m
--  ueber dem Meer, 'bewegt'): geglaettete Hoehe h (3 % je Ortung); ein Nicht-Luftziel hoeher als 'See Hoehe max m' ist
--  Land - nie Ziel fuer die Kanonen, beim Platz-Vergleich wie stehend (50-mal). Im Log lagen fahrende Schiffe bei -2 m
--  (Ausreisser bis +6), stehende Dinge im Wasser bei 3-6 m, die Bodenziele bei 14-16 m (nie unter 6).
-- v3.1 (Andres Test 04.10. am feindlichen Hafen: die See-Plaetze hielten zwei stehende Dinge achtern statt des
--  Patrouillenboots rechts voraus): Ortungen anderer Radare duerfen eine Platz-Spur mit eigenem Radar nur im engen
--  Fangbereich nachfuehren (vorher bis ~230 m - die Spur sprang auf ein Nachbar-Ding, der Sprung zaehlte als 'bewegt');
--  See-Ziele ausserhalb 'See Ziel bis Grad' ab Bug (dort erreicht keine Kanone sie) zaehlen beim Platz-Vergleich
--  20-mal so weit. Im Log: das Boot (bewegt, 760 m) verlor seinen Platz an ein stehendes Ding in 137 m (5 x 137 < 760),
--  flog dann als fernstes aus dem vollen Topf und kam nie wieder. Jetzt: nachweislich stehende See-/Boden-Dinge (15 s
--  vom haltenden Radar gehalten oder 3 passende seltene Ortungen, ohne Fortschritt) zaehlen im Topf 100-mal so weit;
--  fliegt eins aus dem vollen Topf, kommt sein Ort auf die Merkliste CL (24 Orte): Ortungen dort werden kein Kandidat
--  mehr. Ein noch unklares See-Ziel auf einem Platz verdraengt nur ein bewegtes. Der Topf tauscht nach
--  demselben Vergleich wie die Plaetze und vergisst erst nach doppelter 'Ziel vergessen s' (Such-Radar: alle 4 s).
--  Seltene Ortungen (See): Tempo passt nur bis (5 m + 2 % der Entfernung)/Abstand s + 3 m/s (vorher 15 m/s - Spruenge
--  zwischen Hafen-Dingen zaehlten als passend und als 'bewegt'); 'bewegt' ueber seltene Ortungen braucht zusaetzlich
--  10 m + 1 % der Entfernung Fortschritt (Ortungen streuen im Spiel bei 780 m um +-8 m); eine seltene Ortung setzt bei
--  See-Zielen die dichte Zaehlung zurueck (im Topf sprang eine Spur von einem Ding zum naechsten und galt dann als
--  'bewegt'). Ortungen an gemerkten Orten werden vor allem anderen verworfen.
-- v2.7: 'Luft' bleibt nur, solange das Ziel hoeher als 10 m ist (Andres Log: ein Luft-Platz sprang auf ein Ding auf
-- dem Wasser und blieb 'Luft' - die Flak wartete ewig darauf); jedes Ziel zieht auf einen Platz seiner Art um.
-- Ortungen naeher als 'Mindestabstand m' zaehlen nicht (Deck, eigener Heli; v2.5: 30 statt 100 m - Helis kommen naeher).
-- Bedrohung: Luftziel naeher als 'Bedrohung m', kommt mit mehr als 'Bedrohung Annaeherung' m/s naeher.
-- Eingang: Zahl 3i-2..3i Radar i (1-6): Seite (U ab Bug, + rechts), Hoehe (U gegen das Deck), Entfernung (m); Bool i
--  Ortung gueltig; 19 Physik x, 20 Physik z, 21 Physik Hoehe, 22 Kompass (U), 23 Nick-Neigung (U), 24 Quer-Neigung (U);
--  Bool 8-13 Radar i erkannte 'Winkel ab Strahl', 14-19 'ab Sockel'
-- Ausgang: Zahl 3k-2 / 3k-1 Ziel k (1-5) Ost/Nord relativ zu uns (m), 3k gepackt: Tempo/2 (m/s) * 20000 + Hoehe ueber
--  dem Meer + 100 (m); 15+k Kennung; 19+2k / 20+2k Richtung fuer Radar k+1 (U ab Bug / U gegen das Deck); 31 Kurs (U,
--  im Uhrzeigersinn); 32 eigene Hoehe (m); Bool k lebt, 5+k Luftziel, 10+k Radar k+1 haelt, 15+k Ziel fuer die
--  Waffen (bewegt, oder Luftziel hoeher als 'Stehend Ziel ab m'),
--  25 Bedrohung, 27 immer an, v3.4: 21-24 Takt (zaehlt je Tick 0..15, fuer die Mehrspieler-Hilfe im Bildschirm-Chip)
--  (Radare an), 28/29 ein Radar erkannte 'ab Strahl' / 'ab Sockel' (zurueck an alle Mast-Radare)
N=input.getNumber
B=input.getBool
S=output.setNumber
O=output.setBool
P=property.getNumber
m=math
pi2=m.pi*2
function cl(v,a,b) return m.max(a,m.min(b,v)) end
function wr(v) return (v+.5)%1-.5 end
-- Platz-Arten: 1 Luft, 2 See, 0 frei (Raketen spaeter)
KA={1,1,2,2,0}

T={}
for k=1,5 do T[k]={l=false} end
SH={}
CL={}
ci=0
VE,VN,VU=0,0,0
nid=0
X,Z,AL=0,0,0

function dist(t) return m.sqrt((t.p[1]-X)^2+(t.p[2]-Z)^2+(t.p[3]-AL)^2) end
-- Ortung p im Fangbereich von t? -> Abstand (sonst false). e: eng (haltendes Radar - es misst dicht; ein anderes
-- Objekt im Strahl, z. B. ein Schiff unter dem Heli, darf nicht daran haengen bleiben: Hoehe voll, kaum Zugabe)
function fang(t,p,R,e)
	local s,d,z=t.a/60,0,0
	local h=(e or t.air or p[3]>20 or t.p[3]>20) and 1 or .5
	for j=1,3 do
		local q=j<3 and 1 or h
		d=d+((p[j]-t.p[j]-t.v[j]*s)*q)^2
		z=z+((p[j]-t.p[j])*q)^2
	end
	d,z=m.sqrt(d),m.sqrt(z)
	-- haltendes Radar: nah am letzten Ort, weit von der Vorhersage -> Tempo war falsch
	if e and z<25+.015*R and d>z+10 then
		t.v,t.c,t.q,NV={0,0,0},0,nil,true
		return z
	end
	if s>=.3 and t.b>=.5 then
		local w=0
		for j=1,3 do w=w+((p[j]-t.p[j])/s-t.v[j])^2 end
		if w>2500 then return false end
	end
	return d<(e and 25+.015*R+m.min((m.sqrt(t.v[1]^2+t.v[2]^2+t.v[3]^2)+5)*s,60) or 30+.012*R+m.min(t.b<.5 and 120*s or 30*s+10*s*s,t.b<.5 and 250 or 200)) and d
end
function upd(t,p,e)
	local s=t.a/60
	if s<.3 then
		-- dichte Ortungen: Alpha-Beta
		for j=1,3 do
			local pr=t.p[j]+t.v[j]*s
			local r=p[j]-pr
			t.p[j]=pr+.1*r
			t.v[j]=t.v[j]+.005/m.max(s,1/60)*r
		end
		-- haltendes Radar (e): dichte Ortungen zaehlen (Tempo eingeschwungen nach 60), Bezugsort fuer 'bewegt' bei 30
		if e then
			t.c=(t.c or 0)+1
			if t.c==30 then t.q={t.p[1],t.p[2],t.p[3]} end
		end
	else
		-- seltene: Tempo aus zwei Ortungen; passt es zum bisherigen (Luft 15 m/s, See nach Streuung), zaehlt k (sonst 0)
		local f,w,g=t.b>=.5 and .5 or 1,0,t.air and 15 or (5+.02*dist(t))/s+3
		for j=1,3 do
			local n=(p[j]-t.p[j])/s
			w=w+(n-t.v[j])^2
			t.v[j]=t.v[j]+(n-t.v[j])*f
			t.p[j]=p[j]
		end
		t.k=t.b>=.5 and w<g*g and (t.k or 0)+1 or 0
		-- See: 'bewegt' nur aus durchgehend dichter Messung (eine Luecke kann ein Sprung auf ein Nachbar-Ding sein)
		if not t.air then t.c,t.q=0,nil end
	end
	t.b=t.b+m.max(s,1/60)
	t.h=t.h and t.h+(p[3]-t.h)*.03 or p[3]
	t.a=0
end
-- Art: 1 Luft (bleibt), 2 See, 0 noch unklar
function art(t)
	local U,R=t.p[3]+t.v[3]*t.a/60,dist(t)
	local zg=.01*R
	local b=t.b>=.5
	local vh=m.sqrt(t.v[1]^2+t.v[2]^2)
	local c=t.c or 0
	local cf=c>=60 or c==0 and (t.k or 0)>=1
	t.air=t.air and (U>10 or (t.vx or 0)>sv) or U>lim+zg or b and (U>ls+zg or cf and (U>la+zg/2 and vh>15+.002*R or U>5 and vh>45))
	if t.air then return 1 end
	return b and 2 or 0
end
-- Entfernung fuer den Platz-Vergleich: nicht bewegte 5-mal so weit, dicht gemessen stehende Luftziele 20-mal; ein
-- Kandidat mit bestaetigtem Tempo (seltene Ortungen passen zueinander), der seit der ersten Ortung im Schnitt schneller
-- als 4 m/s vorankam, zaehlt wie bewegt (Rauschen mittelt sich weg, falsche Zuordnung passt nicht zusammen)
function mv(t) return t.bw or (t.k or 0)>=1 and m.sqrt((t.p[1]-t.f[1])^2+(t.p[2]-t.f[2])^2)>4*m.max(t.b,1)+10+.01*dist(t) end
-- nachweislich stehend (v3.1, nur See/Boden): 300 dichte Ortungen des haltenden Radars (~15 s) oder 3 passende seltene,
-- ohne Fortschritt
function st(t) return not t.air and not mv(t) and ((t.c or 0)>=300 or (t.k or 0)>=2) end
-- Land (v3.2): kein Luftziel, geglaettet hoeher als 'See Hoehe max m'
function bo(t) return not t.air and (t.h or 0)>sh end
function ed(t)
	local f=mv(t) and not bo(t) and 1 or t.air and ((t.c or 0)>=60 and 20 or 5) or 50
	if not t.air and m.abs((m.atan(t.p[1]-X,t.p[2]-Z)/pi2-HD+.5)%1-.5)>sw then f=f*20 end
	return dist(t)*f
end
-- Platz der Art c fuer das Ziel q: frei, sonst der mit der groessten Vergleichs-Entfernung, wenn die von q < 90 % davon;
-- ein noch unklares See-Ziel (weder bewegt noch nachweislich stehend) wird noch gemessen - nur ein bewegtes verdraengt es
function platz(c,q)
	local f,fd,v=nil,ed(q)/.9,mv(q)
	for k=1,5 do
		local t=T[k]
		if KA[k]==c then
			if not t.l then return k end
			local d=ed(t)
			if c==2 and not v and not mv(t) and not st(t) then d=0 end
			if d>fd then f,fd=k,d end
		end
	end
	return f
end
-- in den Topf (hoechstens 6; voll: statt des mit der groessten Vergleichs-Entfernung, nachweislich stehende 100-mal,
-- wenn kleiner - vorher die fernste Entfernung: im Hafen flog das Boot in 700 m immer raus); ist das herausfallende
-- nachweislich stehend, kommt sein Ort auf die Merkliste
function kand(t)
	t.l=false
	if #SH<6 then SH[#SH+1]=t return end
	local f,fd=0,ed(t)*(st(t) and 100 or 1)
	for k,q in ipairs(SH) do
		local d=ed(q)*(st(q) and 100 or 1)
		if d>fd then f,fd=k,d end
	end
	local w=SH[f] or t
	if f>0 then SH[f]=t end
	if st(w) then
		ci=ci%24+1
		CL[ci]=w.p
	end
end
-- auf einen Platz der Art c (das verdraengte kommt in den Topf), sonst in den Topf
function setz(t,c)
	local f=platz(c,t)
	if not f then kand(t) return end
	if T[f].l then kand(T[f]) end
	if not t.id then
		nid=nid+1
		t.id=nid
	end
	t.l=true
	t.c,t.q=0,nil
	T[f]=t
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
	if not ini then
		ini=1
		kr=P('Kompass Richtung')
		vg=P('Ziel vergessen s')*60
		la,ls=P('Luft ab m'),P('Luft sicher ab m')
		rmx=P('Radar Reichweite m')
		mind=P('Mindestabstand m')
		lim=P('Luft immer ab m')
		sz=P('Stehend Ziel ab m')
		sw=P('See Ziel bis Grad')/360
		sh=P('See Hoehe max m')
		sv=P('See Tempo max m/s')
		bm,ba=P('Bedrohung m'),P('Bedrohung Annaeherung')
		x0,z0,h0=N(19),N(20),N(21)
	end
	local x,z,al=N(19),N(20),N(21)
	X,Z,AL=x,z,al
	local hd,nk,rl=N(22)*kr,N(23),-N(24)
	HD=hd
	VE=VE+((x-x0)*60-VE)*.25
	VN=VN+((z-z0)*60-VN)*.25
	VU=VU+((al-h0)*60-VU)*.25
	x0,z0,h0=x,z,al
	for k=1,5 do
		local t=T[k]
		if t.l then
			t.a=t.a+1
			if t.a==30 and KA[k]>0 then t.v,t.c,t.q={0,0,0},0,nil end
			-- Strecken-Tempo (v3.3): waagerechte Strecke je 2,5 s, abklingendes Maximum
			t.n5=(t.n5 or 0)+1
			if not t.r5 or t.n5>=150 then
				if t.r5 then t.vx=m.max(m.sqrt((t.p[1]-t.r5[1])^2+(t.p[2]-t.r5[2])^2)/2.5,(t.vx or 0)*.8) end
				t.r5,t.n5={t.p[1],t.p[2]},0
			end
			if t.a>vg then T[k]={l=false} end
		end
	end
	for k=#SH,1,-1 do
		SH[k].a=SH[k].a+1
		if SH[k].a>2*vg then table.remove(SH,k) end
	end
	-- Ortungen einarbeiten (in der Welt: Ost x, Nord z, Hoch); DC (Schreiber): was mit der Ortung von Radar i geschah
	-- (k = Platz k nachgefuehrt, -k = haltendes Radar: nicht im engen Fangbereich, 10+j = Kandidat j, 99 = neuer
	-- Kandidat, -8 = an einem gemerkten stehenden Ort, -9 = zu nah/zu weit)
	local DC={0,0,0,0,0,0}
	for i=1,6 do
		if B(i) then DC[i]=-9 end
		if B(i) and N(3*i)<rmx and N(3*i)>mind then
			local az,el,R=N(3*i-2),N(3*i-1),N(3*i)
			local th=az*pi2
			local ew=(el+nk*m.cos(th)-rl*m.sin(th))*pi2
			local ps=(hd+az)*pi2
			local p={x+R*m.cos(ew)*m.sin(ps),z+R*m.cos(ew)*m.cos(ps),al+R*m.sin(ew)}
			local h=T[i-1]
			if h and h.l and KA[i-1]>0 then
				-- haltendes Radar: nur sein eigenes Ziel
				NV=false
				if fang(h,p,R,true) then
					upd(h,p,true)
					DC[i]=NV and 29+i or i-1
				else
					DC[i]=1-i
				end
			else
				local bk,bd,bi=nil,1e9,99
				for _,q in pairs(CL) do
					if (q[1]-p[1])^2+(q[2]-p[2])^2+((q[3]-p[3])/2)^2<(15+.01*R)^2 then bi=-8 end
				end
				for k=1,bi>0 and 5 or 0 do
					local t=T[k]
					local d=t.l and fang(t,p,R)
					if d and KA[k]>0 and d>25+.015*R+m.min((m.sqrt(t.v[1]^2+t.v[2]^2+t.v[3]^2)+5)*t.a/60,60) then d=false end
					if d and d<bd then bk,bd,bi=t,d,k end
				end
				for j,q in ipairs(bi>0 and SH or {}) do
					local d=fang(q,p,R)
					if d and d<bd then bk,bd,bi=q,d,10+j end
				end
				if bk then upd(bk,p) elseif bi>0 then kand({p=p,f={p[1],p[2],p[3]},v={0,0,0},a=0,b=0,c=0}) end
				DC[i]=bi
			end
		end
	end
	-- bewegt (bleibt): seit der 30. dichten Ortung des haltenden Radars weiter als 15 m + 0,5 % gekommen
	for _,L in ipairs({T,SH}) do
		for _,t in pairs(L) do
			if t.q and not t.bw then
				local d=0
				for j=1,3 do d=d+((t.p[j]-t.q[j])*(j==3 and .5 or 1))^2 end
				t.bw=m.sqrt(d)>(t.air and 15+.005*dist(t) or 40+.01*dist(t))
			end
		end
	end
	-- Kandidaten mit bekannter Art auf einen Platz; Luftziel auf einem See-Platz zieht um
	for k=#SH,1,-1 do
		local q=SH[k]
		local c=art(q)
		if c>0 and platz(c,q) then
			table.remove(SH,k)
			setz(q,c)
		end
	end
	for k=1,5 do
		local t=T[k]
		local c=t.l and art(t) or 0
		if c>0 and KA[k]~=c then
			T[k]={l=false}
			setz(t,c)
		end
	end
	-- Doppelte zusammenlegen (das mit kuerzerer Messung faellt weg)
	for k=1,4 do
		for j=k+1,5 do
			local a,b=T[k],T[j]
			if a.l and b.l then
				local d,g=0,40+.01*dist(a)
				for q=1,3 do d=d+((a.p[q]+a.v[q]*a.a/60-b.p[q]-b.v[q]*b.a/60)*(q==3 and .5 or 1))^2 end
				if d<g*g then
					if a.b>=b.b then T[j]={l=false} else T[k]={l=false} end
				end
			end
		end
	end
	local thr=false
	for k=1,5 do
		local t=T[k]
		local q=3*k
		if t.l then
			local s=t.a/60
			local E,Nn,U=t.p[1]+t.v[1]*s-x,t.p[2]+t.v[2]*s-z,t.p[3]+t.v[3]*s
			local sp=t.b>=.5 and m.sqrt(t.v[1]^2+t.v[2]^2+t.v[3]^2) or 0
			local R=m.sqrt(E*E+Nn*Nn+(U-al)^2)
			-- Annaeherung: wie schnell der Abstand faellt (eigenes Tempo abgezogen)
			local cs=t.b>=.5 and -(E*(t.v[1]-VE)+Nn*(t.v[2]-VN)+(U-al)*(t.v[3]-VU))/m.max(R,1) or 0
			if t.air and R<bm and cs>ba then thr=true end
			S(q-2,E) S(q-1,Nn) S(q,m.floor(cl(sp,0,999)/2+.5)*20000+m.floor(cl(U,-99,19899)+100.5))
			S(15+k,t.id)
			-- Richtung fuer das haltende Radar (gegen das Deck)
			local az=wr(m.atan(E,Nn)/pi2-hd)
			local th=az*pi2
			S(19+2*k,az) S(20+2*k,m.atan(U-al,m.sqrt(E*E+Nn*Nn))/pi2-(nk*m.cos(th)-rl*m.sin(th)))
			O(k,true) O(5+k,t.air==true) O(10+k,true) O(15+k,t.bw==true and (t.air==true or not bo(t) and (t.vx or 1e9)<sv) or t.air==true and U>sz)
		else
			S(q-2,0) S(q-1,0) S(q,0) S(15+k,0)
			O(k,false) O(5+k,false) O(10+k,false) O(15+k,false)
		end
	end
	S(31,hd) S(32,al)
	O(25,thr)
	local fs,fb=false,false
	for i=1,6 do fs=fs or B(7+i) fb=fb or B(13+i) end
	O(27,true) O(28,fs) O(29,fb)
	TC=((TC or 0)+1)%16 O(21,TC%2>0) O(22,TC%4>1) O(23,TC%8>3) O(24,TC>7)
	-- Schreiber: jeden Tick 'D' (was mit den Ortungen geschah); alle 4 Ticks die ganze Lage: Schiff (Ort, Kurs, Nick,
	-- Roll, Tempo), Bedrohung, Zahl der Kandidaten; je Platz 1-5 Kennung, Ort relativ (Ost, Nord, Hoehe ueber dem Meer),
	-- Tempo, Ticks ohne Ortung, Messdauer s, Art (1 Luft + 2 bewegt + 4 dicht bestaetigt + 8 nachweislich stehend); je
	-- Kandidat 1-6 Ort, Ticks ohne Ortung, Art; zuletzt die Zahl der gemerkten stehenden Orte
	LG('D',DC,6)
	if LN%4==0 then
		local V={x,z,al,hd,nk,rl,VE,VN,VU,thr,#SH}
		for k,t in ipairs(T) do
			if t.l then
				local j=10*k+1
				V[j+1],V[j+2],V[j+3],V[j+4]=t.id,t.p[1]-x,t.p[2]-z,t.p[3]
				V[j+5],V[j+6],V[j+7]=t.v[1],t.v[2],t.v[3]
				V[j+8],V[j+9],V[j+10]=t.a,t.b,(t.air and 1 or 0)+(t.bw and 2 or 0)+((t.c or 0)>=60 and 4 or 0)+(st(t) and 8 or 0)+(bo(t) and 16 or 0)+((t.vx or 0)>=sv and 32 or 0)
			end
		end
		for k,q in ipairs(SH) do
			local j=56+5*k
			V[j+1],V[j+2],V[j+3],V[j+4],V[j+5]=q.p[1]-x,q.p[2]-z,q.p[3],q.a,(q.air and 1 or 0)+(q.bw and 2 or 0)+((q.c or 0)>=60 and 4 or 0)+(bo(q) and 16 or 0)
		end
		V[92]=#CL
		LG('',V,92)
	end
	LF()
end
