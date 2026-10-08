-- KI-KLEBER v1.0 - KI Landkreuzer: verbindet Schalter, Waffen und Fahr-KI (ein Skript im KI-Chip, laeuft vor KI_FAHREN).
-- Andre 08.10.: "komplett autonom" - darum heissen die Schalter im Instrumentenblock andersherum: aus = die KI darf.
--  Bool 1 'Waffen sperren' (aus = Master Arm an), Bool 3 'KI Pause' (aus = KI faehrt), Bool 4 'Nach Hause'.
-- Nach dem Spawnen wartet die Fahr-KI 'Start Verzoegerung s', die Waffen 'Waffen Verzoegerung s' (laenger: die KI
-- kennt keinen Freund - wer nach dem Spawnen noch in der Naehe ist, soll Zeit haben wegzukommen).
-- Ziel fuer die Fahr-KI: von den Zielen, die der Bildschirm-Chip den beiden Kanonen (BC, AC) gegeben hat, das naechste.
-- Die Vorgabe des Bildschirm-Chips ist Ost/Nord relativ zu uns (m) und Hoehe ueber dem Meer (m) - hier in die Welt
-- umgerechnet.
-- Eingang (Composite): Zahl 1-3 Physik x/Hoehe/z (ganzes Physik-Composite), ueberschrieben: 21-23 BC-Ziel Ost/Nord/Hoehe,
--  24-26 AC-Ziel; Bool 1-4 Instrumente, 5 BC hat Ziel, 6 AC hat Ziel
-- Ausgang: Zahl 20-22 Ziel Welt x/z/Hoehe; Bool 1 KI an, 4 Ziel gueltig, 6 Nach Hause, 10 Master Arm (Waffen frei)
N=input.getNumber
B=input.getBool
S=output.setNumber
O=output.setBool
P=property.getNumber
tk=0

function onTick()
	if not ini then
		ini=1
		sv,wv=P('Start Verzoegerung s')*60,P('Waffen Verzoegerung s')*60
	end
	tk=tk+1
	local x,z=N(1),N(3)
	local los=tk>sv
	local bd,bx,bz,bh
	for k=0,1 do
		if B(5+k) then
			local e,n=N(21+3*k),N(22+3*k)
			local d=math.sqrt(e*e+n*n)
			if not bd or d<bd then bd,bx,bz,bh=d,x+e,z+n,N(23+3*k) end
		end
	end
	S(20,bx or 0)
	S(21,bz or 0)
	S(22,bh or 0)
	O(1,los and not B(3))
	O(4,bd~=nil)
	O(6,B(4))
	O(10,tk>wv and not B(1))
end
