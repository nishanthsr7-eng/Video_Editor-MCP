# Resolve Scripts

A collection of Python scripts for automating repetitive tasks in DaVinci Resolve and Fusion via the Resolve Scripting API.

## Installation

Copy scripts to the DaVinci Resolve Fusion Scripts folder for your OS:

**Windows**
```
%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Fusion\Scripts
```
or per-user:
```
%APPDATA%\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts
```

**macOS**
```
/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts
```
or per-user:
```
~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts
```

**Linux**
```
/opt/resolve/Fusion/Scripts
```

Scripts appear under **Workspace → Scripts** once Resolve is open. Place scripts in `Utility` to show on all pages, or in `Edit`, `Color`, `Deliver`, or `Comp` folders to scope them to those pages.

## Running

Navigate to **Workspace → Scripts → [Script Name]** with Resolve open.

## Debugging

If a script does nothing, open **Workspace → Console** to see any error output.

---

## Scripts

### Coding

**Get Scripting Properties**
Prints all available scripting properties for the selected clip or timeline. Useful for exploring what the Resolve API exposes before writing automation.

---

### Color

**Compute DNG Matrix**
Computes a color matrix from a DNG file, useful for accurate camera color science work.

**Export CDLs**
Exports CDL (Color Decision List) values from graded clips on the Color page to an `.edl` or `.cdl` file for interchange with other grading tools.

**Print Node Tools**
Prints the tools (nodes) applied to the current clip's node graph — helpful for auditing grades or debugging complex node trees.

**Stabilize Clips**
Applies Resolve's built-in stabilizer to a batch of selected clips on the Color page without clicking each one manually.

**Toggle Nodes**
Toggles the enabled/disabled state of a named node across all clips on the Color page — useful for quickly comparing grades with and without a specific node.

---

### Edit

**Copy Timeline Settings**
Copies resolution, frame rate, and other settings from one timeline and applies them to another.

**Gather Clips from XML**
Imports clips referenced in an XML into the current timeline, relinking any offline media automatically.

**Generate All Clips Timeline**
Creates a new timeline containing every clip in the media pool in alphabetical order — useful for QC review passes.

**Rename Clips**
Batch-renames clips in the media pool or on the timeline using find-and-replace, prefix/suffix, or numbering patterns.

**Rename Timelines**
Batch-renames timelines in the current project.

**Update Timeline Resolution**
Changes the resolution of the current timeline and optionally scales all clips to fit the new canvas.

**Update Version Number**
Increments a version number embedded in clip names or timeline names — useful for managing cut versions.

---

### Deliver

**Render Notification**
Sends a system notification (Windows toast or macOS notification) when a render job finishes — so you can step away while rendering without missing the completion.

---

### Utility

**Relink Media Pool Clips**
Relinks offline clips in the media pool to a new root folder. Useful after moving project files to a new drive or directory.

**Remove Empty Bins**
Deletes all empty bins (folders) from the media pool, cleaning up after imports or reorganization.

**Replace Media Pool Clips**
Swaps clips in the media pool with updated versions from a specified folder, preserving timeline placement and grades.
