import streamlit as st
import ezdxf
import aspose.cad as cad
import io
import os

st.set_page_config(page_title="Ârif Viewer", layout="centered")

lang = st.sidebar.selectbox("Dil / Language", ["Türkçe", "English"])

t = {
    "Türkçe": {
        "title": "Ârif DWG/DXF İzleyici",
        "sub": "DWG desteği aktif. Analiz ediliyor...",
        "upload": "DWG veya DXF dosyasını seçin",
        "info": "Teknik Veriler",
        "success": "Dosya başarıyla açıldı."
    },
    "English": {
        "title": "Ârif DWG/DXF Viewer",
        "sub": "DWG support active. Analyzing...",
        "upload": "Choose DWG or DXF file",
        "info": "Technical Data",
        "success": "File opened successfully."
    }
}

st.title(t[lang]["title"])
st.write(t[lang]["sub"])

uploaded_file = st.file_uploader(t[lang]["upload"], type=['dwg', 'dxf'])

if uploaded_file:
    try:
        file_bytes = uploaded_file.read()
        file_name = uploaded_file.name
        
        # Eğer dosya DWG ise geçici olarak DXF'e çevir
        if file_name.lower().endswith('.dwg'):
            with st.spinner("DWG çözülüyor (5-10 sn)..."):
                # Bellekteki dosyayı Aspose ile yükle
                input_stream = io.BytesIO(file_bytes)
                image = cad.Image.load(input_stream)
                
                # Geçici DXF olarak kaydet
                temp_dxf = "temp_project.dxf"
                image.save(temp_dxf, cad.imageoptions.DxfOptions())
                doc = ezdxf.readfile(temp_dxf)
                os.remove(temp_dxf) # Temizlik
        else:
            doc = ezdxf.readptr(io.BytesIO(file_bytes).read())

        st.success(t[lang]["success"])
        
        with st.expander(t[lang]["info"]):
            st.write(f"**Format:** {file_name.split('.')[-1].upper()}")
            st.write(f"**Katman Sayısı:** {len(doc.layers)}")
            
        layers = [layer.dxf.name for layer in doc.layers]
        st.info(", ".join(layers))
        
    except Exception as e:
        st.error(f"Hata: {e}")
