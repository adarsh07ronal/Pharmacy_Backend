from django.core.mail import send_mail
import datetime, pytz
from reservation.models import ForReservation
from pharmacy.settings.base import TIME_ZONE


def reservationsat7():
    try:
        today_date = datetime.datetime.today().replace(tzinfo=pytz.timezone(TIME_ZONE))
        reservations = ForReservation.objects.all()
        for reservation in reservations:            
            reservation_schedule_time=reservation.reservation_scheduled_time
            if reservation_schedule_time:
                # days_remaining=(reservation_schedule_time.replace(tzinfo=pytz.timezone(TIME_ZONE)) - today_date).days
                days_remaining=reservation_schedule_time.day - today_date.day
                if 0<=days_remaining<=1:
                    reservation_schedule_time =str(reservation_schedule_time)
                    l=reservation_schedule_time.split("-")
                    ll =l[2].split(" ")
                    reservation_schedule_time=l[0]+"年"+l[1]+"月"+ll[0]+"日 "+ll[1][0:5]
                    if reservation.is_accepted:
                        if 0<days_remaining<=1:
                            send_mail(
                                '登録した処方箋の受取日は明日{}までになります'.format(reservation_schedule_time),
                                "{} 様\n\nご登録いただいた処方箋予約の受取日が明日になっております。\n以下の日程となりますので、お忘れのないようにお受け取りください。\n{}\n\n申請いただいた日程での受取ができなくなってしまった場合には、\nお手数ですが処方箋受取日の修正申請ををお願いいたします。\n{}\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com".format(reservation.patient.name,reservation_schedule_time,"https://pharmacy-user.netlify.app/mypage/reserve/{}".format(reservation.id)),
                                'developers.geitpl@gmail.com',
                                [reservation.patient.email,'karre@eoraa.com'],
                            )
                    else:
                        if days_remaining==0:
                            # send_mail(
                            #     '登録した処方箋の有効日は本日までです'.format(reservation_schedule_time),
                            #     "{} 様\n\nご登録いただいた処方箋の有効日が本日までになっております。\n有効日をすぎると処方箋の再発行が必要となりますので、本日中に\n処方箋の受取予約、および受取をおこなってください。\n\n処方箋受取予約は以下のアドレスから行っていただけます。\n{}\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\n\nE-mail：info@orthros.com".format(reservation.patient.name,"https://pharmacy-user.netlify.app/mypage/reserve/{}".format(reservation.id)),
                            #     'developers.geitpl@gmail.com',
                            #     [reservation.patient.email,'karre@eoraa.com'],
                            # )
                            pass
                        else:
                            send_mail(
                                '登録した処方箋の有効日は本日までです{}までになります'.format(reservation_schedule_time),
                                "{} 様\n\nご登録いただいた処方箋の有効日が明日になっております。\n有効日をすぎると処方箋の再発行が必要となりますので、期日までに\n処方箋の受取予約、および受取をおこなってください。\n\n処方箋受取予約は以下のアドレスから行っていただけます。\n{}\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com".format(reservation.patient.name,"https://pharmacy-user.netlify.app/mypage/reserve/{}".format(reservation.id)),
                                'developers.geitpl@gmail.com',
                                [reservation.patient.email,'karre@eoraa.com'],
                            )
            
            guidance_schedule_time=reservation.guidance_scheduled_time
            if guidance_schedule_time:
                # days_remaining=(guidance_schedule_time.replace(tzinfo=pytz.timezone(TIME_ZONE)) -today_date).days
                days_remaining=guidance_schedule_time.day - today_date.day
                if reservation.is_remote_accepted and reservation.medication_guidence:
                    guidance_schedule_time =str(guidance_schedule_time)
                    l=guidance_schedule_time.split("-")
                    ll =l[2].split(" ")
                    guidance_schedule_time=l[0]+"年"+l[1]+"月"+ll[0]+"日 "+ll[1][0:5]
                    if 0<days_remaining<=1:
                        send_mail(
                                '遠隔服薬指導の実施日は明日{}です'.format(guidance_schedule_time),
                                "{} 様\n\nご予約いただいた遠隔服薬指導の実施日が明日になっております。\n以下の日時で実施されますので、お忘れのないようにお願いいたします。\n{}\n\n遠隔服薬指導日時になりましたら、以下のURLからサイトにアクセスいただき、\n遠隔服薬指導を実施してください。\n{}\n\nなお、遠隔服薬指導の実施日を変更されたい場合は、以下のURLからお願いいたします。\n{}\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com".format(reservation.patient.name,guidance_schedule_time,"https://pharmacy-user.netlify.app/mypage","https://pharmacy-user.netlify.app/mypage/reserve/{}".format(reservation.id)),
                                'developers.geitpl@gmail.com',
                                [reservation.patient.email,'karre@eoraa.com'],
                            )
        print("Reservation Cron Success!")
    except Exception as e:
        print("Reservation Cron Failure : " + str(e))

def reservationsat7am():
    try:
        today_date = datetime.datetime.today().replace(tzinfo=pytz.timezone(TIME_ZONE))
        reservations = ForReservation.objects.all()
        for reservation in reservations:
            reservation_schedule_time=reservation.reservation_scheduled_time
            if reservation_schedule_time:
                # days_remaining=(reservation_schedule_time.replace(tzinfo=pytz.timezone(TIME_ZONE)) - today_date).days
                days_remaining=reservation_schedule_time.day - today_date.day
                reservation_schedule_time =str(reservation_schedule_time)
                l=reservation_schedule_time.split("-")
                ll =l[2].split(" ")
                reservation_schedule_time=l[0]+"年"+l[1]+"月"+ll[0]+"日 "+ll[1][0:5]
                if days_remaining==0:
                    send_mail(
                        '登録した処方箋の有効日は本日までです'.format(reservation_schedule_time),
                        "{} 様\n\nご登録いただいた処方箋の有効日が明日になっております。\n有効日をすぎると処方箋の再発行が必要となりますので、期日までに\n処方箋の受取予約、および受取をおこなってください。\n\n処方箋受取予約は以下のアドレスから行っていただけます。\n{}\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com".format(reservation.patient.name,"https://pharmacy-user.netlify.app/mypage/reserve/{}".format(reservation.id)),
                        'developers.geitpl@gmail.com',
                        [reservation.patient.email,'karre@eoraa.com'],
                    )        
        print("Reservation Cron Success!")
    except Exception as e:
        print("Reservation Cron Failure : " + str(e))

def reservationsat12():
    try:
        today_date = datetime.datetime.today().replace(tzinfo=pytz.timezone(TIME_ZONE))
        reservations = ForReservation.objects.all()
        for reservation in reservations:
            guidance_schedule_time=reservation.guidance_scheduled_time
            if guidance_schedule_time:
                # days_remaining=(guidance_schedule_time.replace(tzinfo=pytz.timezone(TIME_ZONE)) - today_date).days
                days_remaining=guidance_schedule_time.day - today_date.day
                if reservation.is_remote_accepted and reservation.medication_guidence:
                    guidance_schedule_time =str(guidance_schedule_time)
                    l=guidance_schedule_time.split("-")
                    ll =l[2].split(" ")
                    guidance_schedule_time=l[0]+"年"+l[1]+"月"+ll[0]+"日 "+ll[1][0:5]
                    if 0<days_remaining<=1:
                        send_mail(
                                '遠隔服薬指導の実施日は明日{}です'.format(guidance_schedule_time),
                                "{} 様\n\n{}様との遠隔服薬指導実施日が明日になっております。\n以下の日時で実施されますので、お忘れのないようにお願いいたします。\n{}\n\n遠隔服薬指導日時になりましたら、以下のURLからサイトにアクセスいただき、\n遠隔服薬指導を実施してください。\n{}\n\nなお、遠隔服薬指導の実施日を変更されたい場合は、以下のURLからお願いいたします。\n{}\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com".format(reservation.pharmacy.representative,reservation.patient.name,guidance_schedule_time,"https://pharmacy-user.netlify.app/mypage","https://pharmacy-user.netlify.app/mypage/reserve/{}".format(reservation.id)),
                                'developers.geitpl@gmail.com',
                                [reservation.pharmacy.email,'karre@eoraa.com'],
                            )
        print("Reservation Cron Success!")
    except Exception as e:
        print("Reservation Cron Failure : " + str(e))
            
def testAPI():
    send_mail(
        'TEST CRON MAIL',
        "TEST CRON BODY",
        'developers.geitpl@gmail.com',
        ['karre@eoraa.com'],
    )
