--// REDZ STYLE UI - AUTO FARM LEVEL
local Players = game:GetService("Players")
local LP = Players.LocalPlayer
local UIS = game:GetService("UserInputService")
local RunService = game:GetService("RunService")

--// ScreenGui
local ScreenGui = Instance.new("ScreenGui", game.CoreGui)
ScreenGui.Name = "RedzFarmUI"

--// Main Frame
local Main = Instance.new("Frame", ScreenGui)
Main.Size = UDim2.fromScale(0.32, 0.38)
Main.Position = UDim2.fromScale(0.34, 0.3)
Main.BackgroundColor3 = Color3.fromRGB(15,15,15)
Main.BorderSizePixel = 0
Main.Active = true
Main.Draggable = true
Main.Visible = true
Main.Name = "Main"

--// Corner
local UICorner = Instance.new("UICorner", Main)
UICorner.CornerRadius = UDim.new(0,12)

--// Title
local Title = Instance.new("TextLabel", Main)
Title.Size = UDim2.new(1,0,0.18,0)
Title.BackgroundTransparency = 1
Title.Text = "REDZ | AUTO FARM LEVEL"
Title.TextColor3 = Color3.fromRGB(255,70,70)
Title.Font = Enum.Font.GothamBold
Title.TextScaled = true

--// Line
local Line = Instance.new("Frame", Main)
Line.Position = UDim2.new(0.05,0,0.18,0)
Line.Size = UDim2.new(0.9,0,0,2)
Line.BackgroundColor3 = Color3.fromRGB(255,70,70)
Line.BorderSizePixel = 0

--// Toggle Button
local Toggle = Instance.new("TextButton", Main)
Toggle.Position = UDim2.new(0.1,0,0.3,0)
Toggle.Size = UDim2.new(0.8,0,0.18,0)
Toggle.BackgroundColor3 = Color3.fromRGB(35,35,35)
Toggle.Text = "AUTO FARM : OFF"
Toggle.TextColor3 = Color3.fromRGB(255,255,255)
Toggle.Font = Enum.Font.GothamBold
Toggle.TextScaled = true
Toggle.BorderSizePixel = 0

local ToggleCorner = Instance.new("UICorner", Toggle)
ToggleCorner.CornerRadius = UDim.new(0,10)

--// Status
local Status = Instance.new("TextLabel", Main)
Status.Position = UDim2.new(0.1,0,0.55,0)
Status.Size = UDim2.new(0.8,0,0.15,0)
Status.BackgroundTransparency = 1
Status.Text = "Status: Idle"
Status.TextColor3 = Color3.fromRGB(180,180,180)
Status.Font = Enum.Font.Gotham
Status.TextScaled = true

--// Variables
local AutoFarm = false

--// Toggle Logic
Toggle.MouseButton1Click:Connect(function()
    AutoFarm = not AutoFarm
    if AutoFarm then
        Toggle.Text = "AUTO FARM : ON"
        Toggle.BackgroundColor3 = Color3.fromRGB(255,70,70)
        Status.Text = "Status: Farming..."
    else
        Toggle.Text = "AUTO FARM : OFF"
        Toggle.BackgroundColor3 = Color3.fromRGB(35,35,35)
        Status.Text = "Status: Idle"
    end
end)

--// FARM LOOP (DEMO - GẮN LOGIC SAU)
task.spawn(function()
    while task.wait(0.2) do
        if AutoFarm then
            -- Gắn farm logic Blox Fruits ở đây
            -- Ví dụ: CheckLevel(), BringMob(), Attack()
        end
    end
end)

--// Mini Button (ẩn/hiện giống Redz)
local Mini = Instance.new("TextButton", ScreenGui)
Mini.Size = UDim2.fromScale(0.08,0.06)
Mini.Position = UDim2.fromScale(0.02,0.45)
Mini.Text = "RZ"
Mini.TextColor3 = Color3.fromRGB(255,255,255)
Mini.BackgroundColor3 = Color3.fromRGB(255,70,70)
Mini.Font = Enum.Font.GothamBold
Mini.TextScaled = true
Mini.BorderSizePixel = 0

local MiniCorner = Instance.new("UICorner", Mini)
MiniCorner.CornerRadius = UDim.new(1,0)

Mini.MouseButton1Click:Connect(function()
    Main.Visible = not Main.Visible
end)
