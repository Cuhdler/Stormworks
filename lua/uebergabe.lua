-- UEBERGABE v1.0 - Figet Marena, zweiter Teil des Seeradar-Chips (Andre 06.10.): reicht die Bedienung des grossen
-- Bildschirms an die vorderen Kanonen und die Dachkamera weiter. Hat man auf dem Seeradar ein Ziel angetippt, waehrend
-- BC oder AC vorn gewaehlt war, setzt SEERADAR diese Kanone (Zahl 26) mit dem Ziel (Ost/Nord relativ, Hoehe ueber dem
-- Meer, Kennung) fuer 20 s ein: hier wird ihr Ziel in der Bedienung ersetzt (Kennung 3+4w, Ost/Nord/Hoehe 4+4w..6+4w),
-- 'Ziel da' (Bool 8+w) an, 'Feuer frei' (Bool 4+w) = Master Arm (Bool 1); ist sie die gewaehlte Waffe, schaut auch die
-- Dachkamera darauf (Zahl 3-6). Danach gilt wieder, was der Bildschirm-Chip vorgibt (Automatik).
-- Monitor 1x2 (liegt flach vor dem Sitz): Koordinaten X (Ost) / Y (Nord) der letzten Auswahl ohne Kanone.
-- Eingang (Composite): Bedienung vom Bildschirm-Chip (Zahl 1-25, Bool 1-16), ueberschrieben: Zahl 26 Kanone (0 keine,
--  1 BC, 2 AC), 27/28 Ost/Nord, 29 Hoehe, 30 Kennung, 31/32 Koordinaten X/Y; Bool 32 Koordinaten da
-- Ausgang: Bedienung (Zahl 1-25, Bool 1-16, wie oben ersetzt); Bool 17 immer an (Power Switch des Monitors 1x2);
--  Video an den Monitor 1x2
N=input.getNumber
B=input.getBool
S=output.setNumber
O=output.setBool
m=math
KX,KY,kv=0,0,false

function onTick()
	for i=1,25 do S(i,N(i)) end
	for i=1,16 do O(i,B(i)) end
	O(17,true)
	local w=m.floor(N(26)+.5)
	if w==1 or w==2 then
		S(3+4*w,N(30)) S(4+4*w,N(27)) S(5+4*w,N(28)) S(6+4*w,N(29))
		O(4+w,B(1)) O(8+w,true)
		if m.floor(N(2)+.5)==w then S(3,9) S(4,N(27)) S(5,N(28)) S(6,N(29)) end
	end
	KX,KY,kv=N(31),N(32),B(32)
end

function onDraw()
	local s=screen
	local w,h=s.getWidth(),s.getHeight()
	s.setColor(0,0,0)
	s.drawClear()
	s.setColor(0,200,120)
	local a=kv and string.format('%.0f',KX) or '-'
	local b=kv and string.format('%.0f',KY) or '-'
	if w<h then
		s.drawText(1,1,'X') s.drawText(1,8,a)
		s.drawText(1,18,'Y') s.drawText(1,25,b)
	else
		s.drawText(1,1,'X '..a) s.drawText(1,9,'Y '..b)
	end
end
