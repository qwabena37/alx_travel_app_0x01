from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing, Booking, Review


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model"""
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'review_id', 'user', 'rating', 'comment', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['review_id', 'created_at', 'updated_at']


class ListingSerializer(serializers.ModelSerializer):
    """Serializer for Listing model"""
    
    host = UserSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = [
            'listing_id', 'title', 'description', 'location',
            'price_per_night', 'bedrooms', 'bathrooms', 'max_guests',
            'host', 'created_at', 'updated_at', 'is_available',
            'reviews', 'average_rating', 'total_reviews'
        ]
        read_only_fields = [
            'listing_id', 'created_at', 'updated_at', 
            'reviews', 'average_rating', 'total_reviews'
        ]
    
    def get_average_rating(self, obj):
        """Calculate average rating for the listing"""
        reviews = obj.reviews.all()
        if reviews:
            return round(sum(review.rating for review in reviews) / len(reviews), 2)
        return 0
    
    def get_total_reviews(self, obj):
        """Get total number of reviews"""
        return obj.reviews.count()


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model"""
    
    listing = ListingSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    listing_id = serializers.UUIDField(write_only=True)
    nights = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'listing', 'listing_id', 'user', 
            'check_in_date', 'check_out_date', 'number_of_guests',
            'total_price', 'status', 'created_at', 'updated_at',
            'nights'
        ]
        read_only_fields = [
            'booking_id', 'created_at', 'updated_at', 'nights'
        ]
    
    def get_nights(self, obj):
        """Calculate number of nights"""
        return obj.calculate_nights()
    
    def validate(self, data):
        """Custom validation for booking data"""
        check_in = data.get('check_in_date')
        check_out = data.get('check_out_date')
        
        if check_in and check_out and check_out <= check_in:
            raise serializers.ValidationError(
                "Check-out date must be after check-in date."
            )
        
        return data


class BookingCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating bookings"""
    
    class Meta:
        model = Booking
        fields = [
            'listing', 'check_in_date', 'check_out_date', 
            'number_of_guests', 'total_price'
        ]
    
    def validate(self, data):
        """Validate booking creation data"""
        listing = data.get('listing')
        number_of_guests = data.get('number_of_guests')
        
        if listing and number_of_guests:
            if number_of_guests > listing.max_guests:
                raise serializers.ValidationError(
                    f"Number of guests cannot exceed {listing.max_guests}"
                )
        
        return data