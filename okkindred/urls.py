from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path

from rest_framework.schemas import get_schema_view

import okkindred.views

admin.autodiscover()

handler404 = 'okkindred.views.handler404'
handler505 = 'okkindred.views.handler405'


urlpatterns = [

    #https://www.pythoncircle.com/post/578/adding-robotstxt-file-to-django-application/
    path('robots.txt',  TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),

    path('admin/', admin.site.urls),

    path('about/', okkindred.views.about, name='about'),
    path('languages/', okkindred.views.languages, name='languages'),
    path('', okkindred.views.index),

    #Custom user urls
    path('', include('custom_user.urls')),

    #Sign Up urls
    path('', include('sign_up.urls')),

    #Email confirmation views
    path('', include('email_confirmation.urls')),

    #Maps Views
    path('', include('maps.urls')),

    #Family Tree Views
    path('', include('family_tree.urls')),

    # Gallery views
    path('', include('gallery.urls')),

    # Django Rest Docs
    path('api/schema/', get_schema_view(
        title="ok!Kindred API",
    ), name='openapi-schema'),

    # Route TemplateView to serve Swagger UI template.
    #   * Provide `extra_context` with view name of `SchemaView`.
    path('api/docs/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),

    path('', include('auth_api.urls')),

    # Person API
    path('', include('person_api.urls')),

    # Relation API
    path('', include('relation_api.urls')),

    # Invite Email API
    path('', include('invite_email_api.urls')),

    # Images Api
    path('', include('image_api.urls')),

    # User Api
    path('', include('user_api.urls')),

    # Sign Up Api
    path('', include('sign_up_api.urls')),

    # Profile Image Api
    path('', include('profile_image_api.urls')),

    # Gallerys Api
    path('', include('gallery_api.urls')),

    # Location Api
    path('', include('location_api.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))



