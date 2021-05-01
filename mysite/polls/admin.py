from django.contrib import admin

from .models import Choice, Question

# Inline related objects가 공간을 잡아먹어 StackedInline을 TabularInline으로 교체
# TabularInline은 좀 더 조밀한 테이블 기반 형식으로 표시
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['question_text']}),
                 ('Date infomation', {'fields': ['pub_date'], 'classes':['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)

