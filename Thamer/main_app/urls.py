from django.urls import path
from . import views

app_name = "main_app"

urlpatterns = [
    path("company/add/", views.add_company, name="add_company"),
    path("", views.entry_page, name="entry_page"),
    path("home/", views.index_page, name="index_page"),
    path("company/add/", views.add_company, name="add_company"),
    path("home/faq_page/", views.faq_page, name="faq_page"),
    path("home/contact_us/", views.contact_us, name="contact_us"),
    path("home/market/", views.market_page, name="market_page"),
    path("companys/update/<company_id>/", views.update_company, name="update_company"),
    path("companys/details/<company_id>/", views.company_detail, name="company_detail"),
    path("companys/delete/<company_id>/", views.delete_company, name="delete_company"),
    path("companys/<company_id>/review/add/", views.add_review, name="add_review"),
    path("home/what_we_do/", views.what_we_do, name="what_we_do"),
    path("home/consultion/", views.consultion_page, name="consultion_page"),
    path("home/over_view/", views.over_view, name="over_view"),
    path("home/companys/", views.company_page, name="company_page"),
    path("home/profile/", views.profile_page, name="profile_page"),
    path("home/dashboard", views.dashboard_page, name="dashboard_page"),
    path("companys/owner_details/<company_id>/", views.onwer_details, name="onwer_details"),
    path("submit/done", views.submit_done, name="submit_done"),

]