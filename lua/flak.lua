-- FLAK v2.3 - Figet Marena, Feuerleitung eines Flak-Turms hinten (2 Heavy Autocannons, Fragmentation mit Zeitzuender).
-- Umbau von FLAK v14 (Swifter, im Spiel erprobt): das Ziel kommt von FLAKRADAR (Stellung und Tempo, hochgerechnet).
-- Vorhalt: dorthin zielen, wo das Ziel nach der Flugzeit der Geschosse ist (Flugbahn mit Luftwiderstand und
--  Schwerkraft, Tick fuer Tick wie im Spiel); die Geschosse bekommen unser Tempo mit, der Luftwiderstand bremst es ab.
-- Zeitzuender ('AA Zuender' 1): Fuse Timer = Flugzeit bis zum Zielpunkt (+ 'AA Zuender Zugabe s') - die
--  Fragmentation-Granate platzt am Ziel statt daran vorbei zu fliegen.
-- Streumuster: Spiralen vom Zielpunkt bis 'AA Streuung m' nach aussen (am Ziel gemessen), in 1 s eine Runde.
-- Sperrprofil (PRF, beim Bauen aus dem Fahrzeug berechnet): je 5 Grad Richtung (ab Bug, im Uhrzeigersinn) der
--  tiefste Rohrwinkel, mit dem die Geschosse ueber Mast, Aufbauten und die anderen Tuerme (ganzer Schwenkbereich ihrer
--  Rohre) hinweg gehen; nie flacher, und braeuchte das Ziel es flacher, wird nicht gefeuert.
-- Schiff: Nick/Roll gehen in den Rohrwinkel ein (der Turm steht auf einem schaukelnden Schiff).
-- Turm: Winkelfehler + Vorsteuerung mit der Drehgeschwindigkeit der Ziellinie + langsam gelernter Rest; bei grossen
--  Winkeln hoechstens so schnell, dass er mit 'AA Turm Bremsen' (U/s^2) bis zum Ziel anhalten kann.
-- 'Test Rohre' 1: Flak aus, Turm nach vorn, beide Rohre und die Kamera 20 Grad hoch - zum Pruefen der Richtungen;
--  2: dazu Turm 90 Grad nach rechts (Steuerbord) - dreht er nach links oder immer weiter, ist 'AA Turm Richtung' falsch.
-- Kamera (v1.1, Compact Robotic Pivot auf dem Turm): schaut auf das Ziel selbst (nicht auf den Vorhaltepunkt), damit es
--  auf dem Bildschirm mittig steht; ohne Ziel wie die Rohre.
-- Eingang: Ausgang von FLAKRADAR (Zahl 3-8 Ziel Ost/Nord/Hoch und Tempo, 9 Messdauer, 10 Entfernung, 11 Hoehe,
--  12 Ticks seit Meldung, 13-15 Spuren, 16 Flak-Turm U, 17 Kurs U, 18 Nick U, 19 Roll U, 22 Ziel-Nummer, 23-25 eigenes
--  Tempo Ost/Nord/Hoch; Bool 1 Feuer frei, 2 Ziel), dazu Zahl 26 Munition (Trommel, optional), Bool 3 'Loaded' eines
--  Rohrs (Schusszaehler)
-- Ausgang: Zahl 1 Turm-Tempo, 2 Hoehe Rohr links, 3 Hoehe Rohr rechts (Robotic Pivot), 4 Zuender (s), 5 Kamera-Hoehe;
--  10 Ziel-Entfernung, 11 Zustand (0 aus, 1 sucht, 2 Ziel, 3 feuert, 4 gesperrt: das Ziel liegt flacher als das
--  Sperrprofil / 'AA tiefster Winkel Grad' - v1.7, damit der Bildschirm ihr ein anderes geben kann), 12 Schuesse,
--  13 Ziel-Hoehe, 14 Spuren,
--  15 naechste Spur Entfernung, 16 deren Hoehe, 17 Ziel-Richtung (Grad ab Bug, + rechts);
--  18 fuer den Bildschirm gepackt: Zustand*100000 + Ziel-Entfernung (m);
--  Bool 1 Feuer, 2 Radar an, 3 Zufuehrung (Feeder), 4 Feuer frei
-- v1.3: 'Flak an' heisst jetzt 'Feuer frei' (vom Bildschirm-Chip); gefeuert wird nur damit, Radar und Zufuehrung
--  sind immer an
-- v1.9 (Andre: Leertaste mit gewaehlter Waffe = ein Schuss, die Automatik laeuft weiter): Bool 4 (Einzelschuss, ein
--  Tick vom Bildschirm ueber FLAKRADAR) -> feuern bis zum naechsten Schuss (hoechstens 30 Ticks), auch ohne Ziel oder
--  Toleranz - aber nie flacher als das Sperrprofil
-- v2.0 (Andre 04.10.): die Rohre feuern abwechselnd: Takt 'AA Takt Ticks' (gemessen: ein Rohr laedt 38 Ticks nach),
--  erste Haelfte darf das linke Rohr (Ausgang Bool 1), zweite das rechte (Bool 5) - jedes schiesst in seinem Fenster,
--  sobald es geladen ist; Einzelschuss nur links. Zeitzuender: auf den naechsten ganzen Tick NACH dem Zielpunkt
--  gerundet - eine Granate, die vorbeifliegt, platzt knapp hinter dem Ziel (Andre: Splitter der Heavy-Autocannon-
--  Fragmentation wirken nur auf ~0,5 m; der Zuender zaehlt ganze Ticks, ein Tick sind 12-15 m Flugweg).
-- v2.1: dasselbe Skript steuert die Anti-Schiffs-Kanonen vorn (Chips 'Figet Marena Kanone BC/AC'). Battle Cannon
--  ('Lader Zeit s' > 0): nicht geladen -> Verschluss auf (Bool 6 'Open Breech'), nach 1 s Zufuehrung schieben, nach
--  'Lader Zeit' zu und 2 s auf 'Loaded' warten, sonst von vorn (wie die KI-Panzer im Spiel); waehrenddessen kein
--  Feuer. 'Lader Zeit s' 0 (Autocannon): Zufuehrung immer an, kein Verschluss.
-- v2.2 (Kanonen gegen Schiffe): bei flacher Bahn kosten 0,5 m Hoehenfehler am Ziel ~15 m in der Weite - die Radar-Hoehe
--  rauscht zu stark. 'Ziel Hoehe fest m' (> -900): das Ziel liegt so hoch ueber dem Meer (Rumpf) - v2.9 (Andre 06.10.:
--  Bodenziele vom Seeradar): nur, wenn die Vorgabe tiefer als 'Land ab m' liegt, sonst die Radar-Hoehe; die eigene Hoehe =
--  Physik-Sensor + 'Radar ueber Physik m' + 'Radar vor Physik m' * Nick (das Radar sitzt vorn am Bug). Bahnrechnung:
--  von der Sichtlinie in 0,02-rad-Schritten anheben, bis die Bahn das Ziel erreicht, dann eingrenzen (lange, stark
--  gebremste Bahnen der Battle Cannon kamen mit der alten Rechnung zu kurz; nicht erreichbar -> keine Loesung).
-- v2.3 (Andres Test 04.10.: die Kanonen bewegten sich nicht - ihr Ziel lag achtern, das Turm-Radar sah es durch die
--  Bruecke nie, und ohne Spur stand der Turm in Ruhe): ohne Spur dreht der Turm zur Vorgabe (FLAKRADAR gibt sie dann
--  auf 3/4). BC mit zwei Rohren an einem Magazin ('Rohre' 2): das leere Rohr laedt (links zuerst), die Weiche (Bool 7)
--  zeigt auf seine Seite, Verschluss links Bool 6 / rechts Bool 8, 'Loaded' rechts auf Bool 5; geschossen wird
--  abwechselnd das geladene Rohr. Welche Weichen-Stellung welche Seite ist, lernt der Chip: zwei Ladeversuche ohne
--  'Loaded' -> Weiche umgekehrt.
-- v2.5 (Andres Test 04.10.: 2 Schiffe versenkt, aber die BC schoss nur 11-mal in 51 s - ein Rohr lud 295 Ticks
--  (Verschluss 216 offen, 'Loaded' 79 nach dem Schliessen), beide nacheinander, dann zwei Schuesse 6 Ticks auseinander):
--  Zufuehrung immer an; je Rohr Z (0 zu, 1 offen, 2 zu und wartet bis 150 Ticks auf 'Loaded'). Mit Meldern ('Contains
--  Ammo' der beiden Zufuehrungen auf Bool 6/7): Verschluss auf, sobald die eigene Zufuehrung eine Granate hat; zu
--  'Lader Nachlauf Ticks' nachdem sie sie abgegeben hat (hoechstens 'Lader Zeit'; kein 'Loaded' -> Nachlauf +5) - beide
--  Rohre laden gleichzeitig; die Weiche fuellt die leere Zufuehrung und lernt ihre Polung an den Meldern (Granate kommt
--  auf der anderen Seite an, oder 5 s keine). Ohne Melder (noch nie eine Meldung): wie v2.3 eins nach dem anderen.
--  Feuer abwechselnd im Abstand der halben gemessenen Ladezeit (Schuss bis 'Loaded' desselben Rohrs); Einzelschuss
--  sofort.
-- v2.6 (Andre 04.10.: "automatischer Zoom, der mit der bekannten Entfernung so an das Ziel zoomt, dass man es gut
--  erkennt und spaeter leichter korrigieren kann"): Zahl 19 an 'Field of View' der Turm-Kamera. Bildwinkel so, dass ein
--  Ziel von 'Kamera Zielgroesse m' 'Kamera Bildanteil' des Bildes fuellt - aber so weit, dass das Ziel trotz Vorhalt
--  drin bleibt (die Kamera schaut mit dem Turm voraus, der Hoehe nach auf das Ziel); ohne Ziel 'Kamera FOV ohne Ziel
--  rad'; weich nachgefuehrt. Zoom-Eingang 0 = 'Kamera FOV weit rad', 1 = 'Kamera FOV eng rad' (Camera Medium 2,2 /
--  0,025; dazwischen gleichmaessig angenommen).
-- v2.8 (Andre 04.10.: Korrektur bei ausgewaehlter Waffe per Blick, wie ein Joystick): Zahl 27/28 = Korrektur seitlich /
--  Hoehe (U, + = rechts / hoch) vom Kamera-Chip - der Zielpunkt (samt Vorhalt) verschiebt sich um diesen Winkel.
N=input.getNumber
B=input.getBool
S=output.setNumber
O=output.setBool
P=property.getNumber
m=math
pi2=m.pi*2
function cl(v,a,b) return m.max(a,m.min(b,v)) end
function wr(v) return (v+.5)%1-.5 end
-- Sperrprofil (Grad je 5 Grad Richtung ab Bug); der Bau-Schritt setzt hier die berechneten Werte ein
PRF='0'
-- tiefster erlaubter Rohrwinkel (U) fuer die Rohrrichtung a (U ab Bug, + rechts)
function lim(a)
	local i=m.floor(wr(a+gz0)*72+.5)%72
	return m.max(emn,(PF[i+1] or 0)/360)
end
-- Drehkranz-Befehl fuer Winkelfehler e (U) bei gewuenschtem Mitdrehen o (U/s)
function tb(e,o)
	local b=m.sqrt(2*ab*m.abs(e))
	return cl(e*atk,-b,b)+o
end
-- Flugbahn: Hoehe beim Erreichen der Weite X (m) unter dem Winkel w; n = Ticks bis dahin
function bahn(w,X,v0,d,g)
	local vx,vy=v0*m.cos(w),v0*m.sin(w)
	local q=1-60*X*d/vx
	if vx<=0 or q<=0 then return nil end
	local n=m.log(q)/m.log(1-d)
	local an=(1-d)^n
	return (vy*(1-an)/d-g/d*(n-(1-an)/d))/60,n
end
function ziel(X,Y,v0,d,g)
	local a=m.atan(Y,X)
	local b=a
	repeat
		a=b
		b=b+.02
		local y=bahn(b,X,v0,d,g)
		if not y or b>1.4 then return nil end
	until y>=Y
	for i=1,12 do
		local c=(a+b)/2
		if bahn(c,X,v0,d,g)<Y then a=c else b=c end
	end
	local y,n=bahn(b,X,v0,d,g)
	return b,n
end

ti=0
ph=0
sn=0
es=0
fp=-1
lf=0
fc=0
wi=false
Z={0,0}
Q={0,0}
W={}
PA={}
S0={}
sm=false
tc=0
ts=-1e4
tj=1
jq=0
fq=0

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
		ats=P('AA Turm Richtung')
		atk=P('AA Turm Tempo')
		ahl=P('AA Hoehe Richtung links')
		ahr=P('AA Hoehe Richtung rechts')
		gz0=P('AA Turm Null Grad')/360
		av0=P('AA v0')
		adr=P('AA Drag')
		gg=P('Geschoss g')/60
		arw=P('AA Reichweite m')
		atol=P('AA Toleranz Grad')/360
		emn=P('AA tiefster Winkel Grad')/360
		aoh=P('AA Radar ueber Rohr m')
		zfh=P('Ziel Hoehe fest m')
		lnd=P('Land ab m')
		rvy=P('Radar ueber Physik m')
		rvz=P('Radar vor Physik m')
		asr=P('AA Streuung m')
		atm=P('AA Toleranz m')
		ab=P('AA Turm Bremsen')
		zf=P('AA Zuender')
		zz=P('AA Zuender Zugabe s')
		ftk=P('AA Takt Ticks')
		lz=P('Lader Zeit s')*60
		lzm=lz
		dz=P('Lader Nachlauf Ticks')
		nr=P('Rohre')
		tr=P('Test Rohre')
		khs=P('Kamera Hoehe Richtung')
		kz0=P('Kamera Null Grad')/360
		kzg=P('Kamera Zielgroesse m')
		kba=P('Kamera Bildanteil')
		kfw=P('Kamera FOV ohne Ziel rad')
		kf1=P('Kamera FOV weit rad')
		kf2=P('Kamera FOV eng rad')
		kfv=kfw
		PF={}
		for v in string.gmatch(PRF,'-?[%d%.]+') do PF[#PF+1]=tonumber(v) end
	end
	local ar,hd,nk,rl=N(16),N(17),N(18),N(19)
	local on,ok=B(1),B(2)
	local VE,VN,VU=N(23),N(24),N(25)
	ph=(ph+1)%60
	local st,fire,sp,el,ri,fz,ce,fv=on and 1 or 0,false,0,0,0,0,nil,kfw
	fe=nil
	if tr>0 then
		-- Rohr-Test: Turm nach vorn (2: 90 Grad nach rechts - zeigt die Drehrichtung), Rohre 20 Grad hoch, nichts feuern
		on,ok=false,false
		sp=cl(tb(wr((tr>1 and .25 or 0)-ar-gz0),0),-1,1)
		el=20/360
	elseif ok then
		local E,Nn,U,vE,vN,vU=N(3),N(4),N(5)+aoh,N(6),N(7),N(8)
		if zfh>-900 and N(20)<lnd then
			-- Schiffsziel: feste Hoehe statt Radar-Hoehe; N(11)-N(5) = Hoehe des Physik-Sensors
			U=zfh-(N(11)-N(5)+rvy+rvz*m.sin(nk*pi2))+aoh
			vU=0
		end
		-- Kamera: Sichtlinie zum Ziel jetzt (gegen das Deck)
		local tk=(m.atan(E,Nn)/pi2-hd)*pi2
		ce=m.atan(N(5),m.sqrt(E*E+Nn*Nn))/pi2-(nk*m.cos(tk)-rl*m.sin(tk))
		-- Zoom (v2.6): Ziel fuellt kba des Bildes; Versatz Kamera (mit dem Turm) -> Ziel jetzt passt mit Rand hinein
		local R0=m.max(m.sqrt(E*E+Nn*Nn+N(5)^2),10)
		fv=m.max(kzg/kba/R0,(2*m.abs(wr(tk/pi2-ar-gz0))*pi2+kzg/R0)*1.2)
		if N(22)~=tq then ti=0 end
		tq=N(22)
		local t,f,w=0,0,nil
		local qE,qN,qU
		for k=1,3 do
			qE,qN,qU=E+vE*t+VE*(t-f),Nn+vN*t+VN*(t-f),U+vU*t+VU*(t-f)
			local n
			w,n=ziel(m.sqrt(qE*qE+qN*qN),qU,av0,adr,gg)
			if not w then break end
			t=n/60
			f=(1-(1-adr)^n)/adr/60
		end
		-- keine Bahn erreicht das Ziel (zu weit): nur hinzielen, nicht feuern
		local nl=not w
		if nl then
			w=m.atan(qU,m.sqrt(qE*qE+qN*qN))
		elseif zf>0 then
			fz=(m.floor(t*60)+1)/60+zz
		end
		st=2
		local R=m.sqrt(qE*qE+qN*qN+qU*qU)
		local so=asr*ph/60/m.max(R,50)/pi2
		local wa=ph/60*pi2
		local yw=m.atan(qE,qN)/pi2-hd+so*m.cos(wa)+N(27)
		ri=wr(yw)*360
		local th=yw*pi2
		local err=wr(yw-ar-gz0)
		fe=err
		local om=(qN*vE-qE*vN)/m.max(qE*qE+qN*qN,1)/pi2-wr(hd-(hq or hd))*60
		sp=tb(err,om)+ti
		if m.abs(sp)<1 and m.abs(err)<.01 then ti=cl(ti+err*2/60,-.5,.5) end
		sp=cl(sp,-1,1)
		el=w/pi2-(nk*m.cos(th)-rl*m.sin(th))+so*m.sin(wa)+N(28)
		if el<lim(ar) then st=4 end
		if m.abs(err)*m.cos(el*pi2)<m.max(atol,atm/pi2/R)+so and N(9)>=.4 and N(12)<300 and N(10)<arw and el>=lim(ar) and on and not nl then fire=true st=3 end
	else
		-- ohne Spur: zur Vorgabe drehen (v2.3), ohne Vorgabe Ruhestellung
		local E,Nn=N(3),N(4)
		sp=tb(wr((E~=0 or Nn~=0) and m.atan(E,Nn)/pi2-hd-ar-gz0 or -ar-gz0),0)
		el=.03
	end
	el=m.max(el,lim(ar))
	kfv=kfv*(cl(fv,kf2,kf1)/kfv)^.06
	local ld,lr2,op,fd,opR,wj=B(3),B(5),false,true,false,false
	tc=tc+1
	if B(4) then es=30 end
	if es>0 then es=es-1 end
	-- Schuesse zaehlen ('Loaded' des linken Rohrs geht bei jedem Schuss kurz aus; abwechselnd: je einer rechts) - v2.5
	-- vor der Rohrwahl (sonst schoss beim Einzelschuss im naechsten Tick das andere Rohr)
	if kg and not ld then
		sn=sn+(lz>0 and 1 or 2)
		es=0
		S0[1]=tc
	end
	if kr and not lr2 then
		sn=sn+1
		es=0
		S0[2]=tc
	end
	kg,kr=ld,lr2
	if fire then fp=(fp+1)%ftk else fp=-1 end
	local fL,fR=fire and fp<ftk/2 or es>0,fire and fp>=ftk/2
	if lz>0 then
		local G,A=nr>1 and {ld,lr2} or {ld},{B(6),B(7)}
		sm=sm or A[1] or A[2]
		for j=1,nr do
			local z,q=Z[j],Q[j]+1
			if z==0 then
				if not G[j] and (sm and A[j] or not sm and Z[3-j]==0) then z,q,W[j]=1,0,nil end
			elseif z==1 then
				-- Granate hat die Zufuehrung verlassen -> nach dem Nachlauf zu
				if PA[j] and not A[j] then W[j]=0 end
				if W[j] then W[j]=W[j]+1 end
				if (W[j] or -1)>=dz or q>=lz then z,q=2,0 end
			elseif G[j] then
				z,q,fc=0,0,0
				if S0[j] then lzm,S0[j]=tc-S0[j],nil end
			elseif q>=150 then
				-- kein 'Loaded': nochmal; mit Meldern Nachlauf laenger, ohne nach 2 Fehlversuchen Weiche umgekehrt
				z,q,fc=0,0,fc+1
				if sm then dz=dz+5 elseif fc>=2 then wi,fc=not wi,0 end
			end
			Z[j],Q[j]=z,q
		end
		-- Weiche: mit Meldern bleibt sie auf einer Seite, bis deren Zufuehrung voll ist, dann auf eine leere (beide leer:
		-- abwechselnd); ohne Melder auf das ladende Rohr
		local t=Z[2]>0 and 2 or 1
		if sm then
			t=tj
			if A[tj] then
				if not A[3-tj] then t=3-tj end
			end
		end
		if nr<2 then t=1 end
		if t~=tj then tj,jq=t,0 end
		jq=jq+1
		local o=3-tj
		if sm and nr>1 and jq>30 and (A[o] and not PA[o] or jq>600 and not A[tj]) then wi,jq=not wi,0 end
		wj=(tj==2)~=wi
		PA=A
		op,opR=Z[1]==1,Z[2]==1
		-- abwechselnd: das Rohr, das nicht zuletzt schoss; Abstand halbe Ladezeit (Einzelschuss sofort); das gewaehlte
		-- Rohr bekommt den Abzug, bis es geschossen hat (oder das Feuer endet)
		local fa=fire or es>0
		if fq==1 and not (ld and fa) or fq==2 and not (lr2 and fa) then fq=0 end
		if fq==0 and (fire and tc-ts>=m.max(m.min(lzm/2,300),20) or es>0) then
			if ld and Z[1]==0 and (lf~=1 or nr<2 or not lr2 or Z[2]>0) then fq=1
			elseif nr>1 and lr2 and Z[2]==0 then fq=2 end
			if fq>0 then lf,ts=fq,tc end
		end
		fL,fR=fq==1,fq==2
	end
	hq=hd
	S(1,sp*ats)
	S(2,cl(el/.25,-1,1)*ahl)
	S(3,cl(el/.25,-1,1)*ahr)
	S(4,fz)
	S(5,cl(((ce or el)+kz0)/.25,-1,1)*khs)
	O(1,fL)
	O(2,true)
	O(3,fd)
	O(6,op)
	O(7,wj)
	O(8,opR)
	O(4,on)
	O(5,fR)
	S(10,ok and N(10) or 0) S(11,st) S(12,sn) S(13,ok and N(11) or 0)
	S(14,N(13)) S(15,N(14)) S(16,N(15)) S(17,ri)
	S(18,st*1e5+m.floor(ok and N(10) or 0))
	S(19,cl((kf1-kfv)/(kf1-kf2),0,1))
	-- Schreiber: Ziel da, Feuer frei, Zustand, Feuer, Turm-Befehl, Rohrwinkel (U), tiefster erlaubter, Richtung Grad,
	-- Entfernung, Messdauer, Ticks ohne Meldung, Turm (U), Seitenfehler (U), Zuender s, Schuesse, Turm-Integral, Kamera;
	-- Lader (v2.5): Zustand links + 3 x rechts, Bits (1/2 geladen L/R, 4/8 Zufuehrung L/R hat Granate, 16 Melder da),
	-- Weiche umgekehrt, Nachlauf, gemessene Ladezeit, Weiche auf (1 L, 2 R); Kamera-Bildwinkel rad (v2.6)
	LG('',{ok,on,st,(fL and 1 or 0)+(fR and 2 or 0),sp,el,lim(ar),ri,N(10),N(9),N(12),ar,fe,fz,sn,ti,ce,es,Z[1]+3*Z[2],
		(ld and 1 or 0)+(lr2 and 2 or 0)+(B(6) and 4 or 0)+(B(7) and 8 or 0)+(sm and 16 or 0),wi,dz,lzm,tj,kfv},25)
	LF()
end
