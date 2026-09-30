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

Interface em português para geração de vídeos verticais **9:16 com 30 segundos**.

## Como funciona

O motor oficial LTX-2.5 gera clipes curtos. Este Space monta um vídeo de 30 segundos em **6 segmentos contínuos de 5 segundos**:

1. Gera o primeiro segmento com texto + áudio.
2. Extrai o último frame.
3. Usa esse frame como imagem de referência para o segmento seguinte.
4. Repete o processo por 6 segmentos.
5. Une os seis MP4 em um único vídeo de aproximadamente 30 segundos, preservando o áudio.

O formato final é **832×1472 (9:16)**.

## Recursos

- 30 segundos por geração
- 6 segmentos contínuos de 5s
- Continuidade visual por último-frame
- Áudio do LTX-2.5 em cada segmento
- Prompt em português
- Formato vertical 9:16
- Seed inicial
- Melhoria automática de prompt
- Sem ComfyUI

## Importante

A geração dos segmentos continua dependendo do **Space oficial Lightricks/LTX-2.5** e das cotas/disponibilidade do Hugging Face. O Space oficial atualmente trabalha com duração curta; por isso os 30 segundos são montados por segmentos, e não por uma única inferência de 30 segundos.

A documentação do LTX-2.5 também descreve geração conjunta de vídeo e áudio e suporte a controle de duração. 

## Publicar no Hugging Face

Crie um Space Gradio e copie os arquivos deste repositório para ele.

Motor oficial:
https://huggingface.co/spaces/Lightricks/LTX-2.5

Modelo:
https://huggingface.co/Lightricks/LTX-2.5-Diffusers
