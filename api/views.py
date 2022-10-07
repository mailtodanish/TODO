import random
import json

from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.utils import timezone
from projects.models import Activity, ProjectTask, TaskComment, Favoutite_item
from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (ActivitySerializer, TaskCommentSerializer,
                          TaskSerializer, FavouriteItemSerializer)


class ActivityDone(APIView):
    '''
    API for make activity done.
    There would be button on Activity to make it done.
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        record = get_object_or_404(Activity, pk=pk)
        Act = Activity.objects.get(pk=pk)
        Act.status = "Done"
        Act.save()
        return Response(Act.status)


class ScheduledActivityList(APIView):
    '''
    Get list of scheduled activity to create daily activities.
    Test Case - Done
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        records = Activity.objects.exclude(Type="General").filter(
            status='Open')
        rec = []
        for r in records:
            find_record = Activity.objects.filter(parentActivityId=r.pk,
                                                  status='Open',
                                                  Type="General")
            if find_record.count() == 0:
                rec.append(r)
        data = ActivitySerializer(rec, many=True).data
        return Response(data)


class ChildActivityList(APIView):
    '''
    Get list of child activity of scheduled activity
    Test Case -
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        records = Activity.objects.filter(parentActivityId=pk).order_by("-pk")
        data = ActivitySerializer(records, many=True).data
        return Response(data)


class RevisionItem(APIView):
    '''
    used: Load Revision Item button on Home Page to revise
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        records = TaskComment.objects.all().order_by('updated')[1]
        data = TaskCommentSerializer(records).data
        return Response(data)


class RevisionItemUpdate(APIView):
    '''
    used : NextRevisionItem button on home page
    It only updates updated column of model.
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        comment = TaskComment.objects.get(pk=pk)
        comment.updated = timezone.now()
        comment.save()
        return Response("Success")


class RevisionItemofTheDay(APIView):
    '''
    It has been used in schedules activity to mail open activities
    Test Case - Done
    Status - Completed
    '''
    permission_classes = [permissions.IsAuthenticated]

    def _send_email(self,from_email, to_email, subject, message, attachment_list):
        '''send email using SendGrid
        :param str from_email: Sender email address
        :param str to_email: Email to send message
        :param str subject: Email subject
        :param str message: Email body [HTML]
        :return bool: Return True if message sent
        '''
        import os
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail, To, Attachment, Personalization, Email
        from python_http_client.exceptions import HTTPError

        sender_email = settings.SENDGRID_SENDER_EMAIL

        email = Mail(
            from_email=from_email,
            # to_emails=To((to_email)),
            subject=subject,
            html_content=message)

        personalization = Personalization()
        personalization.add_to(Email(sender_email))
        # personalization.add_to(Email(to_email))
        # personalization.add_cc(Email(sender_email))
        email.add_personalization(personalization)

        for at in attachment_list:
            email.add_attachment(at)

        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)

        try:
            sg.send(email)
        except HTTPError as e:
            print(e.to_dict)
            return False

        return True

    def get(self, request):
        try:


            dt = timezone.now()
            queryset = Activity.objects.filter(
                scheduled__lte=dt,
                Type='General').exclude(status='Done').order_by('-scheduled')
            html_message = loader.render_to_string('api/mail_template.html',
                                                   {'Activities': queryset})
            sender_email = settings.SENDGRID_SENDER_EMAIL
            self._send_email(sender_email, 'mailtodanish@gmail.com', 'Task of the day', html_message, [])
            return Response("Success")
        except Exception as e:
            return Response({"detail": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


class CommentsofTheDay(APIView):
    '''
    It has been used in schedules activity to mail revision items
    Test Case - Done
    Status : Completed.
    '''
    permission_classes = [permissions.IsAuthenticated]

    def _send_email(self,from_email, to_email, subject, message, attachment_list):
        '''send email using SendGrid
        :param str from_email: Sender email address
        :param str to_email: Email to send message
        :param str subject: Email subject
        :param str message: Email body [HTML]
        :return bool: Return True if message sent
        '''
        import os
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail, To, Attachment, Personalization, Email
        from python_http_client.exceptions import HTTPError

        sender_email = settings.SENDGRID_SENDER_EMAIL

        email = Mail(
            from_email=from_email,
            # to_emails=To((to_email)),
            subject=subject,
            html_content=message)

        personalization = Personalization()
        personalization.add_to(Email(sender_email))
        # personalization.add_to(Email(to_email))
        # personalization.add_cc(Email(sender_email))
        email.add_personalization(personalization)

        for at in attachment_list:
            email.add_attachment(at)

        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)

        try:
            sg.send(email)
        except HTTPError as e:
            print(e.to_dict)
            return False

        return True

    def get(self, request, format=None):
        try:
            queryset = TaskComment.objects.exclude(task__is_active=False).all().order_by('updated')[:20]
            queryset1 = TaskComment.objects.all().order_by('-created')[:3]
            object_list = []
            for record in queryset:
                object_list.append(record)
            for record in queryset1:
                object_list.append(record)
            domain = request.build_absolute_uri('/')[:-1]
            html_message = loader.render_to_string('api/revision_items.html', {
                'items': object_list,
                'domain': domain
            })
          
            sender_email = settings.SENDGRID_SENDER_EMAIL
            self._send_email(sender_email, 'mailtodanish@gmail.com', 'Revision Item of the day', html_message, [])
            return Response("Success")
        except Exception as e:
            return Response({"detail": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


class FavouriteItem(APIView):
    '''
    add Fav items
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):

        items = Favoutite_item.objects.all()

        serializer = FavouriteItemSerializer(items, many=True)
        return Response(serializer.data)

    def delete(self, request, format=None):
        '''
        delete favourite items
        '''

        id = request.GET.get("Id", None)
        if not id:
            return Response({"error", "Id is required"},
                            status=status.HTTP_200_OK)
        items = Favoutite_item.objects.filter(id=id).first()
        if not items:
            return Response({"error", "item not found."},
                            status=status.HTTP_200_OK)

        items.delete()
        return Response(status=status.HTTP_200_OK)

    def post(self, request, format=None):
        '''
        create favourite items
        '''

        json_data = request.data

        id = json_data["item_id"]
        item = Favoutite_item.objects.filter(item_id=id).first()
        if item:
            item.delete()
            return Response(status=status.HTTP_200_OK)

        serializer = FavouriteItemSerializer(data=json_data)
        print(serializer)

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response({"data": serializer.data},
                            status=status.HTTP_200_OK)

        return Response({"error": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class MakeTask(APIView):
    '''
    Make comment a task and vice versa
    if comment is a task it will make it remove task flag and vice versa
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):

        id = request.GET.get("id", None)
        if not id:
            return Response({"error", "Id is required"},
                            status=status.HTTP_200_OK)

        comment = TaskComment.objects.filter(id=id).first()
        if not comment:
            return Response({"error", "comment not found."},
                            status=status.HTTP_200_OK)

        if comment.task_flag:
            comment.task_flag = False
        else:
            comment.task_flag = True

        comment.save()

        return Response(status=status.HTTP_200_OK)