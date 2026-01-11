local Players = game:GetService("Players")
local UIS = game:GetService("UserInputService")

local player = Players.LocalPlayer
local gui = Instance.new("ScreenGui", player.PlayerGui)
gui.ResetOnSpawn = false

local toggle = Instance.new("TextButton", gui)
toggle.Size = UDim2.new(0,50,0,50)
toggle.Position = UDim2.new(0.02,0,0.4,0)
toggle.Text = ""
toggle.BackgroundColor3 = Color3.fromRGB(30,30,30)
toggle.BorderSizePixel = 0
Instance.new("UICorner", toggle).CornerRadius = UDim.new(1,0)

local menu = Instance.new("Frame", gui)
menu.Size = UDim2.new(0.7,0,0.55,0)
menu.Position = UDim2.new(0.15,0,0.2,0)
menu.BackgroundColor3 = Color3.fromRGB(0,0,0)
menu.Visible = false
menu.BorderSizePixel = 0
Instance.new("UICorner", menu).CornerRadius = UDim.new(0,14)

local dragging, dragStart, startPos
menu.InputBegan:Connect(function(i)
	if i.UserInputType == Enum.UserInputType.Touch then
		dragging = true
		dragStart = i.Position
		startPos = menu.Position
	end
end)

menu.InputChanged:Connect(function(i)
	if dragging and i.UserInputType == Enum.UserInputType.Touch then
		local delta = i.Position - dragStart
		menu.Position = UDim2.new(
			startPos.X.Scale,
			startPos.X.Offset + delta.X,
			startPos.Y.Scale,
			startPos.Y.Offset + delta.Y
		)
	end
end)

UIS.InputEnded:Connect(function(i)
	if i.UserInputType == Enum.UserInputType.Touch then
		dragging = false
	end
end)

toggle.MouseButton1Click:Connect(function()
	menu.Visible = not menu.Visible
end)

local tabBar = Instance.new("Frame", menu)
tabBar.Size = UDim2.new(0.25,0,1,0)
tabBar.BackgroundColor3 = Color3.fromRGB(20,20,20)
tabBar.BorderSizePixel = 0

local content = Instance.new("Frame", menu)
content.Size = UDim2.new(0.75,0,1,0)
content.Position = UDim2.new(0.25,0,0,0)
content.BackgroundTransparency = 1

local function newTab(name, order)
	local b = Instance.new("TextButton", tabBar)
	b.Size = UDim2.new(1,0,0.15,0)
	b.Position = UDim2.new(0,0,0.15*(order-1),0)
	b.Text = name
	b.TextScaled = true
	b.BackgroundColor3 = Color3.fromRGB(40,40,40)
	b.TextColor3 = Color3.new(1,1,1)
	b.BorderSizePixel = 0
	Instance.new("UICorner", b)

	local page = Instance.new("Frame", content)
	page.Size = UDim2.new(1,0,1,0)
	page.Visible = false
	page.BackgroundTransparency = 1

	b.MouseButton1Click:Connect(function()
		for _,v in pairs(content:GetChildren()) do
			if v:IsA("Frame") then
				v.Visible = false
			end
		end
		page.Visible = true
	end)

	return page
end

local mainTab = newTab("Main",1)
local flyTab = newTab("Fly",2)
local playerTab = newTab("Player",3)
local farmTab = newTab("Farm",4)

mainTab.Visible = true

local flyBtn = Instance.new("TextButton", flyTab)
flyBtn.Size = UDim2.new(0.8,0,0.15,0)
flyBtn.Position = UDim2.new(0.1,0,0.1,0)
flyBtn.Text = "Fly Off"
flyBtn.TextScaled = true
flyBtn.BackgroundColor3 = Color3.fromRGB(60,60,60)
flyBtn.TextColor3 = Color3.new(1,1,1)
Instance.new("UICorner", flyBtn)