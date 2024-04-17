
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
                 <img src=data:image/png;base64,{{ logo_img_path }} alt="Mediwhale logo placeholder" class="h-12 float-left mr-4"> 
                <button onclick="window.print()" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                    출력
                </button>
            </div>
            <br>
            <div class="border-b-4 border-blue-800 pb-4">
                <span class="font-bold">DoctorEye</span>는 서울대학교 교수진이 직접 설계한 AI 알고리즘에 50만 장의 망막 사진을 학습시킨 인공지능 프로그램입니다.<br>
                안저 카메라에서 촬영한 안저 이미지를 DoctorEye를 통해 분석합니다.<br>
                한번에 3가지 질병을 진단 할 수 있어 편리하며 보다 빠르고 정확한 분석이 가능합니다.<br>
                질병을 초기에 진단하는 인공지능 헬스케어 솔루션입니다.
            </div>
                <div class="mt-4">
                    <div class="flex justify-between">
                        <div>
                            <span class="font-bold">이름:</span> {{ name }}
                        </div>
                        <div>
                            <span class="font-bold">나이:</span> {{ age }}
                        </div>
                        <div>
                            <span class="font-bold">성별:</span> {{ sex }}
                        </div>
                        <div>
                            <span class="font-bold">일자:</span> {{ date }}
                        </div>
                        <div>
                            <span class="font-bold">시간:</span> {{ time }}
                        </div>
                    </div>
                </div>
            </div>
            <div class="grid grid-cols-4 gap-2 mt-4">
                <div class="flex justify-center items-center">
                <div>
                    <h2 class="text-center font-bold mb-2">좌안</h2>
                    <img src=data:image/png;base64,{{ normal_path[0] }}  alt="Right eye fundus image placeholder" class="w-120 h-120 place-content-center" />
                </div>
                </div>
                                <div class="flex justify-center items-center">
                <div>
                    <h2 class="text-center font-bold mb-2">우안</h2>
                     <img src=data:image/png;base64,{{ normal_path[1] }} alt="Left eye fundus image placeholder" class="w-120 h-120 place-content-center" />
                </div>
                </div>
                <div>
                    <h2 class="text-center font-bold mb-2">좌안</h2>
                    <img src=data:image/png;base64,{{ left_img_path }} alt="Left eye fundus image placeholder" class="w-120 h-120 place-content-center"  />
                </div>
                <div>
                    <h2 class="text-center font-bold mb-2">우안</h2>
                     <img src=data:image/png;base64,{{ right_img_path }} alt="Right eye fundus image placeholder" class="w-120 h-120 place-content-center"  />
                </div>
            </div>
            <div class="border-b-4 border-blue-800 pb-4 grid grid-cols-2 gap-4 mt-4">
                <h2 class="text-center font-bold mb-2" style="font-size: 22px;">정상 안저이미지</h2>
                <h2 class="text-center font-bold mb-2" style="font-size: 22px;">환자 안저이미지</h2>
            </div>

            <div class="mt-12">
                <table class="w-full text-center">
                    <thead>
                        <tr>
                            <th class="bg-blue-300 text-black p-2">안저 방향</th>
                            <th class="bg-blue-400 text-black p-2" colspan="4">판독결과</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="bg-blue-400 border-blue-400 text-black p-2" rowspan="2">좌안</td>
                            <td class="bg-gray-300 border-blue-200 text-black p-2">당뇨망막병증</td>
                            <td class="bg-gray-300 border-blue-200 text-black p-2">황반변성</td>
                            <td class="bg-gray-300 border-blue-200 text-black p-2">녹내장</td>
                            <td class="bg-gray-300 border-blue-200 text-black p-2">유두부종</td>
                        </tr>
                        <tr>
                            <td class="border border-blue-200 text-black p-2">{{ left_data_value[0] }}</td>
                            <td class="border border-blue-200 text-black p-2">{{ left_data_value[1] }}</td>
                            <td class="border border-blue-200 text-black p-2">{{ left_data_value[2] }}</td>
                            <td class="border border-blue-200 text-black p-2">{{ Papilledema[0] }}</td>
                        </tr>
                        <tr>
                            <td class="bg-blue-200 border-blue-400 text-black p-2" rowspan="2">우안</td>
                            <td class="bg-gray-300 border-blue-200 text-black p-2">당뇨망막병증</td>
                            <td class="bg-gray-300 border-blue-200 text-black p-2">황반변성</td>
                            <td class="bg-gray-300 border-blue-200 text-black p-2">녹내장</td>
                            <td class="bg-gray-300 border-blue-200 text-black p-2">유두부종</td>
                        </tr>
                        <tr>
                            <td class="border border-blue-200 text-black p-2">{{ right_data_value[0] }}</td>
                            <td class="border border-blue-200 text-black p-2">{{ right_data_value[1] }}</td>
                            <td class="border border-blue-200 text-black p-2">{{ right_data_value[2] }}</td>
                            <td class="border border-blue-200 text-black p-2">{{ Papilledema[1] }}</td>
                        </tr>

                    </tbody>
                </table>
            </div>
            <div style='page-break-before:always'></div>
            <div style="margin-top: 20px; margin-bottom: 20px;">
                <hr style="border: 5px solid #cee6ec;">
            </div>
            <table style="width: 100%; margin-left: auto; margin-right: auto;">
                <tr>
                    <div class="border-b-4 border-blue-800 pb-4">
                    <td colspan="2" style="text-align: center;"><br>
                            <p class="text-lg" style="font-size: 27px;">판독소견</p>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="text-align: center; font-size: 20px"><div class="mt-8"><p class="text-md">
                        DoctorEye 인공지능을 이용한 판독 결과,<br>
                        귀하의 좌안 안저사진은 <span style="color:blue" class="font-bold">{{left_label}}</span> 로 판단 됩니다.<br>
                        귀하의 우안 안저사진은 <span style="color:blue" class="font-bold">{{right_label}}</span> 로 판단 됩니다.
                    </div></td>
                    </tr>
                <tr>
                    <td colspan="4" style="text-align: center; font-size: 20px"><div class="mt-12"><p class="text-md">
                        조속한 시일 내에 정확한 진단과 추가적인 검사 및 꾸준한 치료를 위해 가까운 안과에 방문하셔서 안과 전문의에게 검진 받으시기를 권고 드립니다.<br>
                        감사합니다.
                    </div></td>
                </tr>
            </table>
            <table style="width: 100%; margin-left: auto; margin-right: auto;">
                <tr>
                <div class="border-b-4 border-blue-800 pb-4">
                    <td colspan="2" style="text-align: center;">
                        <div class="mt-4">
                            <p class="text-lg" style="font-size: 27px;">권고사항</p>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td colspan="4" style="text-align: left; font-size: 20px"><div class="mt-12"><p class="text-md">
                    본 진단은 50만장의 안저 사진을 학습 한 AI알고리즘이 분석한 결과입니다.
                    본 결과는 단지 안저 이미지를 AI알고리즘 기반으로 한 의학적인 정보를 바탕으로
                    환자의 상태를 파악하는데 도움을 줄 수 있는 참고용으로만 사용하시길 바랍니다.
                    </p></div></td>
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

