from django.core.management.base import BaseCommand
from django.utils import timezone
from portfolio.utils import ContentManager

class Command(BaseCommand):
    help = 'Publish scheduled content that is due'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be published without actually publishing',
        )

    def handle(self, *args, **options):
        if options['dry_run']:
            self.stdout.write('DRY RUN - No content will be published')
            
            from portfolio.models import BlogPost, AcademiaPost, TravelPost, FunStory
            
            now = timezone.now()
            models_to_check = [BlogPost, AcademiaPost, TravelPost, FunStory]
            
            total_to_publish = 0
            
            for model in models_to_check:
                scheduled_items = model.objects.filter(
                    status='scheduled',
                    publish_date__lte=now
                )
                
                count = scheduled_items.count()
                total_to_publish += count
                
                if count > 0:
                    self.stdout.write(f'Would publish {count} {model.__name__} items:')
                    for item in scheduled_items:
                        self.stdout.write(f'  - {item.title} (scheduled for {item.publish_date})')
            
            if total_to_publish == 0:
                self.stdout.write('No scheduled content ready for publishing')
            else:
                self.stdout.write(f'Total items to publish: {total_to_publish}')
        
        else:
            published_count = ContentManager.publish_scheduled_content()
            
            if published_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully published {published_count} scheduled items')
                )
            else:
                self.stdout.write('No scheduled content was ready for publishing')