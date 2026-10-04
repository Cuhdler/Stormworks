-- WELLEN v2 - Figet Marena: Milderung, wenn die Schrauben in hohen Wellen aus dem Wasser kommen.
--  Fahrt 02.10. (18:07 und 20:17): ueber 30 kn 12-14 % der Zeit Schrauben draussen. Dabei drehten die Motoren in 2 s
--  von 20 auf bis 49 RPS frei hoch, das Tempo vom Physik-Sensor fiel scheinbar von 64 auf 12 kn und sprang beim
--  Eintauchen in 0.3 s zurueck. Die Automatik schaltete dann hoch (Motor schnell, Tempo wieder da) und 2 s spaeter
--  wieder runter: 31 von 40 Schaltungen kamen so zustande.
-- Erkennung 'frei': Heck-Wasser (Liquid Meter auf Schrauben-Hoehe; kommt ueber den Flossen-Chip im Physik-Composite
--  Kanal 20, hier Kanal 23; 0 = keiner -> Skript tut nichts) mit 'Frei Vorhalt s' Vorhalt flacher als 'Frei unter m',
--  erst ab 'Wellen ab kn' (gemerktes Tempo: der Tempo-Wert bricht beim Austauchen scheinbar ein; im Stand meldete der
--  Messer beim Rollen auch mal 0.06 m). Keine Erkennung ueber die Drehzahl: die hielte normales Beschleunigen fuer
--  'frei' und wuerde das Gas festhalten.
-- Dann: (1) Drehzahl begrenzen statt abschalten: Gas-Abzug, sobald die schnellste Maschine mehr als 'Frei max RPS
--  Faktor' mal so schnell dreht wie vorher (20 % mehr: kein Gas; 0 = aus) - gegen das Hochdrehen bis 2.5-fach;
--  (2) Schaltsperre, solange 'frei' und 'Wellen Sperre s' danach.
-- v2 Drehzahl-Daempfung ('Drehzahl Daempfung' je RPS/s, 0 = aus; immer, nicht nur in Wellen): steigt die Drehzahl,
--  etwas weniger Gas (hoechstens 30 %) - gegen das Schaukeln in den kleinen Gaengen (Gang 4, Fahrt 02.10. 20:50: Tempo
--  37-52 kn, RPS 18-22.5 im 3-s-Takt bei gleichem Gas, Drehzahl laeuft 0.2 s vor dem Tempo). Gleichmaessig: kein Abzug.
-- Eingang: Composite wie das Schiffs-Skript (RPS Kanal 7/11/15/19, 23 Heck-Wasser)
-- Ausgang: Zahl 1 Gas-Abzug (0 = volles Gas erlaubt, 1 = kein Gas; Wellen-Grenze oder Daempfung, das groessere), Bool 1 Schaltsperre
N=input.getNumber
P=property.getNumber
m=math
-- Halte-Drehzahl (gelernt, solange keine Welle), Sperr-Ticks, Tiefen-Aenderung (m/s), gemerktes Tempo (m/s)
rh=0
wz=0
dv=0
vs=0
-- Drehzahl-Aenderung (RPS/s, geglaettet)
ra=0

function onTick()
	if not ini then
		ini=1
		fu,va,ws=P('Frei unter m'),P('Wellen ab kn')/1.944,P('Wellen Sperre s')*60
		wr,tv,fx,kd=P('Heck-Wasser Richtung'),P('Frei Vorhalt s'),P('Frei max RPS Faktor'),P('Drehzahl Daempfung')
	end
	local r=m.max(N(7),N(11),N(15),N(19))
	ra=ra+(((r0 or r)-r)*-60-ra)*.1
	r0=r
	local mw,fr=N(23),false
	-- Tempo merken: faellt hoechstens 1 m/s je Sekunde
	vs=m.max(N(5),vs-1/60)
	if mw~=0 then
		-- Tiefe der Schraube (+ = unter Wasser), Aenderung geglaettet, mit Vorhalt
		local d=-mw*wr
		dv=dv+(((d0 or d)-d)*-60-dv)*.1
		d0=d
		fr=vs>va and d+tv*dv<fu
	end
	if fr then wz=ws else wz=m.max(wz-1,0) end
	-- Drehzahl von vorher: folgt der schnellsten Maschine (ca. 0.8 s), steht waehrend der Welle
	if wz==0 then rh=rh+(r-rh)*.02 end
	local ab=(wz>0 and rh>3 and fx>0) and m.min(m.max((r/rh-fx)/.2,0),1) or 0
	output.setNumber(1,m.max(ab,m.min(m.max(ra*kd,0),.3)))
	output.setBool(1,wz>0)
end
