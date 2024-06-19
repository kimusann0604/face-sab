import streamlit as st
import numpy as np
import cv2 as cv
import math
from PIL import Image
import pandas as pd

# 歪みを適用する関数
def apply_distortion(im_cv, scale_x, scale_y, amount):
    (h, w, _) = im_cv.shape

    flex_x = np.zeros((h, w), np.float32)
    flex_y = np.zeros((h, w), np.float32)

    center_x = w / 2
    center_y = h / 2
    radius = min(center_x, center_y)

    for y in range(h):
        delta_y = scale_y * (y - center_y)
        for x in range(w):
            delta_x = scale_x * (x - center_x)
            distance = delta_x * delta_x + delta_y * delta_y
            if distance >= (radius * radius):
                flex_x[y, x] = x
                flex_y[y, x] = y
            else:
                factor = 1.0
                if distance > 0.0:
                    factor = math.pow(math.sin(math.pi * math.sqrt(distance) / radius / 2), -amount)
                flex_x[y, x] = factor * delta_x / scale_x + center_x
                flex_y[y, x] = factor * delta_y / scale_y + center_y

    dst = cv.remap(im_cv, flex_x, flex_y, cv.INTER_LINEAR)
    return dst

data = {
    'クリニック名': ['美容外科A', '美容外科B', '美容外科C', '美容外科D', '美容外科E'],
    '評価': [4.5, 4.3, 4.0, 3.8, 3.5]
}
df = pd.DataFrame(data)

# Streamlit UI
page = st.sidebar.radio("アプリ選択", ("美容外科ランキング", "画像歪み調整ツール"))

if page == "画像歪み調整ツール":
    st.title('美容外科ランキング')
    st.table(df)
    
    selection = st.selectbox('クリニックを選択してください', df['クリニック名'])
    clinic_index = df[df['クリニック名'] == selection].index[0]
    st.write(f"選択したクリニック: {selection}")
    st.write(f"評価: {df.at[clinic_index, '評価']}")

elif page == "画像歪み調整ツール":
    st.title("画像歪み調整ツール")

    # ファイルアップローダー
    uploaded_file = st.file_uploader("画像を選択してください...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # 画像を読み込む
        image = Image.open(uploaded_file)
        im_cv = np.array(image)

        # パラメータ用のスライダー
        scale_x = st.slider("スケールX", min_value=0.1, max_value=2.0, value=1.0, step=0.1)
        scale_y = st.slider("スケールY", min_value=0.1, max_value=2.0, value=1.0, step=0.1)
        amount = st.slider("量", min_value=0.1, max_value=2.0, value=1.0, step=0.1)

        # 歪みを適用
        distorted_image = apply_distortion(im_cv, scale_x, scale_y, amount)

        # 歪んだ画像をPIL形式に変換
        distorted_image = Image.fromarray(distorted_image)

        # 元の画像と歪んだ画像を表示
        st.image([image, distorted_image], caption=['元の画像', '歪んだ画像'], width=300)

