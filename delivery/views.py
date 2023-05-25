from typing import Optional, Union
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.core.paginator import Page, Paginator
class DeliveryList(TemplateView):
    template_name = 'delivery_list.html'

class BootstrapPaginator(Paginator):
    def get_page_as_json(self, page):
        return {
            'page_range': list(self.page_range),
            'rows': self.page(page).object_list ,
            'num_pages': self.num_pages,
            'total': self.count,
            'per_page': self.per_page,
        }

def get_page_number(request):
    offset = int(request.GET.get("offset", 0))
    limit = int(request.GET.get("limit", 1))
    return offset // limit + 1
    
def test(request):
    page = get_page_number(request)
    
    data = [
        {"name": "Célio", "cpf": "123123123123", "age": 35, "email": "celio@example.com", "phone": "+1 123-456-7890"},
        {"name": "Maria", "cpf": "456456456456", "age": 28, "email": "maria@example.com", "phone": "+1 987-654-3210"},
        {"name": "João", "cpf": "789789789789", "age": 42, "email": "joao@example.com", "phone": "+1 555-555-5555"},
        {"name": "Ana", "cpf": "321321321321", "age": 31, "email": "ana@example.com", "phone": "+1 999-888-7777"},
        {"name": "XYDCO", "cpf": "84623485268", "age": 48, "email": "xydco@example.com", "phone": "+1 333-222-1111"},
        {"name": "ABNTR", "cpf": "42872198759", "age": 23, "email": "abntr@example.com", "phone": "+1 777-888-9999"},
        {"name": "LQFJU", "cpf": "69241374501", "age": 30, "email": "lqfju@example.com", "phone": "+1 555-666-7777"},
        {"name": "HJNVS", "cpf": "13051742904", "age": 55, "email": "hjnvs@example.com", "phone": "+1 222-333-4444"},
        {"name": "QWEJR", "cpf": "82706341857", "age": 44, "email": "qwejr@example.com", "phone": "+1 999-777-5555"},
        {"name": "TYXJL", "cpf": "95467291237", "age": 20, "email": "tyxjl@example.com", "phone": "+1 444-555-6666"},
        {"name": "MBCRA", "cpf": "54193825609", "age": 39, "email": "mbcra@example.com", "phone": "+1 666-777-8888"},
        {"name": "OXRLW", "cpf": "23856790138", "age": 49, "email": "oxrlw@example.com", "phone": "+1 777-888-9999"},
        {"name": "GKSHZ", "cpf": "61897432605", "age": 42, "email": "gkshz@example.com", "phone": "+1 888-999-0000"},
        {"name": "XQWVF", "cpf": "87263905841", "age": 31, "email": "xqwvf@example.com", "phone": "+1 111-222-3333"},
        {"name": "IUEBF", "cpf": "51279034686", "age": 27, "email": "iuebf@example.com", "phone": "+1 222-333-4444"},
        {"name": "DLGUN", "cpf": "28349106547", "age": 32, "email": "dlgun@example.com", "phone": "+1 333-444-5555"},
        {"name": "OJQWI", "cpf": "49478302961", "age": 46, "email": "ojqwi@example.com", "phone": "+1 444-555-6666"},
        {"name": "XNZMV", "cpf": "13589647280", "age": 39, "email": "xnzmv@example.com", "phone": "+1 555-666-7777"},
        {"name": "GMPWZ", "cpf": "79361528470", "age": 22, "email": "gmpwz@example.com", "phone": "+1 666-777-8888"},
        {"name": "KWSCV", "cpf": "57281693049", "age": 43, "email": "kwscv@example.com", "phone": "+1 777-888-9999"},
        {"name": "TJYIB", "cpf": "18094526370", "age": 52, "email": "tjyib@example.com", "phone": "+1 888-999-0000"},
        {"name": "LPSXO", "cpf": "90632781452", "age": 33, "email": "lpsxo@example.com", "phone": "+1 000-111-2222"},
        {"name": "UFDPQ", "cpf": "23764950182", "age": 29, "email": "ufdpq@example.com", "phone": "+1 111-222-3333"},
    ]

    paginator = BootstrapPaginator(data, per_page=10)
    page_data = paginator.get_page_as_json(page)
    return JsonResponse(page_data, safe=False)