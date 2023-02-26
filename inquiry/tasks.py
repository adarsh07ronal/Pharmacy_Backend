
from django.conf import settings
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
from django.core.mail import send_mail
# from pharmacy.celery import app

# @app.task
def send_email_when_notice_inquiry_created(pk):
    from inquiry.models import Inquiry
    inquiry_obj = Inquiry.objects.get(id = pk)
    from_email = settings.DEFAULT_EMAIL_FROM
    subject= 'じぶん薬局へのお問い合わせを受付けました'
    # html_message = render_to_string('inquiry/notify_user.html', {'inquiry_obj':inquiry_obj})

    send_mail(
        subject,
        "{} 様\n\nこの度はじぶん薬局にお問い合わせをいただきありがとうございます。\nお問い合わせ内容は、運営事務局にて確認後、2営業日以内にご回答いたします。\n\n今回お問い合わせ頂きました内容は以下になります。\nお問い合わせ内容\n{}\n\n2営業日を過ぎても回答がないなどの場合、お手数ですが以下の事務局まで、\nお問い合わせをよろしくお願いいたします。\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com".format(inquiry_obj.name,inquiry_obj.contents_of_inquiry),
        from_email,
        [inquiry_obj.email,'karre@eoraa.com'],
    )
    
    # msg = EmailMultiAlternatives(subject, html_message, from_email, [inquiry_obj.email])
    # msg.attach_alternative(html_message, "text/html")
    # msg.send()

def send_email_when_notice_inquiry_resolved(pk):
    from inquiry.models import InquiryMessage
    inquiry_message_obj = InquiryMessage.objects.get(id = pk)
    from_email = settings.DEFAULT_EMAIL_FROM
    inquiry_obj=inquiry_message_obj.inquiry
    subject= '{} 様 お問い合わせ内容の回答'.format(inquiry_obj.name)
    # html_message = render_to_string('inquiry/resolve_user.html', {'inquiry_obj':inquiry_obj,'inquiry_message_obj':inquiry_message_obj})
    # msg = EmailMultiAlternatives(subject, html_message, from_email, [inquiry_obj.email])
    # msg.attach_alternative(html_message, "text/html")
    # msg.send()
    send_mail(
        subject,
        "{} 様\n\nこの度はじぶん薬局にお問い合わせをいただきありがとうございます。\nお問い合わせ頂きました内容の回答を送信させていただきます。\n\n今回お問い合わせ頂きました内容は以下になります。\nお問い合わせ内容\n{}\n\n回答\n{}\n\nこのメールに心当たりのない方は、お手数ですが本メールを破棄してください。\nまた、本メールに関するお問い合わせは運営事務局までお願いいたします。\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com".format(inquiry_obj.name,inquiry_obj.contents_of_inquiry,inquiry_message_obj.message),
        from_email,
        [inquiry_obj.email,'karre@eoraa.com'],
    )