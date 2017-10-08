import argparse
import os.path
from subprocess import call
from process import process

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract keyframes from a video file')
    parser.add_argument('video', metavar='video_path', type=str,
                        help='video to process')
    args = parser.parse_args()
    if not os.path.isfile(args.video):
        print('Error: File "{0}" does not exist'.format(args.video))
        exit(1)
    videoName = os.path.splitext(args.video)[0]
    basePath = os.path.dirname(os.path.abspath(args.video))
    basePath += "/" + videoName + "/"

    # Create result dir if needed
    if not os.path.exists(basePath):
        if os.path.isfile(basePath):
            print('Error: Connot reate folder "{0}" a file exist with the same name'.format(basePath))
            exit(1)
        os.mkdir(basePath)
    else:
        print("Previous generated dir found")

    # Create keyframes dir if needed and generate it
    if not os.path.exists(basePath + "keyframes/"):
        if os.path.isfile(basePath + "keyframes/"):
            print('Error: Connot reate folder "{0}" a file exist with the same name'.format(basePath))
            exit(1)
        os.mkdir(basePath + "keyframes/")
        print("Generating keyframes... This might take a while")
        call(['ffmpeg', '-loglevel', 'error', '-i',  args.video, '-vf', 'select=eq(pict_type\,I)', '-vsync',  'vfr', \
             basePath + "keyframes/" + 'frame-%04d.png'])
        print("Keyframes generated!")
    else:
        print("Found keyframes dir, assuming already generated")

    # Clear previous matches

    call(['rm', '-Rf', basePath + "/withMatch" ])
    call(['mkdir', '-p', basePath + "/withMatch"])
    call(['rm', '-Rf', basePath + "/faces" ])
    call(['mkdir', '-p', basePath + "/faces"])

    process(basePath)

