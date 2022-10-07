from django.test import TestCase

from projects.models import ApplictaionData,ProjectTask


class ApplictaionDataModelTest(TestCase):
    '''
    Test Case for model : ApplictaionData
    1. cascade delete 
    2. label Name
    3. Max
    '''
    @classmethod
    def setUpTestData(cls):
        ApplictaionData.objects.create(Name='Category',                                                                               
                                       IsCategory=True)
        ApplictaionData.objects.create(Name='Big', 
                                       Value='Bob',
                                       Type= ApplictaionData.objects.get(Name='Category'),                                       
                                       Description="Description")

    def test_name_label(self):
        lov = ApplictaionData.objects.get(id=2)
        field_label = lov._meta.get_field('Name').verbose_name
        self.assertEquals(field_label, 'name')


    def test_name_max_length(self):
        lov = ApplictaionData.objects.get(id=2)
        max_length = lov._meta.get_field('Name').max_length
        self.assertEquals(max_length, 200)

    def test_value_label(self):
        lov = ApplictaionData.objects.get(id=2)
        field_label = lov._meta.get_field('Value').verbose_name
        self.assertEquals(field_label, 'value')


    def test_value_max_length(self):
        lov = ApplictaionData.objects.get(id=2)
        max_length = lov._meta.get_field('Value').max_length
        self.assertEquals(max_length, 200)
    
    def test_IsCategory_label(self):
        lov = ApplictaionData.objects.get(id=2)
        field_label = lov._meta.get_field('IsCategory').verbose_name
        self.assertEquals(field_label, 'category')


    def test_Type_of_lov(self):
        lov = ApplictaionData.objects.get(id=2)
        self.assertEquals(lov.Type, ApplictaionData.objects.get(id=1))

    def test_Type_label(self):
        lov = ApplictaionData.objects.get(id=2)
        field_label = lov._meta.get_field('Type').verbose_name
        self.assertEquals(field_label, 'type')

    def test_cascade_delete_type(self):
        '''
        Cascade delete is working.
        '''
        lov_type = ApplictaionData.objects.get(id=1)
        lov_type.delete()
        lov = ApplictaionData.objects.filter(id=2).exists()
        self.assertEquals(lov, False)
    
    def test_Description_label(self):
        lov = ApplictaionData.objects.get(id=2)
        field_label = lov._meta.get_field('Description').verbose_name
        self.assertEquals(field_label, 'description')
    
    def test_description_max_length(self):
        lov = ApplictaionData.objects.get(id=2)
        max_length = lov._meta.get_field('Description').max_length
        self.assertEquals(max_length, 200)
    

    def test_get_absolute_url(self):
        lov = ApplictaionData.objects.get(id=1)
        self.assertEquals(lov.get_absolute_url(), '/setting/lov/')

    def test_string_representation(self):
        lov = ApplictaionData.objects.get(id=1)
        self.assertEqual(str(lov), lov.Name)


