import os
import base64
import uuid
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from django.conf import settings

def save_quill_images(html_content, title_slug):
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img')

    upload_dir = os.path.join(settings.MEDIA_ROOT, 'articles')
    os.makedirs(upload_dir, exist_ok=True)  # 🔥 디렉토리 없으면 생성

    for img in img_tags:
        src = img.get('src')
        if src.startswith('data:image'):
            format, imgstr = src.split(';base64,')
            ext = format.split('/')[-1]
            unique_name = f"{title_slug}-{uuid.uuid4().hex[:8]}.{ext}"
            file_data = ContentFile(base64.b64decode(imgstr), name=unique_name)

            # 실제 파일 저장
            path = os.path.join(upload_dir, unique_name)
            with open(path, 'wb') as f:
                f.write(file_data.read())

            # HTML 내 src 경로를 /media/articles/..로 변경
            img['src'] = f'{settings.MEDIA_HOST}/media/articles/{unique_name}'

    return str(soup)
