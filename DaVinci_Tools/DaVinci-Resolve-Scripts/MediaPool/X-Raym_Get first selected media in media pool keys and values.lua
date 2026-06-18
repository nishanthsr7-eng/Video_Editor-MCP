
resolve = Resolve()
pm = resolve:GetProjectManager()
proj = pm:GetCurrentProject()
mp = proj:GetMediaPool()
clips = mp:GetSelectedClips()
i = 1
keys = clips[i]:GetClipProperty()
for k, v in pairs( keys ) do
  print( tostring(k) .. "\t" .. tostring(v) )
end