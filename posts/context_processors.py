def categories(request):
    categories = [
        'Programming',
        'Food',
        'Travel'

    ]
    return {'categories': categories}
