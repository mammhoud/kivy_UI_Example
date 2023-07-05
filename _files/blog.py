'''
BoxLayout:
    BoxLayout:
        TextInput:
            id: username
    BoxLayout:
        TextInput:
            id: password
    Button:
        on_press: app.check_login(username.text, password.text)
'''


import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class LoginScreen(BoxLayout):
    def check_login(self, username, password):
        if result:
            # show a success popup
            popup = Popup(title='Success', content=Label(text='You have logged in!'), size_hint=(None, None), size=(300, 200))
            popup.open()
        else:
            # show an error popup
            popup = Popup(title='Error', content=Label(text='Invalid username or password!'), size_hint=(None, None), size=(300, 200))
            popup.open()


class LoginApp(App):
    def build(self):
        # load the kv file
        self.load_kv('login.kv')
        
        # return an instance of LoginScreen
        return LoginScreen()



'''Start with Why is a book by Simon Sinek that explores the power of purpose and motivation in leadership, business, and life. \
    The main idea of the book is that people don't buy what you do, they buy why you do it. \
        Sinek argues that the most successful leaders and organizations are those that communicate their why clearly and consistently, inspiring others to join their cause.

The book is divided into three parts: \
    Part One explains the concept of the Golden Circle, \
        a framework that helps to identify and articulate your why, how, \
            and what. Part Two describes how the Golden Circle can be applied to create loyal customers, employees, and followers. \
                Part Three shows how the Golden Circle can help to build trust, innovation, and lasting impact.

Some of the key takeaways from the book are:

- The why is your reason for being, your cause, your belief,\
    or your purpose. It is the driving force behind everything you do.
- The how is your process, your methods, \
    your values, or your actions.\
    It is how you bring your why to life.
- The what is your product, your service, your result, or your outcome. It is what you do or offer to the world.\
    
- Most people and organizations communicate from the outside in, starting with what they do and ending with why they do it. \
    This approach is ineffective and uninspiring because it doesn't connect with people's emotions or motivations.
- The most influential and successful leaders and organizations communicate from the inside out, \
    starting with why they do what they do and ending with what they do. \
        This approach is powerful and inspiring because it taps into people's innate desire to belong to something bigger than themselves.
- To find your why, you need to look back at your past experiences, \
    stories, \
        and passions, and identify the common thread that connects them.\
        You also need to ask yourself why you do what you do, not what you do or how you do it.
- To communicate your why, you need to use simple and clear language that resonates with your audience. \
    You also need to be consistent and authentic in everything you say and do.
- To inspire others with your why, \
    you need to lead by example and demonstrate your commitment to your cause. \
    You also need to create a culture of trust and empowerment where people feel valued and inspired to contribute to your vision.'''
