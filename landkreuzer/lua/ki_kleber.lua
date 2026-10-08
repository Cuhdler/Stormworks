-- KI-KLEBER v1.0 - KI Landkreuzer: verbindet Schalter, Waffen und Fahr-KI (ein Skript im KI-Chip, laeuft vor KI_FAHREN).
-- Andre 08.10.: "komplett autonom" - darum heissen die Schalter im Instrumentenblock andersherum: aus = die KI darf.
--  Bool 1 'Waffen sperren' (aus = Master Arm an), Bool 3 'KI Pause' (aus = KI faehrt), Bool 4 'Nach Hause'.
-- Nach dem Spawnen wartet die Fahr-KI 'Start Verzoegerung s', die Waffen 'Waffen Verzoegerung s' (laenger: die KI
-- kennt keinen Freund - wer nach dem Spawnen noch in der Naehe ist, soll Zeit haben wegzukommen).
-- Ziel fuer die Fahr-KI: von den Zielen, die der Bildschirm-Chip den beiden Kanonen (BC, AC) gegeben hat, das naechste.
-- Die Vorgabe des Bildschirm-Chips ist Ost/Nord relativ zu uns (m) und Hoehe ueber dem Meer (m) - hier in die Welt
-- umgerechnet.
-- Schutzzone (einfache Freund-Kennung ohne Funk): liegt das Ziel einer Waffe (BC, AC, Flak L, Flak R) naeher als
-- 'Schutzzone m' am Startpunkt (dort steht die Werkbank, Andres Basis), gibt es keinen Master Arm - alle Waffen
-- schweigen, solange so ein Ziel aufgeschaltet ist. Solche Ziele faehrt die KI auch nicht an.
-- Bei wenig Batterie (0 < Ladung < 'Heim Batterie') faehrt die KI von selbst nach Hause (wie Schalter 'Nach Hause'),
-- statt irgendwo im Gelaende stehen zu bleiben; erst ab 'Heim Batterie' + 10 % wieder normal.
-- Eingang (Composite): Zahl 1-3 Physik x/Hoehe/z (ganzes Physik-Composite), ueberschrieben: 21-23 BC-Ziel Ost/Nord/Hoehe,
--  24-26 AC-Ziel, 27 Batterie (0..1, 0 = unbekannt), 28-30 Flak-L-Ziel, 31-33 Flak-R-Ziel; Bool 1-4 Instrumente,
--  5-8 BC/AC/Flak L/Flak R hat Ziel
-- Ausgang: Zahl 20-22 Ziel Welt x/z/Hoehe; Bool 1 KI an, 4 Ziel gueltig, 6 Nach Hause, 10 Master Arm (Waffen frei),
--  11 Schutzzone sperrt die Waffen
N=input.getNumber
B=input.getBool
S=output.setNumber
O=output.setBool
P=property.getNumber
tk=0

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
			local c=k<2 and 21+3*k or 22+3*k
			local e,n=N(c),N(c+1)
			local d=e*e+n*n
			if hx and (x+e-hx)^2+(z+n-hz)^2<zr*zr then
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
	O(10,tk>wv and not B(1) and not sp)
	O(11,sp)
end
