local Players = game:GetService("Players")
local RunService = game:GetService("RunService")

local player = Players.LocalPlayer
local character = player.Character or player.CharacterAdded:Wait()
local humanoid = character:WaitForChild("Humanoid")
local root = character:WaitForChild("HumanoidRootPart")

local gui = Instance.new("ScreenGui")
gui.ResetOnSpawn = false
gui.Parent = player.PlayerGui

local menu = Instance.new("Frame")
menu.Size = UDim2.new(0.4,0,0.4,0)
menu.Position = UDim2.new(0.05,0,0.3,0)
menu.BackgroundColor3 = Color3.fromRGB(0,0,0)
menu.BorderSizePixel = 0
menu.Parent = gui

local corner = Instance.new("UICorner")
corner.CornerRadius = UDim.new(0,14)
corner.Parent = menu

local title = Instance.new("TextLabel")
title.Size = UDim2.new(1,0,0.15,0)
title.BackgroundTransparency = 1
title.Text = "FLY MENU"
title.TextScaled = true
title.TextColor3 = Color3.new(1,1,1)
title.Parent = menu

local function createButton(text,y)
	local b = Instance.new("TextButton")
	b.Size = UDim2.new(0.9,0,0.14,0)
	b.Position = UDim2.new(0.05,0,y,0)
	b.Text = text
	b.TextScaled = true
	b.BackgroundColor3 = Color3.fromRGB(40,40,40)
	b.TextColor3 = Color3.new(1,1,1)
	b.Parent = menu
	local c = Instance.new("UICorner")
	c.Parent = b
	return b
end

local flyButton = createButton("FLY OFF",0.18)
local upButton = createButton("UP",0.34)
local downButton = createButton("DOWN",0.50)
local speedButton = createButton("SPEED 50",0.66)
local lagButton = createButton("FIX LAG",0.82)

local flying = false
local speed = 50
local up = false
local down = false
local bodyVelocity
local bodyGyro

local function startFly()
	bodyVelocity = Instance.new("BodyVelocity")
	bodyVelocity.MaxForce = Vector3.new(1e9,1e9,1e9)
	bodyVelocity.Parent = root

	bodyGyro = Instance.new("BodyGyro")
	bodyGyro.MaxTorque = Vector3.new(1e9,1e9,1e9)
	bodyGyro.P = 90000
	bodyGyro.Parent = root

	RunService:BindToRenderStep("Fly",0,function()
		local cam = workspace.CurrentCamera
		local move = humanoid.MoveDirection
		local y = 0
		if up then y = 1 end
		if down then y = -1 end
		bodyVelocity.Velocity = (move * speed) + Vector3.new(0,y * speed,0)
		bodyGyro.CFrame = cam.CFrame
	end)
end

local function stopFly()
	RunService:UnbindFromRenderStep("Fly")
	if bodyVelocity then bodyVelocity:Destroy() end
	if bodyGyro then bodyGyro:Destroy() end
end

flyButton.MouseButton1Click:Connect(function()
	flying = not flying
	if flying then
		flyButton.Text = "FLY ON"
		startFly()
	else
		flyButton.Text = "FLY OFF"
		stopFly()
	end
end)

upButton.MouseButton1Down:Connect(function()
	up = true
end)

upButton.MouseButton1Up:Connect(function()
	up = false
end)

downButton.MouseButton1Down:Connect(function()
	down = true
end)

downButton.MouseButton1Up:Connect(function()
	down = false
end)

speedButton.MouseButton1Click:Connect(function()
	speed = speed + 25
	if speed > 125 then
		speed = 25
	end
	speedButton.Text = "SPEED "..speed
end)

lagButton.MouseButton1Click:Connect(function()
	for _,v in pairs(humanoid:GetPlayingAnimationTracks()) do
		v:Stop()
	end
	humanoid:SetStateEnabled(Enum.HumanoidStateType.Climbing,false)
	humanoid:SetStateEnabled(Enum.HumanoidStateType.Ragdoll,false)
	humanoid:SetStateEnabled(Enum.HumanoidStateType.FallingDown,false)
	root.CustomPhysicalProperties = PhysicalProperties.new(0,0,0,0,0)
	lagButton.Text = "FIXED"
end)
