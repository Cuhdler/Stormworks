-- FOLGESCHALTER v1.0 (Teil 1) - Andre 06.10.: jedes neue "an" am Eingang schaltet den naechsten Ausgang fuer 'Puls s'
-- (4 s) an: erstes "an" -> Ausgang 1, zweites -> Ausgang 2, ... bis 'Anzahl Ausgaenge' (54). Danach nichts mehr (oder
-- mit 'Nach dem letzten von vorn' 1 wieder ab Ausgang 1).
-- Ein "an" zaehlt nur beim Wechsel aus (an bleibt an = ein Mal) und fruehestens 'Sperre s' (2 s) nach dem letzten.
-- Eingang an = Bool-Eingang an oder Zahl-Eingang mindestens 0,5. Reset an = wieder bei Ausgang 1 anfangen, alle aus.
-- Eingang (Composite, im Chip zusammengefuehrt): Bool 1 Eingang, Bool 2 Reset, Zahl 1 Eingang als Zahl
-- Ausgang: Bool 1-32 = Ausgang 1-32 (Teil 1); Zahl 1-22 = Ausgang 33-54 als 0/1 (ueber das Kabel 'Kette' an Teil 2),
--  Zahl 32 = wie viele Ausgaenge schon geschaltet wurden
N=input.getNumber
B=input.getBool
P=property.getNumber
n=0
sp=0
alt=false
T={}

function onTick()
	if not ini then
		ini=1
		pl=P('Puls s')*60
		sl=P('Sperre s')*60
		an=math.min(P('Anzahl Ausgaenge'),54)
		vr=P('Nach dem letzten von vorn')
		for i=1,54 do T[i]=0 end
	end
	if B(2) then
		n=0
		for i=1,54 do T[i]=0 end
	end
	for i=1,54 do
		if T[i]>0 then T[i]=T[i]-1 end
	end
	local e=B(1) or N(1)>=.5
	sp=sp-1
	if e and not alt and sp<=0 then
		if n>=an and vr>0 then n=0 end
		if n<an then
			n=n+1
			T[n]=pl
			sp=sl
		end
	end
	alt=e
	for i=1,54 do
		local on=T[i]>0
		if i<=32 then output.setBool(i,on) else output.setNumber(i-32,on and 1 or 0) end
	end
	output.setNumber(32,n)
end
