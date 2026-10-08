-- KI FAHREN v1.0 - KI Landkreuzer (08.10.2026): das Fahr-Gehirn des Radpanzers. Links und rechts je ein Antrieb
-- (7 Raeder je Seite), gelenkt wird wie beim Kettenfahrzeug ueber den Unterschied. Panzer ca. 28 m lang, 9,5 m breit,
-- 40-60 t: traege, langer Bremsweg, dreht auf der Stelle in einem Kreis von ca. 15 m Halbmesser.
-- Bedienung von einem Sitz: Schalter 'KI an' -> der Panzer merkt sich die Stelle als Heimat und faehrt allein:
--  - Wegpunkte (bis 8, auf der Karte angetippt, ki_karte.lua) der Reihe nach; im Revier-Modus danach wieder von vorn,
--    sonst bleibt er am letzten stehen (Zustand 9).
--  - ohne Wegpunkte im Revier-Modus: Zufallspunkte hoechstens 'Revier m' um die Heimat (nicht nahe gemerkter Gefahr,
--    nicht nahe besuchter tiefer Orte); am Punkt 'Patrouille Pause s' stehen (Antrieb aus, Strom sparen).
--  - Schalter 'Nach Hause': zur Heimat und dort warten; aus = weiter wie vorher.
--  - W/S/A/D am Sitz: sofort Handbetrieb (auch bei KI aus); 2 s nach dem Loslassen faehrt die KI weiter.
-- Tempo vorwaerts rechnet die KI selbst aus der Ortsaenderung in Kursrichtung (Kanal 7/8 werden nicht gebraucht).
-- Sensoren (alle Laser fest, nur 90-Grad-Richtungen moeglich):
--  - drei Front-Laser (9 links, 10 Mitte, 11 rechts, 3,5 m auseinander, 'Laser Hoehe m' hoch) schauen gerade nach vorn
--    ueber die Gasse, durch die der Panzer faehrt. Ein waagerechter Strahl in Hoehe h trifft einen Hang mit Winkel a
--    bei d = h/tan(a - Nick). Steiler als 'Steigung max Grad' (2,4 m und 30 Grad: unter 4,2 m) = Hindernis. Ob ein
--    Treffer ein Hang oder eine Wand ist, sieht man mit diesen Lasern erst so nah - darum ab 'Hindernis m' langsamer
--    und unter 'Notstopp m' nur kriechen: ein Hang hebt den Bug, der Strahl geht ueber ihn weg (Abstand waechst);
--    eine Wand kommt naeher, bis sie zu steil ist -> zurueck und wegdrehen. Ein Aussenstrahl 5 m kuerzer als der
--    andere = schmales Hindernis: zur freien Seite lenken.
--  - Seiten-Laser (12 links, 13 rechts, Mitte, ab Bordwand): welche Seite frei ist; Abstand zu Waenden.
--  - Bug-Laser (14) senkrecht nach unten: Grundwert 'Boden Laser Hoehe m' (0 = beim Stehen vor dem KI-Start
--    gelernt). Bodenhoehe unter dem Bug = eigene Hoehe - Sensorhoehe + Grundwert - Messung (+ Nick mal halbe Laenge).
--    Unter 0,5 m ueber dem Meer = Wasser (gleich ob der Laser die Oberflaeche oder den Grund trifft). Je tiefer der
--    Boden unter dem Bug, desto langsamer (ab 10 m ueber 'Wasser Hoehe m').
--  - Heck-Laser (15): beim Rueckwaertsfahren nicht anstossen.
-- Treffer-Gedaechtnis: die Front-Laser decken nur +-3,5 m, der Panzer +-4,75 m; die KI merkt sich je Laser den
--  letzten Treffer als Ort und dreht nicht zu Punkten hin, die neben dem Rumpf oder voraus liegen.
-- Gefahr (Zustand 8): Wasser/Kante unter dem Bug, eigene Hoehe unter 'Wasser Stopp m', Schraeglage ueber 'Kipp max'
--  -> kraeftig bremsen, 3 s zurueck (der Weg, den er kam, war sicher), Stelle merken. Gemerkte Stellen (8, die
--  aeltesten fallen raus) stossen den Kurs ab und lenken um sie herum (Wirbel, Richtung je Stelle fest); jedes neue
--  Mal an derselben Stelle waechst sie. Sackgasse (vorn zu, beide Seiten enger als 'Breite m'): gerade zurueck, bis
--  der ganze Rumpf draussen ist, dann die ganze Sackgasse merken.
-- Festgefahren (Befehl gross, weder Fahrt noch Drehung, 3 s): 3 s in Gegenrichtung mit Drehung, Seite wechseln. Ein
--  Ziel, das 3 Fehlschlaege bringt (festgefahren 1, Gefahr 2, je 60 s ohne 5 m naeher 1), wird uebersprungen.
-- Kampf (Ziel gueltig, naeher als 'Kampf Abstand m'): anhalten oder kriechen, Bug zum Ziel (+-'Kampf Winkel'); naeher
--  als 'Mindestabstand m': rueckwaerts. 5 s ohne Ziel: weiter auf der Route.
-- Batterie: unter 'Batterie min' anhalten (Zustand 7), unter 30 % nur 60 % Tempo; Eingang 0 = nicht angeschlossen.
-- Eingang (Composite): Zahl 1 Ost, 2 Hoehe, 3 Nord, 4 Kompass (U), 5 Nick (U), 6 Roll (U), (7/8 ungenutzt),
--  9-11 Front-Laser L/M/R, 12/13 Seite L/R, 14 Bug unten, 15 Heck, 16 Batterie (0 = nicht angeschlossen),
--  17 A/D (+ rechts), 18 W/S (+ vor), 20/21 Ziel Ost/Nord, 23/24 Tipp Ost/Nord, 25 Kartenbefehl (1 Wegpunkte loeschen,
--  2 Revier-Modus um); Bool 1 KI an (mit Startverzoegerung/Pause vom Klebe-Skript), 2 Sitz besetzt, 3 Tipp-Puls,
--  4 Ziel gueltig, 5 Befehl-Puls, 6 Nach Hause (Schalter: zur Heimat und dort warten)
-- Ausgang: Zahl 1/2 Antrieb links/rechts (-1..1), 3 Zustand, 4/5 aktuelles Ziel (im Kampf: der Feind), 6 Soll-Kurs (U),
--  7/8 Heimat, 9 Revier m, 10 Zahl der Wegpunkte, 11 aktueller Wegpunkt, 12-27 Wegpunkte (Ost/Nord), 28 Soll-Tempo,
--  29 Lenkbefehl (-1..1, + rechtsherum), 30 Fahrbefehl (-1..1, + vor) - beide roh, vor Rad-Richtung und Lernen (auch
--  im Handbetrieb: A/D, W/S), 31 eigener Kurs (U im Uhrzeigersinn ab Nord), 32 Tempo vorwaerts (selbst gerechnet);
--  Bool 1 Antrieb aktiv, 2 Waffen frei (KI an, kein Handbetrieb), 3 Revier-Modus, 4 Wegpunkt erreicht (Puls),
--  5/6 Richtung links/rechts wurde umgelernt (anders als das Property)
-- Rad-Richtung: die rechte Seite ist gespiegelt eingebaut -> 'Rad Richtung rechts' -1. Mit 'Richtung lernen' 1 faehrt
--  er nach dem Einschalten bis 2 s gerade an (Anfahrprobe) und merkt selbst, wenn eine Seite (oder beide) falsch
--  herum dreht: gleich gerichtet befohlen, aber 1,5 s andersherum gefahren -> beide umdrehen; gleich gerichtet
--  befohlen, aber gedreht statt gefahren (oder Drehen befohlen, aber gefahren) -> die Seite, die der Dreh- bzw.
--  Fahrsinn zeigt. Nur auf ebenem Boden, ohne Hindernis vorn. Gelernt bleibt bis zum Neustart des Skripts (dann das
--  Property richtig stellen: Bool 5/6 zeigen es).
-- Zustaende: 0 aus, 1 Hand, 2 Wegpunkt/Heimweg, 3 Revier, 4 Ausweichen, 5 Zurueck/Freifahren, 6 Kampf, 7 Batterie,
--  8 Gefahr, 9 am Ziel/wartet/Pause
N=input.getNumber
B=input.getBool
S=output.setNumber
O=output.setBool
P=property.getNumber
m=math
A,I,Z=m.abs,m.min,m.max
pi2=m.pi*2
function cl(v,a,b) return Z(a,I(b,v)) end
-- Winkel in Umdrehungen auf -0,5..0,5
function wr(v) return (v+.5)%1-.5 end
function ab(x,z) return (x*x+z*z)^.5 end
function sg(v) return v<0 and -1 or 1 end
-- waagerechter Laser: 0 = kein Strom/kein Wert -> wie frei; weiter als 99 m ist egal
function LZ(i) local d=N(i) return d>0 and I(d,99) or 99 end
-- Rampe: Ausgang hoechstens RP je Tick naeher an den Wunsch, Richtung 0 (Bremsen) dreimal so schnell; bei Gefahr
-- (Zustand 8) alles viermal so schnell: vom Bug-Laser bis zum Schwerpunkt sind nur ca. 13 m Bremsweg
function RA(o,n) local s=(n*n<o*o and 3 or 1)*RP*RX return o+cl(n-o,-s,s) end
-- Manoever: Soll-Tempo u (m/s, ueber den Tempo-Regler), Lenkung w fuer t Ticks, Zustand c
function MV(u,w,t,c) mu,mw,mt,mc=u,w,t,c end
-- Hindernis? Strahl d in Hoehe LH: Hang bis zum Treffpunkt steiler als SM (mit eigenem Nick PR)
function HI(d) return PR+m.atan(LH,d)>SM end
-- neues Ziel: Fehlschlaege und Fortschritt zuruecksetzen
function NG() fe,bd,pk=0,1e9,0 end
-- Stelle merken (Gefahr/Hindernis): X[i]={Ost,Nord,Radius,Wirbel}. Liegt schon eine da, waechst sie (Sackgasse).
-- Die Wirbelrichtung (herum links/rechts) wird beim Anlegen fest gemerkt - kippte sie mit der Ausweichseite, kippte
-- auch der Soll-Kurs hin und her.
function MK(a,b,r)
	for _,s in ipairs(X) do
		if ab(s[1]-a,s[2]-b)<s[3]+5 then s[3]=I(s[3]+10,80) return end
	end
	xn=xn%8+1
	X[xn]={a,b,r,sd}
end
-- Soll-Tempo begrenzen: f=1 Reisetempo, f=0 Schleich-Tempo
function VL(f) vs=I(vs,VK+(VT-VK)*cl(f,0,1)) end
-- Stelle d m vor der Mitte merken (d<0: hinten), Radius r
function MP(d,r) MK(x+sn*d,z+cs*d,r) end
-- naechster Revier-Punkt: zufaellig im Kreis um die Heimat, nicht zu nah am eigenen Ort, nicht nahe gemerkter
-- Stellen oder tiefer Orte (sonst nach 20 Versuchen der letzte)
function NP()
	for i=1,20 do
		local a,r=m.random()*pi2,RV*m.random()^.5
		px,pz=hx+r*m.sin(a),hz+r*m.cos(a)
		local ok=ab(px-xx,pz-zz)>RV/3
		for _,s in ipairs(X) do if ab(s[1]-px,s[2]-pz)<s[3]+BR+10 then ok=false end end
		for _,s in ipairs(T) do if ab(s[1]-px,s[2]-pz)<60 then ok=false end end
		if ok then break end
	end
	-- Zeit fuer diesen Punkt: doppelte Fahrzeit + 1 min, danach ein neuer
	pq=(ab(px-xx,pz-zz)/VT*2+60)*60
	NG()
end

W={} X={} T={} H={} xn=0 tn=0
wi,hn,mt,am,sd,kt,sk,lu,ph,l1,l2,av,vp,pb,od,c0=1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0
lo,ro,si,vf,pw,ut,wt,qd,bn,bs,BH=0,0,0,0,0,0,0,1,0,0,1
gx,gz,hx,hz,ex,ez,dh,xx,zz=0,0,0,0,0,0,0,0,0
pm=true
NG()

function onTick()
	if not ini then
		ini=1
		VT,VV,VK,ZR,RV=P('Tempo m/s'),Z(P('Vollgas m/s'),1),P('Kriech m/s'),P('Ziel Radius m'),P('Revier m')
		HD,NS,SM,KM=P('Hindernis m'),P('Notstopp m'),m.rad(P('Steigung max Grad')),P('Kipp max Grad')/360
		WH,WS,AB=P('Wasser Hoehe m'),P('Wasser Stopp m'),P('Absturz m')
		BB,LG,LQ,BQ,SQ=P('Breite m'),P('Laenge m')/2,P('Laser Hoehe m'),P('Boden Laser Hoehe m'),P('Sensor Hoehe m')
		KA,KV,KW,MA=P('Kampf Abstand m'),P('Kampf Tempo m/s'),P('Kampf Winkel Grad')/360,P('Mindestabstand m')
		BM,KR,NR,RR=P('Batterie min'),P('Kompass Richtung'),P('Nick Richtung'),P('Roll Richtung')
		RP,LK,DG=1/60/Z(P('Rampe s'),.02),P('Lenk Staerke'),P('Dreh Gas')
		QL,QR,RL=P('Rad Richtung links'),P('Rad Richtung rechts'),P('Richtung lernen')
		FL,FR=QL,QR
		-- Sicherheitsabstand fuer gemerkte Stellen: halbe Breite + 3 m
		BR=BB/2+3
		PP=P('Patrouille Pause s')*60
		-- Kurs und Ort des ersten Ticks als 'vorher' (sonst zuckt die Lenkung einmal)
		ph,xo,zo=wr(KR*N(4)),N(1),N(3)
	end
	x,al,z=N(1),N(2),N(3)
	xx,zz=x,z
	hd=wr(KR*N(4))
	sn,cs=m.sin(hd*pi2),m.cos(hd*pi2)
	pt,rl=N(5)*NR,N(6)*RR
	PR=pt*pi2
	-- Tempo vorwaerts selbst aus der Ortsaenderung je Tick in Kursrichtung, geglaettet (Kanal 8 des Physik-Sensors
	-- ist im Spiel nicht sicher Fahrzeug-bezogen und hat vielleicht ein anderes Vorzeichen)
	vf=vf*.8+((x-xo)*sn+(z-zo)*cs)*12
	xo,zo=x,z
	fl,fc,fr,sl,sr,dn,rk=LZ(9),LZ(10),LZ(11),LZ(12),LZ(13),N(14),LZ(15)
	ad,ws,kon=N(17),N(18),B(1)
	-- Drehrate (U/s) fuer die Daempfung der Lenkung
	yr=wr(hd-ph)*60
	ph=hd

	-- Karte: Tipp = Wegpunkt dazu (hoechstens 8); Befehl 1 = alle loeschen, 2 = Revier-Modus um (je auf die Flanke)
	b3,b5=B(3),B(5)
	if b3 and not l3 and #W<8 then
		W[#W+1]={N(23),N(24)}
		fz=false
		if #W==1 then wi=1 NG() end
	end
	if b5 and not l5 then
		k=m.floor(N(25)+.5)
		if k==1 then W={} wi=1 px=nil NG() end
		if k==2 then pm=not pm px=nil end
		fz=false
	end
	l3,l5=b3,b5

	-- KI eingeschaltet: Heimat hier
	if kon and not ki then hx,hz,px,mt,kt,pb=x,z,nil,0,0,RL>0 and 120 or 0 NG() end
	ki=kon
	-- Hand: jede Bewegung von W/S/A/D, danach 2 s Pause
	hn=B(2) and (A(ws)>.05 or A(ad)>.05) and 120 or Z(hn-1,0)
	-- Batterie (0 = nicht angeschlossen = unbekannt; erst 5 % ueber der Grenze wieder gut)
	ba=N(16)
	bl=ba>0 and (ba<BM or bl and ba<BM+.05)
	-- Kampf: Ziel naeher als KA -> 5 s merken
	if B(4) and ab(N(20)-x,N(21)-z)<KA then kt,ex,ez=300,N(20),N(21) elseif kt>0 then kt=kt-1 end
	-- tiefe Orte merken (Revier-Punkte meiden sie)
	if kon and al<WH then
		f=1
		for _,s in ipairs(T) do if ab(s[1]-x,s[2]-z)<30 then f=nil end end
		if f then tn=tn%8+1 T[tn]={x,z} end
	end

	-- Bug-Laser, Grundwert BH: das Property, wenn > 0; sonst (0 = Automatik) der Mittelwert, solange er vor dem
	-- KI-Start still steht (die Raeder waehlt Andre spaeter, je nach Rad misst er auf ebenem Boden 0,4-1 m); hat er
	-- dafuer keine Zeit, gilt die erste Messung.
	if BQ>0 then BH=BQ elseif dn>0 and dn<9 and (not kon and A(vf)<.1 or bn<1) then bn,bs=bn+1,bs+dn BH=bs/bn end
	-- Front-Laser und Physik-Sensor sitzen 3,2 bzw. 2,2 Bloecke ueber dem Bug-Laser: ihre Hoehe ueber dem Boden folgt
	-- aus BH (0 = Automatik, passt dann zu jeder Radgroesse)
	LH,SH=LQ>0 and LQ or BH+.8,SQ>0 and SQ or BH+.55
	-- Bodenhoehe unter dem Bug (ga); 0 = kein Wert. Kante (kb): der Boden unter dem Bug liegt mehr als
	-- 'Absturz m' unter der Ebene des Rumpfes (dp) UND ist ploetzlich weggefallen: dp im Verhaeltnis zur Strecke, die
	-- er vorwaerts fuhr, seit der Boden normal war (od-c0), steiler als SM. Eine Kuppe (oben auf einer Rampe, Anfang
	-- eines Gefaelles) waechst langsam mit der Strecke - der Bug ragt da nur ueber; eine Klippe springt sofort.
	gv=dn>0
	ga,dp=al+(BH-SH-dn)*m.cos(PR)+LG*m.sin(PR),(dn-BH)*m.cos(PR)
	if vf>0 then od=od+vf/60 end
	if dp<.5 then c0=od end
	kb=gv and dp>AB and m.atan(dp,od-c0)>SM
	tl=Z(A(rl),A(pt))
	-- Hindernis sicher vor dem Bug (zu steil fuer einen Hang); Gefahr unter dem Bug (Wasser/Kante)
	hi,dg=HI(fl) or HI(fc) or HI(fr),gv and (ga<.5 or kb)

	u,w,vs,zs,rp,up=0,0,0,0,false,true
	if mt<1 and A(vf)>.5 then qd=sg(vf) end
	-- 3 Fehlschlaege (festgefahren 1, Gefahr 2, 60 s ohne Fortschritt 1): Ziel ueberspringen - hier vor allem
	-- anderen, sonst haelt eine Gefahr, die immer wieder ausloest, ihn ewig fest
	if fe>=3 then
		NG()
		if B(6) then elseif #W>0 then wi=wi%#W+1 else px=nil end
	end
	if hn>0 then
		-- Hand: links = W/S + A/D, rechts = W/S - A/D
		zs,u,w,up=1,ws,ad,false
	elseif not kon then
		up=false
	elseif bl then
		zs=7
	elseif mt>0 then
		-- Manoever laeuft: Tempo/Lenkung fest; hinten zu nah -> nur drehen; tief (Wasser nah) -> nur kriechen
		mt=mt-1
		zs,vs,w=mc,mu,mw
		if mu<0 and rk<4 then vs=0 end
		if al<WH then vs=cl(vs,-VK,VK) end
		-- Sackgasse: gerade zurueck, bis beide Seiten frei sind und danach noch halbe Laenge + Abstand (mr; die
		-- Seiten-Laser sitzen in der Mitte, vorn steckt er sonst noch drin). Dann die ganze Sackgasse merken: Mitte
		-- zwischen Treffpunkt (ux/uz) und Bug, Radius halbe Tiefe
		if mq then
			if sl>BB and sr>BB then mr=mr-A(vf)/60 end
			if mr<0 then mt=0 end
			if mt<1 then
				a,b=x+sn*LG,z+cs*LG
				mq=nil
				MK((ux+a)/2,(uz+b)/2,ab(ux-a,uz-b)/2+5)
			end
		end
	elseif al<WS or tl>KM or dg and (vf>.2 or lu>.05) then
		-- Gefahr: kraeftig bremsen (Rampe viermal so schnell) und zurueck, Stelle merken. Nur wenn nichts unter dem
		-- Bug ist und er vorher rueckwaerts fuhr (qd: Richtung aus normaler Fahrt, nicht aus Manoevern - sonst
		-- pendelt er an einer Kante vor und zurueck), stattdessen vor
		q=dg and 1 or qd
		MP(q*(LG+8),20)
		fe,zs=fe+2,8
		-- Gefahr unter dem Bug auch ins Treffer-Gedaechtnis: dann haelt die Gassen-Logik den Rumpf von der Kante weg
		if dg then H[14]={x+sn*LG,z+cs*LG} end
		-- zu viel Roll (z. B. eine Seite ueber einer Kante): langsam vor und zur hohen Seite drehen (Hang dann
		-- vorn/hinten) - zurueck entlang der Kante wuerde nie besser; sonst zurueck
		if tl>KM and A(rl)>A(pt) and not dg and al>WS then MV(VK,-sg(rl)*DG,120,8) else MV(-q*2*VK,0,180,8) end
	elseif sk>180 then
		-- festgefahren: 3 s Gegenrichtung mit Drehung, Stelle merken, beim naechsten Mal andere Seite
		sk,fe,sd,zs=0,fe+1,-sd,5
		q=lu<-.1 and -1 or 1
		MP(q*(LG+5),10)
		MV(-q*2*VK,sd*.3,180,5)
	elseif kt>0 then
		-- Kampf: stehen (bzw. kriechen), Bug zum Ziel; zu nah -> rueckwaerts
		zs,gx,gz=6,ex,ez
		dx,dz=ex-x,ez-z
		dh=m.atan(dx,dz)/pi2
		e=wr(dh-hd)
		if ab(dx,dz)<MA then
			vs=rk>8 and -VT/2 or 0
			w=LK*e
		else
			vs=hi and 0 or KV
			if KW>0 then
				if A(e)>KW then kd=1 elseif A(e)<KW/3 then kd=nil end
				if kd then w=LK*e*2 vs=0 end
			end
		end
		w=cl(w,-DG,DG)
	elseif pw>0 and #W<1 and pm and not B(6) then
		-- Patrouillen-Pause am Revier-Punkt: anhalten, dann Antrieb aus (Strom sparen); die Tuerme arbeiten weiter
		pw,zs,up=pw-1,9,A(vf)>.3
	else
		-- Fahren: Ziel = Heimat (Schalter 'Nach Hause'), Wegpunkt oder Revier-Punkt
		n,nh=#W,B(6)
		if nh then
			gx,gz=hx,hz
		elseif n>0 then
			wi=cl(wi,1,n)
			gx,gz=W[wi][1],W[wi][2]
		elseif pm then
			if not px then NP() end
			pq=pq-1
			if pq<0 then NP() end
			gx,gz=px,pz
		end
		dx,dz=gx-x,gz-z
		d=ab(dx,dz)
		if nh and d<ZR or not nh and (fz or n<1 and not pm) then
			zs=9
		else
			zs=(n>0 or nh) and 2 or 3
			if d<ZR and not nh then
				rp=true NG()
				if n<1 then px,pw=nil,PP elseif wi<n then wi=wi+1 elseif pm then wi=1 else fz=true end
			end
			-- Fortschritt: 60 s nicht 5 m naeher = ein Fehlschlag; 3 = Ziel ueberspringen
			if d<bd-5 then bd,pk=d,0 else pk=pk+1 end
			if pk>3600 then pk=0 fe=fe+1 end
			-- Soll-Kurs: zum Ziel, gemerkte Stellen stossen ab und lenken zu ihrer Seite herum (Wirbel)
			vx,vz=dx/(d+.1),dz/(d+.1)
			for _,s in ipairs(X) do
				ax,az=x-s[1],z-s[2]
				q=ab(ax,az)+.1
				k=(s[3]+BR+10-q)/10
				if k>0 then
					k=I(k,2)/q
					vx,vz=vx+k*(ax-s[4]*az),vz+k*(az+s[4]*ax)
				end
			end
			dh=m.atan(vx,vz)/pi2
			e=wr(dh-hd)
			if A(e)>1/6 then
				-- mehr als 60 Grad daneben: auf der Stelle drehen
				w=sg(e)*DG
			else
				w=LK*e-2*yr
				vs=VT*(1-3*A(e))
			end
			-- letzter Wegpunkt ohne Revier-Modus: sanft ankommen
			if nh or n>0 and wi==n and not pm then vs=I(vs,VK+d/20) end

			-- Front-Laser: Gasse vor dem Bug
			fm=I(fl,fc,fr)
			am=Z(am-1,0)
			if fm<HD then
				-- freiere Seite merken (Laser vorn + Seite); einseitige Sperre gilt sofort
				if am<=0 or A(fr-fl)>15 then sd=fr+sr>fl+sl and 1 or -1 end
				am=Z(am,300)
				-- einseitig zu: zur freien Seite lenken; je naeher, desto langsamer
				w=w+(I(fr,HD)-I(fl,HD))/HD*DG
				VL((fm-NS)/(HD-NS))
				if fm<NS then zs=4 end
			end
			-- Treffer-Gedaechtnis: die Front-Laser decken nur +-3,5 m ab, der Panzer ist breiter, und die Seiten-Laser
			-- sitzen in der Mitte. Darum merkt sich die KI je Laser den letzten Treffer als Ort (H[i]): einseitige
			-- Treffer vorn (ein Aussenstrahl 5 m kuerzer als der andere = schmales Hindernis; nicht bei Haengen, die
			-- alle Strahlen gleich treffen), sichere Hindernisse und alles, was die Seiten-Laser naeher als 'Breite m'
			-- sehen (bis 1,5 x 'Breite m'). Ein Punkt gilt, bis er 60 m weg ist (dreht der Panzer um, zaehlt er wieder;
			-- eine Hausecke in der Luecke zwischen Aussenstrahl und Bordwand sieht sonst kein Laser). Liegt er
			-- neben dem Rumpf oder (beim Vorwaertsfahren) bis 'Hindernis m' vor dem Bug, bis 1,5 x Breite seitlich: nicht
			-- zu ihm hin drehen (Ecke/Heck). In der Gasse vor dem Bug (halbe Breite + 2 m): weg lenken, langsamer;
			-- neben dem Rumpf naeher als der Sicherheitsabstand BR: frueh und sanft weg (beim Wegdrehen schwenkt das
			-- Heck eines 28-m-Panzers zur Wand hin - spaet und kraeftig waere zu spaet).
			for i=9,13 do
				y=LZ(i)
				a,b=i<12 and LG+y or 0,i<12 and (i-10)*3.5 or (i*2-25)*(BB/2+y)
				if i>11 and y<BB*1.5 or i<12 and y<HD and (HI(y) or i~=10 and y<(i<10 and fr or fl)-5) then
					H[i]={x+a*sn+b*cs,z+a*cs-b*sn}
				end
			end
			nf=nil
			for i,p in pairs(H) do
				a,b=p[1]-x,p[2]-z
				o,q=a*sn+b*cs,a*cs-b*sn
				if ab(a,b)>60 then H[i]=nil
				elseif A(q)<BB*1.5 and o>-LG-3 and o<LG+HD and (o<LG or vs>0) then
					if w*q>0 then w,vs,nf=0,Z(vs,VK),1 end
					if o>LG then
						if A(q)<BB/2+2 then
							w=w+(A(q)<1 and sd or -sg(q))*.4
							VL((o-LG-NS)/(HD-NS))
						end
					elseif A(q)<BB/2+BR then w=w-sg(q)*.15 end
				end
			end
			-- Patt: Drehen gewollt, aber die Ausweich-Lenkung hebt sie auf -> langsam gerade zurueck (sperrt dagegen
			-- das Gedaechtnis das Drehen (nf), erst langsam vor, bis der Punkt hinter dem Heck liegt)
			if A(e)>1/6 and A(w)<.15 and not nf then vs=rk>8 and -VK or 0 end
			-- Anfahrprobe (nur mit 'Richtung lernen'): nach dem Einschalten bis 2 s gerade anfahren (vorn zu: zurueck,
			-- beides zu: keine Probe), damit das Lernen eindeutige Befehle sieht; faehrt er sauber, ist sie vorbei
			if pb>0 then
				pb=pb-1
				r=fm>NS and 1 or rk>8 and -1 or 0
				w,vs=0,r*VK
				if r==0 or vf*r>.8 and A(yr)<.01 then pb=0 end
			end
			-- Hang/Schraeglage: langsamer; viel Roll -> talwaerts drehen (Hang dann vorn/hinten)
			vs=vs*cl(1-A(PR)/SM*.6,.3,1)
			if A(rl)>KM*.6 then w=w+sg(rl)*.2 end
			-- Wasser naht: je tiefer der Boden unter dem Bug (ga), desto langsamer - ab 10 m ueber 'Wasser Hoehe m'
			-- stufenlos bis Schleich-Tempo (50 t bergab brauchen Weg zum Bremsen)
			if tl>KM*.6 or al<WH then vs=I(vs,VK) end
			if gv then VL((ga-WH)/10) end
			-- Hindernis sicher (zu steil fuer einen Hang): merken, zurueck und wegdrehen; links und rechts eng
			-- (Gasse/Sackgasse): gerade zurueck, bis beide Seiten frei sind
			if hi then
				ux,uz,mr=x+sn*(LG+fm),z+cs*(LG+fm),LG+BR
				MK(ux,uz,10)
				mq=sl<BB and sr<BB or nil
				MV(-2*VK,mq and 0 or sd*.4,mq and 1200 or 180,mq and 5 or 4)
				zs=4
			end
		end
	end

	-- Batterie unter 30 % (wenn bekannt): Soll-Tempo nur 60 %
	if ba>0 and ba<.3 then vs=vs*.6 end
	-- Tempo-Regler (Vorsteuerung + PI auf das gemessene Tempo vorwaerts), Lenkung hat Vorrang
	if up then
		e=vs-vf
		if vs==0 and A(vf)<.5 then si=si*.9 end
		si=cl(si+e*.01,-.7,.7)
		u=cl(vs/VV+.3*e+si,-1,1)
		w=cl(w,-1,1)
		if A(u)+A(w)>1 then u=sg(u)*(1-A(w)) end
	end
	-- festgefahren? Befehl gross, aber weder Fahrt noch Drehung (3 s)
	if kon and hn<1 and mt<1 and (A(u)>.3 or A(w)>.3) and A(vf)<.3 and A(yr)<.005 then sk=sk+1 else sk=0 end
	lu=u
	RX=zs==8 and 4 or 1
	lo,ro=RA(lo,cl(u+w,-1,1)),RA(ro,cl(u-w,-1,1))
	-- Rohbefehle (vor Rad-Richtung und Lernen, ueber die Rampe geglaettet) fuer Fahrzeuge mit Lenkachsen
	ut,wt=RA(ut,cl(u,-1,1)),RA(wt,cl(w,-1,1))
	-- Richtung lernen (nur KI, eben, vorn frei), je 1,5 s lang:
	--  l1: beide Seiten gleich gerichtet befohlen, aber er faehrt (und beschleunigt) andersherum -> beide umdrehen
	--  l2: beide gleich gerichtet befohlen, aber er dreht statt zu fahren (Drehsinn zeigt die falsche Seite), oder
	--      Drehen befohlen (Seiten gegeneinander), aber er faehrt geradeaus (Fahrtrichtung zeigt die falsche Seite)
	--  Gebremst wird nie verwechselt: dabei wird das Tempo in Befehlsrichtung kleiner (av).
	av=av*.9+(vf-vp)*6
	vp=vf
	if RL>0 and kon and hn<1 and A(pt)<.014 and I(fl,fc,fr)>NS then
		g,e=sg(lo+ro),lo*ro>.04
		l1=e and vf*g<-.5 and av*g<.1 and l1+1 or 0
		l2=(e and vf*g<.5 and A(yr)>.015 or lo*ro<-.1 and A(lo+ro)<.3 and A(vf)>1 and A(yr)<.005) and l2+1 or 0
		if l1>90 then FL,FR,si,l1,l2=-FL,-FR,0,0,0 end
		if l2>90 then
			if (e and yr*g or vf*lo)>0 then FR=-FR else FL=-FL end
			l1,l2=0,0
		end
	end

	for i,v in ipairs({lo*FL,ro*FR,zs,gx,gz,dh,hx,hz,RV,#W,wi}) do S(i,v) end
	for i=1,8 do
		p=W[i] or {0,0}
		S(10+2*i,p[1]) S(11+2*i,p[2])
	end
	S(28,vs) S(29,wt) S(30,ut) S(31,hd) S(32,vf)
	O(1,kon or hn>0) O(2,kon and hn<1) O(3,pm) O(4,rp) O(5,FL~=QL) O(6,FR~=QR)
end
