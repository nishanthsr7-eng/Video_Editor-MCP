-- Exports timeline markers as a tab-separated CSV compatible with REAPER's marker import format.


-- USER CONFIG AREA ---------------------------------------
time_offset = 0 -- 0, 3600 if timeline starts at 01:00:00

file_path = "" -- absolute file path for export
----------------------------------- END OF USER CONFIG AREA

function GetSecondsFromFrame( pos, fps )
    return pos/fps
end

function Export( str )
  print( str )
  if file then
    file:write( str .. "\n" )
  end
end

-- INIT
resolve = Resolve()
pm = resolve:GetProjectManager()
proj = pm:GetCurrentProject()
tl = proj:GetCurrentTimeline()
fps = proj:GetSetting("timelineFrameRate")
markers = tl:GetMarkers()

positions = {}
for k, marker in pairs( markers ) do
    table.insert(positions, k)
end

table.sort( positions )

-- Start export
file = io.open( file_path, "w")

Export( "Type\tName\tPos_Start\tPos_End" ) -- header
Export( "-------------------------" )

-- body
for i, pos in ipairs(positions) do
    local marker = markers[pos]
    local position = GetSecondsFromFrame( pos, fps ) + time_offset
    local t = {
        "M" .. i,
        marker.name,
        position,
        position
    }

    Export( table.concat( t, "\t") ) -- line
end

file:close()

Export( (file and "\nExported File:\n" .. file_path) or "No file exported. Edit file_path in the USER CONFIG AREA." )