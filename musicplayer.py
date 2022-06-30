# Importing Required Modules & libraries
from tkinter import *
from tkinter.ttk import *
import pygame
import os

DEBUG = True


class MusicPlayer:
    """One object of this class represents a tkinter GUI application that plays
    audio files and can write and read a .m3u playlist."""

    def __init__(self, root):
        """Creates a tkinter GUI application that plays audio files and
        can write and read a .m3u playlist."""
        self.playlistfilename = 'playlist.m3u'
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("1000x200+200+200")
        pygame.init()
        pygame.mixer.init()
        self.track = StringVar()
        self.status = StringVar()

        # Creating trackframe for songtrack label & trackstatus label
        trackframe = LabelFrame(self.root, text="Song Track", relief=GROOVE)
        trackframe.place(x=0, y=0, width=600, height=100)
        songtrack = Label(trackframe, textvariable=self.track).grid(
            row=0, column=0, padx=10, pady=5)
        trackstatus = Label(trackframe, textvariable=self.status).grid(
            row=0, column=1, padx=10, pady=5)

        # Creating buttonframe
        buttonframe = LabelFrame(
            self.root, text="Control Panel", relief=GROOVE)
        # Inserting song control Buttons
        buttonframe.place(x=0, y=100, width=600, height=100)
        Button(buttonframe, text="Play", command=self.playsong).grid(
            row=0, column=0, padx=10, pady=5)
        Button(buttonframe, text="Pause", command=self.pausesong
               ).grid(row=0, column=1, padx=10, pady=5)
        Button(buttonframe, text="Unpause", command=self.unpausesong
               ).grid(row=0, column=2, padx=10, pady=5)
        Button(buttonframe, text="Stop", command=self.stopsong).grid(
            row=0, column=3, padx=10, pady=5)
        # Inserting playlist control Buttons
        Button(buttonframe, text="Load Playlist", command=self.loadplaylist).grid(
            row=1, column=0, padx=10, pady=5)
        Button(buttonframe, text="Save Playlist", command=self.saveplaylist
               ).grid(row=1, column=1, padx=10, pady=5)
        Button(buttonframe, text="Remove song", command=self.removesong
               ).grid(row=1, column=2, padx=10, pady=5)
        Button(buttonframe, text="Refresh from folder", command=self.refresh).grid(
            row=1, column=3, padx=10, pady=5)
        # Creating songsframe
        songsframe = LabelFrame(self.root, text="Song Playlist", relief=GROOVE)
        songsframe.place(x=600, y=0, width=400, height=200)
        scrol_y = Scrollbar(songsframe, orient=VERTICAL)
        self.playlist = Listbox(songsframe, yscrollcommand=scrol_y.set,
                                selectbackground="gold",
                                selectmode=SINGLE, relief=GROOVE)
        # Applying Scrollbar to playlist Listbox
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH)

        # Changing directory for fetching songs
        os.chdir("./music")
        # Inserting songs into playlist
        self.refresh()

    def playsong(self):
        """Displays selected song and its playing status and plays the song."""
        self.track.set(self.playlist.get(ACTIVE))
        self.status.set("-Playing")
        pygame.mixer.music.load(self.playlist.get(ACTIVE))
        pygame.mixer.music.play()

    def stopsong(self):
        """Displays stopped status and stops the song."""
        self.status.set("-Stopped")
        pygame.mixer.music.stop()

    def pausesong(self):
        """Displays the paused status and pauses the song."""
        self.status.set("-Paused")
        pygame.mixer.music.pause()

    def unpausesong(self):
        """Displays the playing status and unpauses the song."""
        self.status.set("-Playing")
        pygame.mixer.music.unpause()

    def removesong(self):
        """Deletes the active song from the playlist."""
        self.playlist.delete(ACTIVE)

    def loadplaylist(self):
        """
        Clears the current playlist and loads a previously saved playlist
        from the music folder. A user firendly message is appended to the
        status if a FileNotFoundError is caught.
        All other exception messages are appeneded to the status in
        their default string form.
        Ignores the lines that start with #.
        """
        try:
            with open('playlist.m3u', 'r') as file:
                self.playlist.delete(0, END)
                for line in file:
                    if line.startswith('#') is not True:
                        line = line.strip()
                        self.playlist.insert(END, line)
                    else:
                        pass
        except FileNotFoundError:
            errorMessage = " " + "File 'playlist.m3u was not found.'"
            self.status.set(self.status.get() + errorMessage)
        except Exception as e:
            errorMessage = 'error: "{}"'.format(e)
            self.status.set(self.status.get() + errorMessage)

    def saveplaylist(self):
        """Saves the current playlist to the playlist file in the music
        folder. All exception messages are appeneded to the status in their
        default string form.
        The first line of the file is only:
        #EXTM3U
        """
        if os.path.exists("playlist.m3u"):
            os.remove('playlist.m3u')
        try:
            playlistFiles = list(self.playlist.get(0, END))
            with open('playlist.m3u', 'w') as playList:
                playList.write('#EXTM3U\n')
                for item in playlistFiles:
                    playList.write(item)
                    playList.write('\n')
        except Exception as e:
            errorMessage = 'error: "{}"'.format(e)
            self.status.set(self.status.get() + errorMessage)

    def refresh(self):
        """
        Clears the current playlist
        and fills it with all valid sound files from the music folder.
        All exception messages are appened to the status
        in their default string form.
        If file does not starts w/ "." and does end in ".oog, .wav or .mp3"
        then it is inserted into the playlist """
        musicList = os.listdir()
        self.playlist.delete(0, END)
        try:
            for item in musicList:
                if ((item.startswith(".") is not True)
                        and (item.endswith((".ogg", ".wav", ".mp3")))):
                    self.playlist.insert(END, item)
        except Exception as e:
            errorMessage = 'error: "{}"'.format(e)
            self.status.set(self.status.get() + errorMessage)


def main():
    """Create main window and start a MusicPlayer aaplication on it."""
    # Creating TK root window
    root = Tk()
    # Passing root to the MusicPlayer constructor
    app = MusicPlayer(root)
    # Start the main GUI loop
    root.mainloop()


if __name__ == "__main__":
    main()
