
resolve = Resolve()
pm = resolve:GetProjectManager()
proj = pm:GetCurrentProject()
tl = proj:GetCurrentTimeline()

print( "Number of Clips per Track" )

track_type = "audio"
tracks_count = tl:GetTrackCount(track_type)
for id = 1, tracks_count do
    track_name = tl:GetTrackName(track_type, id)
    items = tl:GetItemListInTrack(track_type, id)
    for i, item in ipairs( items ) do
        local entry = {
            id,
            track_name,
            item:GetName(),
            item:GetStart(),
            item:GetEnd(),
            item:GetLeftOffset()
        }
        print( table.concat( entry, "\t" )  )
    end
end