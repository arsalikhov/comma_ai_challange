from video_processing_binary import VideoPlayback
from video_processing_bgrm import RemoveBG

p = VideoPlayback()
p.play(video = r'data\train.mp4', q = 'q', k = 'k')

# mb = RemoveBG()
# mb.play(video = r'data\train.mp4', q = 'q', k = 'k')

