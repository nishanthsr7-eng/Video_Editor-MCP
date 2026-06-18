
colors = { "Orange", "Apricot", "Yellow", "Lime", "Olive", "Green", "Teal", "Navy", "Blue", "Purple", "Violet", "Pink", "Tan", "Beige", "Brown", "Chocolate" }

resolve = Resolve()
pm = resolve:GetProjectManager()
proj = pm:GetCurrentProject()
tl = proj:GetCurrentTimeline()

names = {}

track_types = { "video" }
for i, track_type in ipairs( track_types ) do
  tracks_count = tl:GetTrackCount(track_type)
  for id = 1, tracks_count do
    items = tl:GetItemListInTrack(track_type, id)
    for i, item in ipairs(items) do
      name = item:GetName()
      if not names[name] then names[name] = {} end
      table.insert( names[name], item )
    end
  end
end

-- Sort alphabetically
names_list = {}
for name, items in pairs( names ) do
  print(name)
  table.insert( names_list, name )
end

table.sort( names_list )

for i, name in ipairs( names_list ) do
  print("--------\n", name)
  if i > #colors then break end
  for j, item in ipairs( names[name] ) do
    print( item:GetName() .. " = " .. colors[i] )
    item:SetClipColor( colors[i] )
  end
end