-- KI-LENKUNG v1.0 - KI Landkreuzer, nur fuer die Variante mit lenkbaren Achsen (vorn 2, hinten 2 auf senkrechten
-- Gelenken wie die Ruder der Figet Marena). Lange, schmale Fahrzeuge drehen mit Links/Rechts-Unterschied allein
-- schlecht (die Raeder muessen quer rutschen) - darum lenken vorn und hinten gegenlaeufig (Allrad-Lenkung), die
-- Mitte faehrt geradeaus; der Links/Rechts-Unterschied der Fahr-KI bleibt dazu.
-- Lenkwinkel aus dem Kurven-Befehl der Fahr-KI (Zahl 29, -1..1, + = rechts): Winkel = Befehl * 'Lenk Faktor', hoechstens
-- 'Lenk max Grad'; bei hohem Tempo weniger (ab 'Lenk Tempo m/s' halbiert). Robotic Pivot: Signal 1 = 90 Grad.
-- Rueckwaerts (Fahrbefehl Zahl 30 < 0) schlagen die Achsen andersherum ein: der Kurven-Befehl meint eine Drehung des
-- Panzers (+ = rechtsherum), und rueckwaerts dreht ein Rechts-Einschlag ihn linksherum - sonst arbeiten Lenkung und
-- Links/Rechts-Unterschied beim Zuruecksetzen gegeneinander.
-- Eingang: Ausgang von KI_FAHREN (Zahl 29 Kurve, 30 vorwaerts, 7? Tempo nicht noetig), ueberschrieben: Zahl 32 Tempo m/s
-- Ausgang: Zahl 1 Gelenke vorn, 2 Gelenke hinten (Rotation Target)
N=input.getNumber
S=output.setNumber
P=property.getNumber
w=0
function onTick()
	if not ini then
		ini=1
		lf,lm,lr,lt,lg=P('Lenk Faktor'),P('Lenk max Grad')/90,P('Lenk Richtung'),P('Lenk Tempo m/s'),P('Lenk Tempo Grad/s')/90/60
	end
	local k,v=N(29),math.abs(N(32))
	local z=k*lf*lm*(N(30)<0 and -1 or 1)
	if lt>0 then z=z*lt/math.max(lt,v) end
	z=math.max(-lm,math.min(lm,z))
	-- Gelenke folgen langsam (schont die Gelenke und die Raeder)
	w=w+math.max(-lg,math.min(lg,z-w))
	S(1,w*lr)
	S(2,-w*lr)
end
