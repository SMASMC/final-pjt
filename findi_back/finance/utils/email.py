# finance/utils/email.py

from django.core.mail import EmailMultiAlternatives

# 관리자 금리 수정 시 이메일 전송 로직
def send_interest_change_email(email, product_name):
    subject = f'[Findi] "{product_name}" 상품 금리가 변경되었습니다.'
    from_email = 'msoko89@gmail.com'
    to = [email]
    text_content = f'"{product_name}" 상품의 금리가 변경되었습니다. Findi에서 확인해 주세요.'
    html_content = f"""
        <html>
        <body>
            <h2 style="color:#8A69E1;">Findi 금리 변경 안내</h2>
            <p><strong>{product_name}</strong> 상품의 금리가 변경되었습니다.</p>
            <p>Findi에서 최신 금리를 확인해보세요!</p>
        </body>
        </html>
    """

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
