from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase, APITransactionTestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from projects.models import Activity, TaskComment
from .serializers import ActivitySerializer
from rest_framework.authtoken.models import Token


class ChildActivityList(APITestCase):
    '''
    child activities of a parent activity
    '''

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.token = Token.objects.create(user=self.superuser)
        self.api_authentication()
        self.ParentActivity = Activity.objects.create(
            Title="Activity_Title", Description="Description")
        self.ChildActivity = Activity.objects.create(
            Title="Activity_child_Title", Description="Description", parentActivityId=self.ParentActivity.id)
        self.ChildActivityOne = Activity.objects.create(
            Title="Activity_child_Title1", Description="Description", parentActivityId=self.ParentActivity.id)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_can_get_child_activities(self):
        response = self.client.get(
            reverse('api-child-activity', args=[self.ParentActivity.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_count_child_activities(self):
        # Count Number of Child Activities
        response = self.client.get(
            reverse('api-child-activity', args=[self.ParentActivity.id]))
        self.assertEqual(len(response.data), 2)


class CreateActivityTest(APITestCase):
    '''
    ActivityRouter - Test Cases Create
    '''

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        # self.client.login(username='john', password='johnpassword')
        self.data = {'Title': 'Activity_Title',
                     'Description': 'Activity_Description'}
        self.token = Token.objects.create(user=self.superuser)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_can_create_activity(self):
        response = self.client.post(reverse('api-activity-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ReadActivityTest(APITestCase):
    '''
    ActivityRouter - Test Cases list
    '''

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.Activity = Activity.objects.create(
            Title="Activity_Title", Description="Description")

    def test_can_read_activity_list(self):
        response = self.client.get(reverse('api-activity-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_activity_detail(self):
        response = self.client.get(
            reverse('api-activity-detail', args=[self.Activity.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateActivityTest(APITestCase):
    '''
    ActivityRouter - Test Cases update
    '''

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.Activity = Activity.objects.create(
            Title="Activity_Title", Description="Description")
        self.data = ActivitySerializer(self.Activity).data
        self.data.update({'Description': 'Changed'})

    def test_can_update_user(self):
        response = self.client.put(
            reverse('api-activity-detail', args=[self.Activity.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteActivityTest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.Activity = Activity.objects.create(
            Title="Activity_Title", Description="Description")

    def test_can_delete_user(self):
        response = self.client.delete(
            reverse('api-activity-detail', args=[self.Activity.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ReadScheduledActivityListTest(APITestCase):
    '''
    api/activities/scheduled - Test Cases for scheduled list
    only Get Method is available.
    '''

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.token = Token.objects.create(user=self.superuser)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_can_read_activity_list(self):
        response = self.client.get(reverse('activity_api_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RevisionItemofTheDayTest(APITestCase):
    '''
    api/dailytask/ - Test Cases for RevisionItemofTheDay
    only Get Method is available.
    '''

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.token = Token.objects.create(user=self.superuser)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_can_read_daily_activity_list(self):
        response = self.client.get(reverse('daily_task'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class daily_random_revision_item_Test(APITestCase):
    '''
    api/random_revision_item/ - Test Cases for RevisionItemofTheDay
    only Get Method is available.
    #database is usually recreated from scratch and thus empty - Hence added Records
    '''
    client_class = APIClient

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'john', 'john@snow.com', 'johnpassword')
        self.token = Token.objects.create(user=self.superuser)
        self.api_authentication()
        # database is usually recreated from scratch and thus empty
        TaskComment.objects.create(
            content="Activity_Title", tags=["Description", ])
        TaskComment.objects.create(
            content="Activity_Title1", tags=["Description", ])
        TaskComment.objects.create(
            content="Activity_Title2", tags=["Description", ])
        TaskComment.objects.create(
            content="Activity_Title3", tags=["Description", ])
        TaskComment.objects.create(
            content="Activity_Title4", tags=["Description", ])

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_daily_random_revision_item(self):
        api_response = self.client.get(
            reverse('daily_random_revision_item'), format='json')
        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
