from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from django.db.models import Count

from .models import Attempt, Conjugation, ConjugationValue, Mood, MoodTense, UserMoodTense, Person, Tense, Verb

class IsGoodFilter(SimpleListFilter):
    title = 'Is Good'
    parameter_name = 'good'

    def lookups(self, request, model_admin):
        return [('t', True), ('f', False)]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        is_good = self.value() == 't'
        return queryset.filter(is_good=is_good)

class AttemptAdmin(admin.ModelAdmin):
    readonly_fields = ('created_time',)
    raw_id_fields = ('conjugation',)

class ConjugationValueInline(admin.TabularInline):
    model = ConjugationValue

class ConjugationAdmin(admin.ModelAdmin):
    inlines = [ConjugationValueInline]
    list_select_related = True
    list_filter = ('verb', 'mood_tense', 'person')

class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'index', 'pronoun')

class ConjugationValueAdmin(admin.ModelAdmin):
    list_select_related = True
    raw_id_fields = ('conjugation',)

admin.site.register(Attempt, AttemptAdmin)
admin.site.register(Conjugation, ConjugationAdmin)
admin.site.register(ConjugationValue, ConjugationValueAdmin)
admin.site.register(Mood)
admin.site.register(MoodTense)
admin.site.register(UserMoodTense)
admin.site.register(Person, PersonAdmin)
admin.site.register(Tense)
admin.site.register(Verb)
