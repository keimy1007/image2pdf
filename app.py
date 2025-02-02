import os
import streamlit as st
from PIL import Image
from reportlab.pdfgen import canvas

def image2pdf(input_dir, output_pdf, max_width=2400, max_height=1800, quality=80):
    """
    指定されたディレクトリ内の画像ファイルをPDFに変換する関数
    """
    # 指定されたディレクトリ内の全ての画像ファイルを取得
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    # 画像をソート
    image_files.sort()
    
    # PDFキャンバスを作成
    c = canvas.Canvas(output_pdf)
    
    for image_file in image_files:
        img_path = os.path.join(input_dir, image_file)
        try:
            img = Image.open(img_path)
        except Exception as e:
            st.error(f"画像 {img_path} の読み込みに失敗しました: {e}")
            continue

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

# Streamlitのページ設定
st.set_page_config(page_title="Image2PDF", layout="centered")

# おしゃれな見出しの表示 (HTMLを利用)
st.markdown(
    """
    <h1 style="text-align: center; font-family: 'Courier New', Courier, monospace; color: #2c3e50;">
        Image2PDF
    </h1>
    """, 
    unsafe_allow_html=True
)

# 使い方の説明
st.markdown("""
**使い方:**
1. **入力画像のディレクトリパス** を下のテキストボックスに入力してください。  
   ※ディレクトリ内には変換対象となる画像ファイル（png, jpg, jpeg, gif, bmp）が含まれている必要があります。  
2. （任意）**出力PDFファイルのパス** を入力できます。指定しない場合は、入力した `input_dir` の文字列に「.pdf」を付加したファイル名が利用されます。  
3. 「変換実行」ボタンをクリックすると、指定ディレクトリ内の画像が1ページずつのPDFに変換されます。
""")

# 入力ウィジェット
input_dir = st.text_input("入力画像のディレクトリパス", value="")
output_pdf = st.text_input("出力PDFファイルのパス（任意）", value="")

if st.button("変換実行"):
    if not input_dir:
        st.error("入力ディレクトリのパスを指定してください。")
    elif not os.path.isdir(input_dir):
        st.error("指定された入力ディレクトリは存在しません。")
    else:
        # 出力PDFファイル名が未指定の場合は、input_dir に ".pdf" を付けた名前にする
        if not output_pdf:
            output_pdf = f"{input_dir}.pdf"
        
        try:
            image2pdf(input_dir, output_pdf)
            st.success(f"変換が完了しました！ 出力ファイル: {output_pdf}")
        except Exception as e:
            st.error(f"変換中にエラーが発生しました: {e}")