import streamlit as st
import ezdxf
import io

# Sayfa Yapılandırması (Sade ve Odaklı)
st.set_page_config(page_title="Ârif Viewer", layout="centered")

# Dil Seçimi - Yan Menü
lang = st.sidebar.selectbox("Dil / Language", ["Türkçe", "English"])

# Metin Sözlüğü
t = {
    "Türkçe": {
        "title": "Ârif DWG/DXF İzleyici",
        "sub": "Reklamsız, hızlı, mühendis dostu.",
        "upload": "DXF dosyasını buraya sürükleyin veya seçin",
        "info": "Dosya Teknik Bilgileri",
        "layers": "Mevcut Katmanlar (Layers)",
        "success": "Dosya başarıyla analiz edildi."
    },
    "English": {
        "title": "Ârif DWG/DXF Viewer",
        "sub": "Ad-free, fast, engineer friendly.",
        "upload": "Drag and drop DXF file here or browse",
        "info": "File Technical Info",
        "layers": "Available Layers",
        "success": "File analyzed successfully."
    }
}

st.title(t[lang]["title"])
st.write(t[lang]["sub"])
st.write("---")

# Dosya Yükleme Alanı
uploaded_file = st.file_uploader(t[lang]["upload"], type=['dxf'])

if uploaded_file:
    try:
        # Dosyayı belleğe al ve oku
        file_bytes = uploaded_file.read()
        doc = ezdxf.readptr(file_bytes)
        
        st.success(t[lang]["success"])
        
        # Teknik Detaylar Paneli
        with st.expander(t[lang]["info"]):
            st.write(f"**DXF Version:** {doc.dxfversion}")
            st.write(f"**Entity Count:** {len(doc.modelspace())}")
        
        # Katmanları Listele
        st.subheader(t[lang]["layers"])
        layers = [layer.dxf.name for layer in doc.layers]
        st.info(", ".join(layers))
        
    except Exception as e:
        st.error(f"Hata / Error: {e}")
