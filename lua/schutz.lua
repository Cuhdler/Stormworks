-- SCHUTZ v1.0 - Figet Marena: Auto-Chaff und Lenzpumpen (Andre 04.10.: "Chaff hinzugefuegt, beide Seiten sollen
-- gleichzeitig abfeuern, du baust Auto-Chaff (Radar Detector unter der Kamera); Auto-Chaff ueber den Instrumentenblock
-- mit dem anderen Flip Switch an und aus; ausserdem Wasserpumpen eingebaut").
-- Zwei Ketten zu je 60 Werfern (Launch Passthrough -> Launch des naechsten): ein kurzer Puls auf den ersten feuert den
-- ersten noch vollen der Kette. Auto-Chaff (Schalter an): meldet der Radar Detector eine Ortung, feuern beide Ketten
-- gleichzeitig eine Salve, danach alle 'Chaff Abstand s' wieder, solange die Ortung anhaelt - hoechstens 'Chaff je
-- Ortung' Salven; erst wenn 'Chaff Pause s' lang keine Ortung kam, gilt die naechste als neu. Nach 60 Salven ist leer.
-- Pumpen: folgen dem Schalter 'Water Pumps'.
-- Eingang (Composite): Out Signal des Instrumentenblocks (Bool 1 Master Arm, 2 Zielkorrektur, 3 Auto-Chaff, 4 Pumpen),
--  ueberschrieben: Bool 5 Radar Detector
-- Ausgang: Bool 1 Chaff links (Launch des ersten Werfers), 2 Chaff rechts, 3 Pumpen an
B=input.getBool
O=output.setBool
P=property.getNumber
ns=0
nk=0
ab=0
fr=0

-- SCHREIBER v2 (in allen Waffen-Skripten gleich; Andre 04.10.: "der Log muss ALLES sagen, sonst ist es ein Ratespiel"):
-- je Tick eine Zeile mit dem, was das Skript sieht und entscheidet (Tick + Werte, leer = 0); alle LT Ticks ein Paket
-- an tools/waffen_logger.py. Der Bau-Schritt setzt LQ (Name), LT, LO. LG(Kennbuchstabe, Werte-Tabelle, Anzahl).
-- Gesendet wird erst, wenn die Antwort aufs letzte Paket da ist (hoechstens 300 Ticks warten), fruehestens LT Ticks
-- danach. w = wie viele Ticks die Antwort aufs vorige Paket brauchte (-1 = keine).
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
		ca,cn,cp=P('Chaff Abstand s')*60,P('Chaff je Ortung'),P('Chaff Pause s')*60
	end
	local au,pu,de=B(3),B(4),B(5)
	-- Ortung: neue Folge erst nach cp Ticks ohne Ortung
	if de then fr=0 else fr=fr+1 end
	if fr>cp then nk=0 end
	ab=ab-1
	local sv=au and de and nk<cn and ns<60 and ab<=0
	if sv then
		ns,nk,ab=ns+1,nk+1,ca
	end
	O(1,sv) O(2,sv) O(3,pu)
	-- Schreiber: Auto-Chaff an, Ortung, Salve, Salven gesamt, Salven dieser Ortung, Ticks ohne Ortung, Pumpen an,
	-- Master Arm, Zielkorrektur
	LG('',{au,de,sv,ns,nk,fr,pu,B(1),B(2)},9)
	LF()
end
