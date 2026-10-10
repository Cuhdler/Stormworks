-- SCHOTTEN v2.0 - Figet Marena (Andre 08.10.: "wenn Wasser reinkommt automatisch alle Schotten zu, und falls man unten
-- ist, habe ich neben jede Tuer einen Knopf platziert, damit man sie manuell oeffnen kann"; 10.10.: "gedacht war pro
-- Tuer ein Knopf" - v1.0 hatte nur die 5 Knoepfe an Backbord, jeder schaltete beide Tueren seiner Wand)
-- 5 Schottwaende (vom Bug: z 3, Oberdeck z -13, z -15, z -29, z -53), je 2 Schiebetueren (Backbord + Steuerbord), neben
-- jeder Tuer ein Kippschalter (2 Seiten, in der Wand).
-- Alle zu/auf kommt vom Abteil-Chip (Feld am Monitor, Wasser-Automatik): jede Aenderung dort setzt alle 10 Tueren.
-- Kippschalter: jede Aenderung (an->aus oder aus->an) schaltet seine eigene Tuer um.
-- Eingang (Composite): Bool 1 alle auf, 2-6 Kippschalter Backbord Wand 1-5, 7-11 Kippschalter Steuerbord Wand 1-5
-- Ausgang: Bool 1-5 Wand 1-5 offen (eine ihrer Tueren auf; fuer die Anzeige im Abteil-Chip), 6-10 Tuer Backbord Wand 1-5
--  auf, 11-15 Tuer Steuerbord Wand 1-5 auf (Open/Close)
D={}
K={}
function onTick()
	local g=input.getBool(1)
	if g~=ga then
		for j=1,10 do D[j]=g end
		ga=g
	end
	for j=1,10 do
		local b=input.getBool(1+j)
		if K[j]~=nil and b~=K[j] then D[j]=not D[j] end
		K[j]=b
		output.setBool(5+j,D[j])
	end
	for k=1,5 do output.setBool(k,D[k] or D[5+k]) end
end
