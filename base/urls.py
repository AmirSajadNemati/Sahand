from django.urls import path
from base.views import (
    BasePageAddOrUpdateView, BasePageGetListView, BasePageGetView, BasePageDeleteView, BasePageUndeleteView,
    BranchAddOrUpdateView, BranchGetListView, BranchGetView, BranchDeleteView, BranchUndeleteView,
    CityAddOrUpdateView, CityGetListView, CityGetView, CityDeleteView, CityUndeleteView,
    ContactInfoAddOrUpdateView, ContactInfoGetListView, ContactInfoGetView, ContactInfoDeleteView,
    ContactInfoUndeleteView,
    CountryAddOrUpdateView, CountryGetListView, CountryGetView, CountryDeleteView, CountryUndeleteView,
    FaqAddOrUpdateView, FaqGetListView, FaqGetView, FaqDeleteView, FaqUndeleteView,
    FaqCategoryAddOrUpdateView, FaqCategoryGetListView, FaqCategoryGetView, FaqCategoryDeleteView,
    FaqCategoryUndeleteView,
    HelpAddOrUpdateView, HelpGetListView, HelpGetView, HelpDeleteView, HelpUndeleteView,
    HelpCategoryAddOrUpdateView, HelpCategoryGetListView, HelpCategoryGetView, HelpCategoryDeleteView,
    HelpCategoryUndeleteView,
    LayoutTagAddOrUpdateView, LayoutTagGetListView, LayoutTagGetView, LayoutTagDeleteView, LayoutTagUndeleteView,
    MenuAddOrUpdateView, MenuGetListView, MenuGetView, MenuDeleteView, MenuUndeleteView,
    PageSeoAddOrUpdateView, PageSeoGetListView, PageSeoGetView, PageSeoDeleteView, PageSeoUndeleteView,
    ProvinceAddOrUpdateView, ProvinceGetListView, ProvinceGetView, ProvinceDeleteView, ProvinceUndeleteView,
    SettingAddOrUpdateView, SettingGetListView, SettingGetView, SettingDeleteView, SettingUndeleteView,
    SliderAddOrUpdateView, SliderGetListView, SliderGetView, SliderDeleteView, SliderUndeleteView,
    SpecialCategoryAddOrUpdateView, SpecialCategoryGetListView, SpecialCategoryGetView, SpecialCategoryDeleteView,
    SpecialCategoryUndeleteView,
    SpecialGroupCategoryAddOrUpdateView, SpecialGroupCategoryGetListView, SpecialGroupCategoryGetView,
    SpecialGroupCategoryDeleteView, SpecialGroupCategoryUndeleteView,
    StaticContentAddOrUpdateView, StaticContentGetListView, StaticContentGetView, StaticContentDeleteView,
    StaticContentUndeleteView,
    StaticFormAddOrUpdateView, StaticFormGetListView, StaticFormGetView, StaticFormDeleteView, StaticFormUndeleteView,
    StaticPageAddOrUpdateView, StaticPageGetListView, StaticPageGetView, StaticPageDeleteView, StaticPageUndeleteView,
    SiteInfoAddOrUpdateView, SiteInfoGetListView, SiteInfoGetView, SiteInfoDeleteView, SiteInfoUndeleteView,
    PhotoAddOrUpdateView, PhotoGetListView, PhotoGetView, PhotoDeleteView, PhotoUndeleteView,
    AbstractContentAddOrUpdateView, AbstractContentGetListView, AbstractContentGetView, \
    AbstractContentDeleteView, AbstractContentUndeleteView
)

urlpatterns = [
    # BasePage URLs
    path('BasePageAddOrUpdate/', BasePageAddOrUpdateView.as_view(), name="base_page_add_or_update"),
    path('BasePageList/', BasePageGetListView.as_view(), name="base_page_get_list"),
    path('BasePageGet/', BasePageGetView.as_view(), name="base_page_get"),
    path('BasePageDelete/', BasePageDeleteView.as_view(), name="base_page_delete"),
    path('BasePageUndelete/', BasePageUndeleteView.as_view(), name="base_page_undelete"),
    # Photo URLs
    path('PhotoAddOrUpdate/', PhotoAddOrUpdateView.as_view(), name="photo_add_or_update"),
    path('PhotoList/', PhotoGetListView.as_view(), name="photo_get_list"),
    path('PhotoGet/', PhotoGetView.as_view(), name="photo_get"),
    path('PhotoDelete/', PhotoDeleteView.as_view(), name="photo_delete"),
    path('PhotoUndelete/', PhotoUndeleteView.as_view(), name="photo_undelete"),

    # Branch URLs
    path('BranchAddOrUpdate/', BranchAddOrUpdateView.as_view(), name="branch_add_or_update"),
    path('BranchList/', BranchGetListView.as_view(), name="branch_get_list"),
    path('BranchGet/', BranchGetView.as_view(), name="branch_get"),
    path('BranchDelete/', BranchDeleteView.as_view(), name="branch_delete"),
    path('BranchUndelete/', BranchUndeleteView.as_view(), name="branch_undelete"),

    # City URLs
    path('CityAddOrUpdate/', CityAddOrUpdateView.as_view(), name="city_add_or_update"),
    path('CityList/', CityGetListView.as_view(), name="city_get_list"),
    path('CityGet/', CityGetView.as_view(), name="city_get"),
    path('CityDelete/', CityDeleteView.as_view(), name="city_delete"),
    path('CityUndelete/', CityUndeleteView.as_view(), name="city_undelete"),

    # ContactInfo URLs
    path('ContactInfoAddOrUpdate/', ContactInfoAddOrUpdateView.as_view(), name="contact_info_add_or_update"),
    path('ContactInfoList/', ContactInfoGetListView.as_view(), name="contact_info_get_list"),
    path('ContactInfoGet/', ContactInfoGetView.as_view(), name="contact_info_get"),
    path('ContactInfoDelete/', ContactInfoDeleteView.as_view(), name="contact_info_delete"),
    path('ContactInfoUndelete/', ContactInfoUndeleteView.as_view(), name="contact_info_undelete"),

    # Country URLs
    path('CountryAddOrUpdate/', CountryAddOrUpdateView.as_view(), name="country_add_or_update"),
    path('CountryList/', CountryGetListView.as_view(), name="country_get_list"),
    path('CountryGet/', CountryGetView.as_view(), name="country_get"),
    path('CountryDelete/', CountryDeleteView.as_view(), name="country_delete"),
    path('CountryUndelete/', CountryUndeleteView.as_view(), name="country_undelete"),

    # Faq URLs
    path('FaqAddOrUpdate/', FaqAddOrUpdateView.as_view(), name="faq_add_or_update"),
    path('FaqList/', FaqGetListView.as_view(), name="faq_get_list"),
    path('FaqGet/', FaqGetView.as_view(), name="faq_get"),
    path('FaqDelete/', FaqDeleteView.as_view(), name="faq_delete"),
    path('FaqUndelete/', FaqUndeleteView.as_view(), name="faq_undelete"),

    # FaqCategory URLs
    path('FaqCategoryAddOrUpdate/', FaqCategoryAddOrUpdateView.as_view(), name="faq_category_add_or_update"),
    path('FaqCategoryList/', FaqCategoryGetListView.as_view(), name="faq_category_get_list"),
    path('FaqCategoryGet/', FaqCategoryGetView.as_view(), name="faq_category_get"),
    path('FaqCategoryDelete/', FaqCategoryDeleteView.as_view(), name="faq_category_delete"),
    path('FaqCategoryUndelete/', FaqCategoryUndeleteView.as_view(), name="faq_category_undelete"),

    # Help URLs
    path('HelpAddOrUpdate/', HelpAddOrUpdateView.as_view(), name="help_add_or_update"),
    path('HelpList/', HelpGetListView.as_view(), name="help_get_list"),
    path('HelpGet/', HelpGetView.as_view(), name="help_get"),
    path('HelpDelete/', HelpDeleteView.as_view(), name="help_delete"),
    path('HelpUndelete/', HelpUndeleteView.as_view(), name="help_undelete"),

    # HelpCategory URLs
    path('HelpCategoryAddOrUpdate/', HelpCategoryAddOrUpdateView.as_view(), name="help_category_add_or_update"),
    path('HelpCategoryList/', HelpCategoryGetListView.as_view(), name="help_category_get_list"),
    path('HelpCategoryGet/', HelpCategoryGetView.as_view(), name="help_category_get"),
    path('HelpCategoryDelete/', HelpCategoryDeleteView.as_view(), name="help_category_delete"),
    path('HelpCategoryUndelete/', HelpCategoryUndeleteView.as_view(), name="help_category_undelete"),

    # LayoutTag URLs
    path('LayoutTagAddOrUpdate/', LayoutTagAddOrUpdateView.as_view(), name="layout_tag_add_or_update"),
    path('LayoutTagList/', LayoutTagGetListView.as_view(), name="layout_tag_get_list"),
    path('LayoutTagGet/', LayoutTagGetView.as_view(), name="layout_tag_get"),
    path('LayoutTagDelete/', LayoutTagDeleteView.as_view(), name="layout_tag_delete"),
    path('LayoutTagUndelete/', LayoutTagUndeleteView.as_view(), name="layout_tag_undelete"),

    # Menu URLs
    path('MenuAddOrUpdate/', MenuAddOrUpdateView.as_view(), name="menu_add_or_update"),
    path('MenuList/', MenuGetListView.as_view(), name="menu_get_list"),
    path('MenuGet/', MenuGetView.as_view(), name="menu_get"),
    path('MenuDelete/', MenuDeleteView.as_view(), name="menu_delete"),
    path('MenuUndelete/', MenuUndeleteView.as_view(), name="menu_undelete"),

    # PageSeo URLs
    path('PageSeoAddOrUpdate/', PageSeoAddOrUpdateView.as_view(), name="page_seo_add_or_update"),
    path('PageSeoList/', PageSeoGetListView.as_view(), name="page_seo_get_list"),
    path('PageSeoGet/', PageSeoGetView.as_view(), name="page_seo_get"),
    path('PageSeoDelete/', PageSeoDeleteView.as_view(), name="page_seo_delete"),
    path('PageSeoUndelete/', PageSeoUndeleteView.as_view(), name="page_seo_undelete"),

    # Province URLs
    path('ProvinceAddOrUpdate/', ProvinceAddOrUpdateView.as_view(), name="province_add_or_update"),
    path('ProvinceList/', ProvinceGetListView.as_view(), name="province_get_list"),
    path('ProvinceGet/', ProvinceGetView.as_view(), name="province_get"),
    path('ProvinceDelete/', ProvinceDeleteView.as_view(), name="province_delete"),
    path('ProvinceUndelete/', ProvinceUndeleteView.as_view(), name="province_undelete"),

    # Setting URLs
    path('SettingAddOrUpdate/', SettingAddOrUpdateView.as_view(), name="setting_add_or_update"),
    path('SettingList/', SettingGetListView.as_view(), name="setting_get_list"),
    path('SettingGet/', SettingGetView.as_view(), name="setting_get"),
    path('SettingDelete/', SettingDeleteView.as_view(), name="setting_delete"),
    path('SettingUndelete/', SettingUndeleteView.as_view(), name="setting_undelete"),

    # Slider URLs
    path('SliderAddOrUpdate/', SliderAddOrUpdateView.as_view(), name="slider_add_or_update"),
    path('SliderList/', SliderGetListView.as_view(), name="slider_get_list"),
    path('SliderGet/', SliderGetView.as_view(), name="slider_get"),
    path('SliderDelete/', SliderDeleteView.as_view(), name="slider_delete"),
    path('SliderUndelete/', SliderUndeleteView.as_view(), name="slider_undelete"),

    # SpecialCategory URLs
    path('SpecialCategoryAddOrUpdate/', SpecialCategoryAddOrUpdateView.as_view(),
         name="special_category_add_or_update"),
    path('SpecialCategoryList/', SpecialCategoryGetListView.as_view(), name="special_category_get_list"),
    path('SpecialCategoryGet/', SpecialCategoryGetView.as_view(), name="special_category_get"),
    path('SpecialCategoryDelete/', SpecialCategoryDeleteView.as_view(), name="special_category_delete"),
    path('SpecialCategoryUndelete/', SpecialCategoryUndeleteView.as_view(), name="special_category_undelete"),

    # SpecialGroupCategory URLs
    path('SpecialGroupCategoryAddOrUpdate/', SpecialGroupCategoryAddOrUpdateView.as_view(),
         name="special_group_category_add_or_update"),
    path('SpecialGroupCategoryList/', SpecialGroupCategoryGetListView.as_view(),
         name="special_group_category_get_list"),
    path('SpecialGroupCategoryGet/', SpecialGroupCategoryGetView.as_view(), name="special_group_category_get"),
    path('SpecialGroupCategoryDelete/', SpecialGroupCategoryDeleteView.as_view(), name="special_group_category_delete"),
    path('SpecialGroupCategoryUndelete/', SpecialGroupCategoryUndeleteView.as_view(),
         name="special_group_category_undelete"),

    # StaticContent URLs
    path('StaticContentAddOrUpdate/', StaticContentAddOrUpdateView.as_view(), name="static_content_add_or_update"),
    path('StaticContentList/', StaticContentGetListView.as_view(), name="static_content_get_list"),
    path('StaticContentGet/', StaticContentGetView.as_view(), name="static_content_get"),
    path('StaticContentDelete/', StaticContentDeleteView.as_view(), name="static_content_delete"),
    path('StaticContentUndelete/', StaticContentUndeleteView.as_view(), name="static_content_undelete"),

    # StaticForm URLs
    path('StaticFormAddOrUpdate/', StaticFormAddOrUpdateView.as_view(), name="static_form_add_or_update"),
    path('StaticFormList/', StaticFormGetListView.as_view(), name="static_form_get_list"),
    path('StaticFormGet/', StaticFormGetView.as_view(), name="static_form_get"),
    path('StaticFormDelete/', StaticFormDeleteView.as_view(), name="static_form_delete"),
    path('StaticFormUndelete/', StaticFormUndeleteView.as_view(), name="static_form_undelete"),

    # StaticPage URLs
    path('StaticPageAddOrUpdate/', StaticPageAddOrUpdateView.as_view(), name="static_page_add_or_update"),
    path('StaticPageList/', StaticPageGetListView.as_view(), name="static_page_get_list"),
    path('StaticPageGet/', StaticPageGetView.as_view(), name="static_page_get"),
    path('StaticPageDelete/', StaticPageDeleteView.as_view(), name="static_page_delete"),
    path('StaticPageUndelete/', StaticPageUndeleteView.as_view(), name="static_page_undelete"),

    # SiteInfo URLs
    path('SiteInfoAddOrUpdate/', SiteInfoAddOrUpdateView.as_view(), name="site_info_add_or_update"),
    path('SiteInfoList/', SiteInfoGetListView.as_view(), name="site_info_get_list"),
    path('SiteInfoGet/', SiteInfoGetView.as_view(), name="site_info_get"),
    path('SiteInfoDelete/', SiteInfoDeleteView.as_view(), name="site_info_delete"),
    path('SiteInfoUndelete/', SiteInfoUndeleteView.as_view(), name="site_info_undelete"),

    # AbstractContent
    path('AbstractContentAddOrUpdate/', AbstractContentAddOrUpdateView.as_view(), name="abstract_content_add_or_update"),
    path('AbstractContentList/', AbstractContentGetListView.as_view(), name="abstract_content_get_list"),
    path('AbstractContentGet/', AbstractContentGetView.as_view(), name="abstract_content_get"),
    path('AbstractContentDelete/', AbstractContentDeleteView.as_view(), name="abstract_content_delete"),
    path('AbstractContentUndelete/', AbstractContentUndeleteView.as_view(), name="abstract_content_undelete"),
]
