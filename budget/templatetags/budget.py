from decimal import Decimal
from django import template
from django.conf import settings


register = template.Library()

# To override, copy to your settings file. Make sure to keep the tuples in 
# descending order by percentage.
BUDGET_DEFAULT_COLORS = (
    # (percentage, CSS color class)
    (1.001, 'red'),
    (0.75, 'yellow'),
    (0.0, 'green'),
)


class ColorizeAmountNode(template.Node):
    def __init__(self, estimated_amount, actual_amount):
        self.estimated_amount = template.Variable(estimated_amount)
        self.actual_amount = template.Variable(actual_amount)
    
    def render(self, context):
        if hasattr(settings, 'BUDGET_DEFAULT_COLORS'):
            colors = settings.BUDGET_DEFAULT_COLORS
        else:
            colors = BUDGET_DEFAULT_COLORS
        
        try:
            estimate = self.estimated_amount.resolve(context)
            actual = self.actual_amount.resolve(context)
            estimate = make_decimal(estimate)

            if estimate == 0:
                return ''

            actual = make_decimal(actual)            
            percentage = actual / estimate
            
            for color in colors:
                color_percentage = make_decimal(color[0])
                
                if percentage >= color_percentage:
                    return color[1]
        except template.VariableDoesNotExist:
            return ''


def make_decimal(amount):
    """
    If it's not a Decimal, it should be...
    """
    if not isinstance(amount, Decimal):
        amount = Decimal(str(amount))
    
    return amount
    

def colorize_amount(parser, token):
    """
    Compares an estimate with an actual amount and returns an appropriate
    color as a visual indicator.
    
    Example:
    
        {% colorize_amount estimated_amount actual_amount %}
    """
    try:
        tag_name, estimated_amount, actual_amount = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly two arguments" % token.contents.split()[0])
    return ColorizeAmountNode(estimated_amount, actual_amount)


register.tag('colorize_amount', colorize_amount)
