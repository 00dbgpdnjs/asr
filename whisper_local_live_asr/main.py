''''''

import argparse
import collections, queue
import numpy as np
# import pyaudio
# import webrtcvad
from halo import Halo
import torch
import torchaudio
from audio_io import select_mic
from models.whisper import CJUWhisper
from vad import VADAudio
from utils import Int2Float

DEFAULT_SAMPLE_RATE: int = 16000

def get_parser():
    parser = argparse.ArgumentParser(
        description="Stream from microphone to webRTC and silero VAD"
    )
    # VAD related args
    parser.add_argument('-v', '--webRTC_aggressiveness', type=int, default=3,
                        help="Set aggressiveness of webRTC: an integer between 0 and 3, 0 being the least aggressive about filtering out non-speech, 3 the most aggressive. Default: 3")
    parser.add_argument('--nospinner', action='store_true',
                        help="Disable spinner")
    # parser.add_argument('-d', '--device', type=int, default=None,
    #                     help="Device input index (Int) as listed by pyaudio.PyAudio.get_device_info_by_index(). If not provided, falls back(소리가 나는 마이크 마다 받음) to PyAudio.get_default_device().")

    parser.add_argument('-name', '--silaro_model_name', type=str, default="silero_vad",
                        help="select the name of the model. You can select between 'silero_vad',''silero_vad_micro','silero_vad_micro_8k','silero_vad_mini','silero_vad_mini_8k', default= 'silero_vad'")
    parser.add_argument('--reload', action='store_true',help="download the last version of the silero vad")
    # ASR related args
    parser.add_argument('--task', default='transcribe',
                        help='ARS task, default: "transcribe"')
    parser.add_argument('--lang', default='korean',
                        help='ASR language, default: "korean"')
    parser.add_argument('--base-model', default='openai/whisper-small')
    parser.add_argument('--pretrained-model', default='model_archive\whisper-small',
                        help='ASR pretrained model, default: "model_archive\whisper-small"')
    
    config = parser.parse_args()
    config.rate=DEFAULT_SAMPLE_RATE
    return config

def main(config) -> None:
    '''main function - entry point'''
    mic_id = select_mic()
    print(f'mic_id: {mic_id}')
    
    # whisper model upload
    whisper_model = CJUWhisper(
        task=config.task,
        lang=config.lang,
        base_model=config.base_model,
        pretrained_model=config.pretrained_model
    )
    
    # Start audio with VAD
    vad_audio = VADAudio(
        aggressiveness=config.webRTC_aggressiveness,
        device=mic_id, # 마이크 장치
        input_rate=config.rate
    )

    print("Listening (ctrl-C to exit)...")
    frames = vad_audio.vad_collector()

    # load silero VAD -> deprecate 되서 comment 처리함
    # UserWarning: torchaudio._backend.set_audio_backend has been deprecated. 
    # With dispatcher enabled, this function is no-op. 
    # You can remove the function call. 
    #   torchaudio.set_audio_backend("soundfile")
    # torchaudio.set_audio_backend("soundfile")
    
    # 구글 검색: torch.hub.load('snakers4/silero-vad')
    #   -> https://github.com/snakers4/silero-vad
    # pytorch 로딩 방법: 
    #   -> https://pytorch.org/hub/
    #   -> https://pytorch.org/docs/stable/hub.html#torch.hub.load
    model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                    model=config.silaro_model_name,
                                    force_reload= config.reload)
    get_speech_ts, _, _, _, _ = utils


    # Stream from microphone to DeepSpeech using VAD
    if not config.nospinner:
        spinner = Halo(spinner='line')
    wav_data = bytearray()
    for frame in frames:
        if frame is not None:
            if spinner: spinner.start()

            wav_data.extend(frame)
        else: # 말을 안하는 경우
            if spinner: spinner.stop()
            # print("webRTC has detected a possible speech")

            newsound= np.frombuffer(wav_data,np.int16)
            audio_float32=Int2Float(newsound)
            time_stamps =get_speech_ts(
                audio_float32, 
                model,
            )

            if(len(time_stamps)>0): # 사람 목소리
                # asr 처리 코드
                # - 우리 모델에 audio_float32 (.mp3)를 넘겨줌
                # - 우리 모델은 음성 신호를 텍스트로 변환
                transcript = whisper_model.action(data=audio_float32)
                print(f'transcript: {transcript}')
                # print("silero VAD has detected a possible speech")
            else:
                print("silero VAD has detected a noise")
            print()
            wav_data = bytearray()
if __name__ == '__main__':
    config = get_parser()
    main(config)