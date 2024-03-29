import streamlit as st
from streamlit import session_state
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os
import cv2
import webbrowser
import datetime
from jinja2 import Template

def render_html_template(variables):
    # Define your HTML template with placeholders for variables
    html_template = """
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>판독 결과지</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
            body {
                font-family: 'Noto Sans KR', sans-serif;
            }
        </style>
    </head>
    <body>
        <div class="container mx-auto px-4 py-8">
            <div class="border-b-4 border-blue-800 pb-4">
                <div class="flex justify-between items-center">
                 <img src="../../name_logo.jpg" alt="Mediwhale logo placeholder" class="h-12 float-left mr-4"> 
                <button onclick="window.print()" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                    프린터
                </button>
            </div>

                <div class="mt-4">
                    <div class="flex justify-between">
                        <div>
                            <span class="font-bold">환자 이름:</span> {{ name }}
                        </div>
                        <div>
                            <span class="font-bold">나이:</span> {{ age }}
                        </div>
                        <div>
                            <span class="font-bold">성별:</span> {{ sex }}
                        </div>
                        <div>
                            <span class="font-bold">검사일자:</span> {{ date }}
                        </div>
                        <div>
                            <span class="font-bold">시간:</span> {{ time }}
                        </div>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-2 gap-4 mt-4">
                <div>
                    <h2 class="text-center font-bold mb-2">좌안</h2>
                    <img src={{ left_img_path }} alt="Right eye fundus image placeholder" class="w-full" />
                </div>
                <div>
                    <h2 class="text-center font-bold mb-2">우안</h2>
                    <img src={{ right_img_path }} alt="Left eye fundus image placeholder" class="w-full" />
                </div>
            </div>
            <div class="mt-8">
                <table class="w-full text-center">
                    <thead>
                        <tr>
                            <th class="bg-blue-300 text-black p-2">안저 방향</th>
                            <th class="bg-blue-400 text-black p-2" colspan="4">판독결과</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="bg-blue-400 border border-blue-400 text-black p-2" rowspan="2">좌안</td>
                            <td class="bg-gray-300 border-blue-200 text-black p-2">당뇨망막병증</td>
                            <td class="bg-gray-300 border-blue-200 text-black p-2">황반변성</td>
                            <td class="bg-gray-300 border-blue-200 text-black p-2">녹내장</td>
                        </tr>
                        <tr>
                            <td class="border border-blue-200 text-black p-2">{{ left_data_value[0] }}</td>
                            <td class="border border-blue-200 text-black p-2">{{ left_data_value[1] }}</td>
                            <td class="border border-blue-200 text-black p-2">{{ left_data_value[2] }}</td>
                        </tr>
                        <tr>
                            <td class="bg-blue-200 border-blue-400 text-black p-2" rowspan="2">우안</td>
                            <td class="bg-gray-300 border-blue-200 text-black p-2">당뇨망막병증</td>
                            <td class="bg-gray-300 border-blue-200 text-black p-2">황반변성</td>
                            <td class="bg-gray-300 border-blue-200 text-black p-2">녹내장</td>
                        </tr>
                        <tr>
                            <td class="border border-blue-200 text-black p-2">{{ right_data_value[0] }}</td>
                            <td class="border border-blue-200 text-black p-2">{{ right_data_value[1] }}</td>
                            <td class="border border-blue-200 text-black p-2">{{ right_data_value[2] }}</td>
                        </tr>

                    </tbody>
                </table>
            </div>
            <div style="margin-top: 20px; margin-bottom: 20px;">
                <hr style="border: 5px solid #cee6ec;">
            </div>
            <table style="width: 100%; margin-left: auto; margin-right: auto;">
                <tr>
                    <td colspan="2" style="text-align: center;">
                        <div class="mt-4">
                            <p class="text-lg" style="font-size: 27px;">권고사항</p>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td colspan="4" style="text-align: left; font-size: 20px"><div class="mt-12"><p class="text-md">
                    본 진단은 안저 영상 검사 결과와 안저영상의학의 의사들이 분석한 결과입니다.                    여기서 언급된 결과들은 의사의 전문적인 의학적인 상태를 지칭한 것은 아니며
                    실제로 환자의 건강 상태를 진단하는데 사용될 수 없습니다.                    본 결과는 단지 안저 영상 검사 결과를 기반으로 한 의학적인 정보를 바탕으로
                    환자의 상태를 파악하는데 도움을 줄 수 있는 참고용으로만 사용하시길 바랍니다.
                    출처를 밝히지 않습니다.</p></div></td>
                </tr>
            </table>
            <div style="margin-top: 20px; margin-bottom: 20px;">
                <hr style="border: 5px solid #cee6ec;">
            </div>

        </div>
    </body>
    </html>
    """
    # Create a Jinja2 template object
    template = Template(html_template)
    # Render the template with variables
    rendered_html = template.render(variables)
    return rendered_html


def save_rendered_html(html_content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(html_content)

def lr_classifi(image_path):
    print(image_path)
    image = cv2.imread(image_path)
    # Get the dimensions of the original image
    height, width, _ = image.shape
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Perform edge detection using Canny
    edges = cv2.Canny(blurred, 50, 150)
    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Initialize variables to store the brightest point and its brightness
    brightest_point = None
    max_brightness = 0
    # Loop over the contours
    for contour in contours:
        # Approximate the contour to reduce the number of points
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        # Check if the contour is approximately circular
        if len(approx) >= 8:
            # Compute the bounding box of the contour
            (x, y, w, h) = cv2.boundingRect(contour)
            # Crop the circular region
            mask = np.zeros_like(gray)
            cv2.drawContours(mask, [contour], 0, 255, -1)
            masked_gray = np.where(mask == 255, gray, 0)
            # Find the brightest point within the circular region
            (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(masked_gray)
            # Update the brightest point and its brightness if necessary
            if maxVal > max_brightness:
                brightest_point = maxLoc
                max_brightness = maxVal
# If no circular contours were found, skip further processing
    if brightest_point is None:
        position = "불명"
    else:
        # Draw a circle around the brightest point
        cv2.circle(image, brightest_point, 5, (255, 0, 0), 2)
        # Calculate the center of the original image
        center_x = width // 2
        # Determine if the blue dot is to the left or right of the center
        if brightest_point[0] < center_x:
            position = "좌안"
        elif brightest_point[0] > center_x:
            position = "우안"
        else:
            position = "불명"


        # Display the result
        # cv2.imshow('Result', image)
        # print(f"The blue dot is to the {position} of the center of the original image.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return position
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
    current_path = os.getcwd()
    for uploaded_file in uploaded_files:
        lr_data = lr_classifi(current_path+str('./data/' + save_location + '/' + uploaded_file.name))
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
    current_path = os.getcwd()
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
