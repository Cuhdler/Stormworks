-- ABTEILE v1.6 - Figet Marena (Andre 08.10.: "Liquid Meter und Schotten (elektrische Schiebetuer) sind eingebaut, der
-- andere grosse 9x5-Bildschirm soll fuer die Abteil-Anzeige sein"; Plan: alle Schotten auf einmal schliessen koennen)
-- v1.2: Schalter 'Auto water pumps' an + Wasser in einem Abteil ab 'Pumpe ab %' -> alle Lenzpumpen an ('Nachlauf s'
--  danach); Anzeige pumpt?, L/s, 'RAUS' = seit dem Laden.
-- v1.3/1.4: die 8 Sensoren unten im Doppelboden (y -19) messen die 8 Treibstofftanks - zaehlen nicht als Wasser; SPRIT
--  gesamt, je Tank ein Balken (Abschnitte Heck links -> Bug rechts, oben Steuerbord, unten Backbord), VERBR (Liter
--  genau: der Sammler schickt jeden zweiten Tick Liter statt gepackt, Zahl 32 = 1; Abnahme ueber 2 Minuten), Restzeit,
--  BATTERIE.
-- v1.5 (Andre: "'ABTEILE' steht ueber einem Strich, und die kleinen Punkte sind viel zu unuebersichtlich; wenn Wasser
--  reinkommt automatisch alle Schotten zu; neben jede Tuer ein Knopf"): kein Grundriss mehr - Abteile als Liste mit
--  Namen und Balken, Tueren je Schottwand ein Kaestchen (Zustand vom Schotten-Chip, der auch die Kippschalter an den
--  Waenden auswertet). 'Auto zu ab %' 0,5.
-- v1.6 (Andre: "was heisst OFFEN?" - nach C4 im Vorschiff): Sensor in keinem geschlossenen Raum (Kapazitaet 0) misst
--  die Hoehe zum Wasser: darunter = LECK (rot, zaehlt als voll: Alarm, Schotten zu, Pumpen), darueber = OFFEN (grau,
--  z. B. Luke). Getrennte Raeume einer Seite heissen 'BB'/'SB'; 10 Zeilen.
-- Abteile: Sensoren mit gleicher Kapazitaet und Fuellung liegen im selben Raum (offene Schotten verbinden Abteile), Name
--  vom ersten Sensor ('+' = mit weiteren verbunden). Wasser ab 'Auto zu ab %' -> alle Schotten zu (nur beim Auftreten).
-- Eingang (Composite): Zahl 1-9 Sensor 10-18 gepackt bzw. Liter (Sammel-Chip, Zahl 32 0/1), 10-18 Liquid Level Sensor
--  1-9, 19-27 Fluid Capacity Sensor 1-9, 28/29 Touch x/y, 30 Flow Rate aller Lenzpumpen (L/s, Summe im Chip),
--  31 Batterie-Ladung (0-1); Bool 1 Touch, 2 Knopf Schotten, 3 Schalter 'Auto water pumps', 4-8 Schottwand 1-5 auf
-- Ausgang: Bool 1 alle Schotten auf (an den Schotten-Chip), 2 Monitor an, 3 Pumpen an; Video an den Monitor 9x5
N=input.getNumber
B=input.getBool
P=property.getNumber
m=math
F=string.format
-- Sensoren 1-18 (Bug -> Heck): Art (1 Abteil, 2 Tank) und Name der Abteile
K={1,1,1,1,2,2,2,2,1,1,2,2,1,1,2,2,1,1}
NM={'BUG','BUG','VORSCHIFF','VORSCHIFF',0,0,0,0,'MITTE','MITTE',0,0,'SEITE','SEITE',0,0,'MASCHINE','MASCHINE'}
SD={'BB','SB','BB','SB',0,0,0,0,'BB','SB',0,0,'BB','SB',0,0,'BB','SB'}
TT={5,6,7,8,11,12,15,16}
C,Q,L={},{},{}
for i=1,18 do C[i],Q[i],L[i]=0,0,0 end
GL={}
TW={}
sa=true
tk=0
wz=false
nd=0
pn=0
pu=false
fl=0
rl=0
au=false
bt=0
sp=0
SB={}
vb=0

function onTick()
	if not ini then
		ini=1
		ga,ra,az=P('Gelb ab %')*10,P('Rot ab %')*10,P('Auto zu ab %')*10
		pa,pz=P('Pumpe ab %')*10,P('Nachlauf s')*60
	end
	tk=tk+1
	local ro=N(32)==1
	for i=1,18 do
		local v
		if i<10 then
			local l,c=N(9+i),N(18+i)
			L[i]=l
			v=c<100 and -1 or m.floor(c/200+.5)*1000+m.floor(m.max(0,m.min(1,l/c))*999+.5)
		elseif ro then
			L[i]=N(i-9)
		else
			v=N(i-9)
		end
		if v then
			if v<0 then
				C[i],Q[i]=0,0
			else
				C[i]=m.floor(v/1000)
				Q[i]=v-C[i]*1000
			end
		end
	end
	-- Abteile: gleiche Kapazitaet und Fuellung = ein Raum; {Kapazitaet, Promille, Name, Leck}. Nicht dicht: Hoehe zum
	-- Wasser unter null = LECK (zaehlt als voll), sonst OFFEN
	GL={}
	local mx=0
	nd=0
	for i=1,18 do
		if K[i]==1 then
			local g
			for _,h in ipairs(GL) do
				if h[1]==C[i] and h[2]==Q[i] and C[i]>0 then g=h end
			end
			if g then
				g[3]=g[5]==NM[i] and g[3]~=g[5]..'+' and g[5] or g[5]..'+'
			else
				local lk=C[i]==0 and L[i]<0
				GL[#GL+1]={C[i],Q[i],NM[i]..' '..SD[i],lk,NM[i]}
				if C[i]>0 then mx=m.max(mx,Q[i]) elseif lk then mx=999 else nd=nd+1 end
			end
		end
	end
	sp=0
	for _,i in ipairs(TT) do sp=sp+m.max(0,L[i]) end
	-- Verbrauch: Abnahme je Sekunde ueber bis zu 2 Minuten (ab 10 s)
	if tk%60==0 then
		SB[#SB+1]=sp
		if #SB>121 then table.remove(SB,1) end
		if #SB>10 then vb=m.max(0,(SB[1]-sp)/(#SB-1)) end
	end
	-- Schotten: Feld unten rechts antippen oder Knopf = alle umschalten; Wasser ab 'Auto zu ab %' = alle zu
	local w=az>0 and mx>=az
	if w and not wz then sa=false end
	wz=w
	local t=B(1) and N(28)>=200 and N(29)>=144
	if (t and not k1) or (B(2) and not k2) then sa=not sa end
	k1=t
	k2=B(2)
	for k=1,5 do TW[k]=B(3+k) end
	-- Pumpen: Schalter 'Auto water pumps' an und Wasser ab 'Pumpe ab %' (dann noch 'Nachlauf s')
	au=B(3)
	if au and mx>=pa then pn=pz end
	if not au then pn=0 end
	pu=pn>0
	if pn>0 then pn=pn-1 end
	fl=m.max(0,N(30))
	rl=rl+fl/60
	bt=N(31)
	output.setBool(1,sa)
	output.setBool(2,true)
	output.setBool(3,pu)
end

function fc(q,c)
	if c==0 then return 110,110,110 end
	if q>=ra then return 230,30,30 end
	if q>=ga then return 240,200,0 end
	return 0,170,70
end

function ft(q)
	if q<200 then return 230,30,30 end
	return 255,150,0
end

function bar(s,x,y,w,f,r,g,b)
	s.setColor(r//4,g//4,b//4)
	s.drawRectF(x,y,w,7)
	s.setColor(r,g,b)
	s.drawRectF(x,y,w*f,7)
end

function onDraw()
	local s=screen
	-- Abteile
	s.setColor(255,255,255)
	s.drawText(2,2,'ABTEILE')
	local lk=false
	for _,g in ipairs(GL) do lk=lk or g[4] end
	if wz and tk%40<20 then
		s.setColor(255,0,0)
		s.drawText(44,2,lk and 'LECK!' or 'WASSER!')
	end
	for k,g in ipairs(GL) do
		if k<=10 then
			local y=11+9*(k-1)
			s.setColor(200,200,200)
			s.drawText(2,y+1,g[3])
			if g[4] then
				bar(s,64,y,49,1,230,30,30)
				s.setColor(255,60,60)
				s.drawText(116,y+1,'LECK')
			elseif g[1]==0 then
				bar(s,64,y,49,0,110,110,110)
				s.setColor(150,150,150)
				s.drawText(116,y+1,'OFFEN')
			else
				local r,gg,b=fc(g[2],1)
				bar(s,64,y,49,g[2]/999,r,gg,b)
				s.setColor(r,gg,b)
				s.drawText(116,y+1,F('%.1f%%',g[2]/10))
			end
		end
	end
	-- Tueren je Schottwand (vom Bug)
	s.setColor(255,255,255)
	s.drawText(2,107,'TUEREN')
	for k=1,5 do
		local x=36+21*(k-1)
		if TW[k] then s.setColor(0,150,60) else s.setColor(170,20,20) end
		s.drawRectF(x,105,19,9)
		s.setColor(255,255,255)
		s.drawText(x+2,107,k..(TW[k] and 'AUF' or 'ZU'))
	end
	s.setColor(120,120,120)
	s.drawText(36,116,'BUG -> HECK')
	-- Sprit und Batterie (Tanks: Heck links, Bug rechts; oben Steuerbord, unten Backbord)
	local ka=0
	for _,i in ipairs(TT) do ka=ka+C[i]*200 end
	s.setColor(ft(ka>0 and sp/ka*1000 or 0))
	s.drawText(150,2,F('SPRIT %3d%% %7dL',m.floor(ka>0 and sp/ka*100+.5 or 0),m.floor(sp+.5)))
	s.setColor(200,200,200)
	s.drawText(150,13,'SB')
	s.drawText(150,22,'BB')
	for k,i in ipairs(TT) do
		local x,y=162+(4-(k+1)//2)*31,12+9*(k%2)
		local f=C[i]>0 and m.max(0,m.min(1,L[i]/(C[i]*200))) or 0
		local r,g,b=ft(Q[i])
		bar(s,x,y,29,f,r,g,b)
		s.setColor(255,255,255)
		s.drawText(x+(f<.995 and 6 or 4),y+1,F('%d%%',m.floor(f*100+.5)))
	end
	s.setColor(120,120,120)
	s.drawText(162,31,'HECK')
	s.drawText(267,31,'BUG')
	s.setColor(200,200,200)
	local h=vb>.01 and sp/vb/3600 or -1
	s.drawText(150,42,F('VERBR %4.1fL/S',vb)..(h>=0 and F(' %d:%02dH',m.floor(h),m.floor(h%1*60)) or ' --:--'))
	if bt>.5 then s.setColor(0,200,80) elseif bt>.2 then s.setColor(240,200,0) else s.setColor(230,30,30) end
	s.drawText(150,51,F('BATTERIE %3d%%',m.floor(bt*100+.5)))
	-- Pumpen
	if pu then s.setColor(0,170,255) else s.setColor(150,150,150) end
	s.drawText(150,66,F('PUMPEN %s %6.1fL/S',pu and 'AN ' or 'AUS',fl))
	s.setColor(255,255,255)
	s.drawText(150,75,F('RAUS %d L',m.floor(rl+.5)))
	if au then s.setColor(0,200,80) else s.setColor(230,120,0) end
	s.drawText(150,84,au and 'AUTO AN' or 'AUTO AUS (SCHALTER)')
	-- Feld: alle Schotten
	if sa then s.setColor(150,20,20) else s.setColor(0,120,50) end
	s.drawRectF(200,144,88,16)
	s.setColor(255,255,255)
	s.drawText(204,147,sa and 'ALLE ZU' or 'ALLE AUF')
	s.drawText(204,153,'SCHOTTEN')
end
