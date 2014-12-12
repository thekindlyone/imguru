#IMGURU

Pushes images to imgur from command line.

Wrote this so that I can easily share gui screenshots with my client for aesthetic inputs and use the same screenshots to troubleshoot with other programmers(people who actually know css  )
It works like:
```
thekindlyone@deepthought:~/Pictures/Wallpapers$ imguru.py .
directory detected 
Uploaded Ubuntu (1).jpg to http://i.imgur.com/VBZMmK7.jpg
Uploaded ubuntu-wallpaper-40666-41617-hd-wallpapers.jpg to http://i.imgur.com/j0RiAdp.jpg
Uploaded ubuntu-wallpapers-21.png to http://i.imgur.com/7Rx58My.jpg
Uploaded 1613386.jpg to http://i.imgur.com/o9Vn5nl.jpg
Uploaded ubuntu-4188-1600x900.jpg to http://i.imgur.com/U9uVeqT.jpg
Album Created! title: Wallpapers url: http://thekindlyone.co.in/imguru/gallery/ly4zJ6

```
Once the upload is finished, all the links are sent to a server where an album/gallery is generated with a permalink(this is to bypass the 2 factor authentication needed from imgur to create imgur album..something that is hard to arrange from a terminal)
terminal app:
https://github.com/thekindlyone/imguru
serverside:
https://github.com/thekindlyone/imguru_www
example gallery:
http://thekindlyone.co.in/imguru/gallery/ly4zJ6