from django.db import models
from django.contrib.auth.models import User 
from django.template.defaultfilters import slugify
from datetime import datetime
from pdxguide.middleware import threadlocals
from geopy import geocoders
from pdxguide import settings
import re

ARTICLE_STATUS_CHOICES = (
	('B','Book Active'),
	('A','Web Only'),
	('N','Not Active'),
	('P','Pending Approval'),
    )
QUADRANT_STATUS_CHOICES = (
	('B','Book Only'),
	('W','Web Only'),
	('A','Book and Web'),
    )
SECTION_STATUS_CHOICES = (
	('B','Book Only'),
	('W','Web Only'),
	('A','Book and Web'),
    )

class Contributor(models.Model):
    firstname = models.CharField(blank=True, max_length=200)
    lastname = models.CharField(blank=True, max_length=200)
    abbreviation = models.CharField(blank=True, unique=True, max_length=30)
    email = models.EmailField(blank=True)
    webuser = models.BooleanField()
    class Admin:
        pass
        list_display = ('firstname', 'lastname')
        search_fields = ['firstname']
        fields = (
            (None, {'fields': ('firstname','lastname','email','abbreviation')}),
        )
    def __str__(self):
     return "%s %s (%s)" % (self.firstname, self.lastname, self.abbreviation)

class Section(models.Model):
    slug = models.SlugField(
        'Slug',
        prepopulate_from=('name',),
        help_text='Automatically built from the name.',
        blank=True,
    )
    name = models.CharField(blank=True, max_length=60)
    intro = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=5,choices=SECTION_STATUS_CHOICES,radio_admin=True)
    def __str__(self):
        return self.name
    def is_active(self):
        return self.status == 'A' or self.status == 'W'
    class Admin:
        pass
    class Meta:
        ordering = ('name',)
    def get_absolute_url(self):
        return "/browse/all/%s/" % (self.slug)

class Quadrant(models.Model):
    slug = models.SlugField(
        'Slug',
        prepopulate_from=('name',),
        help_text='Automatically built from the name.',
        blank=True,
    )
    name = models.CharField(blank=True, max_length=60)
    shortname = models.CharField(blank=True, max_length=15)
    description = models.TextField(blank=True)
    order = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=5,choices=QUADRANT_STATUS_CHOICES,radio_admin=True)
#    order = models.OrderingField(with_respect_to=Quadrant)
    def __str__(self):
        return self.name
    def is_active(self):
        return self.status == 'A' or self.status == 'W'
    class Admin:
        pass
    class Meta:
        ordering = ('order',)
    def get_absolute_url(self):
        return "/browse/%s/" % (self.slug)
        
class Image(models.Model):
    fileprefix = models.TextField(blank=True)
    artist = models.ForeignKey(Contributor)
    tiffwidth = models.IntegerField(null=True, blank=True)
    tiffheight = models.IntegerField(null=True, blank=True)
    tiffres = models.IntegerField(null=True, blank=True)
    jpegwidth = models.IntegerField(null=True, blank=True)
    jpegheight = models.IntegerField(null=True, blank=True)
    caption = models.TextField(blank=True)
    def __str__(self):
        return self.fileprefix

class Essay(models.Model):
    slug = models.SlugField(
        'Slug',
        prepopulate_from=('title',),
        help_text='Automatically built from the title.',
    )
    section = models.ForeignKey(Section, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    author = models.ForeignKey(Contributor, blank=True, null=True)
    # owner = models.ForeignKey(User,related_name="essay_owner",blank=True)
    # last_edited_by = models.ForeignKey(User,related_name="essay_last_edited_by",blank=True)
    image = models.ManyToManyField(Image, verbose_name="related images", blank=True)
    status = models.CharField(max_length=5,choices=ARTICLE_STATUS_CHOICES,radio_admin=True,default='A')
    date_added = models.DateTimeField(blank=True, auto_now_add=True)
    date_modified = models.DateTimeField(editable=False,blank=True, auto_now=True)
    def __str__(self):
        return self.title
    def is_active(self):
        return self.status == 'A' or self.status == 'B'
    def get_absolute_url(self):
        return "/essays/%s/" % (self.section.slug)
    class Admin:
        pass
    # def save(self):
    #     # If the object already existed, it will already have an id
    #     if self.id:
    #         # This object is being edited, not saved, set last_edited_by
    #         self.last_edited_by = threadlocals.get_current_user()
    #     else:
    #         # This is a new object, set the owner 
    #         self.owner = threadlocals.get_current_user()
    #         # Without this, raises error that last_edited_by cannot be Null ?
    #         self.last_edited_by = threadlocals.get_current_user()
    #     super(Essay, self).save()    
    
class Rating(models.Model):
    score = models.IntegerField()
    ip = models.IPAddressField(blank=True)
    score_date = models.DateField(auto_now_add=True)
    
class Article(models.Model):
    slug = models.SlugField(
        'Slug',
        prepopulate_from=('name',),
        help_text='Automatically built from the name.',
        unique=True,
    )
    section = models.ForeignKey(Section)
    quadrant = models.ForeignKey(Quadrant)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, blank=True)
    phone = models.PhoneNumberField(blank=True)
    url = models.CharField(max_length=200, blank=True)
    details = models.CharField(max_length=250,blank=True)
    description = models.TextField(blank=True)
    xref_review = models.CharField(max_length=16, blank=True)
    parent = models.ForeignKey("self", null=True, blank=True, related_name="child_set")
    # author = models.ForeignKey(Contributor, blank=True)
    # owner = models.ForeignKey(User,related_name="article_owner",blank=True,null=True)
    # last_edited_by = models.ForeignKey(User,related_name="article_last_edited_by",blank=True)
    image = models.ForeignKey(Image, blank=True)
    status = models.CharField(max_length=5,choices=ARTICLE_STATUS_CHOICES,radio_admin=True,default='A')
    latitude = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)
    mapurl = models.URLField(blank=True)
    trimeturl = models.URLField(blank=True)
    date_added = models.DateTimeField(blank=True, auto_now_add=True)
    date_modified = models.DateTimeField(editable=False,blank=True, auto_now=True)
    admin_notes = models.TextField(blank=True,null=True)
    needs_updating = models.BooleanField()
    # rating = models.ManyToManyField(Rating)

    # indexer = LuceneIndexer('/tmp/article-index', Article,
    #                         text_fields=['Article.description']
    #                         )

    def __str__(self):
        return self.name.encode('utf-8')
    def is_active(self):
        return self.status == 'A' or self.status == 'B'
    def has_info(self):
        return (self.details or self.address or self.phone or self.url) != ''
    def has_map(self):
       return self.latitude > 0 or self.longitude > 0
    def get_absolute_url(self):
        return "/browse/%s/%s/%s/" % (self.quadrant.slug,self.section.slug,self.slug)
    def get_quadrant(self):
        return self.quadrant.shortname
    def fixed_name(self):
#        pattern = re.compile(r'([^,]+),[\s]?(the|a|an)[\s]+(.*)')
#        result = pattern.sub('[2] [1] [3]', self.name)
    	pattern = re.compile(r'([^,]+),\s?(the|a|an)$', re.I)
        result = pattern.sub(r'\2 \1', self.name)
    	return result
    def get_rating(self):
        return 'rating'

    class Admin:
        pass
        ordering = ["-date_modified"]
        date_hierarchy = 'date_modified'
        list_display = ('name','get_quadrant','status')
        search_fields = ('name', 'description')
        list_filter = ('quadrant','section','date_modified', 'status')
        fields = (
            ('Information', {
                'fields': ('section','quadrant','status','needs_updating','name','slug','address','phone','url', 'details','description','parent','image')
            }),
            # ('Author', {
            #     'fields': ('author',)
            # }),
            ('Advanced options', {
                # 'classes': 'collapse',
                'fields' : ('admin_notes','image','parent','latitude','longitude')
            }),
        )

    class Meta:
        ordering = ('name',)
        get_latest_by = 'date_added'

    def save(self):
        # # If the object already existed, it will already have an id
        # if self.id:
        #     # This object is being edited, not saved, set last_edited_by
        #     self.last_edited_by = threadlocals.get_current_user()
        # else:
        #     # This is a new object, set the owner 
        #     self.owner = threadlocals.get_current_user()
        #     # Without this, raises error that last_edited_by cannot be Null ?
        #     self.last_edited_by = threadlocals.get_current_user()

        d = datetime.now()
        pdate = datetime(d.year, d.month, d.day, d.hour, d.minute)
        if self.date_added is None:
            self.date_added = pdate
        self.date_modified = pdate
        self.slug = slugify(self.name)
        # Geocode address
        if self.address and not self.latitude > 0:
            g = geocoders.Google(settings.GOOGLE_ID)
            try:
                place, (latitude, longitude) = g.geocode("%s Portland, OR" % self.address)
                self.latitude, self.longitude = (latitude, longitude)
            except ValueError:
                self.latitude, self.longitude = (0,0)

        super(Article, self).save()
        
