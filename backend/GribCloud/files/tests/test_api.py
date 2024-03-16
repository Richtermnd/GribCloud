from django.urls import reverse
import parameterized
from rest_framework import status
from rest_framework.test import APITestCase

from files.models import File, Tag
from user.models import User


class FileListAPIViewTests(APITestCase):
    fixtures = ["files/fixtures/test.json"]

    def setUp(self):
        self.user = User.objects.get(username="authoruser")
        self.client.force_authenticate(user=self.user)

    def test_get_file_list(self):
        response = self.client.get(reverse("files:list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_files(self):
        url = reverse("files:list")
        data = {"files": [["path/to/file1.jpg", "preview/to/file1.jpg"], ["path/to/file2.jpg", "preview/to/file2.jpg"]]}

        count = File.objects.count()
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(File.objects.count(), count + 2)

    @parameterized.parameterized.expand(
        [
            ({},),
            ({"files": []},),
            ({"files": ["path/to/file1.jpg", "path/to/file2.png"]},),
            (
                {
                    "fiiles": [
                        ["path/to/file1.jpg", "preview/to/file1.jpg"],
                        ["path/to/file2.jpg", "preview/to/file2.jpg"],
                    ],
                },
            ),
        ],
    )
    def test_create_invalid_files(self, data):
        url = reverse("files:list")

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class FileDetailAPIViewTests(APITestCase):
    fixtures = ["files/fixtures/test.json"]

    def setUp(self):
        self.user = User.objects.get(username="authoruser")
        self.client.force_authenticate(user=self.user)
        self.client.post(reverse("files:list"), {"files": [["files/1.jpg", "previews/1.jpg"]]}, format="json")

    def test_get(self):
        url = reverse("files:detail", kwargs={"pk": 1})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        file = response.data
        list_in = ["id", "author", "file", "created_at"]
        for el in list_in:
            self.assertIn(el, file)

    def test_delete(self):
        url = reverse("files:detail", kwargs={"pk": 1})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_post(self):
        url = reverse("files:detail", kwargs={"pk": 1})

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch(self):
        url = reverse("files:detail", kwargs={"pk": 1})

        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_unauthorized_access(self):
        self.client.logout()
        url = reverse("files:detail", kwargs={"pk": 1})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_author_access(self):
        user = User.objects.get(username="admin")
        self.client.force_authenticate(user=user)
        url = reverse("files:detail", kwargs={"pk": 1})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class FileTagAPIViewTestCase(APITestCase):
    fixtures = ["files/fixtures/test.json"]
    
    def setUp(self):
        self.user = User.objects.get(username="authoruser")
        self.file = File.objects.get(file="images/file.jpg")
        self.tag = Tag.objects.get(title="testtag")
        self.url = reverse("files:tags", args=[self.file.pk, self.tag.title])

    def test_get_file_tag(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["file"]["id"], self.file.pk)
        self.assertEqual(response.data["tag"]["title"], self.tag.title)

    def test_get_file_tag_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_file_tag_not_author(self):
        other_user = User.objects.get(username="testuser")
        self.client.force_authenticate(user=other_user)
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_file_tag(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(self.url)
        self.file.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.tag, self.file.tags.all())

    def test_post_file_tag_already_added(self):
        self.client.force_authenticate(user=self.user)
        self.file.tags.add(self.tag)
        
        response = self.client.post(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_delete_file_tag(self):
        self.file.tags.add(self.tag)
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(self.url)
        self.file.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.tag, self.file.tags.all())


    def test_delete_file_tag_not_found(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
