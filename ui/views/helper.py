def get_obj_fields(obj):
    """ повертая словник-об'єкт з полями та значеннями """
    if obj.block_obj.fields is not None:
        return obj.block_obj.fields

    fields_to_check = obj.block_obj.fields or [f.name for f in obj.block_obj_model._meta.fields if
                                                f.name != 'id' and f.name != 'time_created' and f.name != 'time_updated']

    return [
        {
            'label': obj.block_obj_model._meta.get_field(f).verbose_name,
            'value': getattr(obj.block_obj.data, f),
        } for f in fields_to_check
    ]

def get_table_titles(self):
    """
    Повертає заголовки таблиці
    """
    if self.block_table.table_titles is not None:
        return self.block_table.table_titles

    fields_to_check = [f.name for f in self.table_model._meta.fields]
    return [
        self.table_model._meta.get_field(f).verbose_name
        for f in fields_to_check
    ]


def get_table_data(self):
    queryset = self._model.objects.all().values(*[
            f.name for f in self._model._meta.fields
            if f.name != 'id'
        ])

    rows_data = []

    for obj in queryset:
        rows_data.append({
            'values': obj,
            'row_url': reverse('organization:view_ust', kwargs={self.slug_url_kwarg: obj[self.slug_field]}), # .isoformat()}),
            'buttons': [
                UIButtons('view_ust')
                .set_url_name('organization:view_ust')
                .set_kwargs({
                    self.slug_url_kwarg: obj[self.slug_field] # .isoformat()
                }),
            ]
        })
        obj['time_created'] = obj['time_created'].strftime("%d.%m.%Y")
        obj['time_updated'] = obj['time_updated'].strftime("%d.%m.%Y")
    return rows_data