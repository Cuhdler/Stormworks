-- KI-KLEBER v1.0 - KI Landkreuzer: verbindet Schalter, Waffen und Fahr-KI (ein Skript im KI-Chip, laeuft vor KI_FAHREN).
-- Andre 08.10.: "komplett autonom" - darum heissen die Schalter im Instrumentenblock andersherum: aus = die KI darf.
--  Bool 1 'Waffen sperren' (aus = Master Arm an), Bool 3 'KI Pause' (aus = KI faehrt), Bool 4 'Nach Hause'.
-- Nach dem Spawnen wartet die Fahr-KI 'Start Verzoegerung s', die Waffen 'Waffen Verzoegerung s' (laenger: die KI
-- kennt keinen Freund - wer nach dem Spawnen noch in der Naehe ist, soll Zeit haben wegzukommen).
-- Ziel fuer die Fahr-KI: von den Zielen, die der Bildschirm-Chip den beiden Kanonen (BC, AC) gegeben hat, das naechste.
-- Die Vorgabe des Bildschirm-Chips ist Ost/Nord relativ zu uns (m) und Hoehe ueber dem Meer (m) - hier in die Welt
-- umgerechnet.
-- Schutzzone (einfache Freund-Kennung ohne Funk): liegt das Ziel einer Waffe (BC, AC, Flak L, Flak R) naeher als
-- 'Schutzzone m' am Startpunkt (dort steht die Werkbank, Andres Basis) oder an einem Freund-Punkt der Karte (Finger
-- 1,5 s halten), gibt es keinen Master Arm - alle Waffen schweigen, solange so ein Ziel aufgeschaltet ist. Solche
-- Ziele faehrt die KI auch nicht an.
-- Bei wenig Batterie (0 < Ladung < 'Heim Batterie') faehrt die KI von selbst nach Hause (wie Schalter 'Nach Hause'),
-- statt irgendwo im Gelaende stehen zu bleiben; erst ab 'Heim Batterie' + 10 % wieder normal.
-- Eingang (Composite): Zahl 1-3 Physik x/Hoehe/z (ganzes Physik-Composite), ueberschrieben: 21-23 BC-Ziel Ost/Nord/Hoehe,
--  24-26 AC-Ziel, 27 Batterie (0..1, 0 = unbekannt), 28/29 Flak-L-Ziel Ost/Nord, 30/31 Flak-R-Ziel, 4-11 Freund-Punkte
--  der Karte (Ost/Nord), 12 ihre Zahl; Bool 1-4 Instrumente, 5-8 BC/AC/Flak L/Flak R hat Ziel
-- Auto-Chaff (an den Schutz-Chip) nur, wenn die Waffen frei sind UND eine Waffe ein Ziel hat: meldet der Radarwarner
-- auch die eigenen Radare (auf dem Schiff noch offen), verschiesst er so nicht alle Werfer ins Leere.
-- Ausgang: Zahl 20-22 Ziel Welt x/z/Hoehe; Bool 1 KI an, 4 Ziel gueltig, 6 Nach Hause, 10 Master Arm (Waffen frei),
--  11 Schutzzone sperrt die Waffen, 12 Auto-Chaff, 13 immer an (schaltet die Laser ein)
N=input.getNumber
B=input.getBool
S=output.setNumber
O=output.setBool
P=property.getNumber
tk=0

-- in einer Schutzzone? (Heimat oder Freund-Punkt)
function FZ(a,b)
	local r=zr*zr
	if hx and (a-hx)^2+(b-hz)^2<r then return true end
	for i=0,N(12)-1 do
		if (a-N(4+2*i))^2+(b-N(5+2*i))^2<r then return true end
	end
end

function onTick()
	if not ini then
		ini=1
		sv,wv,hb,zr=P('Start Verzoegerung s')*60,P('Waffen Verzoegerung s')*60,P('Heim Batterie'),P('Schutzzone m')
	end
	tk=tk+1
	local x,z=N(1),N(3)
	if tk==30 then hx,hz=x,z end
	local los=tk>sv
	local bd,bx,bz,bh,sp
	for k=0,3 do
		if B(5+k) then
			local c=k<2 and 21+3*k or 24+2*k
			local e,n=N(c),N(c+1)
			local d=e*e+n*n
			if FZ(x+e,z+n) then
				sp=true
			elseif k<2 and (not bd or d<bd) then
				bd,bx,bz,bh=d,x+e,z+n,N(c+2)
			end
		end
	end
	S(20,bx or 0)
	S(21,bz or 0)
	S(22,bh or 0)
	O(1,los and not B(3))
	O(4,bd~=nil)
	local b=N(27)
	if b>0 and b<hb then hl=true elseif b>hb+.1 or b<=0 then hl=false end
	O(6,B(4) or hl)
	local wf=tk>wv and not B(1)
	O(10,wf and not sp)
	O(11,sp)
	O(12,wf and (B(5) or B(6) or B(7) or B(8)))
	O(13,true)
end
