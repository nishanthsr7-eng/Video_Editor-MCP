-- Imports markers from an OBS Studio OBSInfoWriter CSV file (same name/directory as the video clip).
-- Do not use commas in marker names.


-- USER CONFIG AREA -------------------------------------

clip_name = "Cam_2020-09-18.mp4"
csv_path = "H:\\Cam\\Markers_2020-09-18.csv"
framerate = 25

----------------------------------END OF USER CONFIG AREA

print("-------------------------")

function GetFrameFromTimeCode( timecode, fps )
  if not fps then fps = framerate end
  local hours, minutes, seconds = timecode:match("(%d+):(%d+):(%d+)")
  return (hours * 3600 + minutes * 60 + seconds) * fps
end

file = io.input(csv_path, "r")
retval = file:read("a")
io.close(file)

if retval then
  t = {}
  local i = 0
  for line in retval:gmatch("[^\n]*") do
      i = i + 1
      local timecode, name = line:match("(.+),(.+)")
      if timecode then
        t[i] = {
          timecode = timecode,
          name = name
        }
      end
  end
else
	print("Invalid Path.")
	return
end

resolve = Resolve()
pm = resolve:GetProjectManager()
proj = pm:GetCurrentProject()
mp = proj:GetMediaPool()
folder = mp:GetCurrentFolder()
clips = folder:GetClipList()
for i, clip in ipairs( clips ) do
	local name = clip:GetName()
	if name == clip_name then
		for i, marker in ipairs( markers ) do
			clip:AddMarker(GetFrameFromTimeCode( marker.timecode, framerate), "Green", marker.name, 1)
		end
	end
end