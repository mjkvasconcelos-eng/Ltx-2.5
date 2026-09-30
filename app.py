import gradio as gr
from gradio_client import Client

OFFICIAL_SPACE = "Lightricks/LTX-2.5"

def gerar(prompt, duracao, seed, melhorar):
    if not prompt or not prompt.strip():
        raise gr.Error("Digite um prompt.")
    client = Client(OFFICIAL_SPACE)
    # Endpoint público do Space oficial LTX-2.5.
    result = client.predict(
        prompt.strip(),
        None,
        1472, 832,
        float(duracao),
        int(seed),
        "conv",
        False,
        False,
        bool(melhorar),
        api_name="/run",
    )
    # result = [video, prompt_usado, seed_usado, duração]
    return result[0], result[1], result[2], result[3]

exemplo = """Vídeo vertical 9:16, ultra-realista e cinematográfico.
Um ancião sábio de cabelos grisalhos e barba branca caminha lentamente por
uma antiga estrada de pedra ao amanhecer. Montanhas ao fundo, neblina suave,
luz dourada atravessando a atmosfera. A câmera faz uma aproximação lenta e
suave. Vento movimenta naturalmente a roupa e a barba. Atmosfera bíblica,
emocional e épica, movimentos humanos realistas, sem texto na tela."""

with gr.Blocks(title="Voz do Pai — LTX-2.5") as demo:
    gr.Markdown("# ✨ Voz do Pai — LTX-2.5")
    gr.Markdown("Gerador online de vídeos curtos em **9:16**, usando o Space oficial LTX-2.5 do Hugging Face.")

    prompt = gr.Textbox(
        label="Prompt do vídeo",
        value=exemplo,
        lines=8,
        placeholder="Descreva a cena que deseja criar..."
    )

    with gr.Row():
        duracao = gr.Slider(1, 5, value=2, step=0.5, label="Duração (segundos)")
        seed = gr.Number(value=42, precision=0, label="Seed")

    melhorar = gr.Checkbox(
        value=True,
        label="Melhorar prompt automaticamente"
    )

    gerar_btn = gr.Button("🎬 GERAR VÍDEO", variant="primary")

    video = gr.Video(label="Vídeo gerado", autoplay=True)
    prompt_usado = gr.Textbox(label="Prompt enviado ao modelo", interactive=False)
    seed_usado = gr.Number(label="Seed utilizado", interactive=False)
    duracao_real = gr.Textbox(label="Duração gerada", interactive=False)

    gerar_btn.click(
        gerar,
        inputs=[prompt, duracao, seed, melhorar],
        outputs=[video, prompt_usado, seed_usado, duracao_real],
    )

if __name__ == "__main__":
    demo.launch()
