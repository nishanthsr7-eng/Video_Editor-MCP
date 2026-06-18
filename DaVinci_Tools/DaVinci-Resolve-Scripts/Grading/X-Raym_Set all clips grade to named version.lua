
version_type = 1
version_name = "My Version"

resolve = Resolve()
pm = resolve:GetProjectManager()
proj = pm:GetCurrentProject()
tl = proj:GetCurrentTimeline()

track_types = { "video" }
for i, track_type in ipairs( track_types ) do
  tracks_count = tl:GetTrackCount(track_type)
  for id = 1, tracks_count do
    items = tl:GetItemListInTrack(track_type, id)
    for j, item in ipairs(items) do
      item_name = item:GetName()
      version = item:GetCurrentVersion() 

      -- Note: maybe LoadVersionByName can be put right here but this aims to be better on CPU and UndoPoints

      if version.versionType ~= version_type or version.versionName ~= version_name then -- only if necessary
        versions = item:GetVersionNameList( version_type )
        for z, name in ipairs( versions ) do
          if name == version_name then -- Only if this name exist
            item:LoadVersionByName(version_name, version_type)
            print( item_name .. "\t" .. version.versionName )
            break
          end
        end
        
      end

    end
  end
end