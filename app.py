import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import gradio as gr
from gradio_client import Client

OFFICIAL_SPACE = "Lightricks/LTX-2.5"

# O Space oficial trabalha com clipes curtos. Aqui montamos 30s em 6 segmentos
# de 5s, usando o último frame de cada segmento como referência do próximo.
SEGMENT_SECONDS = 5.0
SEGMENTS = 6
TOTAL_SECONDS = SEGMENT_SECONDS * SEGMENTS
WIDTH = 832
HEIGHT = 1472


def run_official(prompt, image_path, seed, melhorar):
    client = Client(OFFICIAL_SPACE)
    return client.predict(
        prompt,
        image_path,
        HEIGHT,
        WIDTH,
        SEGMENT_SECONDS,
        int(seed),
        "conv",
        False,
        False,
        bool(melhorar),
        api_name="/run",
    )


def extract_last_frame(video_path, output_path):
    # Um frame final serve como condição visual para o próximo segmento.
    cmd = [
        "ffmpeg", "-y", "-sseof", "-0.15", "-i", str(video_path),
        "-frames:v", "1", "-q:v", "2", str(output_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def concatenate_segments(segment_paths, output_path):
    concat_file = output_path.parent / "concat.txt"
    with concat_file.open("w", encoding="utf-8") as f:
        for path in segment_paths:
            f.write(f"file '{Path(path).resolve()}'\n")

    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy", "-movflags", "+faststart",
        str(output_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path


def gerar_30s(prompt, seed, melhorar, progresso=gr.Progress()):
    if not prompt or not prompt.strip():
        raise gr.Error("Digite um prompt.")

    seed = int(seed)
    workdir = Path(tempfile.mkdtemp(prefix="voz_pai_ltx_"))
    segment_paths = []
    image_path = None
    usados = []

    try:
        base_prompt = prompt.strip()

        for i in range(SEGMENTS):
            progresso((i) / SEGMENTS, desc=f"Gerando segmento {i + 1}/{SEGMENTS}...")

            if i == 0:
                segment_prompt = base_prompt
            else:
                segment_prompt = f"""
CONTINUAÇÃO DIRETA DO SEGMENTO ANTERIOR.
Mantenha exatamente a identidade visual, aparência dos personagens,
roupas, cenário, iluminação, atmosfera, estilo cinematográfico e direção
de câmera. A primeira imagem recebida é o último frame do segmento anterior.
Comece a ação exatamente a partir desse momento, sem salto temporal,
sem trocar personagens e sem mudar o cenário.

{base_prompt}

Crie apenas a continuação natural desta cena por aproximadamente 5 segundos.
Vídeo vertical 9:16, ultra-realista e cinematográfico. Movimento suave,
físico e natural. Áudio ambiente e fala/narração em português brasileiro
quando o prompt pedir. Sem texto, sem legendas e sem marcas d'água.
""".strip()

            # Pequena variação de seed por segmento, mantendo uma sequência
            # determinística e evitando seis clipes idênticos.
            segment_seed = seed + i
            result = run_official(segment_prompt, image_path, segment_seed, melhorar)

            video_result = result[0]
            if not video_result:
                raise RuntimeError(f"O segmento {i + 1} não retornou vídeo.")

            video_path = Path(video_result)
            if not video_path.exists():
                raise RuntimeError(f"Arquivo do segmento {i + 1} não encontrado.")

            saved_segment = workdir / f"segmento_{i + 1}.mp4"
            shutil.copy2(video_path, saved_segment)
            segment_paths.append(saved_segment)
            usados.append(f"Segmento {i + 1}: seed {segment_seed}")

            # O próximo segmento recebe o último frame como imagem de referência.
            next_image = workdir / f"frame_{i + 1}.jpg"
            extract_last_frame(saved_segment, next_image)
            image_path = str(next_image)

        progresso(0.98, desc="Unindo os 6 segmentos e o áudio...")
        final_path = workdir / "voz_do_pai_30s.mp4"
        concatenate_segments(segment_paths, final_path)

        progresso(1.0, desc="Vídeo de 30 segundos concluído.")

        info = (
            f"30 segundos • 6 segmentos de 5s • 9:16 ({WIDTH}×{HEIGHT})\n"
            + " • ".join(usados)
        )
        return str(final_path), info

    except subprocess.CalledProcessError as e:
        raise gr.Error("O FFmpeg encontrou um erro ao processar os segmentos.") from e
    except Exception as e:
        raise gr.Error(f"Falha na geração: {e}") from e


exemplo = """Vídeo vertical 9:16, ultra-realista e cinematográfico.
Um ancião sábio de cabelos grisalhos e barba branca caminha lentamente por
uma antiga estrada de pedra ao amanhecer. Montanhas ao fundo, neblina suave,
luz dourada atravessando a atmosfera. A câmera acompanha o personagem com
movimento lento e cinematográfico. Vento movimenta naturalmente a roupa e a
barba. Atmosfera bíblica, emocional e épica, movimentos humanos realistas.
Narração masculina em português brasileiro, voz grave, profunda, acolhedora
e emocional, falando de forma natural durante a cena. Sem texto na tela e
sem legendas."""


with gr.Blocks(title="Voz do Pai — LTX-2.5 • 30 segundos") as demo:
    gr.Markdown("# ✨ Voz do Pai — LTX-2.5")
    gr.Markdown(
        "### Gerador de vídeo contínuo de **30 segundos**\n"
        "O vídeo é criado em **6 segmentos de 5 segundos**, usando o último "
        "frame de cada segmento como referência visual para o próximo. "
        "Formato **9:16 — 832×1472**, com áudio."
    )

    prompt = gr.Textbox(
        label="Prompt completo do vídeo",
        value=exemplo,
        lines=10,
        placeholder="Descreva a história, cenas, personagens, câmera e narração..."
    )

    with gr.Row():
        seed = gr.Number(value=42, precision=0, label="Seed inicial")
        melhorar = gr.Checkbox(
            value=True,
            label="Melhorar prompt automaticamente"
        )

    gerar_btn = gr.Button("🎬 GERAR VÍDEO DE 30 SEGUNDOS", variant="primary")

    progresso = gr.Markdown(
        "Cada geração cria 6 segmentos de 5s e depois os une em um único MP4."
    )

    video = gr.Video(label="Vídeo final — 30s", autoplay=True)
    info = gr.Textbox(label="Informações da geração", interactive=False)

    gerar_btn.click(
        gerar_30s,
        inputs=[prompt, seed, melhorar],
        outputs=[video, info],
    )


if __name__ == "__main__":
    demo.launch()
