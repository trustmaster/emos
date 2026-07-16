ffmpeg -i import-url-demo.mov -filter_complex "\
[0:v]trim=0:5,setpts=PTS-STARTPTS[a];\
[0:v]trim=5:40,setpts=(PTS-STARTPTS)/4[b];\
[0:v]trim=40:50,setpts=PTS-STARTPTS[c];\
[0:v]trim=50:56,setpts=(PTS-STARTPTS)/4[d];\
[0:v]trim=56:64,setpts=(PTS-STARTPTS)[e];\
[a][b][c][d][e]concat=n=5:v=1[out]" -map "[out]" -an import-url-demo-edited.mov