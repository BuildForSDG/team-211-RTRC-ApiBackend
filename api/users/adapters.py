from allauth.account.adapter import DefaultAccountAdapter


# override this to change the link you get for an account verification
class AccountAdapter(DefaultAccountAdapter):

    def send_mail(self, template_prefix, email, context):
        URL_PREFIX = 'https://app.orders.com.gh/'
        
        context['activate_url'] = URL_PREFIX + \
        'access/verify-email/' + context['key']
        msg = self.render_mail(template_prefix, email, context)
        msg.content_subtype = 'html'
        msg.send()
