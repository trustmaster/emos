ffmpeg -i weekly-note-demo.mov -filter_complex "\
[0:v]trim=0:6,setpts=(PTS-STARTPTS)/1.5[a];\
[0:v]trim=6:29,setpts=(PTS-STARTPTS)/4[b];\
[0:v]trim=29:42,setpts=(PTS-STARTPTS)/1.5[c];\
[a][b][c]concat=n=3:v=1[out]" -map "[out]" -an weekly-note-demo-edited.mov