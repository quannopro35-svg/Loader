--// DARK HUB UI LIBRARY (REDZ STYLE)
local TweenService = game:GetService("TweenService")
local Players = game:GetService("Players")
local plr = Players.LocalPlayer

-- MAIN GUI
local Gui = Instance.new("ScreenGui", plr.PlayerGui)
Gui.Name = "DarkHub"
Gui.ResetOnSpawn = false

-- COLORS
local C = {
	BG = Color3.fromRGB(18,18,18),
	BG2 = Color3.fromRGB(28,28,28),
	STROKE = Color3.fromRGB(60,60,60),
	ACCENT = Color3.fromRGB(120,80,255),
	TEXT = Color3.fromRGB(230,230,230)
}

-- ICON TOGGLE
local Icon = Instance.new("ImageButton", Gui)
Icon.Size = UDim2.fromScale(0.08,0.12)
Icon.Position = UDim2.fromScale(0.02,0.4)
Icon.Image = "rbxassetid://7734053495"
Icon.BackgroundColor3 = C.BG
Icon.Active, Icon.Draggable = true, true
Instance.new("UICorner", Icon).CornerRadius = UDim.new(1,0)
Instance.new("UIStroke", Icon).Color = C.ACCENT

-- MAIN FRAME
local Main = Instance.new("Frame", Gui)
Main.Size = UDim2.fromScale(0.6,0.65)
Main.Position = UDim2.fromScale(0.2,0.18)
Main.BackgroundColor3 = C.BG
Main.Active, Main.Draggable = true, true
Instance.new("UICorner", Main).CornerRadius = UDim.new(0,14)
Instance.new("UIStroke", Main).Color = C.STROKE

-- TOGGLE MENU
Main.Visible = true
Icon.MouseButton1Click:Connect(function()
	Main.Visible = not Main.Visible
end)

-- SIDEBAR
local Side = Instance.new("Frame", Main)
Side.Size = UDim2.fromScale(0.25,1)
Side.BackgroundColor3 = C.BG2
Instance.new("UICorner", Side).CornerRadius = UDim.new(0,14)

local Title = Instance.new("TextLabel", Side)
Title.Size = UDim2.fromScale(1,0.1)
Title.Text = "⚡ Dark Hub"
Title.Font = Enum.Font.GothamBold
Title.TextSize = 18
Title.TextColor3 = C.ACCENT
Title.BackgroundTransparency = 1

-- PAGES
local Pages = Instance.new("Folder", Main)
Pages.Name = "Pages"

local function NewPage(name)
	local p = Instance.new("Frame", Pages)
	p.Name = name
	p.Size = UDim2.fromScale(0.75,1)
	p.Position = UDim2.fromScale(0.25,0)
	p.BackgroundTransparency = 1
	p.Visible = false
	return p
end

-- TAB SYSTEM
local function Tab(name, y)
	local btn = Instance.new("TextButton", Side)
	btn.Size = UDim2.fromScale(0.9,0.08)
	btn.Position = UDim2.fromScale(0.05,y)
	btn.Text = name
	btn.Font = Enum.Font.Gotham
	btn.TextColor3 = C.TEXT
	btn.BackgroundColor3 = C.BG
	Instance.new("UICorner", btn).CornerRadius = UDim.new(0,10)

	local page = NewPage(name)
	btn.MouseButton1Click:Connect(function()
		for _,v in pairs(Pages:GetChildren()) do v.Visible = false end
		page.Visible = true
	end)
	return page
end

local Farm = Tab("⚔ Farming",0.15)
local Player = Tab("👤 Player",0.25)
Farm.Visible = true

-- UI ELEMENTS
local function Tween(obj,prop,time)
	TweenService:Create(obj,TweenInfo.new(time,Enum.EasingStyle.Quad),prop):Play()
end

-- TOGGLE
local function Toggle(parent,text,y,cb)
	local bg = Instance.new("Frame", parent)
	bg.Size = UDim2.fromScale(0.8,0.08)
	bg.Position = UDim2.fromScale(0.1,y)
	bg.BackgroundColor3 = C.BG2
	Instance.new("UICorner", bg).CornerRadius = UDim.new(0,10)

	local lb = Instance.new("TextLabel", bg)
	lb.Size = UDim2.fromScale(0.7,1)
	lb.Text = text
	lb.TextXAlignment = Left
	lb.BackgroundTransparency = 1
	lb.TextColor3 = C.TEXT

	local btn = Instance.new("TextButton", bg)
	btn.Size = UDim2.fromScale(0.25,0.7)
	btn.Position = UDim2.fromScale(0.72,0.15)
	btn.Text = "OFF"
	btn.BackgroundColor3 = Color3.fromRGB(45,45,45)
	Instance.new("UICorner", btn).CornerRadius = UDim.new(1,0)

	local on = false
	btn.MouseButton1Click:Connect(function()
		on = not on
		btn.Text = on and "ON" or "OFF"
		Tween(btn,{BackgroundColor3 = on and C.ACCENT or Color3.fromRGB(45,45,45)},0.15)
		if cb then cb(on) end
	end)
end

-- SLIDER
local function Slider(parent,text,y,min,max,def,cb)
	local bg = Instance.new("Frame", parent)
	bg.Size = UDim2.fromScale(0.8,0.1)
	bg.Position = UDim2.fromScale(0.1,y)
	bg.BackgroundColor3 = C.BG2
	Instance.new("UICorner", bg).CornerRadius = UDim.new(0,10)

	local lb = Instance.new("TextLabel", bg)
	lb.Size = UDim2.fromScale(1,0.4)
	lb.Text = text.." : "..def
	lb.BackgroundTransparency = 1
	lb.TextColor3 = C.TEXT

	local bar = Instance.new("Frame", bg)
	bar.Size = UDim2.fromScale(0.9,0.2)
	bar.Position = UDim2.fromScale(0.05,0.6)
	bar.BackgroundColor3 = Color3.fromRGB(45,45,45)
	Instance.new("UICorner", bar).CornerRadius = UDim.new(1,0)

	local fill = Instance.new("Frame", bar)
	fill.Size = UDim2.fromScale((def-min)/(max-min),1)
	fill.BackgroundColor3 = C.ACCENT
	Instance.new("UICorner", fill).CornerRadius = UDim.new(1,0)
end

-- DROPDOWN
local function Dropdown(parent,text,y,list,cb)
	local open = false
	local box = Instance.new("TextButton", parent)
	box.Size = UDim2.fromScale(0.8,0.08)
	box.Position = UDim2.fromScale(0.1,y)
	box.Text = text
	box.BackgroundColor3 = C.BG2
	box.TextColor3 = C.TEXT
	Instance.new("UICorner", box).CornerRadius = UDim.new(0,10)

	local menu = Instance.new("Frame", parent)
	menu.Size = UDim2.fromScale(0.8,0)
	menu.Position = UDim2.fromScale(0.1,y+0.09)
	menu.BackgroundColor3 = C.BG2
	menu.ClipsDescendants = true
	Instance.new("UICorner", menu).CornerRadius = UDim.new(0,10)

	box.MouseButton1Click:Connect(function()
		open = not open
		Tween(menu,{Size = open and UDim2.fromScale(0.8,#list*0.06) or UDim2.fromScale(0.8,0)},0.2)
	end)

	for i,v in ipairs(list) do
		local b = Instance.new("TextButton", menu)
		b.Size = UDim2.fromScale(1,0.06)
		b.Position = UDim2.fromScale(0,(i-1)*0.06)
		b.Text = v
		b.BackgroundTransparency = 1
		b.TextColor3 = C.TEXT
		b.MouseButton1Click:Connect(function()
			box.Text = text..": "..v
			open = false
			Tween(menu,{Size = UDim2.fromScale(0.8,0)},0.2)
			if cb then cb(v) end
		end)
	end
end

-- DEMO
Toggle(Farm,"Auto Farm",0.1,function(v) print(v) end)
Slider(Farm,"Health %",0.22,1,100,60)
Dropdown(Farm,"Method",0.36,{"Fast","Safe","Quest"},function(v) print(v) end)