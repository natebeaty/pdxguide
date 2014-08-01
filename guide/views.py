from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.core.mail import send_mail,BadHeaderError,mail_managers 
from django.core import validators
from django import oldforms as forms
from pdxguide.guide.models import *
from pdxguide import settings # FOR YAHOO_ID GLOBAL VAR, SITE_URL
from xml.dom.minidom import parse
import urllib
# from django.utils import simplejson #in replace of import simple_json


def clearcache(request):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE cache")
    return HttpResponseRedirect('/')

#     ---------------
#     SIMPLE SEARCH
#     ---------------

def search(request):
    from django.core.paginator import ObjectPaginator, InvalidPage
    from django.db.models import Q

    if not request.GET: 
        return render_to_response('search.html', {}) 

    q = request.GET['q'].lower()
    page = int(request.GET.get('page',1))
    paginate_by = 10
    message = '';

    # keywords = q.split()
    # sql = ""
    # first = True
    # for word in keywords:
    #     if first:
    #         sql += "(name LIKE '%%" + word + "%%' OR description LIKE '%%" + word + "%%')"
    #         first = False
    #     else:
    #         sql += " AND (name LIKE '%%" + word + "%%' OR description LIKE '%%" + word + "%%')"
    sql = "MATCH (name,description) AGAINST (\"%s\")" % q

    # paginator=ObjectPaginator(Article.objects.extra(where=[sql]).exclude(status='P').exclude(status='N'),paginate_by)
    paginator=ObjectPaginator(Article.objects.extra(where=["MATCH (name,description) AGAINST (\"%s\")"], params=[q]).exclude(status='P').exclude(status='N'),paginate_by)
    # results = Article.objects.search("%s" % q).exclude(status='P').exclude(status='N')[:5]

    try:
        results = paginator.get_page(page-1)
    except (InvalidPage, ValueError):
        results = []
        message = 'No results'

    return render_to_response('search.html', { 'results': results, 'q': q, 'message': message,
        'is_paginated': paginator.pages > 1, 'results_per_page': paginate_by,
        'has_next': paginator.has_next_page(page-1), 'has_previous':
        paginator.has_previous_page(page-1), 'page': page, 'next': page + 1,
        'previous': page - 1, 'pages': paginator.pages, 'hits' :
        paginator.hits, } ) 
        
#     --------------------------------
#     ARTICLE RATINGS / AJAX OR FORM
#     --------------------------------

def details(request):
#        [more stuff]
    if request.POST:
            # Get all the mark for this recipe
            list_mark = Mark.objects.values('mark').filter(recipe__pk=r.id)
            # loop to get the total
            total = 0
            for element in list_mark:
                    total+= element['mark']
            # round it
            total = round((float(total) /  len(list_mark)),1)
            # update the total
            r.total_mark= total
            # save the user mark
            r.save()

            # Now the intersting part for this tut
            import simple_json
            # it was a french string, if we dont't use unicode
            # the result at the output of json in Dojo is wrong.
            message = unicode( message, "utf-8" )
            #
            jsonList = simple_json.dumps((my_mark, total, form_message ,message))
            return HttpResponse(jsonList)
#        [more stuff, if not POST return render_to_response('recettes/details.html' ...]

def all_section(request, section_slug):
    """
    Show all articles in section

    """
    try:
        section = Section.objects.get(slug=section_slug)
    except Section.DoesNotExist:
        raise Http404("No section '%s' found" % section_slug)
#    section = get_object_or_404(Section, slug=section_slug)
    section_article_list = section.article_set.all();
#    section_article_list = get_list_or_404(Article, category_set)
    
    return render_to_response('guide/section_article_list.html', {'section_article_list': section_article_list})

def section_by_quadrant(request, quadrant_slug, section_slug):
    """
    Show all articles in section by quadrant

    """
    from django.views.generic.list_detail import object_list

    q = Quadrant.objects.get(slug=quadrant_slug)
    s = Section.objects.get(slug=section_slug)
    qs = Article.objects.filter(quadrant__slug=quadrant_slug).filter(section__slug=section_slug)

    return object_list(request, qs,extra_context = {"section":s,"quadrant":q},
        paginate_by=20,template_name="guide/section_by_quadrant.html")

#     --------------
#     CONTACT FORM
#     --------------

to_choices = (
    ("editor", "General Contact (Shawn)"),
    ("nate", "Website (Nate)"),
)

class ContactManipulator(forms.Manipulator):
    def __init__(self):
        self.fields = (
            forms.EmailField(field_name="from", length=30, is_required=True),
            forms.TextField(field_name="name", length=30, is_required=True),
            forms.TextField(field_name="subject", length=30, maxlength=200, is_required=False),
            forms.RadioSelectField(field_name="to", choices=to_choices, ul_class='contact-to', is_required=True),
            forms.LargeTextField(field_name="message", is_required=True),
        )

def contact_form(request):
    manipulator = ContactManipulator()
    if request.POST:
        new_data = request.POST.copy()
        errors = manipulator.get_validation_errors(new_data)
        if not errors:
            manipulator.do_html2python(new_data)
            to_email = ["%s@%s" % (new_data['to'], settings.SITE_URL)]
            if not new_data['subject']:
                new_data['subject'] = '%s contact' % (settings.SITE_URL);
            try:
                send_mail(new_data['subject'], new_data['message'], new_data['from'], to_email)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/contact/thanks/')
    else:
        errors = {};
        new_data = {};
        if request.GET:
            new_data['to'] = request.GET['to']
        else:
            new_data['to'] = 'editor'
    form = forms.FormWrapper(manipulator, new_data, errors)
    return render_to_response('contact_form.html', {'form': form})

#     ---------------------
#     CREATE ARTICLE FORM
#     ---------------------

def submit_article(request):
    manipulator = Article.AddManipulator()
    manipulator.fields.append(forms.TextField(field_name="your_name",length=30, is_required=True))
    manipulator.fields.append(forms.EmailField(field_name="your_email",length=30, is_required=True))
    jsCheck = ''

    # attach another validator to the title field, make sure no emails are included (friggin spam)
    for field in manipulator.fields:
        if field.field_name == 'name':
            field.validator_list.append( validators.MatchesRegularExpression('^[^@]+$') )
            break
    
    if request.POST:
        # If data was POSTed, we're trying to create a new Article.
        new_data = request.POST.copy()
        new_data.update(request.FILES)

        if new_data.has_key('jsCheck'):
            # Generate slug
            new_data['slug'] = str(slugify(new_data['name']))

            # Hard coded values
            new_data['status'] = 'P'
            new_data['owner_id'] = 1

            # Add 'from' email to description
        
        
            # Check for errors.
            errors = manipulator.get_validation_errors(new_data)

            if not errors:
            
                # pull contributor fields
                # if new_data['your_name']:
                #     
                    # your_name = str(new_data['your_name'])
                    # if (your_name.count(' ')):
                    #     (first,last) = your_name.split()
                    #     abbr = "%s%s" % (first[:2],last[:2])
                    # else:
                    #     (first,last) = '',your_name
                    #     abbr = last[:4]
                    # email = str(new_data['your_email']) or ''
                    # c = Contributor(firstname=first,lastname=last,abbreviation=abbr,email=email)
                    # c.save()
                    # new_article.author = c
                    # new_article.save()

                # for now we're just adding the name to the description, instead of creating new users like above
                new_data['description'] += "\n\nContributed by: %s (%s)" % (new_data['your_name'],new_data['your_email']) 

                # No errors. This means we can save the data!
                manipulator.do_html2python(new_data)
                new_article = manipulator.save(new_data)

                # EMAIL ADMINS
                mail_subject = 'New article posted on Pdxguide'
                mail_body = 'Title: %s\n\nDescription:%s\n\nEdit: http://pdxguide.org/admin/guide/article/%s/\nDelete: http://pdxguide.org/admin/guide/article/%s/delete/' % (new_data['name'], new_data['description'], new_article.id, new_article.id) 
    #             send_mail(mail_subject, mail_body, 'www@pdxguide.org', ['nate@clixel.com'])
                mail_managers(mail_subject, mail_body, fail_silently=True) 

                # Redirect to the object's "edit" page. Always use a redirect
                # after POST data, so that reloads don't accidently create
                # duplicate entires, and so users don't see the confusing
                # "Repost POST data?" alert box in their browsers.
                return HttpResponseRedirect("/submit/article/thanks/")
        else:
            jsCheck = 'Spambot suspected, please <a href="/contact/">contact</a> us for help!'
            errors = {}
    else:
        # No POST, so we want a brand new form without any data or errors.
        errors = new_data = {}

    # Create the FormWrapper, template, context, response.
    form = forms.FormWrapper(manipulator, new_data, errors)

    # Limit section choices to web-only
    section_choices = [(s.id, s) for s in Section.objects.filter(status__exact="A")]
    form['section'].formfield.choices = section_choices
    
    return render_to_response('guide/submit_article.html', {'form': form, 'errors': errors, 'jsCheck':jsCheck})


class Geocoder:
    """ look up an location using the Yahoo geocoding api

        Requires a Yahoo appid which can be obtained at:
        http://developer.yahoo.net/faq/index.html#appid

        Documentation for the Yahoo geocoding api can be found at:
        http://developer.yahoo.net/maps/rest/V1/geocode.html
    """

    def __init__(self, appid, address_str):
        self.address_str = address_str
        self.addresses = []
        self.result_count = 0
        parms = {'appid': appid, 'location': address_str}

        try:
            url = 'http://api.local.yahoo.com/MapsService/V1/geocode?'+urllib.urlencode(parms)
            # parse the xml contents of the url into a dom
            dom = parse(urllib.urlopen(url))
            results = dom.getElementsByTagName('Result')
            self.result_count = len(results)

            for result in results:
                d = {'precision': result.getAttribute('precision'),
                      'warning': result.getAttribute('warning')}
                for itm in result.childNodes:
                    # if precision is zip, Address childNode will not exist
                    if itm.childNodes:
                        d[itm.nodeName] = itm.childNodes[0].data
                    else:
                        d[itm.nodeName] = ''
                self.addresses.append(d)
        except:
            raise "GeocoderError"

    def __repr__(self):
        s = "Original address:n%snn"%self.address_str
        s += "%d match(s) found:nn"%self.result_count
        for addr in self.addresses:
            s += """Match precision: %(precision)s
Location: (%(Latitude)s,%(Longitude)s)
%(Address)s
%(City)s, %(State)s %(Zip)s
"""%addr
        return s
