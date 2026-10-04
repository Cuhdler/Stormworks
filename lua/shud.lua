-- SHUD v2.5 - Helm-Anzeige der Schiffsfuehrung (Headset Video am Steuersitz), 4 Motoren, Fahrtenschreiber
-- v2.5 (03.10., Andre: der Helm verdeckt den grossen Bildschirm): normal nur eine Zeile ganz unten (Gang, Hebel, Tempo,
--  Kurs, Ruder) und darueber nur HEISS/AUSFALL eines Motors; Hotkey 4 = alles wie bisher (die Gemisch-Seite Q/Luft/Treib ist weg)
-- Eingang: Ausgang von SCHIFF (15 an + Gang: Uebersetzung*10*10000+Gang*100+Automatik*10+1, 16 Hebel (-: rueckwaerts), 17 Tempo m/s, 18 Kurs, 19 Ruder, 20 Bugstrahl,
--  je Motor L1, L2, R1, R2 zwei gepackte Zahlen ab 21: RPS*10*1000+Temperatur, Zustand*1e6+Gas%*1000+(Gemisch+2)*100,
--  29-32 je Motor Q*10*1000+Luft-Drossel %; Bool 8 = Hotkey 4 (alles anzeigen))
-- Fahrtenschreiber ('Log Port', 0 = aus): jeden Tick eine Zeile (Tick, Zahl 1-32 und Bool 1-12 als Bits, roh) - je 4
--  Zeilen per HTTP an tools/logger.py auf dem PC (localhost), das sie entpackt und als CSV in logs/ schreibt. Ein neues
--  Paket geht erst raus, wenn das letzte bestaetigt ist (2 s ohne Antwort: wieder senden). Helm unten: LOG OK n.
N=input.getNumber
F=string.format
m=math
d={}
LB={}
lw=false
tk=0
wt=0
lo=0

function httpReply(port,req,res)
	lw=false
	lo=lo+1
end

function onTick()
	for i=15,32 do d[i]=N(i) end
	p2=input.getBool(8)
	lp=lp or property.getNumber('Log Port')
	if lp>0 then
		tk=tk+1
		local z,b={tk},0
		for i=1,32 do z[#z+1]=F('%.7g',N(i)) end
		for i=1,12 do if input.getBool(i) then b=b+2^(i-1) end end
		z[#z+1]=F('%d',b)
		LB[#LB+1]=table.concat(z,',')
		if #LB>12 then table.remove(LB,1) end
		if lw then
			wt=wt+1
			if wt>120 then lw=false end
		elseif #LB>=4 then
			async.httpGet(lp,'/l?d='..table.concat(LB,';'))
			lw=true
			wt=0
			LB={}
		end
	end
end

function onDraw()
	if not d[15] then return end
	local s=screen
	local h=s.getHeight()
	local w=d[17]
	local v=m.floor(d[15]+.5)
	local zs={'OK','HEISS','AUSFALL','TEMP','LEER','KUPPELT','---'}
	local nm={'L1','L2','R1','R2'}
	if not p2 then
		-- schmal: eine Zeile ganz unten (der Blick auf den grossen Bildschirm bleibt frei), darueber nur Warnungen
		s.setColor(0,255,90)
		s.drawText(2,h-7,v>0 and F('G%d %s %s%3.0f%% %4.1fKN K%03.0f R%+3.0f',m.floor(v/100)%100,m.floor(v/10)%10==1 and 'AUTO' or 'HAND',
			d[16]<0 and 'RUECK' or 'VOR',m.abs(d[16])*100,w*1.944,d[18],d[19]*100) or F('MOTOREN AUS (H1) %4.1fKN K%03.0f',w*1.944,d[18]))
		local x=2
		for e=1,4 do
			local z=m.floor(m.floor(d[20+2*e]+.5)/1e6)
			if z==1 or z==2 then
				s.setColor(255,60,0)
				local t=nm[e]..' '..zs[z+1]
				s.drawText(x,h-14,t)
				x=x+5*#t+6
			end
		end
		return
	end
	-- H4: alles (wie bis v2.4 Seite 1)
	s.setColor(0,255,90)
	s.drawText(2,2,v>0 and F('MOTOREN AN  GANG %d X%.1f %s',m.floor(v/100)%100,m.floor(v/10000)/10,m.floor(v/10)%10==1 and 'AUTO' or 'HAND') or 'MOTOREN AUS  (HOTKEY 1)')
	s.drawText(2,10,F('HEBEL%4.0f%% %s',m.abs(d[16])*100,d[16]<0 and 'RUECK' or 'VOR'))
	s.drawText(2,18,F('TEMPO%4.0f KMH %4.1f KN',w*3.6,w*1.944))
	s.drawText(2,26,F('KURS %03.0f',d[18]))
	s.drawText(2,34,F('RUDER%+4.0f%%  BUG%+4.0f%%',d[19]*100,d[20]*100))
	for e=1,4 do
		local a,b=m.floor(d[19+2*e]+.5),m.floor(d[20+2*e]+.5)
		local z,tp,mx=m.floor(b/1e6),a%1000,b%1000/100-2
		-- rot: heiss/Ausfall, gelb: Temperatur-Regler, dunkel: kein Motor
		if z==1 or z==2 then s.setColor(255,60,0) elseif z==3 then s.setColor(255,200,0) elseif z==6 then s.setColor(0,110,50) else s.setColor(0,255,90) end
		s.drawText(2,36+8*e,F('%s RPS%5.1f T%4.0f GAS%4.0f%% MIX%5.2f %s',nm[e],m.floor(a/1000)/10,tp,m.floor(b%1e6/1000),mx,zs[z+1] or '?'))
	end
	-- Fahrtenschreiber
	if lp and lp>0 then
		s.setColor(0,160,60)
		s.drawText(2,78,lo>0 and F('LOG OK %d',lo) or 'LOG: PC-PROGRAMM AUS?')
	end
end
