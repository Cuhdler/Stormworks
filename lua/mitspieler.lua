-- MITSPIELER v1.0 - Figet Marena, Bildschirm-Chip: Mehrspieler-Hilfe vor BILD (Andre 10.10.)
-- Im Mehrspieler rechnet jeder PC die Lua-Skripte selbst, ihr Zustand wird nicht abgeglichen (Entwickler, Geometa
-- #22188). Beim Mitspieler findet seine eigene Lagezentrale kaum Ziele; vom Host kommen nur ab und zu Zwischenstaende,
-- die seine Chips gleich wieder ueberschreiben - Zielliste, Radar und Kamera-Zoom blitzen nur kurz auf.
-- Erkennung ueber den Takt der Lagezentrale (Bool 21-24, zaehlt je Tick 0..15): beim Host laeuft er lueckenlos, dann
-- reicht dieses Skript alles unveraendert durch. Beim Mitspieler bringt jeder Zwischenstand den Takt des Hosts mit -
-- ein Sprung (bleibt der Takt stehen, haengt nur die Lage - kein Sprung). Ab 4 Spruengen in 60 s gilt 'Mitspieler'
-- (60 s lang, jeder Sprung verlaengert). Ein Stand, dessen Takt nicht zum eigenen passt, ist vom Host: seine 5 Plaetze und die Bedrohung gelten dann bis 'MP halten s' und ersetzen
-- die eigene (leere) Lage. Oben auf dem Radar steht 'MP <Alter des Stands>S'. 'Mehrspieler-Hilfe' 0 = nur durchreichen.
-- (Eine Erkennung an kurz auftauchenden Kennungen ging nicht: auch beim Host pendeln Ziele zwischen Platz und Topf.)
-- Eingang: Composite wie BILD (Lage: Zahl 3k-2..3k Ziel k, 15+k Kennung; Bool k lebt, 5+k Luft, 15+k Ziel fuer die
--  Waffen, 21-24 Takt, 25 Bedrohung; dazu Flak, Wahl, Sitz), Video von BILD. Ausgang: dasselbe Composite, Video mit
--  Anzeige.
N=input.getNumber
B=input.getBool
S=output.setNumber
O=output.setBool
m=math
tk=0
CM=-1
SL=0
HT=-1e9
SP={}

function onTick()
	if not ini then
		ini=1
		mp=property.getNumber('Mehrspieler-Hilfe')>0
		hz=property.getNumber('MP halten s')*60
	end
	tk=tk+1
	local n,b={},{}
	for i=1,32 do n[i]=N(i) b[i]=B(i) end
	-- Takt: Sprung = weder stehen geblieben (Lage haengt) noch um eins weiter; laenger als 1 s ohne Sprung = eigener Takt
	local c=(b[21] and 1 or 0)+(b[22] and 2 or 0)+(b[23] and 4 or 0)+(b[24] and 8 or 0)
	if PC and c~=PC and c~=(PC+1)%16 then
		SL=tk
		SP[#SP+1]=tk
		if #SP>4 then table.remove(SP,1) end
		if mp and #SP>=4 and tk-SP[1]<=3600 then CM=tk+3600 end
	end
	PC=c
	EL=EL and (EL+1)%16 or c
	if tk-SL>60 then EL=c end
	if c~=EL then
		-- Stand vom Host: alle Plaetze und die Bedrohung merken
		H={}
		for k=1,5 do H[k]={n[3*k-2],n[3*k-1],n[3*k],n[15+k],b[k],b[5+k],b[15+k]} end
		HB=b[25]
		HT=tk
	end
	cm=tk<CM
	ag=tk-HT
	if cm and ag<hz then
		for k=1,5 do
			local h=H[k]
			n[3*k-2],n[3*k-1],n[3*k],n[15+k]=h[1],h[2],h[3],h[4]
			b[k],b[5+k],b[15+k]=h[5],h[6],h[7]
		end
		b[25]=HB
	end
	for i=1,32 do S(i,n[i]) O(i,b[i]) end
end

function onDraw()
	if cm then
		local x=m.floor(screen.getWidth()/3)/2-16
		screen.setColor(0,0,0)
		screen.drawRectF(x-1,0,34,7)
		screen.setColor(255,190,0)
		screen.drawText(x,1,ag<6000 and string.format('MP %dS',m.floor(ag/60)) or 'MP --')
	end
end
