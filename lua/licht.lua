-- LICHT v1.0 - Figet Marena (Andre 08.10.: "jede Menge Lichter - sie sollen immer an sein, nur Tag und Nacht
-- unterschiedlich hell; die im Steuerungsraum sollen bei Bedrohung rot werden")
-- 55 kleine RGB-Lampen, immer an. Helligkeit nach der Uhr (Bauteil 'Clock': 0 = Mitternacht, 0,5 = Mittag): von
--  'Tag ab Uhr' bis 'Nacht ab Uhr' 'Hell Tag', sonst 'Hell Nacht'; Uebergang ueber 'Daemmerung h'. Farbe 'Farbe R/G/B'.
-- Steuerungsraum (4 Deckenlampen): wie die anderen; bei Bedrohung (Lage-Chip Bool 25, wie 'BEDROHUNG' am grossen
--  Bildschirm) rot ('Rot hell' mal Tag/Nacht-Helligkeit), bleibt 'Rot halten s' nach der letzten Meldung.
-- Eingang (Composite): Lage-Ausgang, ueberschrieben Zahl 1 Uhr
-- Ausgang: Zahl 1-3 Licht Rot/Gruen/Blau (alle Lampen), 4-6 Steuerungsraum Rot/Gruen/Blau (0-1)
N=input.getNumber
B=input.getBool
S=output.setNumber
P=property.getNumber
function cl(v,a,b) return math.max(a,math.min(b,v)) end
rt=0

function onTick()
	if not ini then
		ini=1
		ta,na,dm=P('Tag ab Uhr'),P('Nacht ab Uhr'),P('Daemmerung h')
		ht,hn=P('Hell Tag'),P('Hell Nacht')
		R,G,Bl=P('Farbe R'),P('Farbe G'),P('Farbe B')
		rh=P('Rot hell')
		rz=P('Rot halten s')*60
	end
	local h=N(1)*24
	local d=cl((h-ta)/dm+.5,0,1)*cl((na-h)/dm+.5,0,1)
	local k=hn+(ht-hn)*d
	if B(25) then rt=rz elseif rt>0 then rt=rt-1 end
	S(1,R*k)
	S(2,G*k)
	S(3,Bl*k)
	if rt>0 then
		S(4,rh*k)
		S(5,0)
		S(6,0)
	else
		S(4,R*k)
		S(5,G*k)
		S(6,Bl*k)
	end
end
