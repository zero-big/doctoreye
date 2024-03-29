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
import webbrowser
from lr_classification import lr_classifi
from make_html import save_rendered_html, render_html_template
import datetime


def open_html_file(url_path):
    current_path = os.getcwd()
    try:
        if os.path.exists(current_path+url_path):
            webbrowser.open(current_path+url_path)
        else:
            st.write('"결과지를 작성중입니다. 잠시만 기다려주세요.')
    except Exception as e:
        st.error(f"An error occurred: {e}")

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

def data_list(name_tag):
    if name_tag == '당뇨망막병증':
        data_value = ['비정상', '정상', '정상']
    if name_tag == '황반변성':
        data_value = ['정상', '비정상', '정상']
    if name_tag == '녹내장':
        data_value = ['정상', '정상', '비정상']
    else:
        data_value = ['정상', '정상', '정상']
    return data_value

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

    return predicted_class_name, highest_value

def save_uploaded_files(uploaded_files):
    folder_name = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    os.makedirs('data/' + folder_name, exist_ok=True)
    for uploaded_file in uploaded_files:
        with open(os.path.join('data/' + folder_name, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
    return folder_name

def createfolder(folder_path):
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    except OSError:
        print("Error: Failed to create the directory.")

def past_data(selected_option, folder_path):

    image_folder_path = './data/' + folder_path

    if st.button("결과지 출력") and folder_path != '':
        current_path = os.getcwd()
        open_past_html(current_path+'/' +image_folder_path+'/'+folder_path+'.html')

    if folder_path != '':
        image_files = [f for f in os.listdir(image_folder_path) if
                       f.endswith('.png') or f.endswith('.jpg') or f.endswith('.jpeg')]
        print('불렀다', image_files, type(image_files))
        if len(image_files) == 2:
            title_name = folder_path
            time_str = title_name[-6:]
            title_name = title_name[:-7]
            formatted_time = f"{time_str[:2]}:{time_str[2:4]}:{time_str[4:]}"
            print('etetet', title_name)
            st.header(f"{title_name}-{formatted_time} 촬영 데이터")
            col1, col2 = st.columns(2)
            with col1:
                image_path = image_folder_path + '/' + image_files[0]
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

def uploaded_file_detect(uploaded_files, save_location):
    col1, col2 = st.columns(2)
    print('iojboifgkbpogfkbpogfkbpofgkbpogfkbpogfkbpfgokbpgfob')


    for uploaded_file in uploaded_files:
        lr_data = lr_classifi(str('./data/' + save_location + '/' + uploaded_file.name))
        label = classify_image(uploaded_file)
        if lr_data == '좌안' or lr_data == '불명':
            left_data = ['./data/' + save_location + '/' + uploaded_file.name,
                         label_change(label[0]),
                         label[1] * 100,
                         data_list(label_change(label[0])),
                         uploaded_file.name]
        else:
            right_data = ['./data/' + save_location + '/' + uploaded_file.name,
                          label_change(label[0]),
                          label[1] * 100,
                          data_list(label_change(label[0])),
                          uploaded_file.name]

    left_side, right_side = save_location.split('_')
    date_value = left_side[0:4] + '년' + left_side[4:6] + '월' + left_side[6:8] + '일'
    time_value = right_side[0:2] + '시' + right_side[2:4] + '분' + right_side[4:6] + '초'

    variables = {'name': '홍길동',
                 'age': 0,
                 'date': date_value,
                 'time': time_value,
                 'sex': "man",
                 'left_img_path': left_data[4],
                 'left_data_value': left_data[3],
                 'right_img_path': right_data[4],
                 'right_data_value': right_data[3],
                 }
    html_content = render_html_template(variables)
    save_rendered_html(html_content, str('./data/' + save_location + '/' + f'{save_location}.html'))

    with col1:
        st.header('좌안')
        st.image(left_data[0])
        st.write('판독 결과: ', left_data[1], str(left_data[2])[0:5] + '%')
    with col2:
        st.header('우안')
        st.image(right_data[0])
        st.write('판독 결과: ', right_data[1], str(right_data[2])[0:5] + '%')
    open_html_file('/data/' + save_location + '/' + save_location + ".html")

def open_past_html(file_path):
    webbrowser.open(file_path, new=2)

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

        selection = st.sidebar.radio("업무 선택", ("메인화면","실시간 판독", "지난 데이터"))
        if selection == '메인화면':
            session_state["rerun"] = True
            st.header("Doctor EYE")
            st.image("logo.png", use_column_width=True)
            side_bg = 'bg.jpg'
        if selection == '실시간 판독':
            if session_state['rerun']:
                session_state['rerun'] = False
                st.rerun()
            if st.button('처음으로'):
                session_state["logged_in"] = True
                st.rerun()
            with st.form("my-form", clear_on_submit=True):
                uploaded_files = st.file_uploader("안저 사진 올리기", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
                submitted = st.form_submit_button("판독 시작")
            print('fsadfadsfdasfdasfsd', len(uploaded_files))
            if len(uploaded_files) != 0:
                save_location = save_uploaded_files(uploaded_files)
                uploaded_file_detect(uploaded_files, save_location)
        if selection == '지난 데이터':
            session_state["rerun"] = True
            if st.button('처음으로'):
                session_state["logged_in"] = True
                st.rerun()
            folder_path = './data'  # 폴더 경로
            subfolders = [f.name for f in os.scandir(folder_path) if f.is_dir()]
            print(subfolders)
            sorted_options = ['']+sorted(subfolders, reverse=True)
            # 셀렉트박스 추가
            selected_option = st.selectbox('지난 데이터', sorted_options, index=0)
            past_data(folder_path, selected_option)

    else:
        st.sidebar.image("logo_3.jpeg", use_column_width=True)
        st.sidebar.markdown('''
        ###        로그인
        ''')
        username = st.sidebar.text_input('아이디')
        password = st.sidebar.text_input('비밀번호', type='password')
        st.header("Doctor EYE")
        st.image("logo.png", use_column_width=True)
        side_bg = 'bg.jpg'
        if st.sidebar.button('로그인') or (username and password):
            if username == 'admin' and password == 'admin':  # 예시용 로그인 정보
                session_state["logged_in"] = True
                st.rerun()
            else:
                st.sidebar.error('아이디 또는 비밀번호가 잘못되었습니다.')
        # 로그인 전 보여질 페이지


                # sidebar_bg(side_bg)
                #
                # set_background_image("bg.jpg")


if __name__ == "__main__":

    main()
