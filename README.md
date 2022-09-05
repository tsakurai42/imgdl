# imgdl
An image/video downloading script for fun

Takes a newline delimited text file of JSONs from either twitter or tiktok, 
finds the image or video URLs and downloads them and saves them in a file
name format that I like.

Knows to stop downloading tiktoks once it hits a video it has seen before.
Also will not download if the video it's trying to download already exists.