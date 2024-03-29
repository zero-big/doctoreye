from jinja2 import Template

# Define your HTML template with placeholders for variables
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



# Define variables
# Save the rendered HTML to a file
def save_rendered_html(html_content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(html_content)


# Render the HTML template with variables
# rendered_html = render_html_template(variables)

# Save the rendered HTML to a file
# save_rendered_html(rendered_html)

# Render the HTML template with variables
# rendered_html = render_html_template(variables)

# Save the rendered HTML to a file










# Create a Jinja2 template object
# # template = Template(html_template)
# abced = '굿잡'
# age_value = 40
# Define variables


# Render the template with variables
# rendered_html = template.render(variables)

# Save the rendered HTML to a file
# with open('test.html', 'w', encoding='utf-8') as file:
#     file.write(rendered_html)
