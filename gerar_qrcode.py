import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

def gerar_qrcode(url, texto_titulo, nome_arquivo_saida):
    # --- 1. Gerar o QR Code ---
    qr = qrcode.QRCode(
        version=None, # Ajusta o tamanho automaticamente
        error_correction=qrcode.constants.ERROR_CORRECT_L, # Menor correção para o código ficar menos denso
        box_size=10,
        border=2, # Borda menor pois será adicionada a uma imagem maior
    )
    qr.add_data(url)
    qr.make(fit=True)
    # Cria a imagem do QR Code (preto no branco)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # --- 2. Criar a imagem final com texto ---
    # Tenta carregar uma fonte TrueType (Arial). Se não tiver, usa uma padrão.
    try:
        # Você pode precisar ajustar o caminho se a fonte não for encontrada
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()
        print("Fonte Arial não encontrada. Usando fonte padrão.")

    # Calcula o tamanho do texto
    draw_dummy = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    text_bbox = draw_dummy.textbbox((0, 0), texto_titulo, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Calcula o tamanho total da imagem final
    qr_width, qr_height = qr_img.size
    padding = 20
    total_width = max(qr_width, text_width + 2 * padding)
    total_height = qr_height + text_height + 3 * padding

    # Cria a imagem de fundo branca
    final_img = Image.new('RGB', (total_width, total_height), 'white')
    draw = ImageDraw.Draw(final_img)

    # Desenha o texto centralizado no topo
    text_x = (total_width - text_width) // 2
    text_y = padding
    draw.text((text_x, text_y), texto_titulo, fill="black", font=font)

    # Cola o QR Code abaixo do texto
    qr_x = (total_width - qr_width) // 2
    qr_y = text_y + text_height + padding
    final_img.paste(qr_img, (qr_x, qr_y))

    # --- 3. Salvar a imagem final ---
    final_img.save(nome_arquivo_saida)
    print(f"Imagem criada com sucesso: {nome_arquivo_saida}")
    return nome_arquivo_saida

if __name__ == "__main__":
    # --- Configurações ---
    # O link completo para o documento do SharePoint
    url = "https://clxgroup.sharepoint.com/sites/BusinessITInfo/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FBusinessITInfo%2FShared%20Documents%2FIT%20Guides%2FPrinters%2FPrinter%20Guide%20v2%2Epdf&parent=%2Fsites%2FBusinessITInfo%2FShared%20Documents%2FIT%20Guides%2FPrinters"
    texto_titulo = "Printer Guide"
    nome_arquivo_saida = "printer_guide_qrcode_com_texto.png"
    
    gerar_qrcode(url, texto_titulo, nome_arquivo_saida)