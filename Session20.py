name='john'
cafe_name="john's cafe"

#raw string-> accepts special characters as data
cafe_name=r'john\'s \ncafe'

quote="search the candle rather than cursing the darkness"

contacts=["john","kia","sia","jennie","joe","jackson","anna"]
search=input("entwer search keyword :")
for contact in contacts:
    if search in contact:
        print(contact)


quote="be exceptional"
s1 = quote.upper()
print("Quote is:",s1)

s3=quote.capitalize()
print("s3 is:", s3)


s4=quote.title()
print("s4 is:", s4)

s5=s4.swapcase()
print(s5)  
