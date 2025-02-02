import os
import argparse
from PIL import Image
from reportlab.pdfgen import canvas

def image2pdf(input_dir, output_pdf, max_width=2400, max_height=1800, quality=80):
    # 指定されたディレクトリ内の全ての画像ファイルを取得
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    # 画像をソート
    image_files.sort()
    
    # PDFキャンバスを作成
    c = canvas.Canvas(output_pdf)
    
    for image_file in image_files:
        img_path = os.path.join(input_dir, image_file)
        img = Image.open(img_path)
        
        # RGBAの場合、RGBに変換
        if img.mode == "RGBA":
            img = img.convert("RGB")
        
        # 画像のオリジナルサイズを保持するが、最大サイズを超える場合は縮小
        original_width, original_height = img.size
        if original_width > max_width or original_height > max_height:
            img.thumbnail((max_width, max_height))
        
        # 圧縮して一時的にJPEG形式で保存
        compressed_img_path = os.path.join(input_dir, f"compressed_{image_file}")
        img.save(compressed_img_path, format="JPEG", quality=quality)
        
        # 圧縮後の画像のサイズを取得
        compressed_img = Image.open(compressed_img_path)
        width, height = compressed_img.size
        
        # PDFページのサイズを設定
        c.setPageSize((width, height))
        
        # 圧縮画像をPDFに描画
        c.drawImage(compressed_img_path, 0, 0, width, height)
        
        # 次のページに移動
        c.showPage()
        
        # 圧縮画像を削除
        os.remove(compressed_img_path)
    
    # PDFを保存
    c.save()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="指定されたディレクトリ内の画像をPDFに変換します。")
    parser.add_argument("input_dir", help="入力画像が保存されているディレクトリのパス")
    parser.add_argument("--output_pdf", help="出力PDFファイルのパス（省略時はinput_dirの名前を利用して生成）")
    args = parser.parse_args()
    
    input_dir = args.input_dir
    # 出力ファイル名が指定されていなければ、ディレクトリ名に基づいたファイル名を生成
    if args.output_pdf:
        output_pdf = args.output_pdf
    else:
        # ディレクトリの末尾のスラッシュを取り除き、basename を使ってファイル名を作成
        # base_dir = os.path.basename(os.path.normpath(input_dir))
        output_pdf = f"{input_dir}.pdf"
        print(output_pdf)
    
    image2pdf(input_dir, output_pdf)