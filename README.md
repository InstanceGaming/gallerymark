# GalleryMark
Faster bulk PDF grading.

## Installation
### Running using Python
1. Ensure you have the latest version of Python 3 installed and on your PATH.
2. Download the GalleryMark repository as a archive.
3. Extract the `gallerymark` folder from the archive into a location of your choosing.
4. Navigate to the `gallerymark` folder.
5. Run the installation script, `install.bat`. This only needs to be done once. You cannot move the installation folder after running this script (if you need to, delete the `env` folder and run again).
6. To run GalleryMark, double-click `gallerymark.bat`.

### Packaged binary
**The executable must be added to Windows Defender as an exclusion or it will not be allowed to run in managed environments.**
1. Download the latest executable (.exe) from the releases page.
2. Run it (double-click).

## Usage

Once GalleryMark is open, you can begin grading in one of two ways:

#### By File

Navigate to File > Open... menu option or press `Ctrl+O`. In the dialog, locate the file you would like to open and choose it.

Once opened, the first page of the document is presented automatically. Use the left or right arrow buttons or keys to navigate between pages in the document.

You can zoom into a page by using the scroll wheel, `Ctrl+Plus`, `Ctrl+Minus` or the "Zoom In/Out" buttons.

To draw on a page, press the "Pen Tool" button or press `P`.
To erase a pen stroke, press the "Eraser Tool" button or press `E`.

For both the pen and eraser, you can undo the last drawn pen segment or eraser mark with `Ctrl+Z`. Use `Ctrl+Shift+Z` to redo.

Once you are done marking the document, navigate to the File > Save menu option or press `Ctrl+S` to save a modified copy of the document. The copy will be saved within the same directory as the original, but with a file name following the form of `<The original file name> (Graded)<The original extension>`.

#### By Directory

Navigate to GalleryMark > Open directory... menu option or press `Ctrl+D`. In the dialog, locate the directory you would like to open and choose it.

Once opened, PDF files present within the directory will be listed on the left (the file list). You can double-click any to open them, or use the up and down arrows keys to navigate between documents.

Within the file list, the names of each file may have the following characters before or after their name:

- A `>` character before the file name indicates the document you are currently viewing.
- A `+` character before the file name indicates that the file is currently in use by the program.
- A `*` character after the file name indicates that there are unsaved changes within that file.

Adding or removing files in the currently opened directory externally will not be reflected in the file list until it is manually refreshed. To refresh, navigate to the GalleryMark > Refresh menu option or press `F5`.

If you would like to save all opened documents at once, navigate to the GalleryMark > Save open files menu option or press `Ctrl+Alt+S`.

If you would like to view the currently opened directory in your systems file explorer, navigate to the GalleryMark > Show in explorer menu option or press `Ctrl+E`.

## Future
In the future, I would like to add the following features (in order of least to most complex):

- A way to customize the file name save template.
- A way to customize where file copies are saved.
- Allowing multiple directories to be open at once.
- A dedicated preferences editor dialog.
- Text tool.
- LaTeX math formula tool.
- Support to view Microsoft Word `DOCX` files.
- Automatic file list refresh upon file system modification.