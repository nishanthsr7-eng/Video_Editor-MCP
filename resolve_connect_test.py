import sys
import DaVinciResolveScript as dvr_script

resolve = dvr_script.scriptapp("Resolve")
if resolve is None:
    print("FAILED: could not connect to Resolve")
    sys.exit(1)

print("Connected:", resolve.GetProductName(), resolve.GetVersionString())
pm = resolve.GetProjectManager()
proj = pm.GetCurrentProject()
print("Current project:", proj.GetName() if proj else "(none open)")
if proj:
    tl = proj.GetCurrentTimeline()
    print("Current timeline:", tl.GetName() if tl else "(none)")
    mp = proj.GetMediaPool()
    root = mp.GetRootFolder()
    clips = root.GetClipList()
    print("Clips in root media pool folder:", len(clips))
    for c in clips[:20]:
        print("   -", c.GetName())
