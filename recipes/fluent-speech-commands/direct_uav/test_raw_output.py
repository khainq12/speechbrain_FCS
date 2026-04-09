import torch
import pandas as pd
from speechbrain.dataio.dataio import read_audio
from speechbrain.inference.SLU import EndToEndSLU

print("Đang tải mô hình SLU từ HuggingFace...")
slu_model = EndToEndSLU.from_hparams(
    source="speechbrain/slu-direct-fluent-speech-commands-librispeech-asr", 
    savedir="../tmp_pretrained"
)

# Tự động lấy đường dẫn file wav thật từ file test.csv
csv_path = "../direct/results/BPE51/1986/save/test.csv"
df = pd.read_csv(csv_path)
test_wav = df['wav'].iloc[0]  # Lấy file đầu tiên

print(f"Đang test với file: {test_wav}")

try:
    # 1. Đọc file âm thanh
    waveform = read_audio(test_wav)
    
    # 2. Tạo batch giả
    batch = waveform.unsqueeze(0)
    rel_length = torch.tensor([1.0])
    
    # 3. Dự đoán lấy tokens
    predicted_tokens, _ = slu_model.decode_batch(batch, rel_length)
    
    # 4. Giải mã tokens thành chuỗi semantics thô
    predicted_semantics = [
        slu_model.hparams.tokenizer.decode_ids(utt_seq).split(" ")
        for utt_seq in predicted_tokens
    ]
    
    # 5. Nối lại thành 1 chuỗi string duy nhất
    final_string = " ".join(predicted_semantics[0])
    
    print("\n" + "="*50)
    print("KẾT QUẢ ĐẦU RA THÔ CỦA MÔ HÌNH FSC:")
    print("="*50)
    print(final_string)
    print("="*50 + "\n")
    
except Exception as e:
    print(f"\nĐã xảy ra lỗi: {e}")