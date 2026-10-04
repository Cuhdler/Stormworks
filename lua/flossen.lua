-- FLOSSEN v1.6 - Figet Marena: 12 Steuerflossen (Control Fin Medium) halten das Schiff gerade (Nick, Roll) und daempfen
--  das Huepfen in Wellen. Je Flosse -1..1 = +-14 Grad. + = Vorderkante hoch = Auftrieb nach oben, bei ALLEN Flossen
--  (Test-Chip 02.10.: +0.7 an alle -> alle Vorderkanten oben, auch die gespiegelten rechts) -> 'Richtung links' und
--  'Richtung rechts' 1. (v1.1/v1.2 hatten je eine Seite umgedreht - das war falsch.)
--  'Flossen Test' 1: im Stand alle Flossen auf Vorderkante hoch (zum Nachsehen, ob alle gleich stehen).
--  Langsamer Ausgleich (I) gegen dauernde Schlagseite/Trimm; vordere Flossen nur Nick/Hub ('Roll vorn Anteil' 0).
-- Eingang (Composite): Physik-Sensor (2 Hoehe, 13 Tempo m/s, 15 Nick-Neigung, 16 Quer-Neigung; Neigung in Umdrehungen),
--  20 Heck-Wasser (Liquid Meter am Heck auf Schrauben-Hoehe; 0 = keiner; Vorzeichen siehe 'Heck-Wasser Richtung')
-- Ausgang: Zahl 1 vorn links, 2 vorn rechts, 3 hinten links, 4 hinten rechts, 5 Mitte links, 6 Mitte rechts,
--  7/8 vorn-Mitte links/rechts (v1.5, (+-9,-21,-2): uebernehmen das Rollen vorn)
-- v1.5 (Fahrt 02.10. 17:40): Schrauben drehten frei, obwohl das Schiff gerade lag und das Heck sogar sank - das Wasser
--  zog unter dem Heck weg. Mit Messer: der Chip lernt die normale Tiefe in Fahrt (langsamer Mittelwert); laeuft die
--  Schraube (mit Vorhalt) 'Wasser Spiel m' flacher als normal oder flacher als 'Schraube tief min m', druecken hinten
--  und Mitte das Heck runter ('Wasser Druck' je m). Die hinteren rollen nur noch 'Roll hinten Anteil' (sie hoben
--  dabei oft eine Schraube an), das Rollen machen Mitte und vorn-Mitte.
-- v1.6 (Fahrt 02.10. 18:07): Andres Messer (seitlich eingebaut) meldet die TIEFE (+ unter Wasser, in Fahrt 1.5-2.5 m;
--  sobald er negativ wird, drehen die Motoren frei hoch) - v1.5 las das andersherum und drueckte hinten und Mitte die
--  ganze Fahrt voll runter. -> 'Heck-Wasser Richtung' -1. Feste Mindesttiefe statt gelernter Normaltiefe (die konnte
--  sich hochschaukeln: drueckt bei 'flacher als im Schnitt' -> Schnitt wird tiefer -> drueckt mehr).
-- Regel: Nase zu hoch -> vorn ab, hinten auf (vorn nur 'Vorn Nick Anteil': den Bug runterdruecken hebelt das Heck
--  hoch); rechte Seite zu tief -> rechts auf, links ab (vorn nur 'Roll vorn Anteil'). Dazu je die Drehrate (D).
--  Wellen (v1.4, Andre: das Wichtigste ist, dass hinten die Schrauben im Wasser bleiben): der Chip rechnet aus Steigen
--  und Nicken, wie schnell sich Heck und Bug heben (Abstand zum Sensor 'Heck/Bug Abstand m'), schaut 'Vorhalt s'
--  voraus (die Flossen wirken verzoegert) und drueckt das Heck kraeftig runter, sobald es steigen wird ('Heck runter'),
--  schwach hoch, wenn es faellt ('Heck hoch'); den Bug daempft 'Hub D'. Der I-Anteil ruht bei mehr als 3 Grad Nick
--  oder Roll (Kurven, Wellen), sonst laedt er sich in langen Kurven auf und uebersteuert danach.
--  Die Kraft einer Flosse waechst mit dem Tempo im Quadrat: Verstaerkung (Bezugs-Tempo/Tempo)^2, hoechstens
--  'Verstaerkung max'; unter 'Ab Tempo kn' (oder 'Flossen an' 0) stehen die Flossen gerade.
-- Fahrtenschreiber ('Log Port', 0 = aus): je Tick Tick, Tempo, Nick, Roll, Nickrate, Rollrate, Steigen, Verstaerkung,
--  Flosse 1-8, Heck-Wasser, per HTTP an tools/logger.py (Port 8767 -> logs/flossen_*.csv); neues Paket erst nach der Antwort.
N=input.getNumber
S=output.setNumber
P=property.getNumber
F=string.format
m=math
function cl(v,a,b) return m.max(a,m.min(b,v)) end

U={0,0,0,0,0,0,0,0}
ip=0
ir=0
ah=0
wh=0
dt=0
dr0=nil
q=0
p=0
w=0
LB={}
lw=false
tk=0
wt=0

function httpReply(port,req,res)
	lw=false
end

function onTick()
	-- Nick + = Nase hoch, Roll + = rechte Seite unten (Grad), Hoehe, Tempo
	local th,ro,z,v=N(15)*360,-N(16)*360,N(2),N(13)
	if not ini then
		ini=1
		an,dir,tz=P('Flossen an'),P('Flossen Richtung'),P('Ziel Nick Grad')
		dl,dr=P('Richtung links'),P('Richtung rechts')
		ki,kri,te=P('Nick I')/60,P('Roll I')/60,P('Flossen Test')
		kp,kd,kr,krd,kh=P('Nick P'),P('Nick D'),P('Roll P'),P('Roll D'),P('Hub D')
		vb,va,gm=P('Bezugs-Tempo kn')/1.944,P('Ab Tempo kn')/1.944,P('Verstaerkung max')
		fr,mn,fp=P('Roll vorn Anteil'),P('Mitte Nick Anteil'),P('Vorn Nick Anteil')
		hr,hh,tv=P('Heck runter'),P('Heck hoch'),P('Vorhalt s')
		lb,ls=P('Bug Abstand m'),P('Heck Abstand m')
		rh,rm,nm=P('Roll hinten Anteil'),P('Roll vorn-Mitte Anteil'),P('Nick vorn-Mitte Anteil')
		dab,kw,wr=P('Schraube tief min m'),P('Wasser Druck'),P('Heck-Wasser Richtung')
		lp=P('Log Port')
		t0,r0,z0=th,ro,z
	end
	-- Raten aus der Aenderung je Tick (Grad/s, m/s), geglaettet
	q=q+((th-t0)*60-q)*.2
	p=p+((ro-r0)*60-p)*.2
	w=w+((z-z0)*60-w)*.2
	t0,r0,z0=th,ro,z
	local g=(an>0 and v>va) and m.min((vb/v)^2,gm) or 0
	-- np + : Nase zu hoch, nr + : rechte Seite zu tief, h + : steigt
	-- Bug und Heck: Steigen (m/s), Heck geglaettet beschleunigt -> Heck in tv Sekunden
	local qr=q*m.pi/180
	local wb,ws=w+lb*qr,w-ls*qr
	ah=ah+((ws-wh)*60-ah)*.1
	wh=ws
	local wv=ws+tv*ah
	-- I-Anteil (Trimm/Schlagseite) nur in Fahrt und bei kleinen Abweichungen, begrenzt
	if g>0 and m.abs(th-tz)<3 and m.abs(ro)<3 then ip=cl(ip+ki*(th-tz),-.6,.6) ir=cl(ir+kri*ro,-.6,.6) end
	local np=(kp*(th-tz)+kd*q)*g+(g>0 and ip or 0)
	local nr=(kr*ro+krd*p)*g+(g>0 and ir or 0)
	-- hb + : Bug steigt; hs + : Heck wird steigen (dann kraeftig runter)
	local hb=kh*wb*g
	local hs=(wv>0 and hr or hh)*wv*g
	-- Heck-Wasser: Tiefe d der Schraube (m), Aenderung geglaettet, in tv Sekunden; flacher als 'Schraube tief min m'
	--  -> Heck runter. 'Heck-Wasser Richtung' -1: der Messer meldet die Tiefe (+ = unter Wasser)
	local hw,mw=0,N(20)
	if mw~=0 then
		local d=-mw*wr
		dt=dt+(((dr0 or d)-d)*-60-dt)*.1
		dr0=d
		local dp=d+tv*dt
		if g>0 and dp<dab then hw=kw*(dab-dp)*m.max(g,1) end
	end
	local soll={-np*fp-nr*fr-hb,-np*fp+nr*fr-hb,np-nr*rh-hs-hw,np+nr*rh-hs-hw,mn*(np-hs)-nr-hw,mn*(np-hs)+nr-hw,-np*nm-nr*rm,-np*nm+nr*rm}
	for i=1,8 do
		U[i]=cl((te>0 and g==0) and .7 or soll[i],-1,1)
		-- Ausgang 1, 3, 5 links, 2, 4, 6 rechts
		S(i,U[i]*dir*(i%2==1 and dl or dr))
	end
	if lp>0 then
		tk=tk+1
		LB[#LB+1]=F('%d,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.2f',tk,v,th,ro,q,p,w,g,U[1],U[2],U[3],U[4],U[5],U[6],U[7],U[8],mw)
		if #LB>12 then table.remove(LB,1) end
		if lw then
			wt=wt+1
			if wt>120 then lw=false end
		elseif #LB>=4 then
			async.httpGet(lp,'/l?d='..table.concat(LB,';'))
			lw=true
			wt=0
			LB={}
		end
	end
end
