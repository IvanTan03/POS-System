from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import database 

class POSApp(App):
    def build(self):
        self.title = "POS System"
        self.layout = BoxLayout(orientation='vertical')

        # Add buttons to the layout
        add_product_btn = Button(text='Add Product')
        add_product_btn.bind(on_release=self.add_product)
        self.layout.add_widget(add_product_btn)

        list_products_btn = Button(text='List Products')
        list_products_btn.bind(on_release=self.list_products)
        self.layout.add_widget(list_products_btn)

        record_sale_btn = Button(text='Record Sale')
        record_sale_btn.bind(on_release=self.record_sale)
        self.layout.add_widget(record_sale_btn)

        check_sale_btn = Button(text='Check Sale')
        check_sale_btn.bind(on_release=self.check_sales)
        self.layout.add_widget(check_sale_btn)

        exit_btn = Button(text='Exit')
        exit_btn.bind(on_release=self.stop)
        self.layout.add_widget(exit_btn)

        return self.layout

    def add_product(self, _):
        self.show_add_product_popup()

    def show_add_product_popup(self):
        layout = BoxLayout(orientation='vertical')
        name_input = TextInput(hint_text='Enter product name')
        price_input = TextInput(hint_text='Enter product price', input_filter='float')
        layout.add_widget(name_input)
        layout.add_widget(price_input)

        def on_add(_):
            name = name_input.text
            price = float(price_input.text)
            database.add_product(name, price)
            popup.dismiss()
            self.show_message("Success", "Product added successfully.")

        add_btn = Button(text='Add')
        add_btn.bind(on_release=on_add)
        layout.add_widget(add_btn)

        popup = Popup(title='Add Product', content=layout, size_hint=(0.8, 0.5))
        popup.open()

    def list_products(self, _):
        products = database.get_products()
        content = GridLayout(cols=3, size_hint_y=None, row_default_height=40)
        content.bind(minimum_height=content.setter('height'))

        headers = ["ID", "Name", "Price"]
        for header in headers:
            content.add_widget(Label(text=header, size_hint_y=None, height=40))

        for product in products:
            for item in product:
                if isinstance(item, float):
                    item = f"{item:.2f}"
                content.add_widget(Label(text=str(item), size_hint_y=None, height=40))

        scrollview = ScrollView(size_hint=(1, 1))
        scrollview.add_widget(content)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(scrollview)

        popup = Popup(title='Product List', content=layout, size_hint=(0.8, 0.8))
        popup.open()

    def record_sale(self, _):
        self.show_record_sale_popup()

    def show_record_sale_popup(self):
        layout = BoxLayout(orientation='vertical')
        product_id_input = TextInput(hint_text='Enter product ID', input_filter='int')
        quantity_input = TextInput(hint_text='Enter quantity', input_filter='int')
        layout.add_widget(product_id_input)
        layout.add_widget(quantity_input)

        def on_record(_):
            product_id = int(product_id_input.text)
            quantity = int(quantity_input.text)
            price = next(p[2] for p in database.get_products() if p[0] == product_id)
            total = quantity * price
            database.add_sale(product_id, quantity, total)
            popup.dismiss()
            self.show_message("Success", f"Sale recorded: ${total:.2f}")

        record_btn = Button(text='Record')
        record_btn.bind(on_release=on_record)
        layout.add_widget(record_btn)

        popup = Popup(title='Record Sale', content=layout, size_hint=(0.8, 0.5))
        popup.open()

    def check_sales(self, _):
        sales = database.get_sales()
        layout = BoxLayout(orientation='vertical')
        content = GridLayout(cols=4, size_hint_y=None, row_default_height=40)
        content.bind(minimum_height=content.setter('height'))

        headers = ["ID", "Product Name", "Quantity", "Total"]
        for header in headers:
            content.add_widget(Label(text=header, size_hint_y=None, height=40))

        for sale in sales:
            for item in sale:
                if isinstance(item, float):
                    item = f"{item:.2f}"
                content.add_widget(Label(text=str(item), size_hint_y=None, height=40))

        scrollview = ScrollView(size_hint=(1, 1))
        scrollview.add_widget(content)
        layout.add_widget(scrollview)

        popup = Popup(title='Sales List', content=layout, size_hint=(0.8, 0.8))
        popup.open()
        
    def show_message(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.5))
        popup.open()

if __name__ == '__main__':
    POSApp().run()
