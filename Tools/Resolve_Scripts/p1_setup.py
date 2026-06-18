"""Phase 1 - import media, set 9:16 project format, create the working timeline."""
from _resolve_env import connect

MOVIE = r"D:\Files\Projects\Multi-Agent Orchestration Framework for Generative Video Editing\Sources\I want to eat your pancreas\I want to eat your pancreas.mp4"
SONG  = r"D:\Files\Projects\Multi-Agent Orchestration Framework for Generative Video Editing\Sources\I want to eat your pancreas\Gigi Perez - Sailor Song  (slowed reverb  lyrics).mp3"
TL_NAME = "sailor_song_edit"


def find_clip_everywhere(mp, name):
    """Search root + all subfolders for a clip whose name matches."""
    seen, stack = [], [mp.GetRootFolder()]
    while stack:
        fol = stack.pop()
        for c in fol.GetClipList():
            if c.GetName() == name:
                return c
        stack.extend(fol.GetSubFolderList())
    return None


def main():
    resolve, pm, proj, mp = connect()
    print("Connected:", resolve.GetProductName(), resolve.GetVersionString())
    print("Project:", proj.GetName())

    # --- project format (only set what isn't already right; frame rate is
    #     locked once media/timelines exist, so don't fail if it refuses) ---
    print("current fps:", proj.GetSetting("timelineFrameRate"),
          "res:", proj.GetSetting("timelineResolutionWidth"),
          "x", proj.GetSetting("timelineResolutionHeight"))
    proj.SetSetting("timelineResolutionWidth", "1080")
    proj.SetSetting("timelineResolutionHeight", "1920")
    if str(proj.GetSetting("timelineFrameRate")).split(".")[0] not in ("24", "23"):
        ok = proj.SetSetting("timelineFrameRate", "24")
        print("set fps 24:", ok)
    proj.SetSetting("timelineInputResMismatchBehavior", "scaleToFit")

    # --- import sources (reuse if already in pool) ---
    root = mp.GetRootFolder()
    sub = None
    for f in root.GetSubFolderList():
        if f.GetName() == "sailor_song_src":
            sub = f
            break
    if sub is None:
        sub = mp.AddSubFolder(root, "sailor_song_src")
    mp.SetCurrentFolder(sub)

    movie_item = find_clip_everywhere(mp, "I want to eat your pancreas.mp4")
    song_name = "Gigi Perez - Sailor Song  (slowed reverb  lyrics).mp3"
    song_item = find_clip_everywhere(mp, song_name)

    to_import = []
    if movie_item is None:
        to_import.append(MOVIE)
    if song_item is None:
        to_import.append(SONG)
    if to_import:
        print("importing:", to_import)
        mp.ImportMedia(to_import)
        movie_item = movie_item or find_clip_everywhere(mp, "I want to eat your pancreas.mp4")
        song_item = song_item or find_clip_everywhere(mp, song_name)
    print("movie:", movie_item and movie_item.GetName())
    print("song :", song_item and song_item.GetName())
    print("movie fps:", movie_item and movie_item.GetClipProperty("FPS"))

    # --- fresh timeline (delete a prior run of the same name) ---
    for i in range(1, proj.GetTimelineCount() + 1):
        t = proj.GetTimelineByIndex(i)
        if t.GetName() == TL_NAME:
            print("removing previous", TL_NAME)
            mp.DeleteTimelines([t])
            break
    mp.SetCurrentFolder(sub)
    tl = mp.CreateEmptyTimeline(TL_NAME)
    proj.SetCurrentTimeline(tl)
    while tl.GetTrackCount("video") < 3:      # ensure V1, V2, V3
        tl.AddTrack("video")

    print("timeline:", tl.GetName(),
          "| res", tl.GetSetting("timelineResolutionWidth"), "x",
          tl.GetSetting("timelineResolutionHeight"),
          "| fps", tl.GetSetting("timelineFrameRate"),
          "| V tracks", tl.GetTrackCount("video"),
          "| start frame", tl.GetStartFrame())
    pm.SaveProject()
    print("OK Phase 1 done")


if __name__ == "__main__":
    main()
