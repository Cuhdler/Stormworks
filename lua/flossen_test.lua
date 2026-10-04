-- FLOSSEN TEST - Figet Marena: alle 8 Ausgaenge (alle 12 Flossen) dauernd +0.7 (ca. 10 Grad), ohne Richtungs-Korrektur.
-- Zum Nachsehen, wohin bei gleichem Signal jede Flosse die Vorderkante dreht. Danach wieder den Flossen-Chip einsetzen.
function onTick()
	for i=1,8 do output.setNumber(i,.7) end
end
