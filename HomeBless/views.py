from django.shortcuts import render, redirect
from django.views.generic import TemplateView


# Create your views here.
class PropertyListing(TemplateView):
    template_name = 'property-listing.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return redirect('HomeBless:property-listing')


class HomePage(TemplateView):
    template_name = 'homepage.html'

    def get(self, request, *args, **kwargs):
        lines = [
            {'name': 'สายสุขุมวิท', 'color': '#6fbe44', 'color_name': 'สีเขียว'},
            {'name': 'สายสีลม', 'color': '#119b49', 'color_name': 'สีเขียวเข้ม'},
            {'name': 'สายสีชมพู', 'color': '#ef5599', 'color_name': 'สีชมพู'},
            {'name': 'สายเฉลิมรัชมงคล', 'color': '#0e76bc', 'color_name': 'สีน้ำเงิน'},
            {'name': 'สายฉลองรัชธรรม', 'color': '#67318f', 'color_name': 'สีม่วง'},
            {'name': 'สายสีทอง', 'color': '#d4af37', 'color_name': 'สีทอง'},
            {'name': 'สายสีส้ม', 'color': '#ee7821', 'color_name': 'สีส้ม'},
            {'name': 'สายสีแดง', 'color': '#d71a28', 'color_name': 'สีแดง'}
        ]
        return render(request, self.template_name, {'lines': lines})

    def post(self, request, *args, **kwargs):
        return redirect('HomeBless:homepage')


class Compare(TemplateView):
    template_name = 'compare.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return redirect('HomeBless:compare')


class PropertyDetail(TemplateView):
    template_name = 'property-detail.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return redirect('HomeBless:property-detail')
