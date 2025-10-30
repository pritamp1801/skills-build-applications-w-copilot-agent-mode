from django.core.management.base import BaseCommand
from octofit_tracker.models import Team, User, Activity, Workout, Leaderboard
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear existing data
        # Delete children first, then parents
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users (super heroes)
        users = []
        users.append(User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel))
        users.append(User.objects.create(name='Captain America', email='cap@marvel.com', team=marvel))
        users.append(User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel))
        users.append(User.objects.create(name='Batman', email='batman@dc.com', team=dc))
        users.append(User.objects.create(name='Superman', email='superman@dc.com', team=dc))
        users.append(User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc))

        # Create workouts
        workouts = []
        workouts.append(Workout.objects.create(name='Cardio Blast', description='High intensity cardio workout', suggested_for='All'))
        workouts.append(Workout.objects.create(name='Strength Training', description='Build muscle and strength', suggested_for='Marvel'))
        workouts.append(Workout.objects.create(name='Agility Drills', description='Improve agility and speed', suggested_for='DC'))

        # Create activities
        Activity.objects.create(user=users[0], type='Running', duration=30, calories=300, date='2025-10-30')
        Activity.objects.create(user=users[3], type='Cycling', duration=45, calories=400, date='2025-10-30')

        # Create leaderboard
        Leaderboard.objects.create(team=marvel, points=100)
        Leaderboard.objects.create(team=dc, points=90)

        # Ensure unique index on email
        with connection.cursor() as cursor:
            cursor.execute('db.users.createIndex({ "email": 1 }, { unique: true })')

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data'))
