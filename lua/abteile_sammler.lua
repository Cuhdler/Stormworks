-- ABTEILE SAMMLER v1.1 - Figet Marena: fasst 9 Liquid Meter (Sensor 10-18, Heckhaelfte) fuer den Abteil-Chip zusammen.
-- Abwechselnd je Tick (Zahl 32 sagt welches):
--  Zahl 32 = 0: je Sensor Kapazitaet in 200 L * 1000 + Fuellung in Promille (0-999); -1 = nicht dicht (Kapazitaet
--   unter 100 L - dann misst der Sensor die Hoehe zum Wasser)
--  Zahl 32 = 1 (v1.1): je Sensor die Liter genau (fuer Sprit und Verbrauch - gepackt nur in 0,1-%-Schritten)
-- Eingang: Zahl 1-9 Liquid Level, 10-18 Fluid Capacity von Sensor 10-18
-- Ausgang: Zahl 1-9 (s. o.), 32 0 = gepackt / 1 = Liter
fr=false
function onTick()
	fr=not fr
	for i=1,9 do
		local l,c=input.getNumber(i),input.getNumber(9+i)
		output.setNumber(i,fr and l or c<100 and -1 or math.floor(c/200+.5)*1000+math.floor(math.max(0,math.min(1,l/c))*999+.5))
	end
	output.setNumber(32,fr and 1 or 0)
end
