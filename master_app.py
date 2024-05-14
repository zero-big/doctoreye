import streamlit as st
from streamlit import session_state
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os
import cv2
from datetime import datetime,timedelta, timezone
from jinja2 import Template
import base64
import streamlit.components.v1 as components
from make_html import render_html_template, save_rendered_html
from lr_classification import lr_classifi

current_path = os.getcwd()
model = load_model(current_path + "/total_dataset_weight_2.h5")
model_papil = load_model(current_path + "/Papillede_V2.h5")
# def render_html_template(variables):
#     # Define your HTML template with placeholders for variables
#     html_template = """
#     <html lang="ko">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>판독 결과지</title>
#         <script src="https://cdn.tailwindcss.com"></script>
#         <style>
#             @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
#             body {
#                 font-family: 'Noto Sans KR', sans-serif;
#             }
#         </style>
#     </head>
#     <body>
#         <div class="container mx-auto px-4 py-8">
#             <div class="border-b-4 border-blue-800 pb-4">
#                 <div class="flex justify-between items-center">
#                  <img src=data:image/png;base64,{{ logo_img_path }} alt="Mediwhale logo placeholder" class="h-12 float-left mr-4">
#                 <button onclick="window.print()" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
#                     출력
#                 </button>
#             </div>
#             <br>
#             <div class="border-b-4 border-blue-800 pb-4">
#                 <span class="font-bold">DoctorEye</span>는 서울대학교 교수진이 직접 설계한 AI 알고리즘에 50만 장의 망막 사진을 학습시킨 인공지능 프로그램입니다.<br>
#                 안저 카메라에서 촬영한 안저 이미지를 DoctorEye를 통해 분석합니다.<br>
#                 한번에 3가지 질병을 진단 할 수 있어 편리하며 보다 빠르고 정확한 분석이 가능합니다.<br>
#                 질병을 초기에 진단하는 인공지능 헬스케어 솔루션입니다.
#             </div>
#                 <div class="mt-4">
#                     <div class="flex justify-between">
#                         <div>
#                             <span class="font-bold">이름:</span> {{ name }}
#                         </div>
#                         <div>
#                             <span class="font-bold">나이:</span> {{ age }}
#                         </div>
#                         <div>
#                             <span class="font-bold">성별:</span> {{ sex }}
#                         </div>
#                         <div>
#                             <span class="font-bold">일자:</span> {{ date }}
#                         </div>
#                         <div>
#                             <span class="font-bold">시간:</span> {{ time }}
#                         </div>
#                     </div>
#                 </div>
#             </div>
#             <div class="grid grid-cols-4 gap-2 mt-4">
#                 <div class="flex justify-center items-center">
#                 <div>
#                     <h2 class="text-center font-bold mb-2">좌안</h2>
#                     <img src=data:image/png;base64,{{ normal_path[0] }}  alt="Right eye fundus image placeholder" class="w-120 h-120 place-content-center" />
#                 </div>
#                 </div>
#                                 <div class="flex justify-center items-center">
#                 <div>
#                     <h2 class="text-center font-bold mb-2">우안</h2>
#                      <img src=data:image/png;base64,{{ normal_path[1] }} alt="Left eye fundus image placeholder" class="w-120 h-120 place-content-center" />
#                 </div>
#                 </div>
#                 <div>
#                     <h2 class="text-center font-bold mb-2">좌안</h2>
#                     <img src=data:image/png;base64,{{ left_img_path }} alt="Left eye fundus image placeholder" class="w-120 h-120 place-content-center"  />
#                 </div>
#                 <div>
#                     <h2 class="text-center font-bold mb-2">우안</h2>
#                      <img src=data:image/png;base64,{{ right_img_path }} alt="Right eye fundus image placeholder" class="w-120 h-120 place-content-center"  />
#                 </div>
#             </div>
#             <div class="border-b-4 border-blue-800 pb-4 grid grid-cols-2 gap-4 mt-4">
#                 <h2 class="text-center font-bold mb-2" style="font-size: 22px;">정상 안저이미지</h2>
#                 <h2 class="text-center font-bold mb-2" style="font-size: 22px;">환자 안저이미지</h2>
#             </div>
#
#             <div class="mt-12">
#                 <table class="w-full text-center">
#                     <thead>
#                         <tr>
#                             <th class="bg-blue-300 text-black p-2">안저 방향</th>
#                             <th class="bg-blue-400 text-black p-2" colspan="4">판독결과</th>
#                         </tr>
#                     </thead>
#                     <tbody>
#                         <tr>
#                             <td class="bg-blue-400 border-blue-400 text-black p-2" rowspan="2">좌안</td>
#                             <td class="bg-gray-300 border-blue-200 text-black p-2">당뇨망막병증</td>
#                             <td class="bg-gray-300 border-blue-200 text-black p-2">황반변성</td>
#                             <td class="bg-gray-300 border-blue-200 text-black p-2">녹내장</td>
#                             <td class="bg-gray-300 border-blue-200 text-black p-2">유두부종</td>
#                         </tr>
#                         <tr>
#                             <td class="border border-blue-200 text-black p-2">{{ left_data_value[0] }}</td>
#                             <td class="border border-blue-200 text-black p-2">{{ left_data_value[1] }}</td>
#                             <td class="border border-blue-200 text-black p-2">{{ left_data_value[2] }}</td>
#                             <td class="border border-blue-200 text-black p-2">{{ Papilledema[0] }}</td>
#                         </tr>
#                         <tr>
#                             <td class="bg-blue-200 border-blue-400 text-black p-2" rowspan="2">우안</td>
#                             <td class="bg-gray-300 border-blue-200 text-black p-2">당뇨망막병증</td>
#                             <td class="bg-gray-300 border-blue-200 text-black p-2">황반변성</td>
#                             <td class="bg-gray-300 border-blue-200 text-black p-2">녹내장</td>
#                             <td class="bg-gray-300 border-blue-200 text-black p-2">유두부종</td>
#                         </tr>
#                         <tr>
#                             <td class="border border-blue-200 text-black p-2">{{ right_data_value[0] }}</td>
#                             <td class="border border-blue-200 text-black p-2">{{ right_data_value[1] }}</td>
#                             <td class="border border-blue-200 text-black p-2">{{ right_data_value[2] }}</td>
#                             <td class="border border-blue-200 text-black p-2">{{ Papilledema[1] }}</td>
#                         </tr>
#
#                     </tbody>
#                 </table>
#             </div>
#             <div style='page-break-before:always'></div>
#             <div style="margin-top: 20px; margin-bottom: 20px;">
#                 <hr style="border: 5px solid #cee6ec;">
#             </div>
#             <table style="width: 100%; margin-left: auto; margin-right: auto;">
#                 <tr>
#                     <div class="border-b-4 border-blue-800 pb-4">
#                     <td colspan="2" style="text-align: center;"><br>
#                             <p class="text-lg" style="font-size: 27px;">판독소견</p>
#                         </div>
#                     </td>
#                 </tr>
#                 <tr>
#                     <td style="text-align: center; font-size: 20px"><div class="mt-8"><p class="text-md">
#                         DoctorEye 인공지능을 이용한 판독 결과,<br>
#                         귀하의 좌안 안저사진은 <span style="color:blue" class="font-bold">{{left_label}}</span> 로 판단 됩니다.<br>
#                         귀하의 우안 안저사진은 <span style="color:blue" class="font-bold">{{right_label}}</span> 로 판단 됩니다.
#                     </div></td>
#                     </tr>
#                 <tr>
#                     <td colspan="4" style="text-align: center; font-size: 20px"><div class="mt-12"><p class="text-md">
#                         조속한 시일 내에 정확한 진단과 추가적인 검사 및 꾸준한 치료를 위해 가까운 안과에 방문하셔서 안과 전문의에게 검진 받으시기를 권고 드립니다.<br>
#                         감사합니다.
#                     </div></td>
#                 </tr>
#             </table>
#             <table style="width: 100%; margin-left: auto; margin-right: auto;">
#                 <tr>
#                 <div class="border-b-4 border-blue-800 pb-4">
#                     <td colspan="2" style="text-align: center;">
#                         <div class="mt-4">
#                             <p class="text-lg" style="font-size: 27px;">권고사항</p>
#                         </div>
#                     </td>
#                 </tr>
#                 <tr>
#                     <td colspan="4" style="text-align: left; font-size: 20px"><div class="mt-12"><p class="text-md">
#                     본 진단은 50만장의 안저 사진을 학습 한 AI알고리즘이 분석한 결과입니다.
#                     본 결과는 단지 안저 이미지를 AI알고리즘 기반으로 한 의학적인 정보를 바탕으로
#                     환자의 상태를 파악하는데 도움을 줄 수 있는 참고용으로만 사용하시길 바랍니다.
#                     </p></div></td>
#                 </tr>
#             </table>
#             <div style="margin-top: 20px; margin-bottom: 20px;">
#                 <hr style="border: 5px solid #cee6ec;">
#             </div>
#
#         </div>
#     </body>
#     </html>
#     """
#     # Create a Jinja2 template object
#     template = Template(html_template)
#     # Render the template with variables
#     rendered_html = template.render(variables)
#     return rendered_html
#
# def save_rendered_html(html_content, filename):
#     with open(filename, 'w', encoding='utf-8') as file:
#         file.write(html_content)

# def lr_classifi(image_path):
#     image = cv2.imread(image_path)
#     # Get the dimensions of the original image
#     height, width, _ = image.shape
#     # Convert the image to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     # Apply Gaussian blur to reduce noise
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#     # Perform edge detection using Canny
#     edges = cv2.Canny(blurred, 50, 150)
#     # Find contours in the edge-detected image
#     contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     # Initialize variables to store the brightest point and its brightness
#     brightest_point = None
#     max_brightness = 0
#     # Loop over the contours
#     for contour in contours:
#         # Approximate the contour to reduce the number of points
#         approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
#         # Check if the contour is approximately circular
#         if len(approx) >= 8:
#             # Compute the bounding box of the contour
#             (x, y, w, h) = cv2.boundingRect(contour)
#             # Crop the circular region
#             mask = np.zeros_like(gray)
#             cv2.drawContours(mask, [contour], 0, 255, -1)
#             masked_gray = np.where(mask == 255, gray, 0)
#             # Find the brightest point within the circular region
#             (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(masked_gray)
#             # Update the brightest point and its brightness if necessary
#             if maxVal > max_brightness:
#                 brightest_point = maxLoc
#                 max_brightness = maxVal
# # If no circular contours were found, skip further processing
#     if brightest_point is None:
#         position = "불명"
#     else:
#         # Draw a circle around the brightest point
#         # cv2.circle(image, brightest_point, 5, (255, 0, 0), 2)
#         # Calculate the center of the original image
#         center_x = width // 2
#         # Determine if the blue dot is to the left or right of the center
#         if brightest_point[0] < center_x:
#             position = "좌안"
#         elif brightest_point[0] > center_x:
#             position = "우안"
#         else:
#             position = "불명"
#
#     return position

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
        return data_value
    if name_tag == '황반변성':
        data_value = ['정상', '비정상', '정상']
        return data_value
    if name_tag == '녹내장':
        data_value = ['정상', '정상', '비정상']
        return data_value
    else:
        data_value = ['정상', '정상', '정상']
        return data_value

def convert_into_pixel(img):
  img = img.resize((299,299))
  img_pixel = np.array(img)
  img_pixel = img_pixel / 255
  return img_pixel

def classify_image(image, load_open= None):
    # 이미지 전처리
    image = Image.open(image)
    image = image.resize((299, 299))
    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    image = image / 255.0
    # 예측

    pred_papilledema = model_papil.predict(image, verbose=0)
    pred_papilledema_class = np.argmax(pred_papilledema)
    if (pred_papilledema_class == 0):
        pred_papill = "정상"
    if (pred_papilledema_class == 1):
        pred_papill = "비정상"
    if (pred_papilledema_class == 2):
        pred_papill = "정상"

    class_names = ['age_related_macular_degeneration', 'diabetic', 'glaucoma', 'normal']
    prediction = model.predict(image, verbose=0)
    highest_value = max(prediction[0])
    predicted_class_index = np.argmax(prediction)
    predicted_class_name = class_names[predicted_class_index]
    return predicted_class_name, highest_value, pred_papill

def save_uploaded_files(uploaded_files):
    folder_name = (datetime.now(timezone.utc)+timedelta(hours=9)).strftime('%Y%m%d_%H%M%S')
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

def past_data(selected_option):
    current_path = os.getcwd()
    image_folder_path = 'data/' + selected_option
    if selected_option != '':
        title_name = selected_option
        time_str = title_name[-6:]
        title_name = title_name[:-7]
        formatted_time = f"{time_str[:2]}:{time_str[2:4]}:{time_str[4:]}"
        st.header(f"{title_name}-{formatted_time} 촬영 데이터")
        image_files = [f for f in os.listdir(image_folder_path) if
                       f.endswith('.png') or f.endswith('.jpg') or f.endswith('.jpeg')]
        if len(image_files) == 2:
            left_count = 0
            right_count = 0
            for image_file in image_files:
                lr_data = lr_classifi(current_path + str('/data/' + selected_option + '/' + image_file))
                if (lr_data == '좌안' or lr_data == '불명') and left_count == 0:
                    left_count += 1
                    left_img = image_file
                elif (lr_data == '좌안' or lr_data == '불명') and right_count == 0 and left_count == 1:
                    right_img = image_file
                elif lr_data == '우안' and right_count == 0:
                    right_count += 1
                    right_img = image_file
                elif lr_data == '우안' and left_count == 0 and right_count == 1:
                    left_img = image_file
            col1, col2 = st.columns(2)
            with col1:
                image_path = image_folder_path + '/' + left_img
                st.image(image_path)
                label2 = classify_image(image_path)
                st.write('판독 결과: %s (%.2f%%)' % (label_change(label2[0]), label2[1] * 100))
            with col2:
                image_path = image_folder_path + '/' + right_img
                st.image(image_path)
                label2 = classify_image(image_path)
                st.write('판독 결과: %s (%.2f%%)' % (label_change(label2[0]), label2[1] * 100))
        if len(image_files) < 2 and len(image_files) > 0:
            image_path = image_folder_path + '/' + image_files[0]
            st.image(image_path, use_column_width=True)
            label2 = classify_image(image_path)
            st.write('판독 결과 : %s (%.2f%%) ' % (label_change(label2[0]), label2[1] * 100))
        with open(current_path+'/' +image_folder_path+'/'+selected_option+'.html', 'r', encoding='utf8') as f:
            html_string = f.read()
    # Streamlit 앱에 HTML 렌더링
        st.components.v1.html(html_string, height=1200, scrolling=True)

def load_img_base(url):
    current_path = os.getcwd()
    with open(current_path + url, "rb") as img_file:
        bytes = img_file.read()
    img_base64 = base64.b64encode(bytes).decode()
    return img_base64
def uploaded_file_detect(uploaded_files, save_location):
    col1, col2 = st.columns(2)
    current_path = os.getcwd()
    left_count = 0
    right_count = 0
    for uploaded_file in uploaded_files:
        lr_data = lr_classifi(current_path+str('/data/' + save_location + '/' + uploaded_file.name))
        label = classify_image(uploaded_file)
        if (lr_data == '좌안' or lr_data == '불명') and left_count == 0:
            left_count += 1
            left_img_base64 = load_img_base(str('/data/' + save_location + '/' + uploaded_file.name))
            # with open(current_path+str('/data/' + save_location + '/' + uploaded_file.name), "rb") as img_file:
            #     img_bytes = img_file.read()
            # left_img_base64 = base64.b64encode(img_bytes).decode()
            left_data = ['./data/' + save_location + '/' + uploaded_file.name,
                         label_change(label[0]),
                         label[1] * 100,
                         data_list(label_change(label[0])),
                         uploaded_file.name,
                         label[2]]
        elif (lr_data == '좌안' or lr_data == '불명') and right_count == 0:
            right_img_base64 = load_img_base(str('/data/' + save_location + '/' + uploaded_file.name))
            # with open(current_path+str('/data/' + save_location + '/' + uploaded_file.name), "rb") as img_file:
            #     img_bytes = img_file.read()
            # right_img_base64 = base64.b64encode(img_bytes).decode()
            right_data = ['./data/' + save_location + '/' + uploaded_file.name,
                          label_change(label[0]),
                          label[1] * 100,
                          data_list(label_change(label[0])),
                          uploaded_file.name,
                          label[2]]
        elif lr_data == '우안' and right_count ==0:
            right_count += 1
            right_img_base64 =load_img_base(str('/data/' + save_location + '/' + uploaded_file.name))
            # with open(current_path+str('/data/' + save_location + '/' + uploaded_file.name), "rb") as img_file:
            #     img_bytes = img_file.read()
            # right_img_base64 = base64.b64encode(img_bytes).decode()
            right_data = ['./data/' + save_location + '/' + uploaded_file.name,
                          label_change(label[0]),
                          label[1] * 100,
                          data_list(label_change(label[0])),
                          uploaded_file.name,
                          label[2]]

        elif lr_data == '우안' and left_count == 0:
            left_img_base64 = load_img_base(str('/data/' + save_location + '/' + uploaded_file.name))
            # with open(current_path+str('/data/' + save_location + '/' + uploaded_file.name), "rb") as img_file:
            #     img_bytes = img_file.read()
            # left_img_base64 = base64.b64encode(img_bytes).decode()
            left_data = ['./data/' + save_location + '/' + uploaded_file.name,
                         label_change(label[0]),
                         label[1] * 100,
                         data_list(label_change(label[0])),
                         uploaded_file.name,
                         label[2]]
    left_side, right_side = save_location.split('_')
    date_value = left_side[0:4] + '년' + left_side[4:6] + '월' + left_side[6:8] + '일'
    time_value = right_side[0:2] + '시' + right_side[2:4] + '분' + right_side[4:6] + '초'
    logo_path = load_img_base("/name_logo.jpg")
    normal_left = load_img_base("/normal_left.jpg")
    normal_right= load_img_base("/normal_right.jpg")
    variables = {'name': '홍길동',
                 'age': str(72)+"세",
                 'date': date_value,
                 'time': time_value,
                 'sex': "남",
                 'left_img_path': left_img_base64,
                 'left_label':left_data[1],
                 'left_data_value': left_data[3],
                 'right_img_path': right_img_base64,
                 'right_label': right_data[1],
                 'right_data_value': right_data[3],
                 'logo_img_path': logo_path,
                 'normal_path': [normal_left, normal_right],
                 'Papilledema' : [left_data[5], right_data[5]]
                 # 'normal_path': normal_right,
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

    st.components.v1.html(html_content, height=1200, scrolling=True)

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
        st.sidebar.markdown('''
                    ### 업무선택
                    ''')
        selection = st.sidebar.radio("업무선택",["메인화면","실시간 판독", "차트 조회"], label_visibility="collapsed")
        if selection == '메인화면':
            session_state["rerun"] = True
            # st.image("name_logo.jpg", use_column_width=True)
            st.header("Doctor Eye", divider='rainbow')
            col1, col2 = st.columns([1,3])
            with col1:
                st.image("logo_4.png", use_column_width=True)
            with col2:
                st.markdown("## Doctor Eye 메뉴 설명")
                st.markdown("1. **메인화면** : 로그인 화면으로 돌아가기")
                st.markdown("2. **실시간 판독** : 촬영한 사진을 업로드 하여 판독")
                st.markdown("3. **차트 조회** : 이전에 촬영한 데이터 확인")

            side_bg = 'bg.jpg'
        if selection == '실시간 판독':
            # if session_state['rerun']:
            #     session_state['rerun'] = False
                # st.rerun()
            with st.form("my-form", clear_on_submit=True):
                uploaded_files = st.file_uploader("안저 사진 올리기",accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
                submitted = st.form_submit_button("판독 시작")
            if len(uploaded_files) >2:
                st.warning('파일 업로드는 최대 2개까지 가능합니다.')
            if len(uploaded_files) != 0 and len(uploaded_files)<=2:
                save_location = save_uploaded_files(uploaded_files)
                uploaded_file_detect(uploaded_files, save_location)
        if selection == '차트 조회':
            session_state["rerun"] = True
            if st.button('처음으로'):
                session_state["logged_in"] = True
                st.rerun()
            folder_path = './data'  # 폴더 경로
            subfolders = [f.name for f in os.scandir(folder_path) if f.is_dir()]
            sorted_options = ['']+sorted(subfolders, reverse=True)
            # 셀렉트박스 추가
            selected_option = st.selectbox('지난 데이터', sorted_options, index=0)
            past_data(selected_option)

    else:
        st.sidebar.image("logo_3.jpeg", use_column_width=True)
        st.sidebar.markdown('''
        ###        로그인
        ''')
        username = st.sidebar.text_input('아이디')
        password = st.sidebar.text_input('비밀번호', type='password')
        # st.header("Doctor EYE")
        st.image("name_logo.jpg", use_column_width=True)
        st.header("", divider='rainbow')
        st.markdown("<span style='font-size: 40px;'>**DoctorEye**</span>는 서울대학교 교수진이 직접 설계한 AI 알고리즘에 50만 장의 망막 사진을 학습시킨 인공지능 프로그램입니다. \n\n 안저 카메라에서 촬영한 안저 이미지를 DoctorEye를 통해 분석합니다. \n\n한번에 3가지 질병을 진단 할 수 있어 편리하며 보다 빠르고 정확한 분석이 가능합니다.\n\n 질병을 초기에 진단하는 인공지능 헬스케어 솔루션입니다.", unsafe_allow_html=True)
        side_bg = 'bg.jpg'
        if st.sidebar.button('로그인') or (username and password):
            if username == 'admin' and password == 'admin':  # 예시용 로그인 정보
                session_state["logged_in"] = True
                st.rerun()
            else:
                st.sidebar.error('아이디 또는 비밀번호가 잘못되었습니다.')

if __name__ == "__main__":
    main()
