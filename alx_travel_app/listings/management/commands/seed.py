from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
import random
from listings.models import Listing, Booking, Review


class Command(BaseCommand):
    help = 'Seed the database with sample listings, bookings, and reviews'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--listings',
            type=int,
            default=10,
            help='Number of listings to create'
        )
        parser.add_argument(
            '--bookings',
            type=int,
            default=20,
            help='Number of bookings to create'
        )
        parser.add_argument(
            '--reviews',
            type=int,
            default=15,
            help='Number of reviews to create'
        )
    
    def handle(self, *args, **options):
        self.stdout.write('Starting database seeding...')
        
        # Create users first
        users = self.create_users()
        self.stdout.write(f'Created {len(users)} users')
        
        # Create listings
        listings = self.create_listings(users, options['listings'])
        self.stdout.write(f'Created {len(listings)} listings')
        
        # Create bookings
        bookings = self.create_bookings(users, listings, options['bookings'])
        self.stdout.write(f'Created {len(bookings)} bookings')
        
        # Create reviews
        reviews = self.create_reviews(users, listings, options['reviews'])
        self.stdout.write(f'Created {len(reviews)} reviews')
        
        self.stdout.write(
            self.style.SUCCESS('Database seeding completed successfully!')
        )
    
    def create_users(self):
        """Create sample users"""
        users_data = [
            {'username': 'john_host', 'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com'},
            {'username': 'jane_traveler', 'first_name': 'Jane', 'last_name': 'Smith', 'email': 'jane@example.com'},
            {'username': 'mike_guest', 'first_name': 'Mike', 'last_name': 'Johnson', 'email': 'mike@example.com'},
            {'username': 'sarah_host', 'first_name': 'Sarah', 'last_name': 'Wilson', 'email': 'sarah@example.com'},
            {'username': 'david_explorer', 'first_name': 'David', 'last_name': 'Brown', 'email': 'david@example.com'},
        ]
        
        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            users.append(user)
        
        return users
    
    def create_listings(self, users, count):
        """Create sample listings"""
        sample_listings = [
            {
                'title': 'Cozy Beachfront Villa',
                'description': 'Beautiful villa with stunning ocean views and private beach access.',
                'location': 'Miami, Florida',
                'price_per_night': Decimal('250.00'),
                'bedrooms': 3,
                'bathrooms': 2,
                'max_guests': 6,
            },
            {
                'title': 'Mountain Cabin Retreat',
                'description': 'Peaceful cabin nestled in the mountains with hiking trails nearby.',
                'location': 'Aspen, Colorado',
                'price_per_night': Decimal('180.00'),
                'bedrooms': 2,
                'bathrooms': 1,
                'max_guests': 4,
            },
            {
                'title': 'Urban Loft Downtown',
                'description': 'Modern loft in the heart of the city with easy access to attractions.',
                'location': 'New York, NY',
                'price_per_night': Decimal('300.00'),
                'bedrooms': 1,
                'bathrooms': 1,
                'max_guests': 2,
            },
            {
                'title': 'Countryside Farmhouse',
                'description': 'Charming farmhouse surrounded by rolling hills and farmland.',
                'location': 'Tuscany, Italy',
                'price_per_night': Decimal('200.00'),
                'bedrooms': 4,
                'bathrooms': 3,
                'max_guests': 8,
            },
            {
                'title': 'Desert Oasis Resort',
                'description': 'Luxurious resort with pool and spa amenities in the desert.',
                'location': 'Scottsdale, Arizona',
                'price_per_night': Decimal('400.00'),
                'bedrooms': 2,
                'bathrooms': 2,
                'max_guests': 4,
            },
        ]
        
        listings = []
        for i in range(min(count, len(sample_listings))):
            listing_data = sample_listings[i].copy()
            listing_data['host'] = random.choice(users)
            
            listing = Listing.objects.create(**listing_data)
            listings.append(listing)
        
        # If we need more listings than our sample data, create variations
        if count > len(sample_listings):
            for i in range(len(sample_listings), count):
                base_listing = sample_listings[i % len(sample_listings)]
                listing_data = base_listing.copy()
                listing_data['title'] = f"{base_listing['title']} - Variant {i+1}"
                listing_data['host'] = random.choice(users)
                listing_data['price_per_night'] += Decimal(random.randint(-50, 100))
                
                listing = Listing.objects.create(**listing_data)
                listings.append(listing)
        
        return listings
    
    def create_bookings(self, users, listings, count):
        """Create sample bookings"""
        bookings = []
        
        for i in range(count):
            listing = random.choice(listings)
            user = random.choice([u for u in users if u != listing.host])
            
            # Generate random dates
            start_date = date.today() + timedelta(days=random.randint(1, 90))
            end_date = start_date + timedelta(days=random.randint(1, 14))
            
            nights = (end_date - start_date).days
            total_price = listing.price_per_night * nights
            
            booking = Booking.objects.create(
                listing=listing,
                user=user,
                check_in_date=start_date,
                check_out_date=end_date,
                number_of_guests=random.randint(1, listing.max_guests),
                total_price=total_price,
                status=random.choice(['pending', 'confirmed', 'completed'])
            )
            bookings.append(booking)
        
        return bookings
    
    def create_reviews(self, users, listings, count):
        """Create sample reviews"""
        reviews = []
        review_comments = [
            "Amazing place! Clean, comfortable, and great location.",
            "Perfect for a family vacation. Host was very responsive.",
            "Beautiful property with stunning views. Highly recommended!",
            "Good value for money. Would definitely stay again.",
            "Excellent amenities and very peaceful surroundings.",
            "Great experience overall. The photos don't do it justice!",
            "Convenient location with easy access to local attractions.",
            "Host went above and beyond to make our stay comfortable.",
        ]
        
        for i in range(count):
            listing = random.choice(listings)
            # Ensure reviewer is not the host
            available_users = [u for u in users if u != listing.host]
            user = random.choice(available_users)
            
            # Check if this user already reviewed this listing
            if not Review.objects.filter(listing=listing, user=user).exists():
                review = Review.objects.create(
                    listing=listing,
                    user=user,
                    rating=random.randint(3, 5),  # Bias towards positive reviews
                    comment=random.choice(review_comments)
                )
                reviews.append(review)
        
        return reviews