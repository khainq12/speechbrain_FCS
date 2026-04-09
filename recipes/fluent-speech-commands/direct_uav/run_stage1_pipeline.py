import json
import torch
import pandas as pd
import sys
import os

# Thêm đường dẫn gốc của repo để import được speechbrain_uav
sys.path.append("/media/data/students/nguyenquangkhai/speechbrain")

# Import các module của bạn
from speechbrain_uav.uav_mapping import UAVMapper
from speechbrain_uav.semantic_packet import SemanticPacket

# Import SpeechBrain (Dùng đúng cách đã test thành công, tránh lỗi torchaudio)
from speechbrain.inference.SLU import EndToEndSLU
from speechbrain.dataio.dataio import read_audio

def main():
    print("Đang tải mô hình SLU...")
    slu_model = EndToEndSLU.from_hparams(
        source="speechbrain/slu-direct-fluent-speech-commands-librispeech-asr", 
        savedir="../tmp_pretrained"
    )
    
    # Khởi tạo mapper của bạn
    uav_mapper = UAVMapper()

    # Lấy danh sách file test (Lấy 5 file đầu tiên để test nhanh)
    csv_path = "../direct/results/BPE51/1986/save/test.csv"
    df = pd.read_csv(csv_path)
    test_wavs = df['wav'].head(5).tolist()
    
    output_packets = []

    print("Bắt đầu chạy Pipeline Stage 1 (Speech -> UAV Mapping -> Packet)...")
    for wav_path in test_wavs:
        if not os.path.exists(wav_path):
            continue
            
        # A. Speech to FSC Raw Semantics
        waveform = read_audio(wav_path)
        batch = waveform.unsqueeze(0)
        rel_length = torch.tensor([1.0])
        
        predicted_tokens, _ = slu_model.decode_batch(batch, rel_length)
        predicted_semantics = [
            slu_model.hparams.tokenizer.decode_ids(utt_seq).split(" ")
            for utt_seq in predicted_tokens
        ]
        fsc_raw_string = " ".join(predicted_semantics[0])
        
        # B. Map sang UAV Schema (Dùng hàm mới sửa có chứa Regex)
        uav_dict = uav_mapper.map_fsc_to_uav(fsc_raw_string)
        
        # (Tạm thời gán cứng cho Phase 1, Phase 2 mới gọi HA normalizer)
        uav_dict["magnitude"] = "medium"
        uav_dict["urgency"] = "low"
        uav_dict["safety"] = "normal"
        
        # C. Tạo Semantic Packet
        packet = SemanticPacket(
            command_type=uav_dict.get("command_type", "unknown"),
            direction=uav_dict.get("direction", "hover"),
            altitude_action=uav_dict.get("altitude_action", "hold"),
            magnitude_rank=0, # Tạm hardcode
            urgency_rank=0,
            safety_rank=0,
            confidence=0.99
        )
        
        # D. Lưu lại kết quả
        output_packets.append({
            "input_wav": os.path.basename(wav_path),
            "fsc_raw_output": fsc_raw_string,
            "uav_mapped_dict": uav_dict,
            "semantic_packet_serialized": packet.serialize(),
            "token_sequence": packet.to_token_sequence()
        })
        print(f"✅ {os.path.basename(wav_path):30} -> {uav_dict.get('command_type')}")

    # 5. Xuất ra file JSON (Yêu cầu bắt buộc của Ngày 2)
    output_file = "stage1_sample_output.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_packets, f, indent=4, ensure_ascii=False)

    print(f"\n🎉 HOÀN THÀNH NGÀY 2! Đã sinh ra file: {output_file}")

if __name__ == "__main__":
    main()