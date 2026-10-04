-- SCHREIBER v1 - Figet Marena, Waffen-Schreiber (Andre 03.10.: "einen Schreiber, der dir ALLE Daten gibt"): schickt das
-- ganze Composite, an dem er haengt, an tools/waffen_logger.py auf dem PC ('Schreiber Port', 0 = aus).
-- Jeden 'Schreiber Takt'-ten Tick eine Zeile: Tick, Zahl 1-32 (0 als leer), Bool 1-32 als Bits; je 5 Zeilen ein Paket
-- per HTTP, ein neues erst nach der Antwort (2 s ohne: wieder senden). Laeuft der PC nicht mit, wird nichts gestaut
-- (hoechstens 40 Zeilen). Der Bau-Schritt setzt Q (Name der Messstelle, z. B. 'r3' = Mast-Radar 3 roh).
-- Eingang: das Composite, das aufgeschrieben werden soll
N=input.getNumber
B=input.getBool
F=string.format
Q='x'
LB={}
lw=false
wt=0
tk=0

function httpReply(port,req,res)
	lw=false
end

function onTick()
	if not ini then
		ini=1
		lp=property.getNumber('Schreiber Port')
		tt=math.max(1,property.getNumber('Schreiber Takt'))
	end
	if lp<=0 then return end
	tk=tk+1
	if tk%tt==0 then
		local z,b={tk},0
		for i=1,32 do
			local v=N(i)
			z[#z+1]=v==0 and '' or F('%.7g',v)
		end
		for i=1,32 do if B(i) then b=b+2^(i-1) end end
		z[#z+1]=F('%.0f',b)
		LB[#LB+1]=table.concat(z,',')
		if #LB>40 then table.remove(LB,1) end
	end
	if lw then
		wt=wt+1
		if wt>120 then lw=false end
	elseif #LB>=5 then
		async.httpGet(lp,'/w?q='..Q..'&d='..table.concat(LB,';',1,5))
		for i=1,5 do table.remove(LB,1) end
		lw=true
		wt=0
	end
end
