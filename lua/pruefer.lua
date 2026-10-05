-- LUA-PRUEFER - findet heraus, welche Lua-Funktionen Stormworks im Microcontroller anbietet (Andre 05.10.: "schreibe
-- alle Funktionen auf, die gehen und die nicht gehen"). Stuetzt sich nur auf das, was im Spiel sicher geht (pairs,
-- ipairs, string.format, string.gmatch, table.concat, table.remove, async.httpGet - in unseren Skripten bestaetigt).
-- 1. jeden globalen Namen und den Inhalt jeder globalen Tabelle auflisten (pairs)
-- 2. eine Liste bekannter Lua-Namen einzeln abfragen (falls die Umgebung Namen nur ueber __index liefert)
-- 3. Versuche einzeln: nur wenn die noetigen Namen da sind; mit pcall, wenn es pcall gibt; sonst vorher 'V:name'
--    senden und erst nach der Antwort ausfuehren - stuerzt das Skript ab, steht im Empfang ein V ohne OK
-- Alles geht per HTTP an tools/pruefer_empfang.py (Port 8769), Paket fuer Paket, das naechste erst nach der Antwort
-- (ohne Antwort nach 300 Ticks dasselbe nochmal - so geht es auch, wenn das PC-Programm erst spaeter startet).
F=string.format
PORT=8769
-- Warteschlange lokal: als globale Tabelle laege sie selbst in der Liste und wuechse beim Auflisten endlos
local Q={}
G=_ENV
if G==nil then G=_G end
TY=G and G.type
TS=G and G.tostring
PC=G and G.pcall
function txt(v)
	if v==nil then return "nil" end
	if v==true then return "true" end
	if v==false then return "false" end
	if TS then return TS(v) end
	return F("%s",v)
end
function wort(v)
	local t={}
	for w in string.gmatch(txt(v),"[%w_%.%-]+") do t[#t+1]=w end
	return table.concat(t,"_")
end
function art(v)
	if TY then return TY(v) end
	if v==nil or v==true or v==false then return txt(v) end
	for w in string.gmatch(txt(v),"(%a+):") do return w end
	return "wert"
end
function add(s) Q[#Q+1]=s end
-- gibt es G[a][b]?
function da(a,b)
	local t=G and G[a]
	if b==nil then return t~=nil end
	return art(t)=="table" and t[b]~=nil
end

add("A:umgebung_"..art(G).."_type_"..txt(TY~=nil).."_tostring_"..txt(TS~=nil).."_pcall_"..txt(PC~=nil))
add("A:version_"..wort(G and G._VERSION))
-- 1. alles, was pairs zeigt
if G then
	for k,v in pairs(G) do
		add("G:"..wort(k)..":"..art(v))
		if art(v)=="table" and v~=G then
			for k2,v2 in pairs(v) do add("T:"..wort(k).."."..wort(k2)..":"..art(v2)) end
		end
	end
end
-- 2. bekannte Namen einzeln
L={
	_={"assert","collectgarbage","dofile","error","getmetatable","ipairs","load","loadfile","loadstring","next","pairs",
		"pcall","print","rawequal","rawget","rawlen","rawset","require","select","setmetatable","tonumber","tostring",
		"type","unpack","xpcall","_G","_VERSION","module","setfenv","getfenv","gcinfo","newproxy","coroutine","debug","io",
		"math","os","package","string","table","utf8","bit32","bit","jit","input","output","property","screen","map",
		"async","httpReply","onTick","onDraw","server","dev"},
	string={"byte","char","dump","find","format","gmatch","gsub","len","lower","match","rep","reverse","sub","upper",
		"pack","packsize","unpack"},
	table={"concat","insert","move","pack","remove","sort","unpack","maxn","getn"},
	math={"abs","acos","asin","atan","atan2","ceil","cos","cosh","deg","exp","floor","fmod","frexp","huge","ldexp","log",
		"log10","max","maxinteger","min","mininteger","modf","pi","pow","rad","random","randomseed","sin","sinh","sqrt",
		"tan","tanh","tointeger","type","ult"},
	os={"clock","date","difftime","execute","exit","getenv","remove","rename","time","tmpname"},
	coroutine={"create","resume","running","status","wrap","yield","isyieldable"},
	debug={"log","traceback","getinfo","sethook","gethook","getlocal","setlocal"},
	input={"getNumber","getBool"},
	output={"setNumber","setBool"},
	property={"getNumber","getBool","getText"},
	screen={"setColor","drawClear","drawLine","drawCircle","drawCircleF","drawRect","drawRectF","drawTriangle",
		"drawTriangleF","drawText","drawTextBox","drawMap","setMapColorOcean","setMapColorShallows","setMapColorLand",
		"setMapColorGrass","setMapColorSand","setMapColorSnow","setMapColorRock","setMapColorGravel","getWidth","getHeight"},
	map={"screenToMap","mapToScreen"},
	async={"httpGet"},
}
for _,n in ipairs(L._) do
	add("N:"..n..":"..art(G and G[n]))
end
for lib,namen in pairs(L) do
	if lib~="_" then
		for _,n in ipairs(namen) do
			add("N:"..lib.."."..n..":"..(da(lib) and art(G[lib][n]) or "keine_bibliothek"))
		end
	end
end
add("A:liste_fertig")

-- 3. Versuche: {Name, noetige Namen {Bibliothek, Funktion}, Versuch}; der mit der String-Methode zuletzt (ohne pcall
-- nicht vorher pruefbar)
V={
	{"math_type_3",{{"math","type"}},function() return math.type(3) end},
	{"math_type_3_0",{{"math","type"}},function() return math.type(3.0) end},
	{"math_atan_2werte",{{"math","atan"}},function() return math.atan(1,-1) end},
	{"math_maxinteger",{{"math","maxinteger"}},function() return math.maxinteger end},
	{"string_rep",{{"string","rep"}},function() return string.rep("x",3) end},
	{"string_sub",{{"string","sub"}},function() return string.sub("abcdef",2,3) end},
	{"string_find",{{"string","find"}},function() return string.find("abcdef","cd") end},
	{"string_gsub",{{"string","gsub"}},function() return string.gsub("a b c"," ","+") end},
	{"table_insert",{{"table","insert"}},function() local t={} table.insert(t,1) table.insert(t,1,2) return t[1]..t[2] end},
	{"table_unpack",{{"table","unpack"}},function() local a,b=table.unpack({4,5}) return a+b end},
	{"unpack",{{"unpack"}},function() local a,b=unpack({4,5}) return a+b end},
	{"select",{{"select"}},function() return select("#",1,2,3) end},
	{"setmetatable",{{"setmetatable"}},function() local t=setmetatable({},{__index=function() return 7 end}) return t.a end},
	{"pcall_faengt_fehler",{{"pcall"}},function() local ok=pcall(function() local x=nil return x.y end) return ok end},
	{"error_mit_pcall",{{"pcall"},{"error"}},function() local ok,e=pcall(error,"test") return e end},
	{"math_random",{{"math","random"}},function() return math.random(1,1) end},
	{"os_time",{{"os","time"}},function() return os.time() end},
	{"os_clock",{{"os","clock"}},function() return os.clock() end},
	{"os_date",{{"os","date"}},function() return os.date("%Y") end},
	{"load",{{"load"}},function() return load("return 7")() end},
	{"loadstring",{{"loadstring"}},function() return loadstring("return 7")() end},
	{"coroutine",{{"coroutine","create"}},function() local c=coroutine.create(function() return 7 end) local ok,r=coroutine.resume(c) return r end},
	{"utf8_char",{{"utf8","char"}},function() return utf8.char(72,105) end},
	{"debug_log",{{"debug","log"}},function() debug.log("Lua-Pruefer") return 1 end},
	{"string_methode",{},function() local s="abc" return s:upper()..s:len() end},
}
vi=0
seq=0
warte=0
paket=nil
offen=nil
function httpReply(port,req,res)
	warte=0
	paket=nil
end
function onTick()
	if warte>0 then
		warte=warte+1
		if warte>300 then warte=0 end
		return
	end
	-- angekuendigter Versuch: erst jetzt, wo die Ankuendigung beim PC ist
	if not paket and offen then
		local v=offen
		offen=nil
		local ok,r=true,nil
		if PC then ok,r=PC(v[3]) else r=v[3]() end
		add((ok and "OK:" or "FEHLER:")..v[1]..":"..wort(r))
	end
	if not paket then
		if #Q==0 then
			vi=vi+1
			local v=V[vi]
			if v then
				local fehlt=nil
				for _,n in ipairs(v[2]) do
					if not da(n[1],n[2]) then fehlt=n[1]..(n[2] and "."..n[2] or "") end
				end
				if fehlt then
					add("FEHLT:"..v[1]..":"..fehlt)
				else
					add("V:"..v[1])
					offen=v
				end
			elseif vi==#V+1 then
				add("A:alles_fertig")
			else
				return
			end
		end
		local t,n={},0
		while #Q>0 and n<1200 do
			local s=table.remove(Q,1)
			t[#t+1]=s
			n=n+#s+1
		end
		seq=seq+1
		paket="/p?s="..seq.."&d="..table.concat(t,";")
	end
	async.httpGet(PORT,paket)
	warte=1
end
