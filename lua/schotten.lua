-- SCHOTTEN v1.0 - Figet Marena (Andre 08.10.: "wenn Wasser reinkommt automatisch alle Schotten zu, und falls man unten
-- ist, habe ich neben jede Tuer einen Knopf platziert, damit man sie manuell oeffnen kann")
-- 5 Schottwaende (vom Bug: z 3, Oberdeck z -13, z -15, z -29, z -53), je 2 Schiebetueren (Backbord + Steuerbord).
-- Alle zu/auf kommt vom Abteil-Chip (Feld am Monitor, Wasser-Automatik): jede Aenderung dort setzt alle Waende.
-- Kippschalter (2 Seiten) an der Wand: jede Aenderung (an->aus oder aus->an) schaltet die Tueren dieser Wand um.
-- Eingang (Composite): Bool 1 alle auf (Abteil-Chip), 2-6 Kippschalter Wand 1-5
-- Ausgang: Bool 1-5 Tueren Wand 1-5 auf (Open/Close; zugleich Zustand fuer die Anzeige)
D={}
K={}
function onTick()
	local g=input.getBool(1)
	if g~=ga then
		for k=1,5 do D[k]=g end
		ga=g
	end
	for k=1,5 do
		local b=input.getBool(1+k)
		if K[k]~=nil and b~=K[k] then D[k]=not D[k] end
		K[k]=b
		output.setBool(k,D[k])
	end
end
