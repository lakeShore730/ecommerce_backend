def get_product_query_params(params):
    kwargs = {}
    
    if 'category' in params:
        kwargs['category'] = params.get('category')
    if 'is_feature' in params:
        kwargs['is_feature'] = True if params.get('is_feature') == "true" else False 
    if 'query' in params:
        kwargs['name__contains'] = params.get('query')

    return kwargs