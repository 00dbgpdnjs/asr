'''wisper streaming'''

import soundcard as sc

def select_mic() -> int:
    mics = sc.all_microphones(include_loopback=True)
    print('\n--------------------------------------------')
    print('사용 가능한 음성 입출력 장치 목록입니다.')
    print('\n--------------------------------------------')
    for idx, mic in enumerate(mics):
        try:
            print(f'\n{idx}: {mic.name}')
        except Exception as e:
            print(e)
    mic_idx = int(input('\n사용할 마이크의 번호를 입력해 주세요: '))
    # print(f'{mic_idx}, type: {type(mic_idx)}')
    print('\n')
    return mic_idx


if __name__ == "__main__":
    select_mic()