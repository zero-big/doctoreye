import streamlit as st
# from streamlit.cli import main
from streamlit import session_state
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import datetime
import os
import re
import base64
def label_change(name_tag):
    if name_tag == 'age_related_macular_degeneration':
        name_tag = '황반변성'
        return name_tag
    if name_tag == 'diabetic':
        name_tag = '당뇨망막병증'
        return name_tag
    if name_tag == 'glaucoma':
        name_tag = '녹내장'
        return name_tag
    if name_tag == 'normal':
        name_tag = '정상'
        return name_tag

# 모델 로드
model = load_model("total_dataset_weight_2.h5")

def classify_image(image, load_open= None):
    # 이미지 전처리
    image = Image.open(image)
    image = image.resize((299, 299))
    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    image = image / 255.0
    # 예측
    class_names = ['age_related_macular_degeneration', 'diabetic', 'glaucoma', 'normal']
    prediction = model.predict(image, verbose=0)
    highest_value = max(prediction[0])
    predicted_class_index = np.argmax(prediction)
    predicted_class_name = class_names[predicted_class_index]
    # yhat = model.predict(image)
    # label = decode_predictions(yhat)
    # label = label[0][0]
    return predicted_class_name, highest_value

def save_uploaded_files(uploaded_files):
    folder_name = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    os.makedirs('data/' + folder_name, exist_ok=True)
    print(uploaded_files)
    # print(folder_path)
    if len(uploaded_files) == 1:
        for uploaded_file in uploaded_files:
            with open(os.path.join('data/' + folder_name, uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
    if len(uploaded_files) > 1:
        for uploaded_file in uploaded_files:
            with open(os.path.join('data/'+folder_name, uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
def createfolder(folder_path):
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    except OSError:
        print("Error: Failed to create the directory.")

def main():
    createfolder('./data')
    if "logged_in" not in session_state:
        session_state["logged_in"] = False
    if session_state["logged_in"]:
        st.sidebar.image("logo_3.jpeg", use_column_width=True)
        st.sidebar.markdown('''
        ### 로그아웃
        ''')
        if st.sidebar.button('로그아웃'):
            session_state["logged_in"] = False
            st.rerun()

        if st.button('처음으로'):  # clear 버튼 추가
            session_state["logged_in"] = True  # 로그인 상태를 False로 설정하여 첫 페이지로 이동
            st.rerun()

        folder_path = 'data'  # 폴더 경로
        subfolders = [f.name for f in os.scandir(folder_path) if f.is_dir()]
        sorted_options = sorted(subfolders, reverse=True)
        selected_option = None
        # 셀렉트박스 추가
        selected_option = st.sidebar.selectbox('지난 데이터', sorted_options,index=None,placeholder="이전 데이터")
        print('선택한 데이터', selected_option)
        uploaded_files = None
        with st.form("my-form", clear_on_submit=True):
            uploaded_files = st.file_uploader("안저 사진 올리기", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
            submitted = st.form_submit_button("판독 시작")
        # print('vadadsfvavav', uploaded_files)

            # pass
        if selected_option is not None:
            # 로그인 후 보여질 페이지
            image_folder_path = os.path.join(folder_path, selected_option)
            print('이미지주소', image_folder_path)
            image_files = [f for f in os.listdir(image_folder_path) if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.jpeg')]
            print('불렀다', image_files, type(image_files))
            if len(image_files) == 2:
                title_name = selected_option
                time_str = title_name[-6:]
                title_name = title_name[:-7]
                formatted_time = f"{time_str[:2]}:{time_str[2:4]}:{time_str[4:]}"
                print('etetet', title_name)
                st.header(f"{title_name}-{formatted_time} 촬영 데이터")
                col1, col2 = st.columns(2)
                with col1:
                    image_path =image_folder_path+'/'+image_files[0]
                    st.image(image_path)
                    print('불러낸 이미지', image_files[0])
                    label2 = classify_image(image_path)
                    st.write('판독 결과: %s (%.2f%%)' % (label_change(label2[0]), label2[1] * 100))
                with col2:
                    image_path = image_folder_path + '/' + image_files[1]
                    st.image(image_path)
                    print('불러낸 이미지', image_files[1])
                    label2 = classify_image(image_path)
                    st.write('판독 결과: %s (%.2f%%)' % (label_change(label2[0]), label2[1] * 100))
            if len(image_files) < 2 and len(image_files) > 0:
                image_path = image_folder_path + '/' + image_files[0]
                st.image(image_path, use_column_width=True)
                print('불러낸 이미지', image_files[0])
                label2 = classify_image(image_path)
                st.write('분류 결과 : %s (%.2f%%) ' % (label_change(label2[0]), label2[1] * 100))
            # if len(uploaded_files) == 0:
                # st.warning("이미지를 업로드해주세99요.")
            # selected_option = None
        if uploaded_files is not None:
            # st.warning("이미지를 업로드해주세요.")
            print(uploaded_files)
            print('fadsfdasfdasfasdf', len(uploaded_files))
            if len(uploaded_files) > 2:
                st.error("최대 2개의 이미지만 업로드할 수 있습니다.")
            elif len(uploaded_files) == 1:
                save_uploaded_files(uploaded_files)
                st.image(uploaded_files, use_column_width=True)
                label = classify_image(uploaded_files[0])
                st.write('판독 결과: %s (%.2f%%)' % (label_change(label[0]), label[1] * 100))
                uploaded_files.clear()
            elif len(uploaded_files) == 2:
                save_uploaded_files(uploaded_files)
                col1, col2 = st.columns(2)
                # for uploaded_file in uploaded_files:
                with col1:
                    st.image(uploaded_files[0])
                    label = classify_image(uploaded_files[0])
                    st.write('판독 결과: %s (%.2f%%)' % (label_change(label[0]), label[1] * 100))
                with col2:
                    st.image(uploaded_files[1])
                    label = classify_image(uploaded_files[1])
                    st.write('판독 결과: %s (%.2f%%)' % (label_change(label[0]), label[1] * 100))
                uploaded_files.clear()
                print('fsadklvnlkasdvnlas', uploaded_files)
            # else:
                # st.warning("이미지를 업로드해주세요.")
        print(',222222fdsfdsf', uploaded_files, selected_option)

    else:
        st.sidebar.image("logo_3.jpeg", use_column_width=True)
        st.sidebar.markdown('''
        ###        로그인
        ''')
        username = st.sidebar.text_input('아이디')
        password = st.sidebar.text_input('비밀번호', type='password')
        if st.sidebar.button('로그인') or (username and password):
            if username == 'admin' and password == 'admin':  # 예시용 로그인 정보
                session_state["logged_in"] = True
                st.rerun()
            else:
                st.sidebar.error('아이디 또는 비밀번호가 잘못되었습니다.')
        # 로그인 전 보여질 페이지
        # st.header("WISKY")
        st.image("logo.png", use_column_width=True)
        side_bg = 'bg.jpg'
        # sidebar_bg(side_bg)

        # set_background_image("bg.jpg")


if __name__ == "__main__":
    main()

