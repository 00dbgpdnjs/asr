''''''

import argparse
from audio_io import select_mic

def get_parser():
    parser = argparse.ArgumentParser()
    # 터미널 옵션 등록
    return parser.parse_args()

def main(config) -> None:
    '''main function - entry point'''
    mic_id = select_mic()
    print(f'mic_id: {mic_id}')
    
    # whisper model upload
    
    # start with VAD

if __name__ == '__main__':
    config = get_parser()
    main(config)