---
title: Voz do Pai — LTX-2.5
emoji: 🎬
colorFrom: purple
colorTo: blue
sdk: gradio
app_file: app.py
pinned: false
---

# Voz do Pai — LTX-2.5

Interface em português para geração de vídeos curtos verticais 9:16.

Este projeto usa o Space oficial **Lightricks/LTX-2.5** como motor de geração através do `gradio_client`. Assim, este repositório não precisa baixar os pesos de 22B nem instalar ComfyUI.

## Recursos

- Prompt em português
- Vídeo 9:16
- 1 a 5 segundos
- Áudio gerado pelo LTX-2.5 quando retornado pelo Space oficial
- Melhoria automática de prompt
- Seed
- Botão GERAR VÍDEO

## Publicar no Hugging Face

Crie um Space Gradio e copie os arquivos deste repositório para ele.

O Space oficial do motor é:
https://huggingface.co/spaces/Lightricks/LTX-2.5

O modelo usado pelo motor é:
https://huggingface.co/Lightricks/LTX-2.5-Diffusers

## Observação

A geração acontece no Space oficial. Portanto, disponibilidade e cota de GPU dependem do serviço do Hugging Face e do Space oficial.
