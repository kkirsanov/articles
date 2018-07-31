a = (1, 2)
a += (3, 4) # (1,2,3,4)
print a[2] #3
#a[2] =5#'tuple' object does not support item assignment 
a = (1,) #(1)

st = "as df gh jk"
if "as" in st:
    print "Bingo"
l = st.split(" ")# ['as', 'df', 'gh', 'jk']
