from pathlib import Path

from datasets import load_dataset  # type: ignore
from torch import cuda, float16, float32
from transformers import AutoModelForSpeechSeq2Seq  # type: ignore
from transformers import AutoProcessor, pipeline

device = 'cpu' # 'cuda:0' if cuda.is_available() else 'cpu'
torch_dtype = float16 if cuda.is_available() else float32

model_id = 'openai/whisper-large-v3'

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    'automatic-speech-recognition',
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch_dtype,
    device=device,
)

# dataset = load_dataset('distil-whisper/librispeech_long', 'clean', split='validation')
# sample = dataset[0]['audio']

# result = pipe(sample, return_timestamps=True)

test_data_path = Path(Path(__file__).resolve().parent, 'test_data')
# result = pipe(str(Path(test_data_path, '123.mp3')), return_timestamps=True)
result = pipe(str(Path(test_data_path, 'amazing-story.mp3')), return_timestamps=True)
print(result['text'])
