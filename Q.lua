local ScreenGui = Instance.new("ScreenGui")
local MainFrame = Instance.new("Frame")
local UICorner = Instance.new("UICorner")
local Title = Instance.new("TextLabel")
local TabContainer = Instance.new("ScrollingFrame")
local ContentFrame = Instance.new("Frame")

-- Setup ScreenGui
ScreenGui.Name = "redz Hub"
ScreenGui.Parent = game.CoreGui
ScreenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling

-- Main Frame (50% man hinh)
MainFrame.Name = "MainFrame"
MainFrame.Parent = ScreenGui
MainFrame.AnchorPoint = Vector2.new(0, 0.5)
MainFrame.BackgroundColor3 = Color3.fromRGB(20, 20, 20)
MainFrame.BorderSizePixel = 0
MainFrame.Position = UDim2.new(0, 10, 0.5, 0)
MainFrame.Size = UDim2.new(0.5, 0, 0.8, 0) -- 50% width, 80% height
MainFrame.Active = true
MainFrame.Draggable = true

UICorner.CornerRadius = UDim.new(0, 10)
UICorner.Parent = MainFrame

-- Title
Title.Name = "Title"
Title.Parent = MainFrame
Title.BackgroundTransparency = 1
Title.Position = UDim2.new(0, 0, 0, 0)
Title.Size = UDim2.new(1, 0, 0, 40)
Title.Font = Enum.Font.GothamBold
Title.Text = "redz Hub : Blox Fruits"
Title.TextColor3 = Color3.fromRGB(255, 255, 255)
Title.TextSize = 16
Title.TextXAlignment = Enum.TextXAlignment.Left
Title.TextYAlignment = Enum.TextYAlignment.Center
Title.TextTransparency = 0.3

-- Tab Container (ben trai)
TabContainer.Name = "TabContainer"
TabContainer.Parent = MainFrame
TabContainer.BackgroundColor3 = Color3.fromRGB(15, 15, 15)
TabContainer.BorderSizePixel = 0
TabContainer.Position = UDim2.new(0, 0, 0, 45)
TabContainer.Size = UDim2.new(0, 180, 1, -45)
TabContainer.ScrollBarThickness = 4
TabContainer.ScrollBarImageColor3 = Color3.fromRGB(100, 100, 100)

-- Content Frame (ben phai)
ContentFrame.Name = "ContentFrame"
ContentFrame.Parent = MainFrame
ContentFrame.BackgroundColor3 = Color3.fromRGB(25, 25, 25)
ContentFrame.BorderSizePixel = 0
ContentFrame.Position = UDim2.new(0, 185, 0, 45)
ContentFrame.Size = UDim2.new(1, -190, 1, -45)

-- Ham tao Tab Button
local function createTabButton(name, icon, position, callback)
    local TabButton = Instance.new("TextButton")
    local TabIcon = Instance.new("ImageLabel")
    local TabText = Instance.new("TextLabel")
    
    TabButton.Name = name
    TabButton.Parent = TabContainer
    TabButton.BackgroundColor3 = Color3.fromRGB(20, 20, 20)
    TabButton.BorderSizePixel = 0
    TabButton.Position = UDim2.new(0, 5, 0, position)
    TabButton.Size = UDim2.new(1, -10, 0, 40)
    TabButton.AutoButtonColor = false
    TabButton.Text = ""
    
    local ButtonCorner = Instance.new("UICorner")
    ButtonCorner.CornerRadius = UDim.new(0, 6)
    ButtonCorner.Parent = TabButton
    
    -- Icon
    TabIcon.Name = "Icon"
    TabIcon.Parent = TabButton
    TabIcon.BackgroundTransparency = 1
    TabIcon.Position = UDim2.new(0, 10, 0.5, -10)
    TabIcon.Size = UDim2.new(0, 20, 0, 20)
    TabIcon.Image = icon
    TabIcon.ImageColor3 = Color3.fromRGB(150, 150, 150)
    
    -- Text
    TabText.Name = "Text"
    TabText.Parent = TabButton
    TabText.BackgroundTransparency = 1
    TabText.Position = UDim2.new(0, 40, 0, 0)
    TabText.Size = UDim2.new(1, -40, 1, 0)
    TabText.Font = Enum.Font.Gotham
    TabText.Text = name
    TabText.TextColor3 = Color3.fromRGB(150, 150, 150)
    TabText.TextSize = 14
    TabText.TextXAlignment = Enum.TextXAlignment.Left
    
    -- Click effect
    TabButton.MouseButton1Click:Connect(function()
        -- Reset tat ca tabs
        for _, tab in pairs(TabContainer:GetChildren()) do
            if tab:IsA("TextButton") then
                tab.BackgroundColor3 = Color3.fromRGB(20, 20, 20)
                tab.Text.TextColor3 = Color3.fromRGB(150, 150, 150)
                tab.Icon.ImageColor3 = Color3.fromRGB(150, 150, 150)
            end
        end
        
        -- Highlight tab nay
        TabButton.BackgroundColor3 = Color3.fromRGB(40, 120, 255)
        TabText.TextColor3 = Color3.fromRGB(255, 255, 255)
        TabIcon.ImageColor3 = Color3.fromRGB(255, 255, 255)
        
        -- Clear content va load moi
        for _, child in pairs(ContentFrame:GetChildren()) do
            child:Destroy()
        end
        
        if callback then
            callback()
        end
    end)
    
    return TabButton
end

-- Ham tao Toggle Button
local function createToggle(parent, text, position, callback)
    local ToggleFrame = Instance.new("Frame")
    local ToggleLabel = Instance.new("TextLabel")
    local ToggleButton = Instance.new("TextButton")
    local ToggleIndicator = Instance.new("Frame")
    local ToggleCorner = Instance.new("UICorner")
    
    ToggleFrame.Parent = parent
    ToggleFrame.BackgroundTransparency = 1
    ToggleFrame.Position = UDim2.new(0, 10, 0, position)
    ToggleFrame.Size = UDim2.new(1, -20, 0, 35)
    
    ToggleLabel.Parent = ToggleFrame
    ToggleLabel.BackgroundTransparency = 1
    ToggleLabel.Size = UDim2.new(1, -60, 1, 0)
    ToggleLabel.Font = Enum.Font.Gotham
    ToggleLabel.Text = text
    ToggleLabel.TextColor3 = Color3.fromRGB(200, 200, 200)
    ToggleLabel.TextSize = 14
    ToggleLabel.TextXAlignment = Enum.TextXAlignment.Left
    
    ToggleButton.Parent = ToggleFrame
    ToggleButton.AnchorPoint = Vector2.new(1, 0)
    ToggleButton.BackgroundColor3 = Color3.fromRGB(50, 50, 50)
    ToggleButton.Position = UDim2.new(1, 0, 0, 5)
    ToggleButton.Size = UDim2.new(0, 45, 0, 25)
    ToggleButton.AutoButtonColor = false
    ToggleButton.Text = ""
    
    ToggleCorner.CornerRadius = UDim.new(1, 0)
    ToggleCorner.Parent = ToggleButton
    
    ToggleIndicator.Parent = ToggleButton
    ToggleIndicator.BackgroundColor3 = Color3.fromRGB(255, 255, 255)
    ToggleIndicator.Position = UDim2.new(0, 2, 0.5, -10)
    ToggleIndicator.Size = UDim2.new(0, 20, 0, 20)
    
    local IndicatorCorner = Instance.new("UICorner")
    IndicatorCorner.CornerRadius = UDim.new(1, 0)
    IndicatorCorner.Parent = ToggleIndicator
    
    local enabled = false
    
    ToggleButton.MouseButton1Click:Connect(function()
        enabled = not enabled
        
        if enabled then
            game:GetService("TweenService"):Create(
                ToggleButton,
                TweenInfo.new(0.2),
                {BackgroundColor3 = Color3.fromRGB(40, 120, 255)}
            ):Play()
            
            game:GetService("TweenService"):Create(
                ToggleIndicator,
                TweenInfo.new(0.2),
                {Position = UDim2.new(1, -22, 0.5, -10)}
            ):Play()
        else
            game:GetService("TweenService"):Create(
                ToggleButton,
                TweenInfo.new(0.2),
                {BackgroundColor3 = Color3.fromRGB(50, 50, 50)}
            ):Play()
            
            game:GetService("TweenService"):Create(
                ToggleIndicator,
                TweenInfo.new(0.2),
                {Position = UDim2.new(0, 2, 0.5, -10)}
            ):Play()
        end
        
        if callback then
            callback(enabled)
        end
    end)
end

-- TAB FARMING CONTENT
local function loadFarmingTab()
    local Container = Instance.new("ScrollingFrame")
    Container.Name = "Container"
    Container.Parent = ContentFrame
    Container.BackgroundTransparency = 1
    Container.Size = UDim2.new(1, 0, 1, 0)
    Container.ScrollBarThickness = 4
    Container.ScrollBarImageColor3 = Color3.fromRGB(100, 100, 100)
    
    -- Title Section
    local SectionTitle = Instance.new("TextLabel")
    SectionTitle.Parent = Container
    SectionTitle.BackgroundTransparency = 1
    SectionTitle.Position = UDim2.new(0, 10, 0, 10)
    SectionTitle.Size = UDim2.new(1, -20, 0, 30)
    SectionTitle.Font = Enum.Font.GothamBold
    SectionTitle.Text = "Level Farm"
    SectionTitle.TextColor3 = Color3.fromRGB(255, 255, 255)
    SectionTitle.TextSize = 18
    SectionTitle.TextXAlignment = Enum.TextXAlignment.Left
    
    -- Fly Toggle
    local flyEnabled = false
    local flySpeed = 50
    local flyConnection
    
    createToggle(Container, "Fly", 50, function(enabled)
        flyEnabled = enabled
        
        local player = game.Players.LocalPlayer
        local char = player.Character
        
        if enabled then
            print("[FLY] Enabled")
            
            if flyConnection then
                flyConnection:Disconnect()
            end
            
            -- Fly loop
            flyConnection = game:GetService("RunService").Heartbeat:Connect(function()
                if not flyEnabled then 
                    if flyConnection then
                        flyConnection:Disconnect()
                    end
                    return 
                end
                
                char = player.Character
                if not char or not char:FindFirstChild("HumanoidRootPart") then return end
                
                local hrp = char.HumanoidRootPart
                local humanoid = char:FindFirstChild("Humanoid")
                
                local moveDirection = Vector3.new()
                local UIS = game:GetService("UserInputService")
                
                -- WASD controls
                if UIS:IsKeyDown(Enum.KeyCode.W) then
                    moveDirection = moveDirection + workspace.CurrentCamera.CFrame.LookVector
                end
                if UIS:IsKeyDown(Enum.KeyCode.S) then
                    moveDirection = moveDirection - workspace.CurrentCamera.CFrame.LookVector
                end
                if UIS:IsKeyDown(Enum.KeyCode.A) then
                    moveDirection = moveDirection - workspace.CurrentCamera.CFrame.RightVector
                end
                if UIS:IsKeyDown(Enum.KeyCode.D) then
                    moveDirection = moveDirection + workspace.CurrentCamera.CFrame.RightVector
                end
                if UIS:IsKeyDown(Enum.KeyCode.Space) then
                    moveDirection = moveDirection + Vector3.new(0, 1, 0)
                end
                if UIS:IsKeyDown(Enum.KeyCode.LeftShift) then
                    moveDirection = moveDirection - Vector3.new(0, 1, 0)
                end
                
                -- Apply velocity
                hrp.Velocity = moveDirection * flySpeed
                humanoid.PlatformStand = true
            end)
        else
            print("[FLY] Disabled")
            
            if flyConnection then
                flyConnection:Disconnect()
            end
            
            if char and char:FindFirstChild("Humanoid") then
                char.Humanoid.PlatformStand = false
            end
            if char and char:FindFirstChild("HumanoidRootPart") then
                char.HumanoidRootPart.Velocity = Vector3.new(0, 0, 0)
            end
        end
    end)
    
    -- Auto Farm Material
    createToggle(Container, "Auto Farm Material", 95, function(enabled)
        print("[AUTO FARM] " .. tostring(enabled))
    end)
    
    -- Mastery Farm Section
    local MasteryTitle = Instance.new("TextLabel")
    MasteryTitle.Parent = Container
    MasteryTitle.BackgroundTransparency = 1
    MasteryTitle.Position = UDim2.new(0, 10, 0, 150)
    MasteryTitle.Size = UDim2.new(1, -20, 0, 30)
    MasteryTitle.Font = Enum.Font.GothamBold
    MasteryTitle.Text = "Mastery Farm"
    MasteryTitle.TextColor3 = Color3.fromRGB(255, 255, 255)
    MasteryTitle.TextSize = 18
    MasteryTitle.TextXAlignment = Enum.TextXAlignment.Left
    
    createToggle(Container, "Auto Farm Mastery Fruit", 190, function(enabled)
        print("[MASTERY FARM] " .. tostring(enabled))
    end)
    
    Container.CanvasSize = UDim2.new(0, 0, 0, 250)
end

-- TAO CAC TABS
createTabButton("Tab Discord", "rbxassetid://0", 5, function()
    print("Discord tab")
end)

createTabButton("Tab Shop", "rbxassetid://0", 50, function()
    print("Shop tab")
end)

createTabButton("Tab Status And...", "rbxassetid://0", 95, function()
    print("Status tab")
end)

createTabButton("Tab Local Player", "rbxassetid://0", 140, function()
    print("Local Player tab")
end)

createTabButton("Setting Farm", "rbxassetid://0", 185, function()
    print("Setting Farm tab")
end)

-- TAB FARMING (MAC DINH)
local FarmingTab = createTabButton("Tab Farming", "rbxassetid://0", 230, loadFarmingTab)
FarmingTab.BackgroundColor3 = Color3.fromRGB(40, 120, 255)
FarmingTab.Text.TextColor3 = Color3.fromRGB(255, 255, 255)
FarmingTab.Icon.ImageColor3 = Color3.fromRGB(255, 255, 255)
loadFarmingTab()

createTabButton("Tab Stack Farm", "rbxassetid://0", 275, function()
    print("Stack Farm tab")
end)

createTabButton("Tab Farming...", "rbxassetid://0", 320, function()
    print("Farming... tab")
end)

createTabButton("Tab Fruit and...", "rbxassetid://0", 365, function()
    print("Fruit and... tab")
end)

createTabButton("Tab Sea Event", "rbxassetid://0", 410, function()
    print("Sea Event tab")
end)

print("[redz Hub] Loaded - 50% screen!")
