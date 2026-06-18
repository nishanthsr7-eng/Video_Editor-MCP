
resolve = Resolve()
pm = resolve:GetProjectManager()
proj = pm:GetCurrentProject()
tl = proj:GetCurrentTimeline()

print( "Number of Clips per Track" )

-- Get Track by Name, no matter the type
track_types =  { "audio", "video", "subtitle" }
local out_track_type, out_track_index
for i, track_type in ipairs( track_types ) do
    print( "--------\n" .. track_type:upper() )
    tracks_count = tl:GetTrackCount(track_type)
    for id = 1, tracks_count do
        track_name = tl:GetTrackName(track_type, id)
        items = tl:GetItemListInTrack(track_type, id)
        print( id .. "." .. track_name .. " = " .. #items )
    end
end