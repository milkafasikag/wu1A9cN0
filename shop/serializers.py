from rest_framework import serializers
from .models import *

    
class OrderChartSerializer22(serializers.ModelSerializer):
    # Add fields from related models
    client_name = serializers.CharField(source='client.guest_name', read_only=True)
    client_phone = serializers.CharField(source='client.guest_phone', read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order_chart
        fields = '__all__'

    def get_total_price(self, instance):
        # Calculate and return the total price of items in the order chart
        total_price = sum(item.item.price*item.quntity for item in instance.order.all())
        return total_price

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'

class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    descriptions = DescriptionSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    type = TypeSerializer()


    class Meta:
        model = Item
        fields = '__all__'

class OrdertSerializer(serializers.ModelSerializer):
    Client = ClientSerializer(read_only=True)
    item = ItemSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class ReciptSerializer(serializers.ModelSerializer):
    class Meta:
        model = recipt
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    recipts = ReciptSerializer(many=True, read_only=True)
    class Meta:
        model = Payment
        fields = '__all__'

class OrderChartSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.guest_name', read_only=True)
    client_phone = serializers.CharField(source='client.guest_phone', read_only=True)
    total_price = serializers.SerializerMethodField()
    order = OrdertSerializer(many=True, read_only=True)
    coupons = CouponSerializer(many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)


    class Meta:
        model = Order_chart
        fields = '__all__'

    def get_total_price(self, instance):
        total_price =  round(sum((1-item.item.disc/100)*item.item.price*item.quntity for item in instance.order.all()),2)
        return total_price
    

class OrderSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    order = OrdertSerializer(many=True, read_only=True)

    class Meta:
        model = Order_chart
        fields = '__all__'

class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class DescriptionCreateSerializer(DescriptionSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())

class ImageCreateSerializer(ImageSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())


class ClientCreateSerializer(ClientSerializer):
    booking = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())