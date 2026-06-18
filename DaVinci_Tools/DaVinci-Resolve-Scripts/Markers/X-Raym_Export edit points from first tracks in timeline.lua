
resolve = Resolve()
pm = resolve:GetProjectManager()
proj = pm:GetCurrentProject()
tl = proj:GetCurrentTimeline()
items = tl:GetItemListInTrack("video", 1)

framerate = proj:GetSetting("timelineFrameRate")

for i, item in ipairs( items ) do
	pos = item:GetStart()/framerate
	print(pos)
end