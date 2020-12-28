import pyparsing as pp

# define a simple grammar for parsing street addresses such
# as "123 Main Street"
#     number word...
number = pp.Word(pp.nums).setName("number")
name = pp.Word(pp.alphas).setName("word")[1, ...]

parser = number("house_number") + name("street")
parser.setName("street address")

# construct railroad track diagram for this parser and
# save as HTML
parser.create_diagram('parser_rr_diag.html')
