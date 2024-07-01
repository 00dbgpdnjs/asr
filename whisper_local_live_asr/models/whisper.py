'''
Implementation of openai/whisper-large-v3
    Source: https://huggingface.co/openai/whisper-large-v3
Fine tuning:
    Source: https://huggingface.co/blog/fine-tune-whisper
'''

import torch
from transformers import (
    WhisperProcessor,
    AutoModelForSpeechSeq2Seq,
    AutoProcessor,
    pipeline,
)

class CJUWhisper:
    def __init__(
        self,
        sampling_rate: int = 16_000, # audio sampling rate
        task: str = 'transcribe', # task, one of ['transcribe', 'translate']
        lang: str = 'korean', # language (ex. korean, english, frech, ...)
        # base_model for processor, feature_extractor, and tokenizer
        base_model: str = 'openai/whisper-small',
        pretrained_model: str = 'model_archive\whisper-small',
    ) -> None:
        self.sampling_rate = sampling_rate
        self.task = task
        self.lang = lang
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.base_model = base_model
        self.pretrained_model = pretrained_model
        # self.processor = WhisperProcessor.from_pretrained(self.base_model)
        self.processor = AutoProcessor.from_pretrained(self.base_model)
        # Applying flash_attention
        #   - https://huggingface.co/openai/whisper-large-v3/discussions/63
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            pretrained_model_name_or_path=self.pretrained_model,
            torch_dtype=self.torch_dtype,
            use_safetensors=True,
            low_cpu_mem_usage=True,
            device_map=self.device,
            # attn_implementation='flash_attention_2' # cpu 쓸거면 주석 처리
        )
        self.model.to(self.device) # attn_implementation 주석 해제 시 이 라인 주석 처리
        self.pipe = pipeline(
            task="automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            max_new_tokens=128,
            chunk_length_s=30,
            batch_size=16,
            return_timestamps=True,
            torch_dtype=self.torch_dtype,
            # device=device,
        )
    
    # whisper는 제일 적당한 언어로 scriping 해주는데 헷갈리면 영어로 나올 수 있어서 정확히 korean으로 force
    def get_forced_decoder_ids(self, lang:str = 'korean') -> object:
        self.processor
        return self.processor.get_decoder_prompt_ids(language=lang, task='translate')
    
    
    def action(self, data: any) -> None:
        '''Perform inference
            data praram : 마이크 목소리, main.py(audio_float32)에서 넘어옴 
        '''
        optinos = {
            'language' : self.lang,
            'task' : self.task,
        }
        # whisper는 data를 numpy로 처리하는 main.py의 audio_float32가 텐서라서 체크
        if isinstance(data, torch.Tensor):
            data = data.numpy()
        result = self.pipe(inputs=data, generate_kwargs=optinos) # 음성으로부터 변환된 텍스트 반환
        
        # 음성 파일이 길면 dict가 아니라 list로 넘어올 수도 있음
        if isinstance(result, dict):
            text = result['text']
            return text
        elif isinstance(result, list):
            text = ''
            for x in result:
                temp_text = [chunk['text'] for chunk in x['chuncks']]
                text += ''.join(temp_text)
            return text
        else:
            print('Type error')
        
    