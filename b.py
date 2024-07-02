import streamlit as st
import base64

st.title("カメラで写真を撮るアプリ")

# カメラの入力を受け取る
picture = st.camera_input("写真を撮る")

if picture:
    # 撮影された写真を表示
    st.image(picture)

    # 撮影された写真を保存
    with open("captured_image.png", "wb") as f:
        f.write(picture.getbuffer())
    st.success("写真が保存されました！")

    # ダウンロードリンクを作成
    with open("captured_image.png", "rb") as f:
        bytes_data = f.read()
        b64 = base64.b64encode(bytes_data).decode()
        href = f'<a href="data:file/png;base64,{b64}" download="captured_image.png">写真をダウンロード</a>'
        st.markdown(href, unsafe_allow_html=True)
