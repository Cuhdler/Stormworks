-- WAFFENWAHL v1.2 - Figet Marena, kleiner Monitor 2x3 rechts neben dem Sitz (liegt flach): das Schiff von oben
-- (Umriss beim Bauen aus dem Fahrzeug gerechnet, Breite 2,2-fach), Bug zur Bildschirm-Seite +x, Steuerbord +y - so
-- liegt die Karte auf dem Monitor wie das Schiff selbst (von jeder Seite aus richtig herum).
-- Die 4 Waffen als Kreise in ihrer Farbe (BC orange, AC vorn lila, Flak L hellblau, Flak R weiss): hell = hat ein Ziel,
-- dunkel = keins; die gewaehlte mit weissem Ring; blinkt = feuert (Flak); ein Strich zeigt in die Richtung ihres Ziels.
-- Waffe antippen = waehlen (die gewaehlte nochmal = keine Waffe). Quadrat in der Ecke = Master Arm (rot = scharf;
-- geschaltet wird am Schalter, nicht hier). Keine Schrift - sie stuende fuer den Sitzenden quer.
-- v1.1: Eingaenge nur noch in onTick (das Spiel verbietet sie in onDraw: 'draw error 202'); Wunsch als Zahl; Master Arm.
-- Eingang: Ausgang 'Bedienung' des Bildschirm-Chips (Zahl 2 Waffe, 3+4w Ziel und 4+4w/5+4w Ost/Nord je Waffe, 23 Kurs,
--  24/25 Flak-Zustand; Bool 8+w Ziel da), ueberschrieben: Zahl 26/27 Touch x/y, Bool 13 Touch, 14 Master-Arm-Schalter
--  (v1.2: Flip Switch 1 am Instrument Panel)
-- Ausgang: Zahl 1 Wunsch, solange getippt wird (1 = keine Waffe, 2-5 = Waffe 1-4); Bool 1 Master Arm (vom Schalter
--  durchgereicht), 4 immer an (Monitor 'Power Switch')
N=input.getNumber
B=input.getBool
O=output.setBool
m=math
st=screen
pi2=m.pi*2
function C(r,g,b) st.setColor(r,g,b) end
-- Umriss: halbe Breite (Bloecke) je Spalte von 96, Bug rechts; der Bau-Schritt setzt die Werte ein
UM='0'
-- Waffen: Teil-Lage (z, x in Bloecken)
WP={{5,0},{31,0},{-105,-10},{-105,10}}
WF={{255,140,0},{190,90,255},{0,210,255},{255,255,255}}
ZA,KZ,KX=-155,92/224,.85
w,h=96,64
U={}
for v in string.gmatch(UM,'-?[%d%.]+') do U[#U+1]=tonumber(v) end
wq=0 tk=0 tl=false wf=0 ma=false
K,R,Z={},{},{}
function px(z) return (2+(z-ZA)*KZ)*w/96 end
function py(x) return h/2+x*KX*h/64 end

function onTick()
	tk=tk+1
	wf=N(2)
	ma=B(14)
	local hd=N(23)
	for a=1,4 do
		-- Ziel da? Richtung ab Bug; Flak-Zustand
		K[a]=B(8+a)
		R[a]=(m.atan(N(4+4*a),N(5+4*a))/pi2-hd)*pi2
		Z[a]=a>=3 and N(21+a) or 0
	end
	-- Wunsch beim Antippen festhalten, solange der Finger bleibt (sonst schaltet die Rueckmeldung ihn um)
	local tp=B(13)
	if tp and not tl then
		local tx,ty=N(26),N(27)
		wq=0
		for a=1,4 do
			if (tx-px(WP[a][1]))^2+(ty-py(WP[a][2]))^2<100 then wq=a==wf and 1 or a+1 end
		end
	elseif not tp then
		wq=0
	end
	tl=tp
	output.setNumber(1,wq)
	O(1,ma) O(4,true)
end

function onDraw()
	w,h=st.getWidth(),st.getHeight()
	C(0,15,10) st.drawRectF(0,0,w,h)
	C(40,70,80)
	for i=1,#U do
		local b=U[i]*KX*h/64
		if b>0 then st.drawRectF((i-1)*w/96,h/2-b,w/96+1,2*b) end
	end
	for a=1,4 do
		local x,y=px(WP[a][1]),py(WP[a][2])
		local f=WF[a]
		if K[a] then C(f[1],f[2],f[3]) st.drawLine(x,y,x+16*m.cos(R[a]),y+16*m.sin(R[a])) end
		local d=K[a] and 1 or .35
		if Z[a]==3 and tk%10<5 then d=.15 end
		C(f[1]*d,f[2]*d,f[3]*d) st.drawCircleF(x,y,5)
		if a==wf then C(255,255,255) st.drawCircle(x,y,7) end
	end
	if ma then C(220,30,20) st.drawRectF(w-12,2,10,10) else C(90,90,90) st.drawRect(w-12,2,9,9) end
end
