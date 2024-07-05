import torch
import os
from config import ASR_MODEL_DIR
from transformers import (
    AutoModelForSpeechSeq2Seq,
    AutoProcessor,
    pipeline, # 긴 문장 처리하기 위해
)

class WhisperInference:
    def __init__(self) -> None:
        self.device: str = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.base_model: str = 'openai/whisper-medium' # small로 쓰려면 아래도 small로
        self.pretrained_model: str = os.path.join(ASR_MODEL_DIR, 'whisper-medium') # small로 쓰려면 위도 small로
        self.torch_type: float = torch.float16 if torch.cuda.is_available() else torch.float32
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            pretrained_model_name_or_path = self.pretrained_model,
            torch_dtype=self.torch_type,
            use_safetensors=True,
            low_cpu_mem_usage=True,
            device_map=self.device, # 데이터를 읽어서 램에 올리고 gpu로 옮겨야하는데 램에서 gpu로 옮기는 이동경로를 최소화/최적화는 위치가 따로 있어서 데이터를 램의 그곳에 둠
            # attn_implementation="flash_attention_2", # cuda16이상
        )
        self.model.to(self.device) 
        self.processor = AutoProcessor.from_pretrained(self.base_model)
        self.pipe = pipeline(
            "automatic-speech-recognition", # task
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor, # 파형 추출
            torch_dtype=self.torch_type
        )
        
    def inference(
        self,
        audio_file: str,
        lang: str = 'korean',
        task: str = 'transcribe',
    ) -> str:
        '''음성파일 -> 텍스트 추론 수행'''
        options = {
            "language": lang,
            "task": task,
        }
        result = self.pipe(audio_file, generate_kwargs=options)
    
        if isinstance(result, dict):
            text = result['text']
        elif isinstance(result, list):
            text = ''
            for x in result:
                chunk_list = x['chunks']
                for chunk in chunk_list:
                    text += chunk['text']
        return text