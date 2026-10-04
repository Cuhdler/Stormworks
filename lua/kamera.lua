-- KAMERA v2.2 - Figet Marena, Dachkamera fuer alle Waffen (Andre 04.10.: "eine bewegliche Kamera auf dem Dach, die fuer
-- alle Waffen ist: waehle ich die BC, schaut die Kamera auf das Ziel der BC"; Camera Stabilized auf dem Bruecken-Dach
-- (0,33,-15), schaut beim Spawnen senkrecht nach oben). Sie schaut direkt auf das Ziel der gewaehlten Waffe (ohne
-- Vorhalt) und zoomt nach der Entfernung: ein Ziel von 'Ziel See m' (BC/AC) bzw. 'Ziel Luft m' (Flaks) fuellt
-- 'Bildanteil' der SICHTBAREN Breite (der grosse Monitor zeigt das Kamerabild nur im mittleren Drittel). Ohne Waffe
-- oder Ziel: geradeaus, waagerecht, weit.
-- v1.1 (Andres Test 04.10. 15:01: "die Kamera hat sich nicht mal bewegt" - Log: Pivot/Pitch sind TEMPO-Eingaenge mit
--  Totzone 0,1 (darunter nichts, darueber 0,106 U/s je 1, ~8 Ticks Verzug); Composite 4/5 = Neigung/Drehung des Kopfs
--  in U relativ zum Spawnen. Alle Neigungs-Befehle v1.0 lagen unter 0,1 - sie blieb oben; gedreht hat sie sich um 40
--  Grad, beim Blick in den Himmel unsichtbar. Laser ohne Treffer meldet 4000): Regler auf die Rueckmeldung mit
--  Totzonen-Ausgleich und Vorsteuerung. MESSFAHRT beim Spawnen (~6 s): (2) mit Befehl 1 nach unten neigen, bis 5 Grad
--  unter waagerecht - misst dabei das Tempo je Befehl und auf welche Seite sie kippt; (3) Laser-Treffer auf dem Meer
--  abwarten (trifft er das eigene Schiff oder nichts: eine halbe Runde weiterdrehen und nochmal); (4) etwas drehen,
--  zweiter Treffer: daraus, wohin 'Drehung 0' zeigt und in welche Richtung sie dreht. Ohne Treffer gelten
--  'Drehung 0 ab Bug U' und 'Drehung Vorzeichen'.
-- v1.2 (Andre 04.10.: "auf dem Bildschirm ist das Bild der Kamera hoch-unten invertiert" - Messfahrt kippte mit +1
--  nach vorn, ueber die 'Stirn' der Kamera): gekippt wird mit 'Kipp Befehl' (-1: zur anderen Seite, danach schaut sie
--  mit einer halben Drehung nach vorn - das Bild steht richtig).
-- v2.0 (Andre 04.10.: "Korrektur bei ausgewaehlter Waffe - je weiter die Sicht vom Fadenkreuz weg, desto weiter
--  korrigiert er in die Richtung; wie beim Swifter, aber nur, wenn der Mittelpunkt meines Sichtfelds in einem kleinen
--  Kreis um das Fadenkreuz ist"; wie ein Joystick, bleibt): Blick X/Y vom Sitz (U) gegen 'Blick Mitte X/Y Grad' (wohin
--  du schaust, wenn du aufs Fadenkreuz siehst). Liegt der Blick im Kreis ('Kreis Grad') und ist eine Waffe gewaehlt,
--  wandert ihr Zielpunkt in Blickrichtung - am Kreisrand um 'Korrektur Tempo' der sichtbaren Bildbreite je Sekunde,
--  innen langsamer, in 'Totzone Grad' gar nicht. Die Korrektur bleibt je Waffe stehen (Ausgang 'Korrektur': Zahl 2+2w
--  seitlich, 3+2w Hoehe, U; + = rechts / hoch). Hotkey 6 kurz = Korrektur der gewaehlten Waffe auf 0; 2 s halten =
--  die Blick-Mitte ist jetzt hier (bis zum naechsten Spawnen). Zeichnet ins Kamerabild: Kreis um die Bildmitte (gelb,
--  solange korrigiert wird) und eine orange Marke, wohin die Waffe gegenueber dem Ziel jetzt zielt.
-- v2.1 (Andre: "der Kreis muss doppelt so gross sein, und das Kreuz muss sich wesentlich langsamer bewegen"; im Test
--  ohne Ziel - Kamera weit, Tempo hing an der sichtbaren Bildbreite, nach 2 s Anschlag): Tempo fest 'Korrektur mrad/s'
--  am Kreisrand (innen linear weniger), unabhaengig vom Zoom; Kreis 8 Grad / 16 Pixel, Totzone 0,8 Grad. Hauptkreuz
--  bleibt auf dem Ziel, das Kreuz der Korrektur zeigt, wohin die Waffe (mit ihrem Vorhalt) jetzt zielt.
-- v2.2 (Andre: "die Zielkorrektur soll standardmaessig deaktiviert sein und mit einem Knopf neben Master Arm aktiviert
--  werden"): Knopf 'Aim correction' im Instrumentenblock (Bool 3 hier). Aus: Blick aendert nichts, Ausgang 'Korrektur'
--  0, kein Kreis/keine Marke; die gemerkten Korrekturen gelten wieder, sobald er an ist.
-- Eingang (Composite): 'Bedienung' des Bildschirm-Chips (Zahl 2 Waffe 0-4, 3 Ziel-Platz, 4-6 Ziel Ost/Nord relativ zum
--  Schiff / Hoehe ueber dem Meer, 23 Kurs U im Uhrzeigersinn), ueberschrieben: 7-11 Kamera-Composite (Laser-Ziel x, y,
--  z, Neigung U, Drehung U), 12/13 Blick X/Y vom Sitz (U), 26-28 Physik x / Hoehe / z, 29 Nick, 30 Roll, 32 Laser-
--  Entfernung m; Bool 1 Hotkey 6, 2 Sitz besetzt, 3 Knopf Zielkorrektur. Video: Dachkamera (wird durchgereicht, darueber gezeichnet)
-- Ausgang: Zahl 1 Pivot Rotation, 2 Pitch Rotation, 3 Field of View (0 weit .. 1 eng), 4-11 Korrektur je Waffe;
--  Bool 1 Laser an
N=input.getNumber
B=input.getBool
S=output.setNumber
O=output.setBool
P=property.getNumber
m=math
pi2=m.pi*2
function wr(v) return (v+.5)%1-.5 end
function cl(v,a,b) return m.max(a,m.min(b,v)) end
-- Tempo r (U/s) -> Befehl mit Totzonen-Ausgleich
function vb(r) return m.abs(r)<4e-4 and 0 or (r>0 and 1 or -1)*m.min(1,dz+m.abs(r)/kv) end
ph=0
ti=0
cP,cY=0,0
s4=1
nv=0
KX={0,0,0,0}
KY={0,0,0,0}
h6=0
ak=false
wa=0

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
		vf,vu=P('Kamera vor Physik m'),P('Kamera ueber Physik m')
		gS,gL,ba,sa=P('Ziel See m'),P('Ziel Luft m'),P('Bildanteil'),P('Sichtbar Anteil')
		f0,f1,f2=P('FOV ohne Ziel rad'),P('FOV weit rad'),P('FOV eng rad')
		dz,kv,kb=P('Totzone'),P('Tempo je Befehl U/s'),P('Kipp Befehl')
		o5,s5=P('Drehung 0 ab Bug U'),P('Drehung Vorzeichen')
		kfv=f0
		ph=P('Messfahrt')>0 and 1 or 9
		mx,my,bxs,bys=P('Blick Mitte X Grad')/360,P('Blick Mitte Y Grad')/360,P('Blick X Richtung'),P('Blick Y Richtung')
		kr,kd,kt,kp=P('Kreis Grad'),P('Totzone Grad'),P('Korrektur mrad/s')/1000,P('Kreis Pixel')
	end
	local wf,zp,E,Nn,U,hd=N(2),N(3),N(4),N(5),N(6),N(23)
	local lx,ly,lz,k4,k5=N(7),N(8),N(9),N(10),N(11)
	local px,py,pz,nk,rl,ld=N(26),N(27),N(28),N(29),-N(30),N(32)
	local h=hd*pi2
	-- Kamera in der Welt (Physik-Sensor + Versatz nach vorn/oben)
	local cx,cz,cy=px+vf*m.sin(h),pz+vf*m.cos(h),py+vu
	-- Laser-Treffer (Welt-Ort; falls relativ zur Kamera gemeldet: passt die Entfernung dann besser) -> Richtung rel. Bug
	if m.abs(m.sqrt((lx-cx)^2+(ly-cy)^2+(lz-cz)^2)-ld)>m.abs(m.sqrt(lx*lx+ly*ly+lz*lz)-ld) then lx,ly,lz=lx+cx,ly+cy,lz+cz end
	local lb=ld>25 and ld<3500 and ly<cy-1 and wr(m.atan(lx-cx,lz-cz)/pi2-hd) or nil
	ti=ti+1
	-- Ziel: Richtung relativ zum Bug, Hoehe gegen das Deck, Entfernung
	local da=wf>0 and zp>0 and ph==9
	local rel,ed,R=0,0,0
	if da then
		local dE,dN,dU=px+E-cx,pz+Nn-cz,U-cy
		local ho=m.sqrt(dE*dE+dN*dN)
		R=m.sqrt(ho*ho+dU*dU)
		rel=wr(m.atan(dE,dN)/pi2-hd)
		local th=rel*pi2
		ed=m.atan(dU,ho)/pi2-(nk*m.cos(th)-rl*m.sin(th))
	end
	-- Soll in Kopf-Winkeln: Kippung aus der Senkrechten u (zur gemessenen Seite s4), Drehung q
	local u,us,q=s4*k4,.25-ed,s5*wr(rel-o5)
	if ph==1 then
		-- 1: kurz warten (Eingaenge da)
		cP,cY=0,0
		if ti>=30 then ti,ph,u0=0,2,k4 end
	elseif ph==2 then
		-- 2: mit 'Kipp Befehl' nach unten neigen bis 5 Grad unter waagerecht; Tempo je Befehl und Kipp-Seite messen
		cP,cY=kb,0
		if ti==40 then u1=k4 end
		if ti==70 then kv=m.max(m.abs(k4-u1)*2/(1-dz),.01) s4=k4>=u0 and 1 or -1 end
		if ti>70 and s4*k4>=.264 or ti>900 then cP,ti,ph,nv=0,0,3,0 end
	elseif ph==3 then
		-- 3: Laser-Treffer auf dem Meer abwarten; sonst halbe Runde weiterdrehen (hoechstens dreimal)
		cP,cY=0,0
		if ti>=40 then
			if lb then b0,y0,ti,ph=lb,k5,0,4
			else
				cY=1
				ys=ys or k5
				if m.abs(k5-ys)>=.5 or ti>800 then ys,ti,nv=nil,0,nv+1 if nv>2 then ph=9 end end
			end
		end
	elseif ph==4 then
		-- 4: etwas drehen (Befehl 0,6), zweiter Treffer -> wohin Drehung 0 zeigt, Drehrichtung
		cP=0
		cY=m.abs(k5-y0)<.05 and .6 or 0
		if cY==0 then
			t4=t4 or ti
			if ti-t4>=25 then
				if lb and m.abs(wr(lb-b0))>.01 then
					s5=wr(lb-b0)*(k5-y0)>0 and 1 or -1
					o5=wr(b0-s5*y0)
				end
				ti,ph=0,9
			end
		end
	else
		-- im Betrieb: Regler auf die Rueckmeldung (2,5/s) + Vorsteuerung mit dem Drehtempo des Ziels
		local du,dq=0,0
		if qq then du,dq=(us-qu)*60,wr(q-qq)*60 end
		cP=vb(2.5*(us-u)+du)*s4
		cY=vb(2.5*wr(q-k5)+dq)
	end
	qu,qq=us,q
	-- Zoom: Ziel fuellt ba der sichtbaren Breite (sa des Bildes)
	local fv=f0
	if da then fv=(wf<=2 and gS or gL)/(ba*sa*m.max(R,50)) end
	kfv=kfv*(cl(fv,f2,f1)/kfv)^.08
	-- Korrektur (v2.0): Blick gegen die Mitte in Grad (+ rechts / hoch); Hotkey 6 kurz = 0, 2 s = Mitte lernen
	local bx,by=(N(12)-mx)*bxs*360,(N(13)-my)*bys*360
	local bd=m.sqrt(bx*bx+by*by)
	wa=wf
	if B(1) and en then
		h6=h6+1
		if h6==120 then mx,my=N(12),N(13) end
	else
		if h6>0 and h6<60 and wf>0 then KX[wf],KY[wf]=0,0 end
		h6=0
	end
	en=B(3)
	ak=en and wf>0 and B(2) and bd<kr and h6==0
	if ak and bd>kd then
		local v=(bd-kd)/(kr-kd)*kt/60/bd
		KX[wf]=cl(KX[wf]+bx*v,-.1,.1)
		KY[wf]=cl(KY[wf]+by*v,-.1,.1)
	end
	S(1,cY) S(2,cP) S(3,cl((f1-kfv)/(f1-f2),0,1))
	for w=1,4 do S(2+2*w,en and KX[w]/pi2 or 0) S(3+2*w,en and KY[w]/pi2 or 0) end
	O(1,true)
	-- Schreiber: Phase, Waffe, Ziel-Platz, Ziel Ost/Nord/Hoehe, Entfernung, Richtung rel. Bug U, Hoehe gegen Deck U,
	-- Befehl Drehung/Neigung, Bildwinkel rad, Rueckmeldung Neigung/Drehung U, Laser-Entfernung, Laser-Treffer x/y/z,
	-- Eichung (Kipp-Seite, Tempo je Befehl, Drehung 0 ab Bug, Drehrichtung, Versuche), Laser-Richtung rel. Bug, Kurs
	LG('',{ph,wf,zp,E,Nn,U,R,rel,ed,cY,cP,kfv,k4,k5,ld,lx,ly,lz,s4,kv,o5,s5,nv,lb,hd,N(12),N(13),bx,by,ak,
		wf>0 and KX[wf],wf>0 and KY[wf],h6,mx*360,my*360,en},36)
	LF()
end
-- Kamerabild + Kreis um die Bildmitte (gelb = korrigiert) + Marke, wohin die gewaehlte Waffe gegenueber dem Ziel zielt
function onDraw()
	if wa==0 or not en then return end
	local sw,sh=screen.getWidth(),screen.getHeight()
	local cx,cy,q=sw/2,sh/2,sw/kfv
	if ak then screen.setColor(255,220,0) else screen.setColor(0,200,80,160) end
	screen.drawCircle(cx,cy,kp)
	local x,y=cx+cl(KX[wa]*q,-sw/6,sw/6),cy-cl(KY[wa]*q,-sh/2,sh/2)
	screen.setColor(255,120,0)
	screen.drawLine(x-3,y,x+4,y)
	screen.drawLine(x,y-3,x,y+4)
end
